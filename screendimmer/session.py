import xrandr

class Session():

    def __init__(self):
        self.setup = self.generate_setup()
        self.monitors = [m[0] for m in self.setup.values()]
        self.brightnesses = [b[1] for b in self.setup.values()]
        self.resolutions = [r[2] for r in self.setup.values()]

    def generate_setup(self):
        """Determine the user's setup. Once per function call.

        @return (dict): {'DisplayPort-2', 0.70}
        Where:
        i = monitor order number (key)
        m = monitor (value)
        b = brightness (value)
        r = resolution (value)

        No need to have a "standardized structure" for the user's
        environment information. All this module needs to do is
        store and retrieve values in a human readable fashion.

        Standardizing data structures should be done where
        GUI processing needs to happen. Such events are
        variable in nature.
        """

        return {i:(m,b,r) for i, (m,b,r) in enumerate(zip(
                xrandr.parse_all_monitors(),
                xrandr.parse_all_brightnesses(),
                xrandr.parse_all_resolutions(),
            ))
        }

    def increment_monitor_brightness(self, monitor_name: str):
        """Increment a specified monitor's brightness by 10%.

        @param monitor_name (str): Full string of the monitor name
        @return (None): None
        """

        current_brightness = self.setup[monitor_name]
        next_brightness_level = str(float(current_brightness) + 0.1)
        xrandr.set_brightness(monitor_name, next_brightness_level)

    def decrement_monitor_brightness(self, monitor_name: str):
        """Increment a specified monitor's brightness by 10%.

        @param monitor_name (str): Full string of the monitor name
        @return (None): None
        """

        current_brightness = self.setup[monitor_name]
        next_brightness_level = str(float(current_brightness) - 0.1)
        xrandr.set_brightness(monitor_name, next_brightness_level)

    def get_monitors(self):
        return self.monitors

    def get_brightnesses(self):
        return self.brightnesses

    def get_resolutions(self):
        return self.resolutions
