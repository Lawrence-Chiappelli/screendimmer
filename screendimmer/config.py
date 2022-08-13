class Colors:

    def __init__(self):
        self.dark_mode=True # TODO: determine with config parser
        self.bg=self.DarkMode().bg if self.dark_mode else self.LightMode().bg
        self.fg=self.DarkMode().fg if self.dark_mode else self.LightMode().fg
        self.entry_bg=self.DarkMode().entry_bg if self.dark_mode else self.LightMode().entry_bg
        self.trough_active_bg=self.DarkMode().trough_active_bg if self.dark_mode else self.LightMode().trough_active_bg

    def get_background_color(self):
        """General background color of an element"""
        return self.bg

    def get_foreground_color(self):
        """Usually refers to the text color"""
        return self.fg

    def get_entry_background_color(self):
        """The background color of input boxes"""
        return self.entry_bg

    def get_trough_active_background_color(self):
        """The background color of the scroll box"""
        return self.trough_active_bg

    class DarkMode:
        def __init__(self):
            # self.bg='#1d1f21'
            self.bg="#1d1f1f"
            self.fg='#d8d4cf'
            self.entry_bg="#111111"
            self.trough_active_bg="#b3b3b3"

    class DevMode:
        def __init__(self):
            self.bg='#ff0000'
            self.fg='#00ff00'
            self.entry_bg="#0000ff"
            self.trough_active_bg="#b3b3b3"

    class LightMode:
        def __init__(self):
            self.bg='#d9d9d9'
            self.fg='#000000'
            self.entry_bg="#ffffff"
            self.trough_active_bg="#b3b3b3"


if __name__ == '__main__':
    print("This should not be the main module")
