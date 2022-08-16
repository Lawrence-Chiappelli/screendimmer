import configparser
import utils

from os import path

"""
A glorified wrapper for configparses and parsing .ini configuration files.

To get your config contents, edit and call retrieve_configuration_file.

That function will automate the steps that need to be taken
care of before your config file can be used!
"""

config = configparser.ConfigParser()  # <--- initially empty

def retrieve_configuration_file():
    """Retrieve your parsed configuration file

    @return (None): if the config file was not found
    @raise type: [description]
    """

    config.read(path_to_config, encoding='utf-8')
    if config and path_to_config:
        return config
    else:
        return None


def save():

    with open(path_to_config, 'w') as new_changes:
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


def get_ini_path(file_name='config.ini', pkgname='screendimmer', in_production=True, continue_if_not_found=True):
    print(f"Getting INI path")
    """The path to the .ini that keeps track of monitor brightness levels and theme preference

    @param file_name (str): The raw name of your configuration file, include the extension
    @param pkgname (str): Part of the path, according to Linux file placement conventions (see code)
    @param in_production (bool): Set this to False if you want to test locally and have your config
    file installed in the production path, otherwise this really doesn't matter, keep as True
    @param continue_if_not_found (bool): Continue the program normally if True

    @return (str, None): Return the string path if config found, or None if not found
    @raise FileNotFoundError: Abort the program if program not found
    """

    absolute_path_production = f'/etc/{pkgname}/{file_name}'
    root_path_development = f"{file_name}"
    up_one_path_development = f'../{file_name}'

    if in_production and path.exists(absolute_path_production):
        print(f"✓ - In production envionment, {file_name} found at {absolute_path_production}")
        return absolute_path_production
    elif path.exists(root_path_development):
        print(f"✓ - In development envionment, {file_name} found at ./{root_path_development}")
        return root_path_development
    elif path.exists(up_one_path_development):
        print(f"✓ - In development envionment, {file_name} found at {up_one_path_development}")
        return up_one_path_development
    else:
        feedback_for_user = f"Unable to find the configuration file {file_name}.\
        I attempted to look for the file in the following places:\n \
        {absolute_path_production}\n{root_path_development}\n{up_one_path_development}\n \
        Maybe the file was moved or deleted?"

        if continue_if_not_found:
            print(feedback_for_user)
            return None
        else:
            raise FileNotFoundError(feedback_for_user)


if __name__ == 'main':
    print(f"This should be an imported module")

# Edit this:
path_to_config = get_ini_path(
    file_name='config.ini',
    pkgname='screendimmer',
    in_production=False,
    continue_if_not_found=True
)
