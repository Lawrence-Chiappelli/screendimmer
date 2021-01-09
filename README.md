# Screen Dimmer

This software is a light-weight tray application that dims your monitor brightness.

**Note**: this software was developed with Arch Linux support in mind.

## **Table of contents**:

* [How does it work?](#How-does-it-work?)
* [Preview](#Preview)
* [Install instructions](#Install-instructions)
* [Technology used](#Technology-used)
* [Wish list](#Wish-list)
* [Motivations](#Motivations)
* [Attributions](#Attributions)

## How does it work?

Right-click the tray icon and select a brightness-level. You can quickly specify which monitors you want to brightness level to apply to. Currently supports up to 3 monitors.

Open with `$ screendimmer`, or search the desktop file `Screen Dimmer`. Brightness level is persistent across each application launch.

## Preview

<img src="https://raw.githubusercontent.com/Lawrence-Chiappelli/screendimmer/main/preview.png"/>

## **Install instructions**

- Arch Linux: `$ yay -S screendimmer`
- Other Linux distros: `TBD`
- Windows: `TBD`
- OSX: `TBD`

## Technology used

**Software**

- [Python 3.9](https://www.python.org/downloads/release/python-390/) - Language of choice
- [PyQt5](https://pypi.org/project/PyQt5/) - The tools to build the tray application
- [screeninfo](https://github.com/rr-/screeninfo) - A useful wrapper for monitor info retrieval

**System**

- Arch Linux - Linux Distro
- i3wm - Window Manager
- LXDE - desktop environment

**Note**: If the tray application looks different from what I screenshotted above, it is most probably due to differences between system  environments.

## Wish list

In order of preference:

- Programmatically create dynamic support for any number of monitors
- Out of the box Windows 10 support
- Out of the box support for other Linux distros
- More accurate monitor names, preferably their brand names
- Support for `xbacklight`

If you make a pull request, it is your preference as to which item you'd like to tackle. It should also be noted I'm open to constructive criticism.

## Motivations

#### AUR

Arch Linux users should be able to search `screen dimmer` on the [Arch User Repository](https://aur.archlinux.org/) to download and install an out-of-the-box GUI-like screen dimmer.

At the time of writing this, I was unsuccessful in finding a screen dimming software with a simple `screen dimmer` search term. If they exist, they're using brand names or "terminology-specific" names in leiu of "screen dimmer". Thus, I programmed a tray icon GUI to handle monitor brightness with the name 'screen dimmer'. That's (mostly) all there is to it.

The only relevent dimming software I could find for Arch Linux is [desktop-dimmer 4.0.4-2](https://aur.archlinux.org/packages/desktop-dimmer/), and, consequently, was unable to compile on my system out of the box. Despite the workarounds in the comments, I found it more time efficient to use `xrandr` in the terminal and move onto other system configuration.

That being said, this software automation will boost productivity in place of the terminal command `$ xrandr --output $monitor --brightness $brightness_value`. More details below.

#### Using xrandr vs xbacklight

This program relies exclusively on xrandr, for the time being.

According to [this Stack Overflow answer](https://unix.stackexchange.com/questions/181496/how-do-dim-screen-even-if-artifically-below-the-minimum/181501#181501), `xrandr` is more-or-less a pseudo screen dimming solution, such that it alters RGB values and not the hardware directly. However, having worked previously with said hardware, I personally find no difference in dimness quality between `xrandr` and `xbacklight`. The use of `xrandr` has always been perfectly sufficient for my eye-saving needs.

## Other

#### Intent

All other intent of this software is to improve my programming skills, help Arch Linux beginners/users find a screen dimmer, and also open the gates to potential GUI applications that I could develop for Linux. If you like this software and would like to see more, please consider [donating](https://www.paypal.com/donate?hosted_button_id=YUU33PC5DC592).

#### Credit

Special thanks to trusted Arch Linux user eschwartz for helping me with the PKGBUILD and getting the software up and running on the AUR.

## Attributions

The lightbulb icon was downloaded from flaticon.com, and as such, requests that I add the following attribution:

<div>Icons made by <a href="https://www.flaticon.com/authors/iconixar" title="iconixar">iconixar</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
