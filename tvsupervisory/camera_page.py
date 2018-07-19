#!/usr/bin/python  
# -*- coding: UTF-8 -*-

"""
author: Jeffrey
date: 2018/7/5
"""

from PyQt5.QtWidgets import QWidget
from tvsupervisory.camerawindow import Ui_Video

class Camera_Page(QWidget, Ui_Video):

    def __init__(self):
        super(Camera_Page, self).__init__()
        self.setupUi(self)
