import tkinter as tk
import utils
import xrandr
import colors

from functools import partial


"""
Package (2)  New Version  Net Change

extra/tcl    8.6.12-3       6.76 MiB
extra/tk     8.6.12-1       4.79 MiB
"""

"""
pack() - The Pack geometry manager packs widgets in rows or columns.
grid() - The Grid geometry manager puts the widgets in a 2-dimensional table.
The master widget is split into a number of rows and columns, and each “cell” in the resulting table can hold a widget.
place() - The Place geometry manager is the simplest of the three general geometry managers provided in Tkinter.
It allows you explicitly set the position and size of a window, either in absolute terms, or relative to another window.
"""

if __name__ == "__main__":
    print("This should not be the main module")
else:
    color = colors.Colors()


class Gui():

    def __init__(self, monitors: list, resolutions: list, brightnesses: list):
        """Initialize the GUI with predefined, easily accessible information.

        @param monitors (list): A list of strings of monitors, xrandr representation
        @param resolutions (list): A list of strings of resolutions, xrandr representation
        @param brightnesses (list): A list of string floats, xrandr representation

        Note: keep in mind that monitors and resolutions are index adjacent / ordered.
        """

        self.root = tk.Tk()
        self.menu = self._construct_menu_bar()
        self.about = self._construct_about_window()
        self.monitors = [monitor for monitor in monitors]
        self.resolutions = [resolution for resolution in resolutions]
        self.brightnesses = [brightness for brightness in brightnesses]

        """
        Note: the TK vars provide uniqueness for GUI elements, such that
        they won't share the same states and cause "mirror'ed" behavior.

        Additionally, with clever engineering, these TK vars can be
        re-used to provide simulatenous dynamic updating between elements
        (that is, without specifying a command for each element).
        """

        self.toggle_vars = [tk.IntVar(value=1) for _ in range(len(self.monitors))]
        self.brightness_vars = [tk.StringVar(value=utils.convert_xrandr_brightness_to_int(brightness)) for brightness in self.brightnesses]
        self.global_brightness_var = tk.StringVar()

        """Note: the following tkinter elements are editable after being packed."""
        self._toggles = []
        self._inputs = []
        self._scrollers = []
        self._global_scroller = None

    def start(self):
        self.root.mainloop()

    def construct_gui(self):
        """Construct the GUI with data, elements, callbacks and color"""
        self._configure_metadata()
        self._populate_monitor_toggles()
        self._populate_brightness_inputs()
        self._populate_brightness_scrollers()
        self._attach_brightness_callbacks()
        self._configure_theme()

    def _configure_metadata(self):
        self.root.attributes('-type', 'dialog')
        self.root.title("Screen Dimmer")

    def _open_about_window(self):
        print("Opening about window")
        self.about.deiconify()
        self.root.withdraw()

    def _close_about_window(self, *args):
        self.about.withdraw()
        self.root.deiconify()

    def _construct_menu_bar(self):
        menu = tk.Menu(self.root)

        file = tk.Menu(menu, tearoff=0)
        file.add_command(label='Preferences', command=None)
        file.add_command(label='Quit', command=self.root.destroy)
        help = tk.Menu(menu, tearoff=0)
        help.add_command(label='About', command=self._open_about_window)

        menu.add_cascade(label='File', menu=file)
        menu.add_cascade(label='Help', menu=help)
        self.root.config(menu=menu)
        return menu

    def _configure_theme(self):
        bg = color.get_background_color()
        fg = color.get_foreground_color()
        entry_bg = color.get_entry_background_color()
        trough_bg = color.get_trough_background_color()
        button_bg = color.get_button_background_color()
        scrollbar_bg = color.get_scrollbar_background_color()
        disabled_bg = color.get_disabled_background_color()
        disabled_fg = color.get_disabled_foreground_color()
        darkmode_enabled = color.get_darkmode_state()

        self.root.configure(background=bg)
        self.menu.configure(background=entry_bg)
        self.menu.configure(foreground=fg)

        if self._global_scroller:
            self._global_scroller.configure(background=bg, foreground=fg,
                highlightbackground=bg,
                troughcolor=trough_bg,
                activebackground=scrollbar_bg
            )

        for index in range(len(self.monitors)):
            self._toggles[index].configure(background=bg, foreground=fg,
                highlightbackground=bg,
                activebackground=scrollbar_bg,
                selectcolor=entry_bg
            )
            self._inputs[index].configure(background=entry_bg, foreground=fg,
                highlightbackground=bg,
                buttonbackground=button_bg,
                disabledbackground=disabled_bg if darkmode_enabled else None,
                disabledforeground=disabled_fg if darkmode_enabled else None
            )

            checkbox_state = self.toggle_vars[index].get()
            self._scrollers[index].configure(
                background=bg,
                foreground=fg if checkbox_state == 1 else disabled_fg,
                highlightbackground=bg,
                troughcolor=trough_bg if checkbox_state == 1 else disabled_bg
            )

    def _populate_monitor_toggles(self):
        """Populate the GUI with checkbox toggles. Information should be parsed."""

        for i in range(len(self.monitors)):
            toggle = tk.Checkbutton(self.root, text=f" {self.monitors[i]} ({self.resolutions[i]})",
                variable=self.toggle_vars[i],
                onvalue=1,
                offvalue=0,
                command=partial(
                    self._checkbox_handler,
                    i
                )
            )
            toggle.grid(row=0, column=i, sticky=tk.E+tk.W, padx=10, pady=(10,0))
            self._toggles.append(toggle)

    def _populate_brightness_inputs(self):
        """Populate the GUI with input boxes accepting new brightness level integers."""

        for i, brightness_var in enumerate(self.brightness_vars):
            input_box = tk.Spinbox(self.root, textvariable=brightness_var,
                from_=0,
                to=100
            )
            input_box.grid(row=1, column=i, sticky=tk.E+tk.W, padx=10, pady=(0, 20))
            self._inputs.append(input_box)

    def _populate_brightness_scrollers(self):
        """Populate the GUI with vertical scrollbars."""

        for i, brightness_var in enumerate(self.brightness_vars):
            scroller = tk.Scale(self.root, variable=brightness_var,
                from_=100,
                to=0,
                orient=tk.VERTICAL,
                length=200,
                takefocus=1,
                tickinterval=10,
                showvalue=False
            )
            scroller.grid(row=2, column=i, sticky=tk.S)
            self._scrollers.append(scroller)

        if len(self.monitors) > 1:
            # Apply the global scroller if we have more than 1 monitor
            global_scroller = tk.Scale(self.root, variable=self.global_brightness_var,
                from_=0,
                to=100,
                orient=tk.HORIZONTAL,
                length=200,
                takefocus=1,
                tickinterval=10
            )
            global_scroller.set(100)  # So that users start scrolling with the max brightness level
            global_scroller.grid(row=3, columnspan=len(self.monitors), sticky=tk.E+tk.W)
            self._global_scroller = global_scroller

    def _attach_brightness_callbacks(self):
        """Attach listeners to brightness variables for dynamic brightness adjusting behavior"""

        [var.trace_add('write', self._brightness_handler_callback) for var in self.brightness_vars]
        self.global_brightness_var.trace_add('write', self._global_brightness_handler_callback)

    def _brightness_handler_callback(self, var, index, mode):
        """Handle more than 1 task when a brightness value is detected

        @param var (str): String representation of pyvar, not the full object
        @param index (None): Gets passed as None from Tkinter, but needed above
        @param mode (str): 'r'/'w' / 'read'/'write', etc
        @return (bool): False to abort, True to indicate done
        """

        if not index:
            # Manually retrieve the index in the event it's returned as None
            pyvar_as_str_repr = [str(brightness_var) for brightness_var in self.brightness_vars]
            index = pyvar_as_str_repr.index(var)

        brightness_value = self.brightness_vars[index].get()

        if brightness_value.isnumeric():
            # Filter
            if int(brightness_value) > 100:
                brightness_value = 100
            elif int(brightness_value) < 0:
                brightness_value = 5
        else:
            # Or abort
            return False

        xrandr.set_brightness(self.monitors[index], brightness_value)
        return True

    def _global_brightness_handler_callback(self, var, index, mode):
        """Pass and set the global brightness value to every brightness pyvar

        @param var (str): String representation of pyvar, not the full object
        @param index (None): Gets passed as None from Tkinter, but needed above
        @param mode (str): 'r'/'w' / 'read'/'write', etc
        @return (bool): False to abort, True to indicate done
        """

        brightness_value = self.global_brightness_var.get()
        # No need to filter the value, there is currently no
        # way for the user to manually enter the information.

        for i in range(len(self.brightness_vars)):
            checkbox_state = self.toggle_vars[i].get()
            # Because we are directly bypassing the spinbox and setting
            # the value directly on its pyvar, we are required to
            # manually check if said spinbox is enabled/disabled.

            if checkbox_state == 1:
                self.brightness_vars[i].set(brightness_value)
                # No need to call xrandr. The change in the pyvar value will
                # automatically call the non-global brightness handler function,
                # which calls the xrandr.set_brightness function for us.
        return True

    def _checkbox_handler(self, i: int):
        checkbox_state = self.toggle_vars[i].get()

        if checkbox_state == 0:
            self._scrollers[i].config(state=tk.DISABLED)
            self._inputs[i].config(state=tk.DISABLED)
        else:
            self._scrollers[i].config(state=tk.NORMAL)
            self._inputs[i].config(state=tk.NORMAL)

        self._configure_theme()

    def _construct_about_window(self):
        # TODO: flesh out later
        import datetime

        about_window = tk.Toplevel(self.root)
        application_name = 'Screen Dimmer'  # TODO - get via config/constants file
        application_version = '2.0.0'  # TODO - same with above
        current_year = datetime.datetime.now().date().strftime("%Y")

        about_window.attributes('-type', 'dialog')
        about_window.geometry('400x200')
        about_window.title(f"About - {application_name} Ver {application_version}")
        label = tk.Label(about_window, text=f"© 2021-{current_year} Lawrence Chiappelli. All Rights Reserved.")
        label.grid(row=0, column=0)

        about_window.withdraw()  # By default, the about window will show - unless we tell it not to
        about_window.bind('<Escape>', self._close_about_window)
        return about_window

    def populate_close_confirmation(self):
        # TODO: https://www.geeksforgeeks.org/python-tkinter-askquestion-dialog/
        # A closing confirmation dialog wouldn't be such a bad idea.
        pass

    def open_config(self):
        # TODO: https://www.geeksforgeeks.org/python-askopenfile-function-in-tkinter/
        pass

    def save_config(self):
        # TODO
        pass
