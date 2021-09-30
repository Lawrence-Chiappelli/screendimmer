import platform
import subprocess

from screeninfo import get_monitors

monitor_names = [monitor.name for monitor in get_monitors()]


def apply_brightness(brightness_level):

    """
    :param brightness_level: The brightness
    level to apply through config and on
    the operating system level.
    Is string to accommodate bash-level
    commands.
    :return: True if want to save
    False otherwise
    """

    print(f"Brightness level: {brightness_level}", end='')

    # Run changes on system
    if platform.system() == "Linux":
        # In this case, use bash:
        for monitor in monitor_names:
            bashCommand = f"xrandr --output {monitor} --brightness {brightness_level}"
            subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            print(f" -> Applied to {monitor}", end='')
        print("")


def convert_label_to_xrandr(label_text: str):

    """
    :param label_text: Assuming the passed
    variable is a string from a label,
    such as 30%
    :return: The converted float value that
    matches the format of xrandr
    """

    return float(str(label_text).replace("%", "")) / 100


def convert_xrandr_to_index(xrandr_val: float):

    """
    :param xrandr_val: usually comes from the
    config value directly, as a string (it's
    just the nature of directly retrieving
    information from a .ini file)
    :return: an index representation
    of the current brightness level, useful
    for switch functions (where we switch
    based on indexes and not string values)
    Example: 0.2 is converted to 1
    """

    return int(xrandr_val * 10 - 1)


def increment():

    """
    Increment the brightness by exactly 0.1 point.
    Currently unused, but useful for testing or
    future expansion.
    :return: None
    """

    val = float(config['brightness']['level'])
    if val >= 1.0:
        print(f"At max brightness!")
    else:
        new_value = "{:.1f}".format(val + 0.1)
        apply_brightness(new_value)


def decrement():

    """
    Decrement the brightness by exactly 0.1 point.
    Currently unused, but useful for testing or
    future expansion.
    :return: None
    """

    val = float(config['brightness']['level'])
    if val <= 0.1:
        print(F"At min brightness!")
    else:
        new_value = "{:.1f}".format(val - 0.1)
        apply_brightness(new_value)

