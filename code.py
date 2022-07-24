# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`code.py`
=========

Main code for functionality, as well as functionalities involving multiple modules

* Author: Alec Delaney
"""

import time
import asyncio
import board
from adafruit_datetime import timedelta
from digitalio import DigitalInOut, Direction
from support.menorah import Menorah
from support.wifi_manager import WiFi
from support.setup_helper import ConnectionStatus
from settings import BURNOUT


def display_error() -> None:
    """Displays an error using menorah lights"""
    while True:
        menorah.light_candles(8)
        time.sleep(1)
        menorah.turn_off_candles()
        time.sleep(1)


async def display_loading(setup_status: ConnectionStatus, interval: float = 1) -> None:
    """Displays loading state using menorah lights

    :param ConnectonStatus setup_status: The ConnectionStatus linking the setup methods
    :param float interval: How long to wait between lighting state changes
    """

    while not setup_status.is_connected:
        for num_candles in range(1, 5):
            menorah.light_candles(num_candles, light_shamash=False)
            await asyncio.sleep(interval)
            menorah.turn_off_candles()
        menorah.set_shamash(True)
        await asyncio.sleep(interval)
        for num_candles in range(5, 9):
            menorah.light_candles(num_candles, light_shamash=True)
            await asyncio.sleep(interval)
            menorah.turn_off_candles()


async def setup_connections(setup_status: ConnectionStatus) -> None:
    """Connect to WiFi network and NTP server

    :param ConnectionStatus setup_status: The ConnectionStatus linking the setup methods
    """

    try:
        await wifi.connect_to_network()
        # await wifi.connect_to_ntp()
        setup_status.is_connected = True
    except RuntimeError:
        display_error()


async def setup_menorah() -> None:
    """Set up the menorah and display loading status"""
    loading_task = asyncio.create_task(display_loading(connection_status))
    connection_task = asyncio.create_task(setup_connections(connection_status))
    await asyncio.gather(loading_task, connection_task)


def main() -> None:
    """Main function"""

    # Turn off lights
    menorah.turn_off_candles()

    # Get candle lighting times
    lighting_times = wifi.get_candle_lighting_times()

    # Past candle lighting date, no need to do anything
    holiday_end = wifi.get_menorah_off_time(lighting_times[7])
    if wifi.get_datetime() >= holiday_end:
        while True:
            pass

    # Compare candle lighting times to current time
    for night_index, lighting in enumerate(lighting_times):

        off_time = wifi.get_menorah_off_time(lighting)

        if wifi.get_datetime() < lighting:
            # Manage turning the candles on at the appropriate time
            while wifi.get_datetime() < lighting:
                menorah.sleep_based_on_delta(lighting, wifi.get_datetime())

        if lighting <= wifi.get_datetime() < off_time:
            # Manage turning the candles off at the appropriate time
            menorah.light_candles(night_index + 1)
            if not menorah.is_muted:
                menorah.play_sound("support/maoztzur.rtttl")
                while wifi.get_datetime() < off_time:
                    menorah.sleep_based_on_delta(off_time, wifi.get_datetime())
            if BURNOUT:
                menorah.turn_off_candles()

    if not BURNOUT:
        final_off_time = lighting_times[7] + timedelta(hours=24)
        while wifi.get_datetime() < final_off_time:
            menorah.sleep_based_on_delta(final_off_time, wifi.get_datetime())
            menorah.turn_off_candles()


# Initialize candles
shamash = DigitalInOut(board.A2)
shamash.direction = Direction.OUTPUT
candles_pins = [
    board.RX,
    board.SCK,
    board.MISO,
    board.MOSI,
    board.A3,
    board.SDA,
    board.SCL,
    board.TX,
]
candles_dios = []
for gpio_pin in candles_pins:
    gpio_dio = DigitalInOut(gpio_pin)
    gpio_dio.direction = Direction.OUTPUT
    candles_dios.append(gpio_dio)
piezo_pin = board.A0
mute_dio = DigitalInOut(board.A1)
mute_dio.direction = Direction.INPUT
menorah = Menorah(shamash, candles_dios, piezo_pin, mute_dio)

wifi = WiFi()

connection_status = ConnectionStatus()

if __name__ == "__main__":
    asyncio.run(setup_menorah())
    main()
