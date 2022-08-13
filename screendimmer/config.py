class Colors:

    def __init__(self):
        self.dark_mode=True # TODO: determine with config parser

        self.bg=self.DarkMode().bg if self.dark_mode else self.LightMode().bg
        self.fg=self.DarkMode().fg if self.dark_mode else self.LightMode().fg
        self.entry_bg=self.DarkMode().entry_bg if self.dark_mode else self.LightMode().entry_bg
        self.button_bg=self.DarkMode().button_bg if self.dark_mode else self.LightMode().button_bg
        self.trough_bg=self.DarkMode().trough_bg if self.dark_mode else self.LightMode().trough_bg
        self.scrollbar_bg=self.DarkMode().scrollbar_bg if self.dark_mode else self.LightMode().scrollbar_bg

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

    class DarkMode:
        def __init__(self):
            #423a4f
            #735a9b
            #70539e
            #181818
            #262525
            self.bg="#26242f"
            self.fg='#d8d4cf'
            self.entry_bg="#262525"
            self.button_bg="#d9d9d9"
            self.trough_bg="#84828c"
            self.scrollbar_bg="#735a9b"

    class LightMode:
        def __init__(self):
            self.bg='#d9d9d9'
            self.fg='#000000'
            self.entry_bg="#ffffff"
            self.button_bg="#d9d9d9"
            self.trough_bg="#b3b3b3"
            self.scrollbar_bg="#b3b3b3"

if __name__ == '__main__':
    print("This should not be the main module")
