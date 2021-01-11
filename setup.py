from setuptools import setup
from screendimmer.utils import running_from_pycharm, get_readme_path
from screendimmer.configappdata import get_application_metadata


if running_from_pycharm():
    print(f"Running from PyCharm, skipping `$ python setup.py build`")
    config = get_application_metadata(False)
else:
    config = get_application_metadata(True)
    app_name = config['Desktop Entry']['Name'].replace(" ", "").lower()

    with open(get_readme_path()) as f:
        long_description = f.read()

    setup(
        name=app_name,
        version=config['Desktop Entry']['Version'],
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
