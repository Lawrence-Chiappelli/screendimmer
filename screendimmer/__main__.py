import session
import gui
import xrandr
import configutils
import preferences
import utils

if __name__ == '__main__':
    sesh = session.Session()
    sesh.append_temporary_test_data()
    monitors = sesh.get_monitors()
    resolutions = sesh.get_resolutions()
    brightnesses = sesh.get_brightnesses()

    config_interface = configutils.Config()
    config_file = config_interface.get_configuration_file()

    def initalize_configuration_with_values():
        """Initialize configuration values from generated session"""
        values_to_initialize_config = [{'brightnesses': (monitors[i].lower(), '1.0')} for i in range(len(monitors))]
        config_interface.initialize_config_with_values(values_to_initialize_config)

    def apply_monitor_brightness_from_configuration_values():
        """Apply brightness values from configuration file - these could be default or user-saved"""
        config_brightness_values = [config_file['brightnesses'][monitors[i]] for i in range(len(monitors))]
        [xrandr.set_brightness(monitors[i], config_brightness_values[i]) for i in range(len(config_brightness_values))]

    initalize_configuration_with_values()
    apply_monitor_brightness_from_configuration_values()

    tray = gui.Gui(
        monitors,
        resolutions,
        brightnesses
    )

    tray.construct_gui()
    tray.start()

    """
    At this point, the mainloop has terminated and we no longer
    have access to the GUI.

    Any exit behaviors are handling on the WM_DELETE_WINDOW
    protocol handler. See gui.py.
    """
    # TODO: position window to tray
    # TODO: outclicking window minimizes it
    # TODO: tray icon
    # TODO: right click on tray icon opens window

    # TODO: rewrite config file for production, add, commit, push, then add to .gitignore
    # TODO: console messages for specific configuration calls

    print("Main loop terminated")
else:
    print("This should be the main module")
