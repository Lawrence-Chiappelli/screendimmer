import session
import gui
import xrandr


if __name__ == '__main__':
    sesh = session.Session()

    sesh.append_temporary_test_data()
    monitors = sesh.get_monitors()
    resolutions = sesh.get_resolutions()
    brightnesses = sesh.get_brightnesses()

    tray = gui.Gui(
        monitors,
        resolutions,
        brightnesses
    )

    tray.construct_gui()
    tray.start()

    print("Done")
