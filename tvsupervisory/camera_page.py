#!/usr/bin/python  
# -*- coding: UTF-8 -*-

"""
author: Jeffrey
date: 2018/7/5
"""

from PyQt5 import QtWidgets, QtMultimediaWidgets
from tvsupervisory.camerawindow import Ui_Video


class CameraPage(QtWidgets.QWidget, Ui_Video):

    def __init__(self):
        super(CameraPage, self).__init__()
        self.setupUi(self)

        self.viewfinder = QtMultimediaWidgets.QCameraViewfinder(self.video_window)
        # self.viewfinder = QtMultimediaWidgets.QCameraViewfinder()
