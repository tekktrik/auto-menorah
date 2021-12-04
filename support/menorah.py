try:
    import typing  # pylint = disable:unused-import
    from digitalio import DigitalInOut
except ImportError:
    pass


class Menorah:
    """Class for representing the menorah and manages lighting and flickering the candles
    """
    
    def __init__(self, shamash_dio: DigitalInOut, candles_dio: DigitalInOut):

        self.shamash = shamash_dio
        self.candles = candles_dio
