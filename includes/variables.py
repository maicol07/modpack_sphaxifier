"""
Global variables
"""

import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # The application is frozen
    ROOT_DIR = os.path.dirname(sys.executable)
else:
    # The application is not frozen
    # Change this bit to match where you store your data files:
    ROOT_DIR = Path(__file__).parent.parent

LICENSED = False
