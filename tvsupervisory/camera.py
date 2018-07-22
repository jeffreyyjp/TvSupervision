#!/usr/bin/python  
# -*- coding: UTF-8 -*-

"""
author: Jeffrey
date: 2018/7/12
"""

from PyQt5 import QtMultimedia
from PyQt5 import QtWidgets
import sys

class CameraDevice(QtMultimedia.QCamera):

    def __init__(self, camera_id):
        super(CameraDevice, self).__init__()
        self.camera_id = bytearray(camera_id, encoding='ascii')

    @staticmethod
    def get_available_devices():
        cameras_info = QtMultimedia.QCameraInfo.availableCameras()
        cameras = []
        for item in cameras_info:
            cameras.append(CameraDevice(item.deviceName()))
        return cameras


    def camera_name(self):
        camera_info = QtMultimedia.QCameraInfo(self)
        print(self)
        return camera_info.description()

    def camera_id(self):
        return self.camera_id

    def is_opened(self):
        pass

    def start(self):
        self.start()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = CameraDevice.get_available_devices()
    print(a)
    for x in a:
        print(x.camera_name())
