try:
    import typing  # pylint = disable:unused-import
    from digitalio import DigitalInOut
except ImportError:
    pass


class Menorah:
    def __init__(self, shamash_dio: DigitalInOut, candles_dio: DigitalInOut):

        self.shamash = shamash_dio
        self.candles = candles_dio
