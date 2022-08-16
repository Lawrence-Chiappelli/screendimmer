"""
Color-related constants ONLY.

If you want a theme, return any one of the below SUBclasses,
and do so somewhere else.

Example:
import colors
theme = colors.DarkMode()
"""

class Colors:

    def __init__(self, bg, fg, entry_bg, button_bg, trough_bg, scrollbar_bg, disabled_bg, disabled_fg, hyperlink_fg):
        self.bg=bg
        self.fg=fg
        self.entry_bg=entry_bg
        self.button_bg=button_bg
        self.trough_bg=trough_bg
        self.scrollbar_bg=scrollbar_bg
        self.disabled_bg=disabled_bg
        self.disabled_fg=disabled_fg
        self.hyperlink_fg=hyperlink_fg

    # Generally, I just want these human readable functions to be re-used:
    def get_background_color(self):
        """General background color of an element"""
        return self.bg

    def get_foreground_color(self):
        """Usually refers to the text color"""
        return self.fg

    def get_entry_background_color(self):
        """The background color of input boxes"""
        return self.entry_bg

    def get_button_background_color(self):
        """The background color of buttons"""
        return self.entry_bg

    def get_trough_background_color(self):
        """The background color of the scroll box"""
        return self.trough_bg

    def get_scrollbar_background_color(self):
        """The color of the scrollbar itself"""
        return self.scrollbar_bg

    def get_disabled_background_color(self):
        """Use for any element that's disabled"""
        return self.disabled_bg

    def get_disabled_foreground_color(self):
        """Use for any element that's disabled"""
        return self.disabled_fg

    def get_hyperlink_foreground_color(self):
        """Hyperlink blue needs to different shades for each mode"""
        return self.hyperlink_fg

class DarkMode(Colors):

    def __init__(self):
        self.bg="#26242f"
        self.fg='#d8d4cf'
        self.entry_bg="#262525"
        self.button_bg="#d9d9d9"
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
