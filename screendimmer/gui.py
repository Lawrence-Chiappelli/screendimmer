import tkinter as tk
import utils

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

    def __init__(self):
        self.root = tk.Tk()
        # self.root.geometry('+%d+%d'%(0,0))
        self.root.geometry('300x600')
        self.root.attributes('-type', 'dialog')
        self.root.title("Screen Dimmer")

        # Note: tkinter elements are editable after being packed.
        self.labels = []
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

        toggle_button = tk.IntVar()
        for i, monitor in enumerate(monitors):
            toggle = tk.Checkbutton(self.root, text = f" {monitor} ({resolutions[i]})",
                variable = toggle_button,
                onvalue = 1,
                offvalue = 0,
                height = 2)
            toggle.pack()
            self.toggles.append(toggle)

    def populate_brightness_inputs(self, brightnesses: list):
        """Populate the GUI with input boxes accepting new brightness level integers.

        @param brightnesses (list): A list of raw brightnesses from xrandr.
        Parse after passing argument! The value should initially be a raw string.
        @return (None): None

        Brightnesses should look something like '0.9'.
        """

        for brightness in brightnesses:
            converted = utils.convert_xrandr_brightness_to_int(brightness)
            input_box = tk.Spinbox(self.root, from_=0, to=100, textvariable=tk.IntVar(value=converted))
            input_box.pack()
            self.inputs.append(input_box)

    def populate_brightness_scollers(self, brightnesses: list):
        """Populate the GUI with vertical scrollbars.

        @param brightnesses (list): A list of raw brightnesses from xrandr.
        Parse after passing argument! The value should initially be a raw string.
        @return (None): None

        Brightnesses should look something like '1.0'.
        """


        for brightness in brightnesses:
            scroller = tk.Scale(self.root, variable=tk.DoubleVar(), from_=100, to=1, orient=tk.VERTICAL)
            converted = utils.convert_xrandr_brightness_to_int(brightness)
            scroller.set(converted)
            scroller.pack()
            self.scrollers.append(scroller)
