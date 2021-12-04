from adafruit_datetime import timedelta

try:
    import typing  # pylint = disable:unused-import
    from digitalio import DigitalInOut
    from adafruit_datetime import datetime
except ImportError:
    pass


class Menorah:
    """Class for representing the menorah and manages lighting and flickering the candles
    """
    
    def __init__(self, shamash_dio: DigitalInOut, candles_dio: DigitalInOut):

        self.shamash = shamash_dio
        self.candles = candles_dio

    @staticmethod
    def get_menorah_off_time(lighting_time: datetime) -> datetime:
        """Get the time at while candles should be turned off"""
        hour_difference: datetime = 29 - lighting_time.hour
        projected_time: datetime = lighting_time + timedelta(hours=hour_difference)
        projected_time.minute = 0
        projected_time.second = 0
        projected_time.microsecond = 0
        return projected_time
