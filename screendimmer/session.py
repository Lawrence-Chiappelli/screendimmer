import xrandr

class Session():

    def __init__(self):
        self.setup = self._generate_setup()
        self.monitors = [m[0] for m in self.setup.values()]
        self.brightnesses = [b[1] for b in self.setup.values()]
        self.resolutions = [r[2] for r in self.setup.values()]

    def _generate_setup(self):
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
        variable in nature and don't necessarily need
        to be stored permanently.
        """

        return {i:(m,b,r) for i, (m,b,r) in enumerate(zip(
                xrandr.parse_all_monitors(),
                xrandr.parse_all_brightnesses(),
                xrandr.parse_all_resolutions(),
            ))
        }

    def get_monitors(self):
        return self.monitors

    def get_brightnesses(self):
        return self.brightnesses

    def get_resolutions(self):
        return self.resolutions

    def append_temporary_test_data(self):
        self.monitors.append('TEST-1')
        self.resolutions.append('1920x1080')
        self.brightnesses.append('0.8')

    def __str__(self):
        return f"Your setup: {self.setup}"
