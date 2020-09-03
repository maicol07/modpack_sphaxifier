from PySide2 import QtWidgets
from PySide2.QtCore import QSettings, Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWizard, QMessageBox

from App.Views.MainWindow import MainWindow
from App.Views.Window import get_window
from includes.helpers import path, pick, verify_license

Window = get_window('wizard')

settings = QSettings()
if settings.status() == QSettings.Status.AccessError:
    # noinspection PyTypeChecker
    QMessageBox.critical(None, "Can't access to the registry",
                         "We can't access the Windows Registry to save settings. You can continue, but your settings "
                         "won't be saved")
elif settings.status() == QSettings.Status.FormatError:
    # noinspection PyTypeChecker
    QMessageBox.critical(None, "Malformed settings file",
                         "The settings file is malformed. Therefore, we can't save your settings. You can continue,"
                         "but your settings won't be saved")


# noinspection PyMethodMayBeStatic
class Wizard(Window):
    """
    Main Window Controller
    """

    def __init__(self):
        super().__init__('wizard')

        # Set logo
        logo = QPixmap(path("resources/img/logo.png")).scaled(50, 50, Qt.KeepAspectRatio)
        self.setPixmap(QWizard.LogoPixmap, logo)

        # Buttons actions
        self.pushButton_LicenseVerify.clicked.connect(lambda: verify_license(self.lineEdit_License.text(),
                                                                             self.label_LicenseStatus,
                                                                             self))

        self.toolButton_PatchesFolder.clicked.connect(lambda: pick(self, self.lineEdit_PatchesFolder, directory=True))
        self.toolButton_Credits.clicked.connect(lambda: pick(self, self.lineEdit_Credits, directory=True))

        self.button(QWizard.FinishButton).clicked.connect(self.save_settings)

    def save_settings(self):
        """
        Save settings
        """
        settings.setValue('license_key', self.lineEdit_License.text())
        settings.setValue('patches_folder', self.lineEdit_PatchesFolder.text())
        settings.setValue('pack_credits', self.lineEdit_Credits.text())
        settings.setValue('pack_author', self.lineEdit_Author.text())
        settings.sync()
        MainWindow().show()

    def __stubs(self):
        """ This just enables code completion. It should never be called """
        self.Wizard = QtWidgets.QWizard()
        self.wizardPage1 = QtWidgets.QWizardPage()
        self.lineEdit_License = QtWidgets.QLineEdit()
        self.label_6 = QtWidgets.QLabel()
        self.pushButton_LicenseVerify = QtWidgets.QPushButton()
        self.label_LicenseStatus = QtWidgets.QLabel()
        self.label = QtWidgets.QLabel()
        self.wizardPage2 = QtWidgets.QWizardPage()
        self.label_5 = QtWidgets.QLabel()
        self.lineEdit_PatchesFolder = QtWidgets.QLineEdit()
        self.lineEdit_Author = QtWidgets.QLineEdit()
        self.lineEdit_Credits = QtWidgets.QLineEdit()
        self.label_3 = QtWidgets.QLabel()
        self.label_4 = QtWidgets.QLabel()
        self.toolButton_PatchesFolder = QtWidgets.QToolButton()
        self.toolButton_Credits = QtWidgets.QToolButton()
        raise AssertionError("This should never be called")
