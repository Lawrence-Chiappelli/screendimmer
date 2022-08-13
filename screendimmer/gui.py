import tkinter as tk
import utils
import xrandr
import config

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

class Gui():

    def __init__(self, monitors: list, resolutions: list, brightnesses: list):
        """Initialize the GUI with predefined, easily accessible information.

        @param monitors (list): A list of strings of monitors, xrandr representation
        @param resolutions (list): A list of strings of resolutions, xrandr representation
        @param brightnesses (list): A list of string floats, xrandr representation

        Note: keep in mind that monitors and resolutions are index adjacent / ordered.
        """

        self.root = tk.Tk()
        self.root.attributes('-type', 'dialog')
        self.root.title("Screen Dimmer")

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

        """
        Note: tkinter elements are editable after being packed.
        """
        self.toggles = []
        self.inputs = []
        self.scrollers = []

    def start(self):
        self.root.mainloop()

    def generate_gui(self):
        """Initalize the GUI with interactive elements and callbacks"""

        self._populate_monitor_labels()
        self._populate_monitor_toggles()
        self._populate_brightness_inputs()
        self._populate_brightness_sliders()
        self._populate_brightness_callbacks()
        self.root['background'] = config.Colors().get_background_color()

    def _populate_monitor_labels(self):
        """Populate the GUI with monitor names."""

        for i, monitor in enumerate(self.monitors):
            tk.Label(self.root, text=monitor).grid(row=0, column=i)

    def _populate_monitor_toggles(self):
        """Populate the GUI with checkbox toggles. Information should be parsed."""

        for i in range(len(self.monitors)):
            toggle = tk.Checkbutton(self.root, text=f" {self.monitors[i]} ({self.resolutions[i]})",
                variable=self.toggle_vars[i],
                onvalue=1,
                offvalue=0,
                height=2,
                command=partial(
                    self._checkbox_handler,
                    i
                )
            )
            toggle.grid(row=0, column=i, sticky=tk.W, padx=2)
            self.toggles.append(toggle)

    def _populate_brightness_inputs(self):
        """Populate the GUI with input boxes accepting new brightness level integers."""

        for i, brightness_var in enumerate(self.brightness_vars):
            input_box = tk.Spinbox(self.root, textvariable=brightness_var,
                from_=0,
                to=100
            )
            input_box.grid(row=1, column=i, sticky=tk.W, padx=2)
            self.inputs.append(input_box)

    def _populate_brightness_sliders(self):
        """Populate the GUI with vertical scrollbars."""

        for i, brightness_var in enumerate(self.brightness_vars):
            scroller = tk.Scale(self.root, variable=brightness_var,
                from_=100,
                to=1,
                orient=tk.VERTICAL,
                length=200,
                takefocus=1,
            )
            scroller.grid(row=2, column=i, sticky=tk.S, pady=2)
            self.scrollers.append(scroller)

    def _populate_brightness_callbacks(self):
        """Attach listeners to brightness variables for dynamic brightness adjusting behavior"""

        [var.trace_add('write', self._brightness_handler_callback) for var in self.brightness_vars]

    def _brightness_handler_callback(self, var, index, mode):
        """Handle more than 1 task when a brightness value is detected

        @param var (str): String representation of pyvar, not the full object
        @param index (type): [description] TBD
        @param mode (str): 'r'/'w' / 'read'/'write', etc
        @return (bool): False to abort, True to indicate done
        """

        if not index:
            # Manually retrieve the index in the event it's returned as None
            vars_as_str_repr = [str(brightness_var) for brightness_var in self.brightness_vars]
            index = vars_as_str_repr.index(var)

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

    def _checkbox_handler(self, i):
        checkbox_state = self.toggle_vars[i].get()

        if checkbox_state == 0:
            # TODO: create config file that has colors for light mode and dark mode
            self.scrollers[i].config(state=tk.DISABLED)
            self.scrollers[i].config(troughcolor="#ff0000")
        else:
            self.scrollers[i].config(state=tk.NORMAL)
            self.scrollers[i].config(troughcolor="#00ff00")

    def populate_about_window(self):
        # TODO: flesh out later
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("200x200")
        tk.Label(about_window, text="This is a Toplevel1 window").pack()
        about_window.mainloop()

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
