import configparser
from screendimmer import utils
from setuptools import setup


def get_application_metadata():

    """
    :return: The screendimmer.desktop configuration
    file. The file itself uses the .ini standard,
    so it can be processes like any regular .ini
    configuration file.
    """

    desktop_config = configparser.ConfigParser()
    desktop_path = utils.get_desktop_path()
    desktop_config.read(desktop_path, encoding='utf-8')
    return desktop_config


config = get_application_metadata()['Desktop Entry']

if utils.running_from_pycharm():
    print(f"Running from PyCharm, skipping `$ python setup.py build`")
else:
    app_name = config['Name'].replace(" ", "").lower()

    with open(utils.get_readme_path()) as f:
        long_description = f.read()

    setup(
        name=app_name,
        version=config['Version'],
        description='A tray application that dims your monitor brightness.',
        license="MIT",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='Lawrence Chiappelli',
        author_email='lawrencechip@protonmail.com',
        url=f'https://github.com/Lawrence-Chiappelli/{app_name}',
        packages=[f'{app_name}'],
        include_package_data=True,
        install_requires=[
            'screeninfo',
            'PyQt5'
        ],
        entry_points={
            'gui_scripts': [
                f'{app_name}={app_name}.tray:create_tray',
            ],
        },
    )
