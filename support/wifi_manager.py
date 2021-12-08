"""
`wifi_manager`
================================================================================

Module for managing network connections and API requests

* Author: Alec Delaney
"""

import json
import time
import asyncio
from secrets import secrets, location
from adafruit_esp32spi.adafruit_esp32spi import ESP_SPIcontrol
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_datetime import datetime, timezone

try:
    from typing import Optional, List
    from busio import SPI
    from digitalio import DigitalInOut
except ImportError:
    pass

CALENDAR_API: str = (
    "http://www.hebcal.com/hebcal?"
    "v=1;maj=on;min=off;i=off;lg=s;"
    "c=on;year=now;month=[|MONTH|]"
    ";geo=zip;zip={0};cfg=json".format(location["zipcode"])
)


class WiFi(ESP_SPIcontrol):
    """Class for representing the Wi-Fi and the associate functions it provides
    to the auto-menorah

    :param SPI spi: The SPI bus object for the board
    :param DigitalInOut cs_dio: The chip select digital io for the ESP32
    :param DigitalInOut ready_dio: The READY digital io for the ESP32
    :param DigitalInOut reset_dio: The RESET digital io for the ESP32
    :param DigitalInOut gpio0_dio: The GIO0 digital io for the ESP32, optional
    """

    def __init__(
        self,
        spi: SPI,
        cs_dio: DigitalInOut,
        ready_dio: DigitalInOut,
        reset_dio: DigitalInOut,
        gpio0_dio: Optional[DigitalInOut] = None,
    ):
        super().__init__(spi, cs_dio, ready_dio, reset_dio, gpio0_dio)
        self._latest_events = None
        self._month_checking = 11

    async def connect_to_network(self) -> None:
        """Connect to the Wi-Fi network, attempt until connection is made"""

        requests.set_socket(socket, self)
        for attempt in range(5):
            try:
                self.connect(secrets)
                break
            except RuntimeError as runtime_error:
                if attempt != 9:
                    print("Could not connect, retrying in 5 seconds...")
                    await asyncio.sleep(5)
                else:
                    raise runtime_error

    async def connect_to_ntp(self, num_attempts: int = 10) -> None:
        """Connect to NTP server, attempt until connection is made

        :param int num_attempts: The number of connection attempts to make
        """

        for attempt in range(num_attempts):
            try:
                super().get_time()[0]
                return
            except ValueError:
                if attempt != (num_attempts - 1):
                    print("Failed to sync with NTP server")
                    print("Trying again in 5 seconds")
                    await asyncio.sleep(10)
        raise RuntimeError("Could not sync time")

    def _update_json(self) -> str:
        """Get new JSON from the API

        :return str: The JSON string containing holiday information
        """

        api_response: requests.Response = requests.get(
            CALENDAR_API.replace("[|MONTH|]", str(self._month_checking))
        )

        return api_response.json()["items"]

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

    def get_datetime(self) -> time.struct_time:
        """Get the current datetime

        :return time.struct_time: The current datetime
        """

        return time.localtime(self.get_time()[0])
