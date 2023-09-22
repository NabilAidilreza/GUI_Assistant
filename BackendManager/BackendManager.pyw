from time import sleep
import win32gui, win32con
from collections import Counter

### MANAGES WINDOWS AND PC SYSTEMS ###

def main():
    sleep(1)
    relevant_windows(hide)
    
def relevant_windows(function):
    handles = return_duplicate_window_handles()
    for hwds in handles:
        function(hwds)

def hide(hwds):
    win32gui.ShowWindow(hwds, win32con.SW_MINIMIZE)
        
def close(hwds):
    win32gui.PostMessage(hwds,win32con.WM_CLOSE,0,0)

## EnumWindows enumerates all top-level windows on the screen by passing the handle to each window, in turn, to an application-defined callback function. ##
# winEnumHandler -> function to call on each window instances with thier respective handles #
# Second param not needed since func only needs the handle #
def print_all_windows():
    winds = []
    win32gui.EnumWindows(winEnumAppend,winds)
    for win in winds:
        print(win)
    
def winEnumAppend(hwnd, lst ):
    if win32gui.IsWindowVisible(hwnd):
        if win32gui.GetWindowText(hwnd) != "":
            lst.append((hwnd, win32gui.GetWindowText(hwnd)))

def return_duplicate_window_handles():
    '''Return list window handles of that match a given window name'''
    windows = []
    win32gui.EnumWindows(winEnumAppend, windows)
    window_name = find_duplicate_window_name()
    hwnds = []
    for wind in windows:
        if window_name in wind[1] or window_name == wind[1]:
            hwnds.append(wind[0])
    return hwnds

def find_duplicate_window_name():
    windows = []
    win32gui.EnumWindows(winEnumAppend, windows)
    name_dict = {"name":0}
    for win in windows:
        if win[1] not in name_dict.keys():
            name_dict[win[1]] = 1
        else:
            name_dict[win[1]] += 1
    ### Only can find one duplicate ###
    key_list = list(name_dict.keys())
    val_list = list(name_dict.values())
    duplicate = max(val_list)
    return key_list[val_list.index(duplicate)]

    
if __name__ == "__main__":  #runs the function main() automatically
    main()
