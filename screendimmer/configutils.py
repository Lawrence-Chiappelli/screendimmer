import configparser

from os import path, stat


class Config:

    def __init__(
        self,
        file_name='config.ini',
        pkg_name='screendimmer',
        in_production=True,
        get_none_if_not_found=True,
        print_console_feedback=True,
        data=[],
    ):
        """Initialize the configuration FILE using needed parameters.
        Do NOT initalize with keys/values in constructor.

        @param file_name (str): The raw name of your configuration file, include the extension
        @param pkg_name (str): Part of the path, according to Linux file placement conventions (see code)
        @param in_production (bool): Set this to False if you want to test locally and have your config
        file installed in the production path, otherwise this really doesn't matter, keep as True
        @param get_none_if_not_found (bool): Continue the program normally if True
        @param print_console_feedback (bool): If you need to import the config in more than 1 module,
        you can optionally set this to False to keep the console clean of duplicate messages
        @param create_file_if_first_run=False:
        """
        self._file_name = file_name
        self._pkg_name = pkg_name
        self._in_production = in_production
        self._get_none_if_not_found = get_none_if_not_found
        self._print_console_feedback = print_console_feedback
        self._path_to_config = self._get_full_path_to_config()
        self._data = data if data else None

        self.file = self._return_read_config()

    def save(self):
        with open(self._path_to_config, 'w') as new_changes:
            self.file.write(new_changes)

    def _config_file_is_empty(self):
        stat(self._path_to_config).st_size == 0

    def get_all_values_from_section_as_list(self, section_name='brightnesses', fallback_value='1.0'):
        """Get all VALUES (not KEYS) from a section/category

        @param category (str): The name of the config category
        @return (list): A list of values as strings
        """

        return [value or fallback_value for value in self.file[section_name].values()]

    def save_section_keys_with_values(self, keys: list, values: list, section='brightnesses'):
        """Save config section keys with values.

        1) Assume indices are adjacent.
        2) Have your keys/values ready and processed.
        3) Meant for sections with multiple keys - just access the
        config directly if you want to save a single section/key value.
        """

        if self.file:
            for i in range(len(keys)):
                if self.file.has_option(section, keys[i]):
                    self.file[section][keys[i]] = values[i]
                else:
                    print(f"Warning: missing section/key in config: {section}/{key}")

            self.save()
        else:
            raise FileNotFoundError("Config file must be read or parsed before using this function.")

    def _return_read_config(self):
        """Retrieve your parsed configuration file

        @return (None): if file path N/A or there was an issue reading the file.
        """

        if self._path_to_config:
            # The below lines of code are strictly required to be written
            # the way they are, or we will not get a configparser object!
            config = configparser.ConfigParser()
            config.read(self._path_to_config, encoding='utf-8')
            return config
        else:
            return None

    def print_entire_config_for_verification(self):
        for section in self.file.sections():
            print(f"[{section}]")
            for item in self.file.items(section):
                print(f"{item[0]} = {item[1]}")
            print(f"")

    def print_specific_section_items_for_verification(self, section_name: str):
        print(f"[{section_name}]")
        for item in self.file[section_name].items():
            print(f"{item[0]} = {item[1]}")
        print(f"")

    def _get_full_path_to_config(self):
        """The path to the .ini that keeps track of monitor brightness levels and theme preference

        @return (str, None): Return the string path if config found, or None if not found
        @raise FileNotFoundError: Abort the program if program not found
        """

        absolute_path_production = f'/etc/{self._pkg_name}/{self._file_name}'
        root_path_development = f"{self._file_name}"
        up_one_path_development = f'../{self._file_name}'
        full_path = None

        if path.exists(absolute_path_production) and self._in_production:
            feedback_for_user = f"✓ - In production envionment, {self._file_name} found at {absolute_path_production}"
            full_path = absolute_path_production
        elif path.exists(root_path_development):
            feedback_for_user = f"✓ - In development envionment, {self._file_name} found at ./{root_path_development}"
            full_path = root_path_development
        elif path.exists(up_one_path_development):
            feedback_for_user = f"✓ - In development envionment, {self._file_name} found at {up_one_path_development}"
            full_path = up_one_path_development
        else:
            feedback_for_user = f"Unable to find the configuration file '{self._file_name}'!\nThis program attempted to look for the file in the following places:\n\t{absolute_path_production}\n\t{root_path_development}\n\t{up_one_path_development}\nMaybe the file was moved or deleted?"

            if self._get_none_if_not_found:
                # Your responsibility to ensure this is handled correctly
                full_path = None
            else:
                print(feedback_for_user)
                raise FileNotFoundError("\n\nIf you're seeing this error, please report this issue upstream. It's likely that support for no config file is in development.\nA temporary solution would be to manually copy and paste the config file from GitHub into one of the above directories.")

        if self._print_console_feedback:
            print(feedback_for_user)

        return full_path

if __name__ == '__main__':
    print(f"This should be an imported module")
