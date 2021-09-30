from setuptools import setup
from screendimmer.utils import get_readme_path, get_desktop_file_metadata

desktop_config = get_desktop_file_metadata()
app_name = desktop_config['Desktop Entry']['Name'].replace(" ", "").lower()

with open(get_readme_path()) as f:
    long_description = f.read()

setup(
    name=app_name,
    version=desktop_config['Desktop Entry']['Version'],
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
