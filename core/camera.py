#!/usr/bin/python  
# -*- coding: UTF-8 -*-

"""
author: Jeffrey
date: 2018/7/12
"""

from PyQt5.QtMultimedia import QCamera, QCameraInfo

class CameraDevice(QCamera):

    def __init__(self):
        super(CameraDevice, self).__init__()


    @staticmethod
    def get_available_devices():
        cameras = QCameraInfo.availableCameras()


    def camera_flag(self):
        pass

    def camera_name(self):
        pass

    def camera_id(self):
        pass

    def is_opened(self):
        pass

    def start(self):
        super().start()
