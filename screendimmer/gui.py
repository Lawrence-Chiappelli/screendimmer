import tkinter as tk

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

    def start(self):
        self.root.mainloop()

    def populate_with_monitors(self, monitors: list):
        """Populate the GUI with monitor names.

        @param monitors (list): A list of strings of monitors
        @return (None): None
        """
        for monitor in monitors:
            label = tk.Label(self.root, text=monitor).pack()

    def populate_brightness_toggles(self, monitors: list, resolutions=None):

        toggle_button = tk.IntVar()
        for i, monitor in enumerate(monitors):
            toggle_button = tk.Checkbutton(self.root, text = f" - {monitor} @ {resolutions[i]}",
                variable = toggle_button,
                onvalue = 1,
                offvalue = 0,
                height = 2).pack()
