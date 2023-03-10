import os, sys

def resource_path(relative_path, absolute_patch):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = absolute_patch
    pt = os.path.join(base_path, relative_path,)
    
    return pt.replace('\\','/')