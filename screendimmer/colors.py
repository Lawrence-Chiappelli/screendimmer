"""
Color-related constants ONLY.

If you want a theme, return any one of the below SUBclasses,
and do so somewhere else.

Example:
import colors
theme = colors.DarkMode()

Do not import anything as I am using this file to
process information related to this module's members.
"""

class Colors:

    def __init__(self, bg, fg, entry_bg, button_bg, trough_bg, scrollbar_bg, disabled_bg, disabled_fg, hyperlink_fg):
        self.BG=bg
        self.FG=fg
        self.ENTRY_BG=entry_bg
        self.BUTTON_BG=button_bg
        self.TROUGH_BG=trough_bg
        self.SCROLLBAR_BG=scrollbar_bg
        self.DISABLED_BG=disabled_bg
        self.DISABLED_FG=disabled_fg
        self.HYPERLINK_FG=hyperlink_fg

    # Generally, I just want these human readable functions to be re-used:
    def get_background_color(self):
        """General background color of an element"""
        return self.BG

    def get_foreground_color(self):
        """Usually refers to the text color"""
        return self.FG

    def get_entry_background_color(self):
        """The background color of input boxes"""
        return self.ENTRY_BG

    def get_button_background_color(self):
        """The background color of buttons"""
        return self.BUTTON_BG

    def get_trough_background_color(self):
        """The background color of the scroll box"""
        return self.TROUGH_BG

    def get_scrollbar_background_color(self):
        """The color of the scrollbar itself"""
        return self.SCROLLBAR_BG

    def get_disabled_background_color(self):
        """Use for any element that's disabled"""
        return self.DISABLED_BG

    def get_disabled_foreground_color(self):
        """Use for any element that's disabled"""
        return self.DISABLED_FG

    def get_hyperlink_foreground_color(self):
        """Hyperlink blue needs to different shades for each mode"""
        return self.HYPERLINK_FG

class DarkMode(Colors):

    def __init__(self):
        self.bg="#26242f"
        self.fg='#d8d4cf'
        self.entry_bg="#262525"
        self.button_bg="#262525"
        self.trough_bg="#84828c"
        self.scrollbar_bg="#735a9b"
        self.disabled_bg="#444444"
        self.disabled_fg="#000000"
        self.hyperlink_fg="lightblue"

        super().__init__(*self.__dict__.values())

    def __str__(self):
        return "Dark Mode"

class LightMode(Colors):

    def __init__(self):
        self.bg='#d9d9d9'
        self.fg='#000000'
        self.entry_bg="#ffffff"
        self.button_bg="#d9d9d9"
        self.trough_bg="#b3b3b3"
        self.scrollbar_bg="#b3b3b3"
        self.disabled_bg="#d9d9d9"
        self.disabled_fg="#a3a3a3"
        self.hyperlink_fg="blue"

        super().__init__(*self.__dict__.values())

    def __str__(self):
        return "Light Mode"

if __name__ == '__main__':
    print("This should be an imported module.")
    quit()
