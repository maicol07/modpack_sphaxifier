"""
Main module
"""

import sys

import pyside_material
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication

# Init QApplication
app = QApplication(sys.argv)
app.setOrganizationName('Maicol07')
app.setOrganizationDomain('maicol07.it')
app.setApplicationName('Modpack Sphaxifier')
app.setApplicationVersion('1.0.1')

from App.Views.MainWindow import MainWindow
from App.Views.Wizard import Wizard
from includes.helpers import setting, verify_license

# Load style
theme = setting('appearance/style')
if theme:
    app.setStyle(theme)
    if theme in pyside_material.list_themes():
        pyside_material.apply_stylesheet(app, theme, 'windowsvista', light_secondary=('light' in theme))
font = setting('appearance/font')
if font:
    # noinspection PyTypeChecker
    app.setFont(QFont(font, 8))

if setting('patches_folder') is None:
    wizard = Wizard()
    wizard.show()
else:
    if setting('license_key'):
        verify_license(setting('license_key'))
    MainWindow().show()
app.exec_()
