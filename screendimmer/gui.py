import tkinter as tk

"""
Package (2)  New Version  Net Change

extra/tcl    8.6.12-3       6.76 MiB
extra/tk     8.6.12-1       4.79 MiB
"""

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('+%d+%d'%(-50,0))
    # Label(root, text = 'It\'s resizable').pack(side = TOP, pady = 10)

    # On window managers, start the window floating as opposed to tiled
    # iconwindow
    # iconmask
    # maxsize
    # minsize
    # positionfrom
    # 'wm_aspect', 'wm_attributes', 'wm_client', 'wm_colormapwindows'
    # 'wm_command', 'wm_deiconify', 'wm_focusmodel', 'wm_forget',
    # 'wm_frame', 'wm_geometry', 'wm_grid', 'wm_group', 'wm_iconbitmap'
    # 'wm_iconify', 'wm_iconmask', 'wm_iconname', 'wm_iconphoto',
    # 'wm_iconposition', 'wm_iconwindow', 'wm_manage', 'wm_maxsize',
    # 'wm_minsize', 'wm_overrideredirect', 'wm_positionfrom',
    # 'wm_protocol', 'wm_resizable', 'wm_sizefrom', 'wm_state', 'wm_title',
    # 'wm_transient', 'wm_withdraw'
    root.attributes('-type', 'dialog')
    root.title("Screen Dimmer")
    print(help(root))
    print("This should not be the main module")
    root.mainloop()
