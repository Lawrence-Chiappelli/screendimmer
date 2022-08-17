import utils
import colors
import configutils

configutilities = configutils.Config()

class Preferences:

    def __init__(self):
        self._config = configutilities.get_configuration_file()
        self.theme = self._set_theme()  # Set the CLASS object, not the STR
        self.save_on_exit = self._set_save_on_exit()
        self.restore_on_exit = self._set_restore_on_exit()

    def get_theme(self):
        return self.theme

    def get_save_on_exit(self):
        return self.save_on_exit

    def get_restore_on_exit(self):
        return self.restore_on_exit

    def _set_theme(self):
        if self._config:
            theme_value = self._config['color']['theme']
            for theme in utils.get_all_available_themes():
                if theme.__str__() == theme_value:
                    return theme

        return colors.DarkMode()

    def _set_save_on_exit(self):
        if self._config:
            if eval(self._config['preferences']['save_on_exit']):
                return True

        return False

    def _set_restore_on_exit(self):
        if self._config:
            if eval(self._config['preferences']['restore_on_exit']):
                return True

        return False

    def is_dark_mode_enabled(self):
        if self.theme == colors.DarkMode().__str__():
            return True
        else:
            return False

    def save_new_theme(self, theme_class):
        if self._config:
            self._config['color']['theme'] = theme_class.__str__()
            configutilities.save()

        self.theme = theme_class

    def apply_save_on_exit(self, selected_value: int):
        if self._config:
            self._config['preferences']['save_on_exit'] = str(bool(selected_value))
            configutilities.save()

        self.save_on_exit = selected_value

    def apply_restore_on_exit(self, selected_value: int):
        if self._config:
            self._config['preferences']['restore_on_exit'] = str(bool(selected_value))
            configutilities.save()

        self.restore_on_exit = selected_value

    def __str__(self):
        return str(self.__dict__())


if __name__ == '__main__':
    print(f"This should be an imported module")
