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

    def get_all_available_themes(self):
        # TODO: relocate?
        class_names = [member for member in dir(colors)[1:] if not member.startswith("__")]
        all_themes = [getattr(colors, class_name)() for class_name in class_names]
        return all_themes

    def set_theme(self):
        if config:
            theme_value = config['color']['theme']
            for theme in self.get_all_available_themes():
                if theme.__str__() == theme_value:
                    return theme

        return colors.DarkMode()

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

    def save_new_theme(self, theme_class):
        if type(theme_class) is str:
            raise TypeError("The passed theme should be an object\
            and not the str representation")

        if config:
            config['color']['theme'] = theme_class.__str__()
            configutil.save_changes()

        self.theme = theme_class

    def __str__(self):
        return self.theme.__str__()
