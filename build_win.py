from cx_Freeze import setup, Executable

base = None    

executables = [Executable("AromaPy_win.py", base=base)]

packages = ["idna", "psutil", "tkinter", "webbrowser", "os", "urllib.request", "sys", "zipfile", "subprocess", "shutil", "json"] # Put imports here! (idna is required for all Python programs, no matter what.) Example: packages = ["idna", "example"], example being from "import example" somewhere in the code.
options = {
    'build_exe': {    
        'packages':packages,
    },    
}
# Change metadata here!
setup(
    name = "AromaPy",
    options = options,
    version = "1",
    description = 'UI for Aroma (Wii U hacking method)',
    executables = executables
)
