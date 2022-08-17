import session
import gui
import xrandr
import configutils
import preferences
import utils

if __name__ == '__main__':
    sesh = session.Session()
    sesh.append_temporary_test_data()
    print(sesh)
    monitors = sesh.get_monitors()
    resolutions = sesh.get_resolutions()
    brightnesses = sesh.get_brightnesses()

    # Initialize configuration values from generated session:
    configutilities = configutils.Config()
    values_to_initialize_config = [{'brightnesses': (monitors[i].lower(), '1.0')} for i in range(len(monitors))]
    configutilities.initialize_config_with_values(values_to_initialize_config)

    # Apply monitor brightnesses from configuration file values:
    configfile = configutilities.get_configuration_file()
    config_brightness_values = [configfile['brightnesses'][monitors[i]] for i in range(len(monitors))]
    [xrandr.set_brightness(monitors[i], config_brightness_values[i]) for i in range(len(config_brightness_values))]

    tray = gui.Gui(
        monitors,
        resolutions,
        brightnesses
    )

    tray.construct_gui()
    tray.start()

    # When program is exited or closed, consult configuration for user's preferences:
    preferences = preferences.Preferences()

    # Saving monitor brightnesses to config (default is yes)
    if preferences.get_save_on_exit():
        for i in range(len(monitors)):
            monitor = monitors[i].lower()
            brightness = utils.convert_converted_brightness_to_xrandr(tray.brightness_vars[i].get())
            configfile['brightnesses'][monitor] = brightness
            configutilities.save()
        pass  # TODO: clear config on exit?

    # Restore brightnesses when the application exists (default is yes)
    if preferences.get_restore_on_exit():
        for monitor in monitors:
            xrandr.set_brightness(monitor, '1.0')

    print("Done")
