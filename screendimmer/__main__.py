import session
import gui

if __name__ == '__main__':
    sesh = session.Session()
    print(sesh.setup)
    monitors = sesh.get_monitors()
    brightnesses = sesh.get_brightnesses()
    resolutions = sesh.get_resolutions()

    tray = gui.Gui()

    tray.populate_brightness_toggles(monitors, resolutions)
    tray.populate_brightness_inputs(brightnesses)
    tray.populate_brightness_scollers(brightnesses)

    print(tray.toggles)
    print(tray.inputs)
    print(tray.scrollers)

    tray.start()
