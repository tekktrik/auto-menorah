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

    def grab_candle_lighting_time(
        self,
    ) -> Dict[str, str]:  # TODO: Check and finalize typing
        # Function to grab data on the Hebrew calendar for the dates and times
        requests.get()
