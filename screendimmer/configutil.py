import configparser

try:
    import utils
except ImportError:
    from screendimmer import utils

config = configparser.ConfigParser()
ini_config = utils.get_ini_path()


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
