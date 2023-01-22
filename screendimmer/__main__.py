import session
import gui
import xrandr
import configutils
import preferences
import utils

if __name__ == '__main__':
    config = configutils.Config() # Important that all modules using a config share the same memory address, so pass this where possible
    prefs = preferences.Preferences(config_file=config.file)
    sesh = session.Session(append_test_data=False)

    monitors = sesh.get_monitors()
    resolutions = sesh.get_resolutions()
    brightnesses = None

    if config.file:
        brightnesses = config.get_all_values_from_section_as_list(section_name='brightnesses')
        config.save_section_keys_with_values(section='brightnesses', keys=monitors, values=brightnesses)  # As a fallback, overwrite brightness values if we are missing any (unlikely scenario)
    else:
        brightnesses = sesh.get_brightnesses()
        print(f"Basic features will work, but changes will not be saved.")

    [xrandr.set_brightness(monitors[i], brightnesses[i]) for i in range(len(monitors))]

    tray = gui.Gui(
        monitors=monitors,
        resolutions=resolutions,
        brightnesses=brightnesses,
        config=config
    )

    tray.construct_gui()
    tray.start()

    """
    At this point, the mainloop has terminated and we no longer
    have access to the GUI.

    Exit behavior is handled on the WM_DELETE_WINDOW protocol
    handler. See gui.py.
    """

    config.save()

    # TODO: tray icon
    # TODO: position window to tray
    # TODO: outclicking window to minimize it
    # TODO: right click on tray icon to open window

    # TODO: support for better config intialization
    # TODO: better naming of preferences
    # TODO: save (en/dis)abled monitors for "Save monitor config on exit?"
    print("Successfully exited program! (Mainloop terminated)")
else:
    print("This should be the main module")
