from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="screendimmer",
    version='0.1.0',
    description='A tray application designed to dim the brightness of your monitors',
    license="MIT",
    long_description=long_description,
    author='Lawrence C',
    author_email='lawrencechip@protonmail.com',
    url='https://github.com/lawrence-chiappelli/screen-dimmer',
    packages=['screendimmer'],
    include_package_data=True,
    install_requires=[
        'screeninfo',
        'PyQt5'
    ],
    entry_points={
        'gui_scripts': [
            'screendimmer=screendimmer.tray:create_tray',
        ],
    },
)
