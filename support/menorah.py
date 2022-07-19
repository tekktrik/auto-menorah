# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`menorah`
================================================================================

Module for managing lighting and turning off candles, as well as the
piezo speaker

* Author: Alec Delaney
"""

import time
from adafruit_datetime import timedelta
from adafruit_rtttl import play

try:
    from typing import List
    from microcontroller import Pin
    from digitalio import DigitalInOut
    from adafruit_datetime import datetime  # pylint: disable=ungrouped-imports
except ImportError:
    pass


class Menorah:
    """Class for representing the menorah and manages lighting and flickering the candles

    :param DigitalInOut shamash_dio: The shamash candle digital io
    :param List[DigitalInOut] candles_dio: The candles digital ios
    """

    def __init__(
        self,
        shamash_dio: DigitalInOut,
        candles_dio: List[DigitalInOut],
        piezo_pin: Pin,
        mute_dio: DigitalInOut,
    ):

        self.shamash = shamash_dio
        self.candles = candles_dio
        self.piezo_pin = piezo_pin
        self._mute_dio = mute_dio

    @staticmethod
    def get_sleep_time_based_on_delta(
        lighting_time: datetime, current_time: datetime
    ) -> float:
        """Get the amount of time to sleep depend on the time delta

        :param datetime lighting_time: The time at which candles should be lit for that day
        :param datetime current_time: The current time
        """

        time_diff: timedelta = lighting_time - current_time
        time_diff_s = time_diff.total_seconds()
        return 60 if time_diff_s > 60 else time_diff_s

    @staticmethod
    def sleep_based_on_delta(lighting_time: datetime, current_time: datetime) -> None:
        """Sleeps the program for a given amount of time depending on the time delta

        :param datetime lighting_time: The time at which candles should be lit for that day
        :param datetime current_time: The current time
        """

        time_to_sleep = Menorah.get_sleep_time_based_on_delta(
            lighting_time, current_time
        )
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    def _set_candles(
        self, num_candles: int, candle_state: bool, light_shamash: bool = True
    ) -> None:
        """Sets the state of a given number of candles

        :param int num_candles: The number of candles to light
        :param bool candle_state: The candle state to set
        :param bool light_shamash: Whether the shamash should also be lit, if other candles are
        """

        shamash_setting = light_shamash if candle_state else False
        self.set_shamash(shamash_setting)
        for candle in self.candles[0:num_candles]:
            candle.value = candle_state

    def turn_off_candles(self) -> None:
        """Turns off all the candles of the menorah"""

        self._set_candles(8, False)

    def light_candles(self, night_number: int, light_shamash: bool = True) -> None:
        """Turns on a given number of candles on the menorah

        :param int number_number: The Hannukah night number
        :param bool light_shamash: Whether the shamash should be lit
        """
        self.turn_off_candles()
        self._set_candles(night_number, True, light_shamash=light_shamash)

    def set_shamash(self, candle_setting: bool) -> None:
        """Sets the shamash setting

        :param bool candle_setting: The candle state to set
        """

        self.shamash.value = candle_setting

    @property
    def is_muted(self) -> bool:
        """Whether the speaker is set to the muted position"""
        return not self._mute_dio.value

    def play_sound(self, sound_file: str) -> None:
        """Play the given RTTTL file

        :param str sound_file: The RTTTL sound file to play
        """

        with open(sound_file, mode="r", encoding="utf-8") as rtttl_file:
            rtttil_contents = rtttl_file.read()
        play(self.piezo_pin, rtttil_contents)
