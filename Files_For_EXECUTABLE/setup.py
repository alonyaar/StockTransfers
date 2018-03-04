import sys
import os
import cx_Freeze 

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["tkinter","os"],'includes': ['tkinter'], "include_files": ["logo.ico", "logo.jpg", "tcl86t.dll", "tk86t.dll"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("TransfersDriver.py", base=base, icon='logo.ico')]

os.environ['TCL_LIBRARY'] = "C:\\Python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Python36\\tcl\\tk8.6"

cx_Freeze.setup(  name = 'Transfers',
                  version = '0.1',
                  description = 'Studio Noa - Transfers',
                  options = {"build_exe" : build_exe_options},
                  executables = executables)
