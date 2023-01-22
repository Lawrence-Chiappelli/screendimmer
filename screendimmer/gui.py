import tkinter as tk
import datetime
import webbrowser
import utils
import xrandr
import colors
import configutils
import preferences
import constants

from tkinter import messagebox
from functools import partial

"""
Package (2)  New Version  Net Change

extra/tcl    8.6.12-3       6.76 MiB
extra/tk     8.6.12-1       4.79 MiB
"""

if __name__ == "__main__":
    print("This should be an imported module")
    quit()


class Gui():

    def __init__(self, monitors: list, resolutions: list, brightnesses: list, config):
        """Initialize the GUI with predefined, easily accessible information.

        @param monitors (list): A list of strings of monitors, xrandr representation
        @param resolutions (list): A list of strings of resolutions, xrandr representation
        @param brightnesses (list): A list of string floats, xrandr representation

        Note: keep in mind that monitors and resolutions are index adjacent / ordered.
        """
        self.config = config
        self.prefs = preferences.Preferences(self.config.file)

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self._handle_close_callback)
        self.root.title("Screen Dimmer")

        self.monitors = [monitor for monitor in monitors]
        self.resolutions = [resolution for resolution in resolutions]
        self.brightnesses = [brightness for brightness in brightnesses]

        """Tkinter PyVars"""

        # Main interface vars
        self.toggle_vars = [tk.IntVar(value=1) for _ in range(len(self.monitors))]
        self.global_brightness_var = tk.StringVar(value='100')
        self.brightness_vars = [tk.StringVar(
            value=utils.convert_xrandr_brightness_to_int(
                    self.config.file['brightnesses'][self.monitors[i]].lower() if self.config.file else '100'
                )
            )
            for i, brightness in enumerate(self.brightnesses)
        ]

        # Preference vars:
        self.theme = tk.StringVar(value=self.prefs.get_theme())
        self.save_on_exit_var = tk.IntVar(value=self.prefs.is_save_on_exit())
        self.restore_on_exit_var = tk.IntVar(value=self.prefs.is_restore_on_exit())

        """Tkinter GUI elements"""

        # Main interface elements:
        self._toggles = self._populate_monitor_toggles()
        self._inputs = self._populate_brightness_inputs()
        self._scrollers = self._populate_brightness_scrollers()
        self._global_scroller = self._populate_global_scroller()

        """New windows"""
        self.menu = self._construct_menu_bar()
        self.about = self._construct_about_window()
        self.preferences = self._construct_preferences_window()

    def start(self):
        self.root.mainloop()

    def construct_gui(self):
        """Construct the callbacks, colors and window size"""
        self._attach_brightness_callbacks()
        self._apply_theme()
        self._configure_window_size()

    def debug_geometry(self):
        print(f"Geometry after: {self.root.winfo_geometry()}\n{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")

    def _configure_window_size(self):
        self.root.attributes('-type', 'dialog')

        def place_to_corner():
            """
            Window width: NOT including side borders
            Window height: not including window bar NOR file menu!

            Size / coordinates should be:
            369 331 2191 1079
            """
            self.root.update()  # <--- needed to get the window's width and height
            bar_height = self.root.winfo_rooty()
            print(bar_height)
            window_width, window_height = self.root.winfo_width(), self.root.winfo_height()
            window_res_x, window_res_y = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

            file_menu_height = self.menu.winfo_reqheight()
            window_bar_height = 30

            taskbar_on_top = True

            if taskbar_on_top:
                y_pos = window_bar_height
            else:
                y_pos = window_res_y - window_height - window_bar_height

            x_pos = window_res_x - window_width

            print(self.root.winfo_reqheight())

            self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        # place_to_corner()

    def _get_bar_height(self):
        from sys import platform
        offset_y = 0
        if platform in ('win32', 'darwin'):
            import ctypes
            try: # >= win 8.1
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except: # win 8.0 or less
                ctypes.windll.user32.SetProcessDPIAware()
            offset_y = int(self.root.geometry().rsplit('+', 1)[-1])
            print(offset_y)

        print(self.root.winfo_rooty())
        bar_height = self.root.winfo_rooty() - offset_y
        return bar_height

    """
    Various data configurators:
    """
    def _apply_theme(self):
        theme = self.prefs.get_theme()

        bg = theme.get_background_color()
        fg = theme.get_foreground_color()
        entry_bg = theme.get_entry_background_color()
        trough_bg = theme.get_trough_background_color()
        button_bg = theme.get_button_background_color()
        scrollbar_bg = theme.get_scrollbar_background_color()
        disabled_bg = theme.get_disabled_background_color()
        disabled_fg = theme.get_disabled_foreground_color()
        hyperlink_fg = theme.get_hyperlink_foreground_color()

        self.root.configure(background=bg)
        self.about.configure(background=bg)
        self.preferences.configure(background=bg)
        self.menu.configure(background=entry_bg, foreground=fg)

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
                disabledbackground=disabled_bg if self.prefs.is_dark_mode_enabled() else None,
                disabledforeground=disabled_fg if self.prefs.is_dark_mode_enabled() else None
            )

            checkbox_state = self.toggle_vars[index].get()
            self._scrollers[index].configure(
                background=bg,
                foreground=fg if checkbox_state == 1 else disabled_fg,
                highlightbackground=bg,
                troughcolor=trough_bg if checkbox_state == 1 else disabled_bg,
                activebackground=scrollbar_bg
            )


        for widget in self.about.winfo_children():
            if type(widget) == type(tk.Label()) and "GitHub" in widget['text']:
                widget.configure(background=bg, foreground=hyperlink_fg)
            elif type(widget) == type(tk.Button()):
                widget.configure(background=button_bg, foreground=fg)
            else:
                widget.configure(background=bg, foreground=fg)

        for widget in self.preferences.winfo_children():
            if type(widget) == type(tk.Label()):
                widget.configure(background=bg, foreground=fg)
            elif type(widget) == type(tk.Button()):
                widget.configure(background=button_bg, foreground=fg)
            elif type(widget) == type(tk.Checkbutton()):
                widget.configure(background=bg, foreground=fg,
                    highlightbackground=bg,
                    activebackground=scrollbar_bg,
                    selectcolor=entry_bg
                )
            elif type(widget) == type(tk.OptionMenu(None, None, None)):
                widget.configure(background=button_bg, foreground=fg,
                    highlightbackground=bg,
                    activebackground=scrollbar_bg,
                )
            else:
                widget.configure(background=bg, foreground=fg)

    """
    Widget constructions/populations:
    """
    def _construct_menu_bar(self):
        menu = tk.Menu(self.root)

        file = tk.Menu(menu, tearoff=0)
        file.add_command(label='Preferences', command=self._open_preferences_window)
        file.add_command(label='Quit', command=self._handle_close_callback)
        help = tk.Menu(menu, tearoff=0)
        help.add_command(label='About', command=self._open_about_window)

        menu.add_cascade(label='File', menu=file)
        menu.add_cascade(label='Help', menu=help)
        self.root.config(menu=menu)
        return menu

    def _populate_monitor_toggles(self):
        """Populate the GUI with checkbox toggles. Information should be parsed."""

        toggles = []
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
            toggles.append(toggle)
        return toggles

    def _populate_brightness_inputs(self):
        """Populate the GUI with input boxes accepting new brightness level integers."""

        inputs = []
        for i, brightness_var in enumerate(self.brightness_vars):
            input_box = tk.Spinbox(self.root, textvariable=brightness_var,
                from_=0,
                to=100
            )
            input_box.grid(row=1, column=i, sticky=tk.E+tk.W, padx=10, pady=(0, 20))
            input_box.bind('<Button-4>', self._handle_mousewheel_callback)
            input_box.bind('<Button-5>', self._handle_mousewheel_callback)
            inputs.append(input_box)
        return inputs

    def _populate_brightness_scrollers(self):
        """Populate the GUI with vertical scrollbars."""

        scrollers = []
        only_one_monitor = len(self.brightness_vars) == 1
        for i, brightness_var in enumerate(self.brightness_vars):
            scroller = tk.Scale(self.root, variable=brightness_var,
                from_=100,
                to=0,
                orient=tk.VERTICAL,
                length=200,
                takefocus=1,
                tickinterval=10,
                showvalue=False,
            )
            scroller.grid(row=2, column=i, sticky=tk.S, pady=(0,20 if only_one_monitor else 0))
            scroller.bind('<Button-4>', self._handle_mousewheel_callback)
            scroller.bind('<Button-5>', self._handle_mousewheel_callback)
            scrollers.append(scroller)

        return scrollers

    def _populate_global_scroller(self):
        """Apply the global scroller, IFF we have more than 1 monitor"""

        if len(self.monitors) > 1:
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
            global_scroller.bind('<Button-4>', self._handle_mousewheel_global_callback)
            global_scroller.bind('<Button-5>', self._handle_mousewheel_global_callback)
            return global_scroller
        else:
            return None

    """
    About window:
    """
    def _construct_about_window(self):

        def openurl(url):
           webbrowser.open_new_tab(url)

        about_window = tk.Toplevel(self.root)
        application_name = 'Screen Dimmer'  # TODO - get via config/constants file
        application_version = '2.0.0'  # TODO - same with above
        current_year = datetime.datetime.now().date().strftime("%Y")

        about_window.attributes('-type', 'dialog')
        about_window.title(f"About - {application_name} Ver {application_version}")
        image = tk.Label(about_window, image="::tk::icons::information")
        image.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        # Copyright:
        copyright_label = tk.Label(about_window, text=f"© 2021-{current_year} {constants.FULL_NAME}. All Rights Reserved.",
            font=10,
            justify=tk.LEFT,
        )
        copyright_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))

        # GitHub link:
        github_label = tk.Label(about_window, text="View on GitHub",
            font=10,
            fg="blue",
            cursor="hand2"
        )
        github_label.grid(row=1, column=1, sticky=tk.W, pady=(0, 20))
        github_label.bind("<Button-1>", lambda e:
            openurl(constants.GITHUB_LINK_REPO)
        )

        # Contact:
        # TODO: can't copy and paste this label, may want to use tk.Text() intead
        contact_label = tk.Label(about_window, text=f"Contact: {constants.EMAIL}",
            font=10,
            justify=tk.LEFT,
        )
        contact_label.grid(row=2, column=1, sticky=tk.W, pady=(0, 20))

        # Ok button:
        button = tk.Button(about_window, text="Close", command=self._close_about_window)
        button.grid(row=3, column=0, columnspan=2, sticky=tk.S, pady=(0,20))
        button.bind('<Return>', self._close_about_window)

        about_window.withdraw()  # By default, the about window will show - unless we tell it not to
        about_window.bind('<Escape>', self._close_about_window)
        about_window.bind('<Return>', self._close_about_window)
        return about_window

    def _open_about_window(self):
        self.about.deiconify()
        self.root.withdraw()

    def _close_about_window(self, *args):
        self.about.withdraw()
        self.root.deiconify()

    """
    Preferences window:
    """
    def _construct_preferences_window(self):
        preferences_window = tk.Toplevel(self.root)
        application_name = 'Screen Dimmer'

        preferences_window.attributes('-type', 'dialog')
        preferences_window.title(f"Preferences")

        label_theme = tk.Label(preferences_window, text='Theme:')
        label_theme.grid(row=0, column=0, padx=4, pady=4, sticky=tk.W)

        all_themes = utils.get_all_available_themes()
        theme_select = tk.OptionMenu(preferences_window, self.theme, *all_themes, command=self._theme_handler_callback)
        theme_select.grid(row=0, column=1, padx=4, pady=4, sticky=tk.E)

        # Save on exit:
        checkbox_save_on_exit = tk.Checkbutton(preferences_window, text="Save monitor config on exit",
            variable=self.save_on_exit_var,
            command=self._save_on_exit_handler_callback,
            onvalue=1,
            offvalue=0,
        )
        checkbox_save_on_exit.grid(row=1, column=0,
            columnspan=2,
            sticky=tk.W,
            padx=0,
            pady=4
        )

        # Restore on exit:
        checkbox_restore_on_exit = tk.Checkbutton(preferences_window, text="Set brightnesses to 100% on exit",
            variable=self.restore_on_exit_var,
            command=self._restore_on_exit_handler_callback,
            onvalue=1,
            offvalue=0
        )
        checkbox_restore_on_exit.grid(row=2, column=0,
            columnspan=2,
            sticky=tk.W,
            padx=(0, 4),
            pady=4
        )

        button_confirm = tk.Button(preferences_window, text="Confirm", command=self._close_preferences_window)
        button_confirm.grid(row=3, column=0, columnspan=2, sticky=tk.N, pady=15)
        button_confirm.bind('<Return>', self._close_preferences_window)

        preferences_window.withdraw()  # By default, the about window will show - unless we tell it not to
        preferences_window.bind('<Escape>', self._close_preferences_window)
        preferences_window.bind('<Return>', self._close_preferences_window)
        return preferences_window

    def _open_preferences_window(self):
        self.preferences.deiconify()
        self.root.withdraw()

    def _close_preferences_window(self, *args):
        self.preferences.withdraw()
        self.root.deiconify()
        self.config.save()  # Overkill to save here, but doesn't hurt in the event an exception is raised during mainloop

    """
    Callbacks:
    """
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

        self._apply_theme()

    def _theme_handler_callback(self, selected_theme_as_class):
        self.prefs.save_new_theme(selected_theme_as_class)
        self._apply_theme()

    def _save_on_exit_handler_callback(self):
        self.prefs.apply_save_on_exit(self.save_on_exit_var.get())

    def _restore_on_exit_handler_callback(self):
        self.prefs.apply_restore_on_exit(self.restore_on_exit_var.get())

    def _handle_close_callback(self):


        """
        After the mainloop has been terminated / destroyed, let's
        consult the user's preferences and apply any applicable
        exit behaviors.
        """

        def save_brightnesses_to_config():
            """"Saving monitor brightnesses to config (default is enabled)"""
            for i in range(len(self.monitors)):
                monitor = self.monitors[i].lower()
                brightness = utils.convert_converted_brightness_to_xrandr(
                    self.brightness_vars[i].get()
                )
                self.config.file['brightnesses'][monitor] = brightness

        def restore_brightnesses_to_max():
            """Restore brightnesses when the application exists (default is enabled)"""
            for monitor in self.monitors:
                xrandr.set_brightness(monitor, '1.0')

        self.root.destroy()
        self.prefs.apply_save_on_exit(self.save_on_exit_var.get())
        self.prefs.apply_restore_on_exit(self.restore_on_exit_var.get())

        try:
            save_brightnesses_to_config() if self.prefs.is_save_on_exit() else None
            restore_brightnesses_to_max() if self.prefs.is_restore_on_exit() else None
        except Exception as e:
            print(f"Error exiting the program. Unable to consult your preferences.\nException message: \"{e}\"\nIt's likely the configuration file is missing.\nPlease consider reporting this upstream: https://github.com/lawrence-chiappelli/screendimmer/issues")

    def _handle_mousewheel_callback(self, event):
        mouse_wheel_up = event.num == 4
        mouse_wheel_down = event.num == 5

        if type(event.widget) == type(tk.Scale()):
            index = self._scrollers.index(event.widget)
        else:
            index = self._inputs.index(event.widget)

        var = self.brightness_vars[index]
        brightness_value = var.get()

        if self.toggle_vars[index].get() == 1:
            if mouse_wheel_up:
                var.set(str( int(brightness_value) + 1) )
            elif mouse_wheel_down:
                var.set(str( int(brightness_value) - 1) )

    def _handle_mousewheel_global_callback(self, event):
        mouse_wheel_up = event.num == 4
        mouse_wheel_down = event.num == 5

        var = self.global_brightness_var
        brightness_value = self.global_brightness_var.get()

        if mouse_wheel_up:
            var.set(str( int(brightness_value) + 1) )
        elif mouse_wheel_down:
            var.set(str( int(brightness_value) - 1) )
