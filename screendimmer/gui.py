import tkinter as tk
import utils
import xrandr

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

    def __init__(self, brightnesses: list):
        self.root = tk.Tk()
        self.root.attributes('-type', 'dialog')
        self.root.title("Screen Dimmer")

        """
        Note: the TK vars provide uniqueness for GUI elements, such that
        they won't share the same states and cause "mirror'ed" behavior.

        On the flipside, with clever engineering, these TK vars can be
        re-used to provide simulatenous dynamic updating between elements
        (that is, without specifying a command for each element).
        """
        self.toggle_vars = [tk.IntVar() for _ in range(len(brightnesses))]
        self.brightness_vars = [tk.IntVar(value=utils.convert_xrandr_brightness_to_int(val)) for val in brightnesses]

        # Note: tkinter elements are editable after being packed.
        self.toggles = []
        self.inputs = []
        self.scrollers = []

    def start(self):
        self.root.mainloop()

    def populate_with_monitors(self, monitors: list):
        """Populate the GUI with monitor names.

        @param monitors (list): A list of strings of monitors
        @return (None): None
        """

        for monitor in monitors:
            tk.Label(self.root, text=monitor).pack()

    def populate_brightness_toggles(self, monitors: list, resolutions: list):
        """Populate the GUI with checkbox toggles. Information should be parsed.

        @param monitors (list): A list of monitors, parsed as raw strings from xrandr
        @param resolutions (list): A list of resolutions, parsed as raw strings from xrandr
        @return (None): None

        Note: monitors and resolutions are index adjacent / ordered.
        """

        for i, monitor in enumerate(monitors):
            toggle = tk.Checkbutton(self.root, text = f" {monitor} ({resolutions[i]})",
                variable = self.toggle_vars[i],
                onvalue = 1,
                offvalue = 0,
                height = 2)
            toggle.grid(row=0, column=i, sticky=tk.W, padx=2)
            self.toggles.append(toggle)

    def populate_brightness_inputs(self, brightnesses: list):
        """Populate the GUI with input boxes accepting new brightness level integers.

        @param brightnesses (list): A list of raw brightnesses from xrandr.
        Parse after passing argument! The value should initially be a raw string.
        @return (None): None

        Brightnesses should look something like '0.9'.
        """

        for i, brightness in enumerate(brightnesses):
            converted = utils.convert_xrandr_brightness_to_int(brightness)
            input_box = tk.Spinbox(self.root, textvariable=self.brightness_vars[i],
                from_=0,
                to=100
            )
            input_box.grid(row=1, column=i, sticky=tk.W, padx=2)
            self.inputs.append(input_box)

    def populate_brightness_sliders(self, brightnesses: list):
        """Populate the GUI with vertical scrollbars.

        @param brightnesses (list): A list of raw brightnesses from xrandr.
        Parse after passing argument! The value should initially be a raw string.
        @return (None): None

        Brightnesses should look something like '1.0'.
        """

        for i, brightness in enumerate(brightnesses):
            scroller = tk.Scale(self.root, variable=self.brightness_vars[i],
                from_=100,
                to=1,
                orient=tk.VERTICAL,
                length=200
            )
            scroller.grid(row=2, column=i, sticky=tk.W, pady=2)
            self.scrollers.append(scroller)

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
