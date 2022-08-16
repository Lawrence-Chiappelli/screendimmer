import colors
import configutil

class Preferences:

    def __init__(self):
        self._config = configutil.retrieve_configuration_file()

        self.theme = self.set_theme()  # <--- the class, not the str representation
        self.save_on_exit = self.set_save_on_exit()
        self.restore_on_exit = self.set_restore_on_exit()

    def get_theme(self):
        return self.theme

    def get_save_on_exit(self):
        return self.save_on_exit

    def get_restore_on_exit(self):
        return self.restore_on_exit

    def get_all_available_themes(self):
        # TODO: relocate?
        class_names = [member for member in dir(colors)[1:] if not member.startswith("__")]
        all_themes = [getattr(colors, class_name)() for class_name in class_names]
        return all_themes

    def set_theme(self):
        if self._config:
            theme_value = self._config['color']['theme']
            for theme in self.get_all_available_themes():
                if theme.__str__() == theme_value:
                    return theme

        return colors.DarkMode()

    def set_save_on_exit(self):
        if self._config:
            if eval(self._config['preferences']['save_on_exit']):
                return True

        return False

    def set_restore_on_exit(self):
        if self._config:
            if eval(self._config['preferences']['save_on_exit']):
                return True

        return True

    def is_dark_mode_enabled(self):
        if self.theme == colors.DarkMode().__str__():
            return True
        else:
            return False

    def save_new_theme(self, theme_class):
        if self._config:
            self._config['color']['theme'] = theme_class.__str__()
            configutil.save()

        self.theme = theme_class

    def apply_save_on_exit(self, selected_value: int):
        if self._config:
            self._config['preferences']['save_on_exit'] = str(bool(selected_value))
            configutil.save()

        self.save_on_exit = selected_value

    def apply_restore_on_exit(self, selected_value: int):
        if self._config:
            self._config['preferences']['restore_on_exit'] = str(bool(selected_value))
            configutil.save()

        self.save_on_exit = selected_value

    def save_monitor_config(self, monitor: str, brightness: str):
        if self._config:
            self._config['monitors'][monitor] = brightness
            configutil.save()

    def __str__(self):
        return self.theme.__str__()
