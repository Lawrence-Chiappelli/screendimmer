class Colors:

    def __init__(self):
        self.dark_mode=True # TODO: determine with config parser
        self.bg=self.DarkMode().bg if self.dark_mode else self.LightMode().fg
        self.text=self.DarkMode().text if self.dark_mode else self.LightMode().text

    def get_background_color(self):
        return self.bg

    def get_foreground_color(self):
        return self.fg

    def get_text_color(self):
        return self.text

    class DarkMode:
        def __init__(self):
            self.bg='#131516'
            self.text='#d8d4cf'

    class DevMode:
        def __init__(self):
            self.bg='#0f0000'
            self.text='#000f00'

    class LightMode:
        def __init__(self):
            self.bg='#d9d9d9'
            self.text='#000000'


if __name__ == '__main__':
    print("This should not be the main module")
