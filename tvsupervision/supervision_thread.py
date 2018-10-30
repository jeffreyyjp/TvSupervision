#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/30
"""

from PyQt5 import QtCore


class SupervisionThread(QtCore.QThread):

    def __init__(self):
        super().__init__()
        self.current_finished = QtCore.pyqtSignal()

    def run(self):
        pass

    @QtCore.pyqtSlot()
    def capture_curr(self):
        pass
