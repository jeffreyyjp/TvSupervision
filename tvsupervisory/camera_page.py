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

        self.viewfinder = QtMultimediaWidgets.QCameraViewfinder()
        # self.video_size = self.video_window.size()
        # self.viewfinder.setSizePolicy(self.video_size.width(), self.video_size.height())
        self.video_layout = QtWidgets.QGridLayout(self.video_window)
        self.video_window.setLayout(QtWidgets.QHBoxLayout(self))
        self.video_layout.addWidget(self.viewfinder)
