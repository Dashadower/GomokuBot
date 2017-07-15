import sys,requests,glob,os
from cx_Freeze import setup, Executable
os.environ['TCL_LIBRARY'] = r'C:\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\\Python36\tcl\tk8.6'
build_exe_options = {"packages":[],"include_files":[("C:/Python36/DLLs/tk86t.dll","tk86t.dll"),("C:/Python36/DLLs/tcl86t.dll","tcl86t.dll"),"settings.config"]}
setup(
    name = "Omok",
    version = "1.0",
    options = {"build_exe":build_exe_options},
    description = "Gomoku AI",
    executables = [Executable("GomokuUI.py", base = "Console")])
