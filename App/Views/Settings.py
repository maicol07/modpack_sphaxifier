import pyside_material
from PySide2 import QtWidgets
from PySide2.QtCore import QSettings
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QStyleFactory, QApplication

from App.Views.Window import get_window
from includes.helpers import setting, pick, verify_license

Dialog = get_window('dialog')
settings = QSettings()


class Settings(Dialog):
    """
    Settings Controller
    """

    def __init__(self):
        super().__init__('settings')
        self.app = QApplication.instance()

        # Font
        idx = self.ComboBox_Font.findText(setting('appearance/font', QFont().defaultFamily()))
        self.ComboBox_Font.setCurrentIndex(idx)

        # Themes
        themes = QStyleFactory.keys() + pyside_material.list_themes()
        self.ComboBox_Theme.addItems(themes)
        idx = self.ComboBox_Theme.findText(setting('appearance/style', self.app.style().objectName()))
        self.ComboBox_Theme.setCurrentIndex(idx)

        # App settings
        self.lineEdit_PatchesFolder.setText(setting('patches_folder'))
        self.lineEdit_PatchesFolder.mousePressEvent = lambda: pick(self,
                                                                   self.lineEdit_PatchesFolder,
                                                                   directory=True)
        self.lineEdit_Credits.setText(setting('pack_credits'))
        self.lineEdit_Credits.mousePressEvent = lambda: pick(self,
                                                             self.lineEdit_Credits,
                                                             directory=True)
        self.lineEdit_Author.setText(setting('pack_author'))

        # License verify
        if self.lineEdit_License.text():
            self.verify_license()
        self.pushButton_LicenseVerify.clicked.connect(self.verify_license)

        self.buttonBox.accepted.connect(self.save_settings)
        self.buttonBox.button(self.buttonBox.Reset).clicked.connect(self.reset_settings)

    def verify_license(self):
        """
        Verify license
        """
        verify_license(self.lineEdit_License.text(), self.label_LicenseStatus, self)

    def save_settings(self):
        """
        Save settings
        """
        # Font
        new_font = QFont(self.ComboBox_Font.currentText(), 8)
        settings.setValue('appearance/font', self.ComboBox_Font.currentText())
        self.app.setFont(new_font)

        # Theme
        newtheme = self.ComboBox_Theme.currentText()
        settings.setValue('appearance/style', newtheme)
        if newtheme in pyside_material.list_themes():
            pyside_material.apply_stylesheet(self.app, newtheme, 'windowsvista', light_secondary=('light' in newtheme))
        else:
            self.app.setStyle(newtheme)

        # App settings
        settings.setValue('patches_folder', self.lineEdit_PatchesFolder.text())
        settings.setValue('pack_credits', self.lineEdit_Credits.text())
        settings.setValue('pack_author', self.lineEdit_Author.text())

        settings.sync()

        self.close()

    def reset_settings(self):
        """
        Reset settings
        """
        self.ComboBox_Font.setCurrentText('MS Shell Dlg 2')
        self.ComboBox_Theme.setCurrentText(QStyleFactory.keys()[0])
        self.lineEdit_PatchesFolder.clear()
        self.lineEdit_Credits.clear()
        self.lineEdit_Author.clear()

    def __stubs(self):
        """ This just enables code completion. It should never be called """
        self.Dialog = QtWidgets.QDialog()
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.ComboBox_Font = QtWidgets.QFontComboBox()
        self.label = QtWidgets.QLabel()
        self.ComboBox_Theme = QtWidgets.QComboBox()
        self.label_2 = QtWidgets.QLabel()
        self.label_3 = QtWidgets.QLabel()
        self.lineEdit_PatchesFolder = QtWidgets.QLineEdit()
        self.label_4 = QtWidgets.QLabel()
        self.lineEdit_Credits = QtWidgets.QLineEdit()
        self.label_5 = QtWidgets.QLabel()
        self.lineEdit_Author = QtWidgets.QLineEdit()
        self.frame = QtWidgets.QFrame()
        self.toolButton_PatchesFolder = QtWidgets.QToolButton()
        self.toolButton_Credits = QtWidgets.QToolButton()
        self.label_6 = QtWidgets.QLabel()
        self.pushButton_LicenseVerify = QtWidgets.QPushButton()
        self.label_LicenseStatus = QtWidgets.QLabel()
        self.lineEdit_License = QtWidgets.QLineEdit()
        self.label_7 = QtWidgets.QLabel()
        raise AssertionError("This should never be called")
