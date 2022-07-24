import session
import gui

if __name__ == '__main__':
    sesh = session.Session()
    print(sesh.setup)
    monitors = sesh.get_monitors()
    brightnesses = sesh.get_brightnesses()
    resolutions = sesh.get_resolutions()
    print(monitors)
    print(brightnesses)
    print(resolutions)

    # tray = gui.Gui()
    # tray.populate_with_monitors(monitors)
    # tray.populate_brightness_toggles(monitors, ["2560x1440"])
    # tray.start()
