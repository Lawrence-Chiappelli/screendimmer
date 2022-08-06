import session
import gui

if __name__ == '__main__':
    sesh = session.Session()
    print(sesh.setup)
    monitors = sesh.get_monitors()
    resolutions = sesh.get_resolutions()
    brightnesses = sesh.get_brightnesses()

    # Temporary test data 1:
    monitors.append('TEST-1')
    resolutions.append('1920x1080')
    brightnesses.append('0.8')

    # Temporary test data 2:
    monitors.append('TEST-2')
    resolutions.append('1600x1050')
    brightnesses.append('1.0')

    tray = gui.Gui()

    tray.populate_brightness_toggles(monitors, resolutions)
    tray.populate_brightness_inputs(brightnesses)
    tray.populate_brightness_scollers(brightnesses)

    print(tray.toggles)
    print(tray.inputs)
    print(tray.scrollers)

    tray.start()
