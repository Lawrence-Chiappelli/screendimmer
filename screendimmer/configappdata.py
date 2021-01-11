import configparser
from screendimmer import utils


def get_application_metadata(is_building=True):

    """
    :param is_building: Path to screendimmer.desktop
    can be extracted from current directory, no
    need to change directories (assuming we are in the
    process of building, as in the case of setup.py)
    :return: The screendimmer.desktop configuration
    file. The file itself uses the .ini standard,
    so it can be processes like any regular .ini
    configuration file.
    """

    desktop_config = configparser.ConfigParser()
    desktop_path = 'screendimmer.desktop' if is_building else utils.get_desktop_path()
    desktop_config.read(desktop_path, encoding='utf-8')
    return desktop_config
