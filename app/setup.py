"""
Executable build script, modify and run this on the appropriate OS.
Run with 'python setup.py build'
"""

import sys
from cx_Freeze import setup, Executable
includefiles = ['../data/', '../img/']

if sys.platform == 'win32':
    exe = Executable('beertally.py', targetName="BeerTally.exe", base="Win32GUI")
else:
    exe = Executable('beertally.py', targetName="BeerTally")

options = {
    'build_exe': {
        'includes': ['atexit', 'PySide.QtCore', 'cffi'],
        'include_files':includefiles
    }
}

setup(name='Turflijst JvB7',
      version='1.0',
      description='Turflijst voor JvB7',
      options=options,
      executables=[exe],
      )
