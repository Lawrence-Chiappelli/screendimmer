import configparser

from os import path


class Config:

    def __init__(
        self,
        file_name='config.ini',
        pkg_name='screendimmer',
        in_production=True,
        get_none_if_not_found=True
    ):
        """Initialize the configuration FILE using needed parameters.
        Do NOT initalize with keys/values in constructor.

        @param file_name (str): The raw name of your configuration file, include the extension
        @param pkg_name (str): Part of the path, according to Linux file placement conventions (see code)
        @param in_production (bool): Set this to False if you want to test locally and have your config
        file installed in the production path, otherwise this really doesn't matter, keep as True
        @param continue_if_not_found (bool): Continue the program normally if True
        """
        self._file_name = file_name
        self._pkg_name = pkg_name
        self._in_production = in_production
        self._get_none_if_not_found = get_none_if_not_found
        self._path_to_config = self._get_full_path_to_config()

        self.file = self._return_read_config()

    def save(self):
        with open(self._path_to_config, 'w') as new_changes:
            self.file.write(new_changes)

    def get_configuration_file(self):
        return self.file

    def initialize_config_with_values(self, sections_values_list: list):
        """Initialize the configuration with new values.

        Note:
            1) You MUST have [sectionnames] already in your config file!
            2) The sections_values_list must be in the correct format

        Justification:
        The assumption here is that an end-user is launching your program
        for the first time, and your program is written such that your config
        file cannot contain any keys/values *until* you launch the program
        first and retrieve them.

        In such a scenario, you may want to use an *automated* function to
        populate with values - contingent on having the information ready
        for passing into this function.

        (Nothing is stopping you from doing so manually - but, if you get into
        that habit, it's very hard to determine where that starts and ends,
        leading to a confusing and unmaintainable order of events.
        That's just my opinion.)

        This function makes checks for section name existence, key name existence,
        and key value existence.
        Read below to see how the program responds to a combination of any of
        the above scenarios. It probably will do what you think it does.

        @param sections_values_list (list): Within this list contains
        the following dictionaries:
        {section_name: (section_key, default_value)}

        @return (None): Nothing to return
        @raise KeyError: If the user failed to have the section name prepared
        beforehand, abort the program.
        """
        for item in sections_values_list:
            for section_name, value_tuple in item.items():
                section_key, default_value = value_tuple[0], value_tuple[1]
                """
                Note: it is YOUR responsibility to ensure config values types are correct!
                Remember, we are only initializing values, we are NOT checking for value type correctness.
                """
                if self.file.has_section(section_name):
                    if self.file.has_option(section_name, section_key):
                        # If the section NAME and KEY exists, we can run into 2 possible scenarios:
                        #   1) We are missing a value on the key, so assign a new value using the user's default value
                        #   2) We have the value on the key already, in which case, continue
                        existing_value = self.file[section_name][section_key]
                        if existing_value:
                            continue
                        else:
                            print(f"Found a missing value! Assigning with default {default_value}")
                            self.file[section_name][section_key] = default_value
                    else:
                        # Create the section with the default value.
                        # In this case, there's no existing value, so just assign a default value.
                        print(f"Creating new config key/value for [{section_name}]: {section_key} = {default_value}")
                        self.file[section_name][section_key] = default_value
                else:
                    raise KeyError(f"Missing section [{section_name}]. This must be manually defined first\n!")

        self.save() if sections_values_list else None

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

        if path.exists(absolute_path_production) and self._in_production:
            print(f"✓ - In production envionment, {self._file_name} found at {absolute_path_production}")
            return absolute_path_production
        elif path.exists(root_path_development):
            print(f"✓ - In development envionment, {self._file_name} found at ./{root_path_development}")
            return root_path_development
        elif path.exists(up_one_path_development):
            print(f"✓ - In development envionment, {self._file_name} found at {up_one_path_development}")
            return up_one_path_development
        else:
            feedback_for_user = f"Unable to find the configuration file {self._file_name}.\
            I attempted to look for the file in the following places:\n \
            {absolute_path_production}\n{root_path_development}\n{up_one_path_developer}\n \
            Maybe the file was moved or deleted?"

            if self._get_none_if_not_found:
                print(feedback_for_user)
                return None
            else:
                raise FileNotFoundError(feedback_for_user)

if __name__ == '__main__':
    print(f"This should be an imported module")
