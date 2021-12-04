import json
import time
from adafruit_esp32spi.adafruit_esp32spi import ESP_SPIcontrol
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_datetime import datetime
from secrets import secrets, location

try:
    from typing import Optional, Dict, Any, List
    from busio import SPI
    from digitalio import DigitalInOut
except ImportError:
    pass

CALENDAR_API: str = "http://www.hebcal.com/hebcal/?" + \
                "v=1;maj=on;min=off;i=off;lg=s;" + \
                "c=on;year=now;month=[|MONTH|]" + \
                ";geo=zip;zip=" + \
                location["zipcode"] + \
                ";cfg=json"


class WiFiManager(ESP_SPIcontrol):
    def __init__(
        self,
        spi: SPI,
        cs_dio: DigitalInOut,
        ready_dio: DigitalInOut,
        reset_dio: DigitalInOut,
        gpio0_dio: Optional[DigitalInOut] = None,
    ):
        super().__init__(spi, cs_dio, ready_dio, reset_dio, gpio0_dio)
        self.ntp_time = None
        self._latest_events = None
        requests.set_socket(socket, self)
        for attempt in range(5):
            try:
                self.connect(secrets)
                break
            except RuntimeError:
                if attempt != 9:
                    print("Could not connect, retrying in 5 seconds...")
                    time.sleep(5)

    def sync_time(self, num_attempts: int = 5) -> bool:
        for attempt in range(num_attempts):
            try:
                self._ntp_time = super().get_time()[0]
                return True
            except ValueError:
                if attempt != (num_attempts - 1):
                    print("Failed to sync with NTP server")
                    print("Trying again in 5 seconds")
                    time.sleep(5)
        return False

    def _update_json(self, month):
        return requests.get(CALENDAR_API.replace("[|MONTH|]", str(month)))["items"]

    def _parse_time_for_night(self, num_night):
        for event in self._latest_events:
            if event["title"] == ("Chanukah: " + str(num_night) + " Candle"):
                return datetime.fromisoformat(event["date"])
        self._month_checking += 1
        self._update_json()
        return self._parse_time_for_night(num_night)

    def get_candle_lighting_time(
        self,
    ) -> List[datetime]:  # TODO: Check and finalize typing
        """Function to grab data on the Hebrew calendar for the dates and times"""
        self._month_checking = 11
        lighting_times = []

        # recursion

        self._latest_events = self._update_json()

        for night in range(8):
            lighting_times.append(self._parse_time_for_night(night))

        return lighting_times