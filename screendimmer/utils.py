import os
import sys
import platform
import configparser
from os import path
print(f"Checking system resources... (Current working directory: {os.getcwd()})")

"""
For non-config utilities
"""


def sys_env_checker(func):
    """
    :param func: Function to wrap
    and validate system environment
    :return: func() if system
    environment is valid.

    Specifically, we want to check
    for OS compatibility and cmd
    line argument validity. Any
    invalid setups will call
    sys.exit() and exit
    the program.
    """

    def inner():

        if platform.system() != "Linux":  # TODO: Remove from decorator if more OS's are supported
            print("This OS is currently not supported. Please check the repo if you'd like to make changes.")
            sys.exit()

        try:
            return func()
        except NameError as ne:
            print("\nThere was an issue running the program.")
            print(F"An exception was caught. Please report upstream or re-install the application:\n{ne}")
            sys.exit()

    return inner


def open_donation_link():

    url = "https://www.paypal.com/donate?hosted_button_id=YUU33PC5DC592"
    if platform.system() == "Linux":
        os.system(f"xdg-open \"{url}\"")
    elif platform.system() == "Windows":
        os.system(f"start \"{url}\"")
    else:
        return


@sys_env_checker
def get_ini_path():

    """
    :return: The path to the configuration file,
    mainly for keeping track of brightness levels.

    Three types of config paths:
        1) current root directory (for development)
        2) /etc/$pkgname (Linux, for production)
        3) The .desktop file in /usr/share/applications/$pkgname.desktop (after packaging)
    """

    file_name = 'brightness.ini'
    ini_path_production = f'/etc/screendimmer/{file_name}'

    if path.exists(ini_path_production):
        print(f"✓ - Brightness file path:\t{file_name} @ {ini_path_production}")
        return ini_path_production
    else:
        print(f"x - Unable to find {file_name} file from path {ini_path_production}. Using local file.")

    if path.exists(file_name):
        return file_name

    return f"../{file_name}"  # Implies that users are cd'd into root directory of tray.py


@sys_env_checker
def get_desktop_path():

    """
    :return: Path to the .desktop file

    Note: the .desktop file uses the .ini
    standard, and so information can retrieved
    like a regular configuration file.
    The use case for this is to retrieve the
    application metadata information from one
    place.

    Path to .desktop files:
    $pkgdir/usr/share/applications/$pkgname.desktop
    """

    file_name = 'screendimmer.desktop'
    desktop_path_production = f'/usr/share/applications/{file_name}'

    if path.exists(desktop_path_production):
        print(f"✓ - Desktop file:\t{file_name} @ {desktop_path_production}")
        return desktop_path_production
    else:
        if len(sys.argv) > 1 and sys.argv[1] == "build":
            print(f"Installing desktop file to {desktop_path_production}")
        else:
            print(f"x - Unable to find {file_name} file from path {desktop_path_production}. Using local file.")

    if path.exists(file_name):
        return file_name

    return f"../{file_name}"  # Implies that users are cd'd into root directory of tray.py


@sys_env_checker
def get_icon_path():

    file_name = "resources/screendimmer.png"
    icon_path_production = f"/usr/share/pixmaps/{file_name}"

    if path.exists(icon_path_production):
        print(f"✓ - Icon file:\t\t{file_name} @ {icon_path_production}")
        return icon_path_production
    else:
        print(f"x - Unable to find {file_name} file from path {icon_path_production}. Using local file.")

    if path.exists(f"resources/{file_name}"):
        return f"resources/{file_name}"

    return f"../resources/{file_name}"  # Implies that users are cd'd into root directory of tray.py


@sys_env_checker
def get_desktop_file_metadata():

    """
    :return: The 'read' config file

    A wrapper to get and read the actual
    content of the screendimmer.desktop file.
    """

    desktop_config = configparser.ConfigParser()
    desktop_config.read(get_desktop_path(), encoding='utf-8')

    return desktop_config


@sys_env_checker
def get_readme_path():

    """
    :return: The README.md path

    Should only be used by README.md
    """

    if path.exists("README.md"):
        return 'README.md'

    return "../README.md"  # Implies that users are cd'd into root directory of tray.py
