try:
    from .GUI.mainWindowScripts import *
    from .GUI.mainWindow import *
    from .services.config import *
except ImportError:
    from GUI.mainWindowScripts import *
    from GUI.mainWindow import *
    from services.config import *
from pathlib import Path

def get_script_dir(follow_symlinks=True, for_res=False):
    if os.name == "posix" and not for_res:
        home = str(Path.home())
        path = os.path.join(home, ".emailresender")
        if not os.path.exists(path):
            os.mkdir(path)
        return path
    
    if getattr(sys, 'frozen', False):
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

def main():
    work_dir = get_script_dir()
    work_dir_for_res = get_script_dir(for_res=True)
    config = Config.load(work_dir)
    
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow(config, work_dir, work_dir_for_res)
    sys.exit(app.exec())

def create_shortcut():
    def get_script_dir(follow_symlinks=True):
        if getattr(sys, 'frozen', False):
            path = os.path.abspath(sys.executable)
        else:
            path = inspect.getabsfile(get_script_dir)
        if follow_symlinks:
            path = os.path.realpath(path)
        return os.path.dirname(path)
    try:
        from pyshortcuts import make_shortcut
        patch = get_script_dir()
        if os.name == "posix":
            icon = '/res/icon_active.png'
        else:
            icon = '/res/icon_active.ico'
        make_shortcut(script=patch, name='Email Resender',
                                icon=patch+icon,
                                terminal=False)
    except ImportError:
        print("Can't create desktop shortcut, without package pyshortcuts")
if __name__ == "__main__":
    main()