#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/7/5
"""

from PyQt5 import QtWidgets

from tvsupervision.ui.camerawindow import Ui_Video


class CameraPage(QtWidgets.QWidget, Ui_Video):

    def __init__(self):
        super(CameraPage, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = CameraPage()
    main_window.show()
    sys.exit(app.exec_())
