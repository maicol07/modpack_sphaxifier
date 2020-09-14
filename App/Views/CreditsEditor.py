"""
Credits Editor Controller
"""

import json
import os

from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QTableWidgetItem

from App.Views.Window import get_window
from includes.helpers import data

Dialog = get_window('dialog')


class CreditsEditor(Dialog):
    """
    Settings Controller
    """

    def __init__(self):
        super().__init__('credits_editor')
        self.app = QApplication.instance()

        # Load credits
        if os.path.exists(data('credits.json')):
            file = open(data('credits.json'))
            cred = json.loads(file.read())
            for slug, text in cred.items():
                idx = list(cred.keys()).index(slug)
                self.tableWidget.insertRow(idx)
                self.tableWidget.setItem(idx, 0, QTableWidgetItem(slug))
                self.tableWidget.setItem(idx, 1, QTableWidgetItem(text))
            file.close()

        self.pushButton_Add.clicked.connect(lambda: self.tableWidget.insertRow(self.tableWidget.rowCount()))
        self.pushButton_Remove.clicked.connect(self.remove_rows)

        self.buttonBox.accepted.connect(self.save_credits)

    def remove_rows(self):
        """
        Remove selected table rows
        """
        for i in self.tableWidget.selectedIndexes():
            self.tableWidget.removeRow(i.row())

    def save_credits(self):
        """
        Save credits
        """
        cred = {}
        for row in range(self.tableWidget.rowCount()):
            try:
                cred[self.tableWidget.item(row, 0).text()] = self.tableWidget.item(row, 1).text() or ''
            except AttributeError:
                pass

        file = open(data('credits.json'), 'w')
        file.write(json.dumps(cred))
        file.close()

    def __stubs(self):
        """ This just enables code completion. It should never be called """
        self.Dialog = QtWidgets.QDialog()
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.tableWidget = QtWidgets.QTableWidget()
        self.pushButton_Add = QtWidgets.QPushButton()
        self.pushButton_Remove = QtWidgets.QPushButton()
        raise AssertionError("This should never be called")
