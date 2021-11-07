from adafruit_ssd1681 import SSD1681
import displayio
from adafruit_sdcard import SDCard

try:
    import typing  # pylint: disable=unused-import
    from busio import SPI
    from microcontroller import Pin
except ImportError:
    pass


class Screen(SSD1681):
    def __init__(
        self,
        spi: SPI,
        command_pin: Pin,
        cs_pin: Pin,
        reset_pin: Pin,
        busy_pin: Pin,
        baudrate: int = 1000000,
    ):
        display_bus = displayio.FourWire(
            spi,
            command=command_pin,
            chip_select=cs_pin,
            reset=reset_pin,
            baudrate=baudrate,
        )
        super().__init__(
            display_bus,
            width=200,
            height=200,
            busy_pin=busy_pin,
            highlight_color=0xFF0000,
            rotation=180,
        )

class ScreenStorage(SDCard):

    pass