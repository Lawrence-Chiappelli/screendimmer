import session
import gui
import xrandr
import configutils

if __name__ == '__main__':
    sesh = session.Session()
    print(sesh)
    sesh.append_temporary_test_data()
    monitors = sesh.get_monitors()
    resolutions = sesh.get_resolutions()
    brightnesses = sesh.get_brightnesses()

    configutilities = configutils.Config()
    brightness_values_to_initialize = [{'brightnesses': (monitors[i].lower(), '1.0')} for i in range(len(monitors))]
    configutilities.initialize_config_with_values(brightness_values_to_initialize)

    tray = gui.Gui(
        monitors,
        resolutions,
        brightnesses
    )

    tray.construct_gui()
    tray.start()

    print("Done")
