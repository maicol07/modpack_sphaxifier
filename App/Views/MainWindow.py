import json
import os
import shutil
import webbrowser
from distutils import file_util, dir_util
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED

from PySide2 import QtWidgets
from PySide2.QtCore import QSettings, Qt, QByteArray
from PySide2.QtWidgets import QMessageBox, QProgressDialog, QListWidgetItem, QFileDialog
from dotted_dict import DottedDict

from App.Views.Settings import Settings
from App.Views.Window import get_window
from includes.helpers import data, setting, path

Window = get_window()
settings = QSettings()


# noinspection PyMethodMayBeStatic
class MainWindow(Window):
    """
    Main Window Controller
    """
    temp_folder_name = data("tmp")

    pack_formats = {
        "1.8.9": 1,
        "1.10.2": 2,
        "1.12.2": 3,
        "1.14.4": 4,
        "1.16.1": 5,
        "1.16.2": 6
    }

    pack_mcmeta = {
        "pack_format": 3,  # see here: https://minecraft.gamepedia.com/Resource_Pack#Contents
        "description": "Sphax PureBDCraft {res} patch for {name}\nby \u00A7{author}\u00A71 - http://bdcraft.net ",
        "built_with": 'Modpack Sphaxifier by maicol07 (https://maicol07.it)'
    }

    def __init__(self):
        super().__init__('main')

        self.settings = Settings()

        # Start Button
        self.pushButton_Start.clicked.connect(self.pack)

        # Combobox
        # noinspection PyTypeChecker
        self.comboBox_PackVersion.addItems(filter(lambda x: os.path.isdir(os.path.join(setting('patches_folder'), x)),
                                                  os.listdir(setting('patches_folder'))))
        self.comboBox_PackVersion.currentTextChanged.connect(self.load_resolutions)

        self.load_resolutions(self.comboBox_PackVersion.currentText())
        self.comboBox_PackResolution.currentTextChanged.connect(lambda: self.load_patches(True))
        try:
            # noinspection PyTypeChecker
            self.comboBox_Previous.addItems([selection.replace('.json', '') for selection in filter(
                lambda x: os.path.join(data('selections'), x).endswith('.json'), os.listdir(data('selections'))
            )])
        except FileNotFoundError:
            pass
        # Use lambda because of event parameter
        self.comboBox_Previous.currentTextChanged.connect(lambda: self.load_patches())

        # Menu Bar
        self.actionExit.triggered.connect(self.close)

        self.actionSettings.triggered.connect(self.open_settings)

        self.actionSupport.triggered.connect(lambda: webbrowser.open('https://maicol07.it/#contact'))
        self.actionAbout.triggered.connect(self.open_info)
        self.actionAbout_Qt.triggered.connect(lambda: QMessageBox.aboutQt(self, "About Qt"))

    def load_resolutions(self, value):
        """
        Load pack resolutions

        :param value:
        """
        self.comboBox_PackResolution.clear()
        # noinspection PyTypeChecker
        self.comboBox_PackResolution.addItems(filter(
            lambda x: os.path.isdir(os.path.join(setting('patches_folder'), value, x)),
            os.listdir(os.path.join(setting('patches_folder'), value))
        ))
        self.load_patches(True)

    def load_patches(self, changed=False):
        """
        (Re)load patches list
        """
        selected = []
        if changed:
            self.listWidget.clear()
            already = []
        else:
            selection = self.comboBox_Previous.currentIndex()
            if selection != "New":
                selection_name = self.comboBox_Previous.itemText(selection)
                selection_path = data("selections/{}.json".format(selection_name))
                if selection > 0 and os.path.exists(selection_path):
                    file = open(selection_path)
                    selected = DottedDict(json.loads(file.read()))
                    file.close()
                    self.comboBox_PackVersion.setCurrentText(selected.version)
                    self.comboBox_PackResolution.setCurrentText(selected.res)
                    self.lineEdit_ModpackName.setText(selection_name)

            already = [self.listWidget.item(index).text() for index in range(self.listWidget.count())]

        folder = os.path.join(setting("patches_folder"),
                              self.comboBox_PackVersion.currentText(),
                              self.comboBox_PackResolution.currentText())
        patches = [
            name
            for name in os.listdir(folder)
            if os.path.isdir(os.path.join(folder, name)) and name[0] != "." and name not in (
                "forge", "minecraft", self.temp_folder_name
            )
        ]
        for patch in patches:
            state = Qt.Unchecked
            if selected and patch in selected.patches:
                state = Qt.Checked

            if patch in already:
                item = self.listWidget.findItems(patch, Qt.MatchCaseSensitive)[0]
                item.setCheckState(state)
                self.listWidget.editItem(item)
                continue

            # Create list item
            QListWidgetItem(patch, self.listWidget).setCheckState(state)

        if already:
            self.listWidget.sortItems()

    def pack(self):
        """
        Create the zip pack
        """
        # Get selected patches
        selected = [self.listWidget.item(index).text()
                    for index in range(self.listWidget.count())
                    if self.listWidget.item(index).checkState() == Qt.Checked]

        # Check if data is valid
        invalid = []

        pack_version = self.comboBox_PackVersion.currentText()
        if not pack_version:
            invalid.append('Pack version (Not selected)')

        pack_res = self.comboBox_PackResolution.currentText()
        if not pack_res:
            invalid.append('Pack resolution (Not selected)')

        pack_name = self.lineEdit_ModpackName.text()
        if not pack_name:
            invalid.append('Pack name (Not entered)')
        if not selected:
            invalid.append('Selected patches (anything selected)')

        if invalid:
            ul = ''
            for item in invalid:
                ul += '<li>{}</li>'.format(item)

            QMessageBox.critical(
                self,
                'Invalid data',
                'You have provided invalid options:<br><ul>{}</ul><br>Please fix them to continue'.format(ul)
            )
            return

        # Progress window
        progress = QProgressDialog("Saving selections...", "Abort", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        # noinspection PyUnresolvedReferences
        progress.canceled.connect(lambda: QMessageBox.information(progress, 'Pack building aborted',
                                                                  'Pack building has been aborted successfully'))

        # Save checked for reloading in case of crash
        if not os.path.exists(data('selections')):
            os.mkdir(data('selections'))
        file = open(data(r"selections\{}.json".format(pack_name)), "w")
        file.write(json.dumps({
            'res': pack_res,
            'version': pack_version,
            'patches': selected
        }))
        file.close()
        if self.comboBox_Previous.findText(pack_name, Qt.MatchCaseSensitive) == -1:
            self.comboBox_Previous.addItem(pack_name)

        progress.setValue(25)
        if progress.wasCanceled():
            return

        progress.setLabelText("Copying files to pack... 2/4")

        # Add Minecraft and Forge Directory
        if os.path.exists(os.path.join(setting('patches_folder'), pack_version, pack_res, 'minecraft')):
            selected.append("minecraft")
        if os.path.exists(os.path.join(setting('patches_folder'), pack_version, pack_res, 'forge')):
            selected.append("forge")

        # Create temp folder
        if not os.path.exists(data(self.temp_folder_name)):
            os.mkdir(data(self.temp_folder_name))

        # Find mcmeta pack_format
        pack_version = self.comboBox_PackVersion.currentText()
        for version, number in self.pack_formats.items():
            if pack_version <= version:
                self.pack_mcmeta["pack_format"] = number

        self.pack_mcmeta['description'] = self.pack_mcmeta['description'].format(res=pack_res, name=pack_name,
                                                                                 author=setting('author'))

        # Make mcmeta
        mcmeta = open(data(self.temp_folder_name + "/pack.mcmeta"), "w")
        mcmeta.write(json.dumps({"pack": self.pack_mcmeta}))
        mcmeta.close()

        # Copy pack icon
        file_util.copy_file("resources/img/pack.png", self.temp_folder_name)

        progress.setValue(30)
        if progress.wasCanceled():
            return

        progress_once = len(selected) / 20

        # Copy folders to a temp folder
        for patch in selected:
            dir_util.copy_tree(os.path.join(setting("patches_folder"), pack_version, pack_res, patch),
                               data(self.temp_folder_name + '/assets/' + patch))
            progress.setValue(progress.value() + progress_once)

        progress.setValue(50)
        if progress.wasCanceled():
            return

        progress.setLabelText("Zipping... 3/4")

        # Make zip
        filename = QFileDialog.getSaveFileName(self,
                                               'Save the pack',
                                               os.path.join('[{res}][{version}] Sphax {name} Patch.zip'.format(
                                                   res=pack_res,
                                                   version=pack_version,
                                                   name=pack_name
                                               )), 'ZIP Archives (*.zip)')
        archive = ZipFile(filename[0], 'w', ZIP_DEFLATED, strict_timestamps=False)
        for root, dirs, files in os.walk(data(self.temp_folder_name)):
            for file in files:
                path = os.path.join(root, file)
                archive.write(path, path.replace(data(self.temp_folder_name), ""))
        archive.close()

        # shutil.make_archive('pack', 'zip',  os.path.dirname(os.path.join(os.path.dirname(__file__),
        # temp_folder_name))) ↑↑ Bugged: https://bugs.python.org/issue38288

        progress.setValue(50)
        if progress.wasCanceled():
            return

        progress.setLabelText("Cleaning... 4/4")

        # Delete Temp folder
        shutil.rmtree(self.temp_folder_name)

        progress.setValue(100)
        progress.setLabelText("Done!")

        QMessageBox.information(progress, "Completed", "Pack created")
        progress.destroy()

    def open_info(self):
        """
        Opens the info dialog
        """
        html = open("resources/html/about.html")
        version = open(path('VERSION'))

        QMessageBox.about(self, "About Modpack Sphaxifier", html.read().format(version=version.read().strip()))

        version.close()
        html.close()

    def open_settings(self):
        """
        Settings
        """
        self.settings.show()

    def __stubs(self):
        """ This just enables code completion. It should never be called """
        self.MainWindow = QtWidgets.QMainWindow()
        self.centralwidget = QtWidgets.QWidget()
        self.listWidget = QtWidgets.QListWidget()
        self.comboBox_PackVersion = QtWidgets.QComboBox()
        self.label = QtWidgets.QLabel()
        self.label_4 = QtWidgets.QLabel()
        self.label_5 = QtWidgets.QLabel()
        self.pushButton_Start = QtWidgets.QPushButton()
        self.label_2 = QtWidgets.QLabel()
        self.comboBox_PackResolution = QtWidgets.QComboBox()
        self.pushButton_Reload = QtWidgets.QPushButton()
        self.label_3 = QtWidgets.QLabel()
        self.comboBox_Previous = QtWidgets.QComboBox()
        self.label_6 = QtWidgets.QLabel()
        self.lineEdit_ModpackName = QtWidgets.QLineEdit()
        self.menubar = QtWidgets.QMenuBar()
        self.menuFile = QtWidgets.QMenu()
        self.menuEdit = QtWidgets.QMenu()
        self.menuHelp = QtWidgets.QMenu()
        self.statusbar = QtWidgets.QStatusBar()
        self.actionExit = QtWidgets.QAction()
        self.actionSettings = QtWidgets.QAction()
        self.actionCheck_updates = QtWidgets.QAction()
        self.actionSupport = QtWidgets.QAction()
        self.actionAbout_Qt = QtWidgets.QAction()
        self.actionAbout = QtWidgets.QAction()
        raise AssertionError("This should never be called")
