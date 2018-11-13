#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/8/14
"""

import sys

from PyQt5 import QtWidgets

from tvsupervision.mainwindow import Ui_Form


class Test_UI(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def main():
    """Module's main entrance, """
    app = QtWidgets.QApplication(sys.argv)
    main_window = Test_UI()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
