import platform
from os import path, getenv


def get_icon_path():

    file_name = "screendimmer.png"
    image_path = f"/usr/share/pixmaps/{file_name}"

    if platform.system() == "Linux" and path.exists(image_path) and not running_from_pycharm():
        print(f"Image file path: {image_path}")
        return image_path
    else:
        print(f"Icon file path: (root)")
        return "../"+file_name


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

    raw_file_name = 'screendimmer.desktop'
    linux_path = f'/usr/share/applications/screendimmer/{raw_file_name}'

    if platform.system() == "Linux" and path.exists(linux_path) and not running_from_pycharm():
        print(f"Desktop file path: {linux_path}")
        return linux_path
    else:
        print(f"Desktop file path: {raw_file_name} (root)")
        return "../"+raw_file_name


def get_config_path():

    """
    :return: The path to the configuration file,
    mainly for keeping track of brightness levels.

    Three types of config paths:
        1) current root directory
        2) /etc/$pkgname (Linux)
        3) The .desktop file in /usr/share/applications/$pkgname.desktop
    """

    raw_file_name = 'brightness.ini'
    linux_path = f'/etc/screendimmer/{raw_file_name}'

    if platform.system() == "Linux" and path.exists(linux_path) and not running_from_pycharm():
        print(f"Brightness file path: {linux_path}")
        return linux_path
    else:
        print(f"Brightness file path: {raw_file_name} (root)")
        return "../"+raw_file_name


def get_readme_path():

    """
    :return: The README.md path
    (not necessarily OS specific)
    """

    if running_from_pycharm():
        return '../README.md'
    else:
        return 'README.md'


def running_from_pycharm():

    """
    :return: True if we are running the Tray application
    from Pycharm IDE, False otherwise.
    Remove usage of this function to see the resulting
    pathing errors. Or, install this program and try both
    combinations of pathing and examine the errors.
    """

    return getenv("PYCHARM_HOSTED") is not None
