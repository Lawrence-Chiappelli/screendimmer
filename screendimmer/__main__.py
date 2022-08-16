import session
import gui
import xrandr
import preferences

if __name__ == '__main__':
    sesh = session.Session()
    print(sesh.setup)
    monitors = sesh.get_monitors()
    resolutions = sesh.get_resolutions()
    brightnesses = sesh.get_brightnesses()

    # Temporary test dataabout_window 1:
    monitors.append('TEST-1')
    resolutions.append('1920x1080')
    brightnesses.append('0.8')

    # Temporary test data 2:
    monitors.append(monitors[0])
    resolutions.append(resolutions[0])
    brightnesses.append(brightnesses[0])

    tray = gui.Gui(
        monitors,
        resolutions,
        brightnesses
    )

    tray.construct_gui()
    tray.start()

    # When the application is exited, consult the user's preferences
    preference = preferences.Preferences()

    if preference.get_save_on_exit():
        pass  # TODO: clear config on exit?

    if preference.get_restore_on_exit():
        for monitor in monitors:
            xrandr.set_brightness(monitor, '1.0')

    print("Done")
