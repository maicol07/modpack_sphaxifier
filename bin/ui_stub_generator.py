from __future__ import print_function

import os
import sys
import xml.etree.ElementTree


def generate_stubs(file):
    """
    Stub generator

    :param file:
    """
    root = xml.etree.ElementTree.parse(file).getroot()
    print('Stub for file: ' + os.path.basename(file))
    print()
    print('    def __stubs(self):')
    print('        """ This just enables code completion. It should never be called """')

    for widget in root.findall('.//widget'):
        name = widget.get('name')
        cls = widget.get('class')
        try:
            imp = __import__('PySide2.QtWidgets', fromlist=cls)
            getattr(imp, cls)
            group = 'QtWidgets'
        except AttributeError:
            group = 'QtCore'
        print('        self.{} = {}.{}()'.format(
            name, group, cls
        ))
    for action in root.findall('.//addaction'):
        name = action.get('name')
        if 'menu' in name:
            continue
        cls = 'QAction'
        print('        self.{} = QtWidgets.{}()'.format(
            name, cls
        ))

    print('        raise AssertionError("This should never be called")')
    print()


if __name__ == '__main__':
    for file in sys.argv[1:]:
        generate_stubs(file)
