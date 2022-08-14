import configutil

config = configutil.get_parsed_config()

class Colors:

    def __init__(self):
        self.dark_mode=eval(config['theme']['darkmode'])

        self.bg=self.DarkMode().bg if self.dark_mode else self.LightMode().bg
        self.fg=self.DarkMode().fg if self.dark_mode else self.LightMode().fg
        self.entry_bg=self.DarkMode().entry_bg if self.dark_mode else self.LightMode().entry_bg
        self.button_bg=self.DarkMode().button_bg if self.dark_mode else self.LightMode().button_bg
        self.trough_bg=self.DarkMode().trough_bg if self.dark_mode else self.LightMode().trough_bg
        self.scrollbar_bg=self.DarkMode().scrollbar_bg if self.dark_mode else self.LightMode().scrollbar_bg
        self.disabled_bg=self.DarkMode().disabled_bg if self.dark_mode else self.LightMode().disabled_bg
        self.disabled_fg=self.DarkMode().disabled_fg if self.dark_mode else self.LightMode().disabled_fg
        self.hyperlink_fg=self.DarkMode().hyperlink_fg if self.dark_mode else self.LightMode().hyperlink_fg

    def get_darkmode_state(self):
        return self.dark_mode

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
        """The background color of input boxes"""
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
        """Hyperlink blue needs to different shades for each"""
        return self.hyperlink_fg

    class DarkMode:
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

    class LightMode:
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

if __name__ == '__main__':
    print("This should not be the main module")