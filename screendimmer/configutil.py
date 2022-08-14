import configparser
# try:
import utils
# except ImportError:
#     from screendimmer import utils

from os import path

"""
A glorified wrapper for configparses and parsing .ini configuration files.
"""

def get_parsed_config():

    """
    :return: the parsed version of the config file.
    Note: it is encoded as utf-8 so that emojis
    can be retrieved (it wouldn't work otherwise)
    Otherwise, return None (not a critical feature)
    """

    if ini_config:
        config.read(ini_config, encoding='utf-8')
        return config

    return None


def get_ini_path(file_name='config.ini', in_production=True):
    """The path to the .ini that keeps track of monitor brightness levels and theme preference

    @param in_production (bool): Allows the developer to forcefully not check for the prod path
    @return (str): The path to config.ini

    Available pathing options:
        1) Development: ../brightness.ini
        2) Production: /etc/$pkgname/brightness.ini (Linux, for production)
        3) The .desktop file in /usr/share/applications/$pkgname.desktop (after packaging)
    """

    # TODO: may want to rewrite this to be more general for config files
    # abstract between production, development, and fallback
    ini_path_production = f'/etc/screendimmer/{file_name}'

    if in_production and path.exists(ini_path_production):
        print(f"✓ - Brightness file path:\t{file_name} @ {ini_path_production}")
        return ini_path_production
    else:
        print(f"x - Unable to find {file_name} file from path {ini_path_production}. Using local file.")

    if path.exists(file_name):
        return file_name

    return f"../{file_name}"  # Implies that users are cd'd into root directory of tray.py


def overwrite_config_section(section: str, section_items: list):

    """
    :param section: The name of the section category
    :param section_items: For iterating over the section
    :return: None
    """

    if list(config[section]) == section_items:
        return  # No need to overwrite for equivalent lists

    def _converted_to_key(obj):
        return str(obj).replace(" ", "").lower()

    for item in section_items:
        key = _converted_to_key(item)
        config[section][key] = item


def write_brightness(brightness_level: str):

    """
    :param brightness_level: Brightness level to write
    to config file. Does not necessarily save the
    changes to storage. Call save_changes() if
    you'd like to save the written changes.
    """

    config['brightness']['level'] = brightness_level


def save_changes():

    with open(ini_config, 'w') as new_changes:
        config.write(new_changes)


def print_entire_config_for_verification():

    """
    :return: None
    Should just print out the config
    in a "1-to-1" style (i.e., should
    look exactly the same as the
    brightness.ini file)
    """

    for section in config.sections():
        print(f"[{section}]")
        for item in config.items(section):
            print(f"{item[0]} = {item[1]}")
        print(f"")


def print_specific_section_items_for_verification(section_name: str):

    """
    :param section_name: Section name as a string
    :return: None
    """

    print(f"[{section_name}]")
    for item in config[section_name].items():
        print(f"{item[0]} = {item[1]}")
    print(f"")


def get_key_name_as_convention(desired_name: str):

    """
    :param desired_name: The name you would
    like to convert
    :return: The key name as a personal
    convention I'm using for brightness.ini
    """

    return desired_name.lower().replace(" ", "").replace(":", "")


if __name__ == 'main':
    print(f"This should not be the main module")
else:
    config = configparser.ConfigParser()
    ini_config = get_ini_path(file_name='config.ini', in_production=False)
