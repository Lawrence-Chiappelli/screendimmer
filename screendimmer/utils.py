import platform
from os import path


def get_icon_path():

    file_name = "screendimmer.png"
    image_path = f"/usr/share/pixmaps/{file_name}"

    if platform.system() == "Linux" and path.exists(image_path):
        print(f"Image file path: {image_path}")
        return image_path
    else:
        print(f"Icon file path: (root)")
        return "../"+file_name


def get_config_path():

    raw_file_name = 'brightness.ini'
    linux_path = f'/etc/screendimmer/{raw_file_name}'
    if platform.system() == "Linux" and path.exists(linux_path):
        print(f"Brightness file path: {linux_path}")
        return linux_path
    else:
        print(f"Brightness file path: {raw_file_name} (root)")
        return "../"+raw_file_name
