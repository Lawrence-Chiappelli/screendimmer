#!/usr/bin/python3
import os
import sys
import platform
import setup
from screendimmer import configutil, xrandr, utils
from screeninfo import get_monitors
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

config = configutil.get_parsed_config()


class Tray(QSystemTrayIcon):
    
    def __init__(self):
        super(Tray, self).__init__()
        self.setIcon(QIcon(utils.get_icon_path()))
        self.setVisible(True)
        self.setToolTip("Adjust brightness here")
        self.init_ui()

    def init_ui(self):

        self._create_elements()
        self._add_actions()
        self._apply_connections()
        self._apply_properties()

    def _create_elements(self):
        self.menu = QMenu()
        self.monitors = [QAction(monitor.name + f" ({monitor.width}x{monitor.height})") for monitor in get_monitors()]
        self.percents = [QAction(f'{i+1}0%') for i in range(10)]        
        self.misc = QAction('Donate / Support')
        self.about = QAction("About")
        self.terminator = QAction("Quit")    

    def _add_actions(self):

        """
        Some of the following may be reversed to
        accommodate initial user intuition and
        also personal preference
        :return: None
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

        # Donate action
        self.menu.addAction(self.misc)

        # About popup action
        self.menu.addAction(self.about)

        # Quit action
        self.menu.addAction(self.terminator)

    def _apply_properties(self):

        [percent.setCheckable(True) for percent in self.percents]
        self.setContextMenu(self.menu)

        config_val = float(config['brightness']['level'])
        [val.setChecked(True) for val in self.percents if config_val == xrandr.convert_label_to_xrandr(val.iconText())]
        index_repr = xrandr.convert_xrandr_to_index(config_val)  # Get brightness index for switcher
        self._switch_brightness_func(index_repr)()  # Apply last brightness

    def _apply_connections(self):

        # Percentage connections:
        [(i, percent.triggered.connect(self._switch_brightness_func(i))) for i, percent in enumerate(self.percents)]

        # Monitor connections:
        [(i, monitor.triggered.connect(self._switch_monitor_func(i))) for i, monitor in enumerate(self.monitors)]

        self.about.triggered.connect(self._popup)
        self.misc.triggered.connect(self._open_link)

        # Quit connection
        self.terminator.triggered.connect(self._quit)

    def _quit(self):
        xrandr.apply_brightness('1.0', False)
        sys.exit()

    def _open_link(self):
        url = "https://www.paypal.com/donate?hosted_button_id=YUU33PC5DC592"
        if platform.system() == "Linux":
            os.system(f"xdg-open \"{url}\"")
        elif platform.system() == "Windows":
            os.system(f"start \"{url}\"")
        else:
            return

    def _popup(self):
        self.popup = QMessageBox()
        self.popup.setWindowTitle(f"About - {setup.config['Name']} Ver. {setup.config['Version']}")
        self.popup.setIcon(QMessageBox.Information)
        self.popup.setText("© 2021 Lawrence Chiappelli. All Rights Reserved.")
        github_link = "<a href='https://github.com/Lawrence-Chiappelli/screendimmer'>View on GitHub</a><br><br>"
        self.popup.setInformativeText(f"{github_link}Contact: lawrencechip@protonmail.com")
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
        Intended for connections. Beats creating
        10 individual functions in different
        places.
        Assume 0-based indexing.
        :return: A brightness function object
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
            9: self._full
        }

        return switcher[index]

    def _toggle_monitor_1(self):
        self._update_xrandr_list(0)
        self._check_active_monitors()

    def _toggle_monitor_2(self):
        self._update_xrandr_list(1)
        self._check_active_monitors()

    def _toggle_monitor_3(self):
        self._update_xrandr_list(2)
        self._check_active_monitors()

    def _update_xrandr_list(self, index: int):

        """
        :param index: Index of local xrandr
        list to adjust. The module iterates over all
        available monitors, and those "available"
        monitors should be removed if the user
        no longer wants it there (determined by
        the user clicking the tray checkmark)
        :return: None
        """

        if self.monitors[index].isChecked():
            xrandr.monitor_names.append(get_monitors()[index].name)
        else:
            xrandr.monitor_names.remove(get_monitors()[index].name)

    def _check_active_monitors(self):

        """
        Disable percent checkbox control IFF
        all monitors are disabled (to non-verbally
        communicate to the user that one or more
        monitors must be active)
        :return: None
        """

        disabled_count = 0
        for monitor in self.monitors:
            if not monitor.isChecked():
                disabled_count += 1
        print(F"Disabled count: {disabled_count} | Num monitors: {len(self.monitors)}")
        if disabled_count == len(self.monitors):
            [percent.setDisabled(True) for percent in self.percents]
        else:
            [percent.setDisabled(False) for percent in self.percents]

        # Note: the following might be slightly faster, but for the
        # sake of not completely depending on the xrandr module, it makes
        # more sense to iterate over the checkboxes from this class.
        if not xrandr.monitor_names:
            pass

    def _ten(self):
        xrandr.apply_brightness('0.1')
        self._untick_irrelevant_checkboxes(self.percents[0])

    def _twenty(self):
        xrandr.apply_brightness('0.2')
        self._untick_irrelevant_checkboxes(self.percents[1])

    def _thirty(self):
        xrandr.apply_brightness('0.3')
        self._untick_irrelevant_checkboxes(self.percents[2])

    def _fourty(self):
        xrandr.apply_brightness('0.4')
        self._untick_irrelevant_checkboxes(self.percents[3])

    def _fifty(self):
        xrandr.apply_brightness('0.5')
        self._untick_irrelevant_checkboxes(self.percents[4])

    def _sixty(self):
        xrandr.apply_brightness('0.6')
        self._untick_irrelevant_checkboxes(self.percents[5])

    def _seventy(self):
        xrandr.apply_brightness('0.7')
        self._untick_irrelevant_checkboxes(self.percents[6])

    def _eighty(self):
        xrandr.apply_brightness('0.8')
        self._untick_irrelevant_checkboxes(self.percents[7])

    def _ninety(self):
        xrandr.apply_brightness('0.9')
        self._untick_irrelevant_checkboxes(self.percents[8])

    def _full(self):
        xrandr.apply_brightness('1.0')
        self._untick_irrelevant_checkboxes(self.percents[9])

    def _untick_irrelevant_checkboxes(self, user_checked_box: type(QAction)):

        """
        :param user_checked_box: The currently ticket
        brightness level checkbox.
        :return: None
        """

        for i, action in enumerate(self.percents):
            if action == user_checked_box:
                if user_checked_box.isChecked():  # Do nothing, this behavior is normal
                    continue
                else:  # Re-tick the checkmark if clicked again
                    user_checked_box.setChecked(True)
                    continue

            action.setChecked(False)  # Set false for all other checkmarks


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


if __name__ == "__main__":
    create_tray()
