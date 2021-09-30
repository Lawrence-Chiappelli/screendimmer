# Screen Dimmer

This software is a GUI tray application that dims your monitor brightness.

**This software was developed with Arch Linux support.**

## **Table of contents**:

- Software
  - [Preview](#Preview)
  - [Installation](#Installation)
  - [How to use](#How-to-use)
  - [Technology used](#Technology-used)


- Other:
  - [Wish list](#Wish-list)
  - [Support](#Support)
  - [Motivations](#Motivations)    
  - [Attributions](#Attributions)

## Preview

<p align="center">
  <kbd>
    <img src="https://raw.githubusercontent.com/Lawrence-Chiappelli/screendimmer/main/resources/preview.png"/>
  </kbd>
</p>

## **Installation**

There are 2 recommended methods of installation:

### 1) Via AUR

In your terminal, type:

`$ yay -S screendimmer`

Where `yay` represents the [AUR helper](https://wiki.archlinux.org/title/AUR_helpers) of your choice.

### 2) Manual

Install the following dependencies:

- `python`
- `python-screeninfo`
- `python-pyqt5`

Then clone this repository.

After cloning:

1) Change directory to `$download_location/screendimmer/screendimmer`
2) Run `python tray.py`

**Done**. The screen dimmer should be running.

It's required to be changed into the above directory. Application resource file paths are hardcoded until further notice. So, if you make a helper script, make sure it change into that directory first. This options is best if all you want is the application up and running.

#### OR:

Take it a step a further. These steps will get your desktop file up and running:

1) Move or copy the following resources to these directories:
- `/etc/screendimmer/brightness.ini`
- `/usr/share/applications/screendimmer.desktop`
- `/usr/share/pixmaps/screendimmer.png`
2) `$ cd $download_location/screendimmer/screendimmer/`
3) `$ python tray.py`

The program searches for those paths first. If they do not exist there, it will use the files relative to your initial download.

Manual installations are performed at your own risk.

## How to use

Right-click the tray icon and select a brightness-level. You can easily specify which monitors you want to brightness level to apply to. Currently supports up to 3 monitors.

Open with `$ screendimmer`, or search the desktop file `Screen Dimmer`. Brightness level is persistent across each application launch.

## Technology used

**Software**

- [Python 3.9](https://www.python.org/downloads/release/python-390/) - Language of choice
- [PyQt5](https://pypi.org/project/PyQt5/) - The tools to build the GUI / tray
- [screeninfo](https://github.com/rr-/screeninfo) - A useful wrapper for monitor info retrieval
- [xrandr](https://wiki.archlinux.org/title/xrandr) - Linux configuration utility that adjusts the raw brightness (see [motivations](#motivations))

**My System**

- Linux Distro - `Arch`
- Window Manager - `i3wm`
- Desktop Environment - `none`
- Other - `lxappearance`

The tray application on your system may look visually different compared to my [preview](#preview) screenshot above. If that's the case, chances are it's a difference between our system setups.

## Wish list

In order of preference, these are the features I would *like* to have implemented as nice-to-haves:

- Toggle-able light/dark mode button
- Dynamically detect/update monitors (while maintaining performance)
- Better file resource pathing support
- Out-of-the-box support for other Linux distros
- Alternative monitor name labels (such as their brand name)
- Support for `xbacklight`
- Out-of-the-box Windows 10 support

## Support

If you like this application, please consider showing support. Showing support can include ways other than monetarily or raw code. Here are some suggestions:

1) Upvote on the AUR
2) Report a bug
3) Package this software for other distros
4) Implement a feature mentioned in [wish-list](#Wish-list)
5) Donate on PayPal [here](https://www.paypal.com/donate?hosted_button_id=YUU33PC5DC592)

### Bug reporting

To report a bug:

1) Open the application in terminal with `$ screendimmer` (assuming AUR install)
2) Replicate the issue
3) Screenshot/copy+paste any errors/tracebacks from the terminal
4) Provide a description of the issue and any details you feel are necessary to share

## Motivations

This software should boost productivity by automating the terminal command `$ xrandr --output $monitor --brightness $brightness_value`.

At the time of writing this, I was unsuccessful in finding a screen dimming software with a simple `screen dimmer` search term. If they exist, they're using brand names or "terminology-specific" names in leiu of "screen dimmer". This issue becomes paramount as beginners (as I once was, to both Arch and Linux) need a quick screen dimming solution and aren't necessarily sure how to approach adjusting monitor brightness on a software level.

Thus, I programmed a tray icon GUI to handle monitor brightness with the name 'screen dimmer'. That's (mostly) all there is to it.

#### AUR

Arch Linux users should be able to search `screen dimmer` on the [Arch User Repository](https://aur.archlinux.org/) to download and install an out-of-the-box GUI-like screen dimmer.

The only relevent dimming software I could find for Arch Linux is [desktop-dimmer 4.0.4-2](https://aur.archlinux.org/packages/desktop-dimmer/), and, consequently, was unable to compile on my system out of the box. Despite the workarounds in the comments, I found it more time efficient to use `xrandr` in the terminal and move onto other system configuration.

#### Using xrandr vs xbacklight

This program relies exclusively on xrandr. My personal desktop does not support xbacklight.

According to [this Stack Overflow answer](https://unix.stackexchange.com/questions/181496/how-do-dim-screen-even-if-artifically-below-the-minimum/181501#181501), `xrandr` is more-or-less a pseudo screen dimming solution, such that it alters RGB values and not the hardware directly. However, having worked previously with said hardware, I personally find no difference in dimness quality between `xrandr` and `xbacklight`. The use of `xrandr` has always been perfectly sufficient for my eye-saving needs.

## Intent

All other intent of this software is to improve my programming skills, help Arch Linux beginners/users find a convenient screen dimmer, and also open the gates to potential GUI applications that I could develop for Linux.

## Credit

Special thanks to trusted Arch Linux user eschwartz for helping me with the PKGBUILD and getting the software up and running on the AUR.

## Attributions

The lightbulb icon (used as the desktop icon) was downloaded from flaticon.com and requests that I add the following attribution:

> <div>Icons made by <a href="https://www.flaticon.com/authors/iconixar" title="iconixar">iconixar</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
