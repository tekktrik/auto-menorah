import time
from adafruit_datetime import timedelta

try:
    from typing  import List
    from digitalio import DigitalInOut
    from adafruit_datetime import datetime
except ImportError:
    pass


class Menorah:
    """Class for representing the menorah and manages lighting and flickering the candles
    """
    
    def __init__(self, shamash_dio: DigitalInOut, candles_dio: List[DigitalInOut]):

        self.shamash = shamash_dio
        self.candles = candles_dio

    @staticmethod
    def get_menorah_off_time(lighting_time: datetime) -> datetime:
        """Get the time at while candles should be turned off
        
        :param datetime lighting_time: The time at which candles should be lit for that day
        """
        hour_difference: datetime = 29 - lighting_time.hour
        projected_time: datetime = lighting_time + timedelta(hours=hour_difference)
        projected_time.minute = 0
        projected_time.second = 0
        projected_time.microsecond = 0
        return projected_time

    @staticmethod
    def sleep_based_on_delta(lighting_time: datetime, current_time: datetime) -> None:
        """Sleeps the program for a given amount of time depending on the time delta
        
        :param datetime lighting_time: The time at which candles should be lit for that day
        :param datetime current_time: The current time
        """
        time_diff: timedelta = lighting_time - current_time
        time_diff_s = time_diff.total_seconds()
        time_to_sleep = 60 if time_diff_s > 60 else time_diff_s
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)
