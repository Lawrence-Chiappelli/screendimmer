from decimal import *

def convert_xrandr_brightness_to_int(brightness_val: str):
    """Convert the raw xrandr brightness value to a human readable integer.
    @param brightness_val (str): Xrandr representation of brightness.
    Note that xrandr brightness uses values between 0.0 and 1.0. These are
    strings, not ints/floats!
    @return (int): Xrandr brightness value as a shifted-by-two-decimals integer.
    Example: 0.3 = 30
    @raise TypeError: Raise a TypeError if the user already casted the input.
    """


    if not type(brightness_val) is str:
        raise TypeError("Only strings allowed. Note that the retrieved values from Linux OS are strings.")

    if float(brightness_val) < 1.0:
        brightness_val = "{:.2f}".format(float(brightness_val))

    return Decimal(brightness_val).shift(2)
