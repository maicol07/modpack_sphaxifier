"""
Window loader
"""

from PySide2.QtCore import QFile
from PySide2.QtWidgets import QMainWindow, QDialog, QWizard

import resources.resources
from includes.UiLoader import loadUi
from includes.helpers import path


def get_window(window_type='window'):
    """
    Get window

    :param window_type:
    :return:
    """
    if window_type == 'window':
        parent = QMainWindow
    elif window_type == 'wizard':
        parent = QWizard
    else:
        parent = QDialog

    class Window(parent):
        """
        Manage a window
        """
        def __init__(self, view: str):
            """
            Window constructor

            :param view: The name of the view to load
            """
            super(Window, self).__init__()
            ui_file = QFile(path("resources/views/{}.ui".format(view)))
            ui_file.open(QFile.ReadOnly)

            loadUi(ui_file, self, workingDirectory=path("resources/views"))
            ui_file.close()

        # noinspection PyMethodMayBeStatic
        def __stub(self):
            """ This code is only for imports optimizations. Don't run it """
            a = resources.resources
            raise AssertionError("You shouldn't run this code!" + str(a))

    return Window
