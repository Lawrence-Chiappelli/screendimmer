from decimal import *

def convert_xrandr_brightness_to_int(brightness_val: str):
    """Convert the raw xrandr brightness value to a human readable integer.

    @param brightness_val (str): Xrandr representation of brightness.
    Note that xrandr brightness uses values between 0.0 and 1.0. These are
    strings, not ints/floats!
    @return (int): Tkinter representation of brightness.
    Xrandr brightness value as a shifted-by-two-decimals integer.
    Example: 0.3 = 30
    @raise TypeError: Raise a TypeError if the user already casted the input.
    """

    if not type(brightness_val) is str:
        raise TypeError("Only strings allowed. Note that values retrieved from Linux OS are strings.")

    if float(brightness_val) < 1.0:
        brightness_val = "{:.2f}".format(float(brightness_val))

    return Decimal(brightness_val).shift(2)

def convert_converted_brightness_to_xrandr(brightness_val: str):
    """Convert the "tkinter" brightness to an xrandr-usable value.

    @param brightness_val (str): Tkinter representation of brightness.
    Ideally, this value should automatically come from the spinner/scale.
    @return (str): Xrandr representation of brightness.
    @raise TypeError: Only strings should be passed. Keep things simple.
    @raise ValueError: Values between 1 and 100 only. May or may not change.
    """

    if not type(brightness_val) is str:
        raise TypeError("Only strings allowed. Note that values retrieved from TK spinners/scales are strings.")

    if not int(brightness_val) > -1 and int(brightness_val) < 101:
        raise ValueError("Brightness should be between 1 and 100 - inclusive.")

    return str(Decimal(float(brightness_val) / 100))
