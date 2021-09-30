#!/usr/bin/python3
print("\nWelcome!")

import utils
import sys
import configutil
import xrandr
import traceback
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from screeninfo import get_monitors

config = configutil.get_parsed_config()
config_app = utils.get_desktop_file_metadata()


class Tray(QSystemTrayIcon):

    def __init__(self):
        super(Tray, self).__init__()
        self.setIcon(QIcon(utils.get_icon_path()))
        self.setVisible(True)
        self.setToolTip("Right-click to adjust brightness")

        try:
            print(f"Done! Right-click the tray icon to adjust brightness."
                  f"\nPlease see 'About' or 'Donate / Support' "
                  f"buttons for more info.\n")
            self.init_ui()
        except Exception:
            print(f"\nException caught initializing the UI:\n{traceback.format_exc()}\n\nPlease try re-installing or reporting this issue "
                  f"upstream at:\nhttps://github.com/Lawrence-Chiappelli/screendimmer/issues")
            sys.exit()

    def init_ui(self):
        self._create_elements()
        self._add_actions()
        self._apply_connections()
        self._apply_properties()

    def eventFilter(self, obj: type(QMenu), event: type(QEvent)):

        """
        This function name is character sensitive.
        Do not rename it.

        This function filters events and *can* override
        default behaviors.

        :param obj: PyQt object to perform filtering on.
        In this case, I want to prevent the application
        from automatically closing, so I want to filter
        on a QMenu object.
        :param event: On which event do we want to
        perform the filtering and override behavior?        
        :return: False, if default behavior ok
        :return: True, if default behavior not ok        
        """

        if obj == self.menu:

            if event.type() == QEvent.MouseButtonRelease:

                action = self.menu.actionAt(event.pos())
                if not action:
                    print(
                        f"Exception caught.\n\nWhat action were you trying to perform? If this is a recurring issue, "
                        f"please report the issue upstream. Otherwise, please try again.")
                    return False
                elif action == self.terminator or action in self.percents:
                    return False  # Ok for default behavior
                else:
                    action.trigger()  # Trigger the action...                    
                    self.menu.exec_()  # ...WIHTOUT automatically closing
                    return True

        return False  # Default behavior in all other situations

    def stage_brightness(self, brightness_level: float, save=True):

        """
        :param brightness_level: Brightness level to apply.
        No need to pass as string, bash will interpret
        a Python float as valid argument.
        :param save: If save, write to configuration file.
        This should be the default behavior.
        :return:
        """

        xrandr.apply_brightness(brightness_level)
        index = xrandr.convert_xrandr_to_index(brightness_level)
        self._tick_checkbox(self.percents[index])

        if save:
            configutil.write_brightness(str(brightness_level))
            configutil.save_changes()

    def _create_elements(self):

        """
        (1/4)

        Create menu items.

        They're not placed on the menu, yet.
        See the remaining functions.
        """

        self.menu = QMenu()
        self.menu.installEventFilter(self)  # See eventFilter function
        self.monitors = [QAction(monitor.name + f" ({monitor.width}x{monitor.height})") for monitor in get_monitors()]
        self.percents = [QAction(f'{i + 1}0%') for i in range(10)]
        self.terminator = QAction("Quit")
        self.about = QAction("About")
        self.misc = QAction('Donate / Support')
        self.version = QAction(f"VERSION {config_app['Desktop Entry']['Version']}")

        # Note: please manually adjust the version number in screendimmer.desktop
        # when updating the application and pushing changes remotely.

    def _add_actions(self):

        """
        (2/4)
        
        Add actions to menu, visually.

        Connect functionality later.
        """

        # Monitor actions:
        self.menu.addSection('Apply brightness to:')
        for q_action in reversed(self.monitors):
            q_action.setCheckable(True)
            q_action.setChecked(True)
            self.menu.addAction(q_action)

        self.menu.addSection("Brightness level:")

        # Percentage Actions
        [self.menu.addAction(action) for action in reversed(self.percents)]

        self.menu.addSeparator()

        # Quit action
        self.menu.addAction(self.terminator)

        # About popup action
        self.menu.addAction(self.about)

        # Donate action
        self.menu.addAction(self.misc)

        self.menu.addSeparator()
        self.menu.addAction(self.version)
        self.menu.setWindowTitle("Window title")

    def _apply_connections(self):

        """
        (3/4)

        Attach functionality.

        Do note that connections are asking for
        function *objects*. As far as I'm aware,
        parameters cannot be passed.

        This means that when applying brightness,
        tell that specific checkbox function
        to pass a hardcoded index.
        """

        # Percentage connections:
        [(i, percent.triggered.connect(self._switch_brightness_func(i))) for i, percent in enumerate(self.percents)]

        # Monitor connections:
        [(i, monitor.triggered.connect(self._switch_monitor_func(i))) for i, monitor in enumerate(self.monitors)]

        self.about.triggered.connect(self._popup_about)
        self.misc.triggered.connect(self._popop_support)

        # Quit connection
        self.terminator.triggered.connect(quit_tray_and_reset_brightness)

    def _apply_properties(self):

        """
        (4/4)

        Apply any necessary property
        extensions to the menu items.
        """

        self.version.setDisabled(True)
        self.setContextMenu(self.menu)
        [percent.setCheckable(True) for percent in self.percents]

        config_val = float(config['brightness']['level'])
        [val.setChecked(True) for val in self.percents if config_val == xrandr.convert_label_to_xrandr(val.iconText())]
        index_repr = xrandr.convert_xrandr_to_index(config_val)  # Get brightness index for switcher
        self._switch_brightness_func(index_repr)()  # Apply last brightness

    def _popup_about(self):
        self.popup = QMessageBox()
        self.popup.setWindowTitle(
            f"About - {config_app['Desktop Entry']['Name']} Ver. {config_app['Desktop Entry']['Version']}")
        self.popup.setIcon(QMessageBox.Information)
        self.popup.setText("© 2021 Lawrence Chiappelli. All Rights Reserved.")
        github_link = "<a href='https://github.com/Lawrence-Chiappelli/screendimmer'>View on GitHub</a><br><br>"
        self.popup.setInformativeText(f"{github_link}Contact: lawrencechip@protonmail.com")
        self.popup.exec_()

    def _popop_support(self):
        self.popup = QMessageBox()
        self.popup.setWindowTitle(f"Donate / Support - {config_app['Desktop Entry']['Name']} Ver. {config_app['Desktop Entry']['Version']}")
        self.popup.setIcon(QMessageBox.Information)

        aur_link = "<a href='https://aur.archlinux.org/packages/screendimmer/'>AUR</a>"
        github_link = "<a href='https://github.com/Lawrence-Chiappelli/screendimmer'>GitHub</a>"
        upstream_link = "<a href='https://github.com/Lawrence-Chiappelli/screendimmer/issues'>upstream</a>"
        paypal_link = "<a href='https://www.paypal.com/donate?hosted_button_id=YUU33PC5DC592'><b>Open PayPal " \
                      "link</b></a><br><br> "

        self.popup.setText(f"Want to support me? Consider donating:<br><br>{paypal_link}\
            Showing support can include ways other than monetarily or raw code. Here are some suggestions:\
            <ul>\
            <li>Upvote on the {aur_link}</li>\
            <li>Star on {github_link}</li>\
            <li>Report a bug {upstream_link}</li>\
            <li>Package this software for other distros</li>\
            </ul>")

        self.popup.setInformativeText(
            f"Any form of support is greatly appreciated.<br><br>"
            f"For questions, comments, or concerns, feel free to contact me any number of ways.<br><br>Email: "
            f"lawrencechip@protonmail.com")
        self.popup.exec_()

    def _switch_monitor_func(self, index: int):

        switcher = {
            0: self._toggle_monitor_1,
            1: self._toggle_monitor_2,
            2: self._toggle_monitor_3
        }

        return switcher[index]

    def _switch_brightness_func(self, index: int):

        """
        :param index: determines which function
        to return based on the current index.
        Intended for connections.
        Assume 0-based indexing.
        :return: A brightness function,
        as an object
        """

        switcher = {
            0: self._ten,
            1: self._twenty,
            2: self._thirty,
            3: self._fourty,
            4: self._fifty,
            5: self._sixty,
            6: self._seventy,
            7: self._eighty,
            8: self._ninety,
            9: self._hundred
        }

        return switcher[index]

    def _toggle_monitor_1(self):
        self.stage_monitor(0)

    def _toggle_monitor_2(self):
        self.stage_monitor(1)

    def _toggle_monitor_3(self):
        self.stage_monitor(2)

    def stage_monitor(self, monitor_index: int):

        """
        :param monitor_index: Monitor index to stage.
        Assume 0 based indexing.
        """

        self._update_xrandr_list(monitor_index)
        self._check_active_monitors()

    def _update_xrandr_list(self, index: int):

        """
        This is the final monitor list
        that the program will iterate
        through before updating monitor
        brightness.
        
        :param index: Index of local xrandr
        list to adjust. The module iterates over all
        available monitors, and those "available"
        monitors should be removed if the user
        no longer wants it there (determined by
        the user clicking the tray checkmark)
        :return: None
        """

        monitor_name = get_monitors()[index].name
        if self.monitors[index].isChecked():
            xrandr.monitor_names.append(monitor_name)
            print(f"Enabled {monitor_name}:  ", end='')
        else:
            xrandr.monitor_names.remove(monitor_name)
            print(f"Disabled {monitor_name}: ", end='')

    def _check_active_monitors(self):

        """
        Disable brightness checkbox IFF
        the user unticks all monitors
        from within the application.
        This is to non-verbally communicate
        that one or more monitors must be
        enabled.
        :return: None
        """

        enabled_count = 0
        for monitor in self.monitors:
            if monitor.isChecked():
                enabled_count = 1

        print(F"{enabled_count}/{len(self.monitors)} monitors active")

        if enabled_count == 0:
            [percent.setEnabled(False) for percent in self.percents]
        else:
            [percent.setEnabled(True) for percent in self.percents]

    def _ten(self):
        self.stage_brightness(0.1)

    def _twenty(self):
        self.stage_brightness(0.2)

    def _thirty(self):
        self.stage_brightness(0.3)

    def _fourty(self):
        self.stage_brightness(0.4)

    def _fifty(self):
        self.stage_brightness(0.5)

    def _sixty(self):
        self.stage_brightness(0.6)

    def _seventy(self):
        self.stage_brightness(0.7)

    def _eighty(self):
        self.stage_brightness(0.8)

    def _ninety(self):
        self.stage_brightness(0.9)

    def _hundred(self):
        self.stage_brightness(1.0)

    def _tick_checkbox(self, user_checked_box: type(QAction)):

        """
        :param user_checked_box: The currently ticket
        brightness level checkbox.
        :return: None
        """

        for i, action in enumerate(self.percents):
            if action == user_checked_box:
                if user_checked_box.isChecked():  # Do nothing, the user just clicked the same item
                    continue
                else:
                    user_checked_box.setChecked(True)  # Tick the user selected checkbox
                    continue

            action.setChecked(False)  # Set false for all other checkboxes being iterated


def create_tray():
    """
    Create the tray related objects
    :return: None
    """

    # Initializing the app
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray = Tray()
    tray.show()
    sys.exit(app.exec_())


def quit_tray_and_reset_brightness():
    xrandr.apply_brightness('1.0')
    sys.exit()


if __name__ == "__main__":
    create_tray()
