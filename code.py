import board
import busio
import time
from digitalio import DigitalInOut, Direction
from support.menorah import Menorah
from support.wifi_manager import WiFi
from support.eink_display import Screen, ScreenStorage


def display_error() -> None:
    while True:
        menorah.light_candles(8)
        time.sleep(1)
        menorah.turn_off_candles()
        time.sleep(1)

def display_loading() -> None:
    # TODO: Write loading display code
    pass

def main() -> None:

    # Get candle lighting times
    lighting_times = wifi.get_candle_lighting_times()

    # Past candle lighting date, no need to do anything
    if wifi.get_datetime() >= lighting_times[7]:
        return
    
    # Main loop
    while True:

        # Compare candle lighting times to current time
        for lighting in lighting_times:

            current_time = wifi.get_datetime()
            off_time = menorah.get_menorah_off_time(lighting)

            if current_time < lighting:
                # Manage turning the candles on at the appropriate time
                while wifi.get_datetime() < lighting:
                    menorah.sleep_based_on_delta(lighting, wifi.get_datetime())

                

            if lighting <= current_time < off_time:
                # Manage turning the candles off at the appropriate time
                while wifi.get_datetime() < off_time:
                    menorah.sleep_based_on_delta(off_time, wifi.get_datetime())

# Initialize SPI
sck_pin = board.GP18
copi_pin = board.GP19
cipo_pin = board.GP16
spi = busio.SPI(sck_pin, copi_pin, cipo_pin)

# Initialize candles
shamash = DigitalInOut(board.GP15)
shamash.direction = Direction.OUTPUT
candles = []
for gpio_num in range(14, 6, -1):
    gpio_str = "GP" + str(gpio_num)
    gpio_dio = DigitalInOut(getattr(board, gpio_str))
    gpio_dio.direction = Direction.OUTPUT
    candles.append(gpio_dio)
menorah = Menorah(shamash, candles)
    
# Initialize screen and screen storage
screen_command = board.GP6
screen_cs = board.GP5
screen_reset = board.GP4
screen_busy = board.GP3
#sram_cs = board.GP2
#sd_cs = board.GP1
screen = Screen(spi, screen_command, screen_cs, screen_reset, screen_busy)
#storage = ScreenStorage(spi, sd_cs)

# Initialize ESP32 I/O
esp32_cs = DigitalInOut(board.GP17)
esp32_ready = DigitalInOut(board.GP20)
esp32_reset = DigitalInOut(board.GP21)
esp32_gpio0 = DigitalInOut(board.GP22)

# Try to connect to WiFi network and sync time
try:
    wifi = WiFi(spi, esp32_cs, esp32_ready, esp32_reset, esp32_gpio0)
    wifi.sync_time()
except RuntimeError:
    display_error()

if __name__ == "__main__":
    main()