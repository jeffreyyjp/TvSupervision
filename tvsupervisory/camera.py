#!/usr/bin/python  
# -*- coding: UTF-8 -*-

"""
author: Jeffrey
date: 2018/7/12
"""

from PyQt5.QtMultimedia import QCamera, QCameraInfo
from PyQt5.QtGui import QGuiApplication
import sys

class CameraDevice(QCamera):

    def __init__(self, id, name):
        super(CameraDevice, self).__init__()
        self.device_id = id
        self.device_name = name


    @staticmethod
    def get_available_devices():
        cameras_info = QCameraInfo.availableCameras()
        cameras = []
        for item in cameras_info:
            cameras.append(CameraDevice(item.deviceName(), item.description()))
        return cameras


    def camera_name(self):
        return self.device_name

    def camera_id(self):
        return self.device_id

    def is_opened(self):
        pass

    def start(self):
        super().start()

app = QGuiApplication(sys.argv)

a = CameraDevice.get_available_devices()
for x in a:
    print(x.camera_name(), x.camera_id())
