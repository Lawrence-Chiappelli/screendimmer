import xrandr

class Session():

    def __init__(self):

        self.setup = self.generate_setup()

    def generate_setup(self):
        """
        Determine the user's setup. Once per function call.
        @return (dict): {'DisplayPort-2', }
        TODO: are monitor names unique? Might be a better identifier than index.

        m = monitor
        b = brightness
        """
        return {m:b for m,b in enumerate(
            zip(
                xrandr.get_all_monitors(),
                xrandr.get_all_brightnesses(),
                )
            )
        }

    def increase_monitor_brightness(self, monitor_name):
        current_brightness = self.setup[monitor_name]
        next_brightness_level = str(float(current_brightness) + 0.1)
        xrandr.set_brightness(monitor_name, next_brightness_level)

    def decrease_monitor_brightness(self, monitor_name):
        current_brightness = self.setup[monitor_name]
        next_brightness_level = str(float(current_brightness) - 0.1)
        xrandr.set_brightness(monitor_name, next_brightness_level)
