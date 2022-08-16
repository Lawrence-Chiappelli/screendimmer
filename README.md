# Screen Dimmer

A Linux desktop tray application designed to dim your monitor's brightness.

(Show previews)

## Features

- Light/dark mode toggle
- Supports any number of monitors
- Supports duplicated monitors
- Supports extended monitors
- [b]Fine-tuned control over monitors[/b]
    - Individual monitor toggles
    - Individual monitor brightness scrollbars
    - Global monitor brightness scrollbar
    - Global scrollbar accounts for toggled monitors
    - Manual entry box for typing brightness level
    - Manual entry box updates brightness as you type
    - Values are restricted from 1%-100% for user safety

## Installation

This software was developed with Arch Linux support in mind.

As I am only familiar with the Arch distribution, I am unable to offer support for installation on other Linux distros.

If you successfully get the program installed and running on another distro, please document your process and I'll be more than happy to get it listed as one of the supported operating systems.

<!-- TODO: add images next to each -->
<table style="width:100%">
  <tr>
    <th>Operating System</th>
    <th>Method</th>
    <th>Instructions</th>
  </tr>
  <tr>
    <td>Linux</td>
    <td>Manual <i>(you assume responsibility)</i></td>
    <td>`$ git clone [url]`<br>`$ python screendimmer/__main__.py`</td>
  </tr>
  <tr>
    <td>Arch Linux</td>
    <td>Arch User Repository</td>
    <td>`$ yay -S screendimmer`<br>Where `yay` represents your <a href='https://wiki.archlinux.org/title/AUR_helpers'>AUR helper</a>.</td>
  </tr>
  <tr>
    <td>Pop OS</td>
    <td>WIP</td>
    <td>WIP</td>
  </tr>
  <tr>
    <td>Windows 10</td>
    <td>TBD</td>
    <td>TBD (probably a link to an .exe)</td>
  </tr>
  <tr>
    <td>Windows 11</td>
    <td>Unsupported</td>
    <td></td>
  </tr>
  <tr>
    <td>MacOS</td>
    <td>Contributors wanted</td>
    <td></td>
  </tr>
</table>

## Feedback

Happy to read your thoughts via email (write email here) or GitHub.

See the below section for details on contributing.

## Contributing

Contributing is open-ended. Get your thoughts or changes out there via any method - provided I'm able to see it. If I had to pick: GitHub issues would be the easiest for me to keep track of things.

I am open to:
- bug fixes
- bug reports
- translations
- documentation

On the fence with brand-new features except for those listed in the below wishlist section.

## Wishlist

I personally consider this software to be complete in terms of requirements.

However, if you are inclined to contribute to the codebase with a predefined task, consult this list of good-to-have features:

| Task      | Description                       |
| :-------- | :-------------------------------- |
| Dynamic monitor detection | Dynamically update the GUI interface as monitor changes are detected |
| Monitor order detection | Display the order of the monitors in which they are positioned by xrandr |
| Refactor `gui.py` | Simplify infrastructure for ease of developer maintenance and scalability |
| More docstrings | Enhance user readability and interpretation speed by supplying more docs |
| Windows 10 support | Modify the codebase to work with Windows 10 |
| Windows 11 support | Modify the codebase to work with Windows 11 |

My involvement with any of the above items are highly contingent on my willingness to commit the time - especially considering my satisfaction with the usability of the software's current feature set.

Should you take the initiative, feel free to reach out for support or questions.

## Support

Leave a comment in GitHub issues if you have any questions.

## Roadmap

I intend to support this software by maintaining it on as-needed basis and ensure it continues to run on Arch Linux.

## Technologies used

- Python
- Tkinter


## Acknowledgements

 - [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [How to write a Good readme](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)
