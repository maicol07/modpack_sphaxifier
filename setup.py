import os
import sys

from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll')

# Find version
file = open('VERSION')
version = file.read()
file.close()

build_exe_options = {
    "zip_include_packages": [
        # Bundled
        '__future__',
        'datetime',
        'distutils',
        'json',
        'os',
        'pathlib',
        'shutil',
        'sys',
        'webbrowser',
        'zipfile',
        # 3rd party
        'dotted_dict',
        'PySide2',
        'PySide2.QtGui'
        'pyside_material',
        'requests'
    ],
    "zip_exclude_packages": [
        "tkinter",
        "sqlite3"
    ],
    "include_files": [
        ('resources/KOMIKAX_.ttf', 'resources/KOMIKAX_.ttf'),
        ('resources/html', 'resources/html'),
        ('resources/img', r'resources/img'),
        ('resources/views', r'resources/views'),
        (os.environ['TCL_LIBRARY'], os.path.join('lib', 'tcl86t.dll')),
        (os.environ['TK_LIBRARY'], os.path.join('lib', 'tk86t.dll'))
    ],
    "optimize": 2,
    "build_exe": "build",
}

setup(
    name="Modpack Sphaxifier",
    version=version,
    description="A tool to compress mods texture patches together. Designed principally for Sphax ones",
    options={
        "build_exe": build_exe_options
    },
    executables=[
        Executable(
            "main.py",
            base="Win32GUI" if sys.platform == "win32" else None,
            icon="resources/img/logo.ico",
            shortcutName="Modpack Sphaxifier",
            shortcutDir="DesktopFolder"
        )
    ])
