import utils
import colors
import configutils

class Preferences:

    def __init__(self, config_file):
        self.config_file = config_file  # Unless I NEED custom config functions I wrote, this is probably good enough
        self.theme = self._set_theme()  # Set the CLASS object, not the STR
        self.save_on_exit = self._set_save_on_exit()
        self.restore_on_exit = self._set_restore_on_exit()

    def get_theme(self):
        return self.theme

    def is_save_on_exit(self):
        return self.save_on_exit

    def is_restore_on_exit(self):
        return self.restore_on_exit

    def _set_theme(self):
        if self.config_file:
            theme_value = self.config_file['color']['theme']
            for theme in utils.get_all_available_themes():
                if theme.__str__() == theme_value:
                    return theme

        return colors.DarkMode()

    def _set_save_on_exit(self):
        if self.config_file:
            if eval(self.config_file['preferences']['save_on_exit']):
                return True

        return False

    def _set_restore_on_exit(self):
        if self.config_file:
            if eval(self.config_file['preferences']['restore_on_exit']):
                return True

        return False

    def is_dark_mode_enabled(self):
        if self.theme.__str__() == colors.DarkMode().__str__():
            return True
        else:
            return False

    def save_new_theme(self, theme_class):
        if self.config_file:
            self.config_file['color']['theme'] = theme_class.__str__()

        self.theme = theme_class

    def apply_save_on_exit(self, selected_value: int):
        # TODO: better name for this - *what* is being applied *to*?
        if self.config_file:
            self.config_file['preferences']['save_on_exit'] = str(bool(selected_value))

        self.save_on_exit = selected_value

    def apply_restore_on_exit(self, selected_value: int):
        if self.config_file:
            self.config_file['preferences']['restore_on_exit'] = str(bool(selected_value))

        self.restore_on_exit = selected_value

    def __str__(self):
        return str(self.__dict__())


if __name__ == '__main__':
    print(f"This should be an imported module")
