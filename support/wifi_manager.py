# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`wifi_manager`
================================================================================

Module for managing network connections and API requests

* Author: Alec Delaney
"""

import socketpool
import wifi
import ssl
import asyncio
from secrets import secrets, location
import adafruit_requests as requests
from adafruit_datetime import datetime, timezone, timedelta

try:
    from typing import List
except ImportError:
    pass

# Get our username, key and desired timezone
try:
    aio_username = secrets["aio_username"]
    aio_key = secrets["aio_key"]
except KeyError as err:
    raise KeyError("You need to add the Adafruit IO information!") from err

TIME_URL = "https://io.adafruit.com/api/v2/%s/integrations/time/clock?x-aio-key=%s" % (
    aio_username,
    aio_key,
)
TIME_URL += "&fmt=%25Y-%25m-%25dT%25H%3A%25M%3A%25S.%25L%25z"


# class WiFi(ESP_SPIcontrol):
class WiFi:
    """Class for representing the Wi-Fi and the associate functions it provides
    to the auto-menorah

    :param SPI spi: The SPI bus object for the board
    :param DigitalInOut cs_dio: The chip select digital io for the ESP32
    :param DigitalInOut ready_dio: The READY digital io for the ESP32
    :param DigitalInOut reset_dio: The RESET digital io for the ESP32
    :param DigitalInOut gpio0_dio: The GIO0 digital io for the ESP32, optional
    """

    # def __init__(
    #    self,
    #    spi: SPI,
    #    cs_dio: DigitalInOut,
    #    ready_dio: DigitalInOut,
    #    reset_dio: DigitalInOut,
    #    gpio0_dio: Optional[DigitalInOut] = None,
    # ):
    def __init__(self):
        # super().__init__(spi, cs_dio, ready_dio, reset_dio, gpio0_dio)
        self._latest_events = None
        self._month_checking = 11
        self.requests = None

    async def connect_to_network(self) -> None:
        """Connect to the Wi-Fi network, attempt until connection is made"""

        for attempt in range(5):
            try:
                wifi.radio.connect(secrets["ssid"], secrets["password"])
                pool = socketpool.SocketPool(wifi.radio)
                context = ssl.create_default_context()
                self.requests = requests.Session(pool, context)
                break
            except RuntimeError as runtime_error:
                if attempt != 9:
                    print("Could not connect, retrying in 5 seconds...")
                    await asyncio.sleep(5)
                else:
                    raise runtime_error

    def _update_json(self) -> str:
        """Get new JSON from the API

        :return str: The JSON string containing holiday information
        """

        calendar_api: str = (
            "http://www.hebcal.com/hebcal?"
            "v=1;maj=on;min=off;i=off;lg=s;"
            "c=on;year=now;month={0}"
            ";geo=zip;zip={1};cfg=json".format(
                self._month_checking, location["zipcode"]
            )
        )

        api_response: requests.Response = self.requests.get(calendar_api)

        json_response = api_response.json()
        return json_response["items"]

    def _parse_time_for_night(self, num_night: int) -> datetime:
        """Recursive method for getting the candle lighting time for a specific night

        :param int num_night: The night of Hannukah to look for
        :return datetime: The datetime for the specific night of Hannukah
        """
        for event in self._latest_events:
            title_option_1 = "Chanukah: " + str(num_night) + " Candle"
            title_option_2 = "Chanukah: " + str(num_night) + " Candles"
            if event["title"] == title_option_1 or event["title"] == title_option_2:
                return datetime.fromisoformat(event["date"])
        self._month_checking += 1
        self._latest_events = self._update_json()
        return self._parse_time_for_night(num_night)

    def get_candle_lighting_times(
        self,
    ) -> List[datetime]:
        """Function to grab data on the Hebrew calendar for the dates and times

        :return List[datetime]: A list of candle light datetimes
        """

        lighting_times = []
        self._latest_events = self._update_json()

        for night_index in range(8):
            lighting_times.append(self._parse_time_for_night(night_index + 1))

        return lighting_times

    @staticmethod
    def get_menorah_off_time(lighting_time: datetime) -> datetime:
        """Get the time at while candles should be turned off

        :param datetime lighting_time: The time at which candles should be lit for that day
        :return datetime: The associated off time for the candles
        """
        projected_time: datetime = lighting_time + timedelta(hours=12)
        return projected_time

    def get_datetime(self) -> datetime:
        """Get the current datetime

        :return time.struct_time: The current datetime
        """

        current_datetime: datetime = datetime.fromisoformat(self.get_time())
        current_datetime._tzinfo = timezone.utc

        # add_delta = timedelta(275, hours=12)
        # current_datetime += add_delta
        # print(current_datetime)

        return current_datetime

    def get_time(self) -> str:
        """Get the time from Adafruit IO in ISO format

        :return str: The time as an ISO format string
        """

        response = self.requests.get(TIME_URL)
        return response.text
