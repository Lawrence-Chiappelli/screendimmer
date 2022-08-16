import colors
import configutil

config = configutil.retrieve_configuration_file()

class Preferences:

    def __init__(self):
        self.theme = self.set_theme()
        self.save_on_exit = self.set_save_on_exit()
        self.restore_on_exit = self.set_restore_on_exit()

    def get_theme(self):
        return self.theme

    def get_save_on_exit(self):
        return self.save_on_exit

    def get_restore_on_exit(self):
        return self.restore_on_exit

    def set_theme(self):
        if config:
            if eval(config['theme']['darkmode']):
                return colors.DarkMode()

        return colors.LightMode()

    def set_save_on_exit(self):
        if config:
            if eval(config['preferences']['save_on_exit']):
                return True

        return False

    def set_restore_on_exit(self):
        if config:
            if eval(config['preferences']['save_on_exit']):
                return True

        return True

    def is_dark_mode_enabled(self):
        if self.theme == colors.DarkMode().__str__():
            return True
        else:
            return False

    def __str__(self):
        return self.theme.__str__()
