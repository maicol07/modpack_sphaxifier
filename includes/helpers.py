"""
Helper functions
"""

import os.path
from datetime import datetime

import requests
from PySide2.QtCore import QSettings
from PySide2.QtWidgets import QFileDialog, QMessageBox
from dotted_dict import DottedDict

from includes.variables import *


def path(relative: str) -> str:
    """
    Generate an absolute path for the specified relative folder

    :param relative: Relative path to transform to absolute
    :return:
    """
    return os.path.join(ROOT_DIR, relative)


def data(uri='') -> str:
    """
    Returns the folder where all the user data is stored

    :param uri:
    :type uri str

    :return: User data path
    :rtype: str
    """
    return os.path.join(os.getenv('APPDATA'), r'Maicol07\Modpack Sphaxifier', uri)


settings = QSettings()


def setting(key: str, default=None):
    """
    Return a setting, given the key

    :param default:
    :param key:
    :return:
    """
    return settings.value(key, default)


def pick(parent, line_edit=None, starting_dir='', directory=False):
    """
    Pick a file or a directory

    :param parent:
    :param starting_dir:
    :param line_edit:
    :type line_edit QLineEdit
    :param directory:
    """
    if directory:
        picked = QFileDialog.getExistingDirectory(parent, 'Pick a directory', starting_dir or line_edit.text())
    else:
        picked = QFileDialog.getOpenFileName(parent, 'Pick a file', starting_dir or line_edit.text(),
                                             QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
    if line_edit:
        line_edit.setText(picked)


def verify_license(license_key, status_label=None, parent=None):
    """
    Verify license

    :param parent:
    :param status_label:
    :type license_key str
    """
    r = requests.post('https://maicol07.it/license_server/verify.php', {
        'sub_id': license_key,
        'uuid': setting('uuid')
    })
    response = DottedDict(r.json())
    if response.success:
        date_time = datetime.fromtimestamp(response.expiry_date)
        if status_label:
            status_label.setText('''
            <html>
                <head/>
                <body style="color: {color};">
                    <p>Current status: License {}added!</p>
                    <ul>
                        <li>Status: {}</li>
                        <li>Expiry date: {}</li>
                    </ul>
                </body>
            </html>'''.format('not ' if response.status not in ('ACTIVE', 'FULL') else '',
                              response.status,
                              date_time.strftime("%m/%d/%Y, %H:%M:%S"),
                              color='#00aa00' if response.status == 'ACTIVE' else '#ffaa00'))
        if response.status in ('ACTIVE', 'FULL'):
            LICENSED = True
        else:
            LICENSED = False
        settings.setValue('uuid', response.uuid)
    else:
        QMessageBox.critical(parent, 'Error while verifying your license', response.error)
        status_label.setText('''
        <html>
            <head/>
            <body style="color:#ff0000;">
                <p>Current status: No license! Will be activated a free demo with a limit</p>
                <p>of 10 mods</p>
            </body>
        </html>''')
        LICENSED = False
    settings.setValue('license_key', license_key)
    return LICENSED
