#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/7/12
"""

# imports
import sys

from PyQt5 import QtMultimedia
from PyQt5 import QtWidgets


def check_camera_availability():
    """
    Check if host machine has any cameras(build-in or usb cameras).

    :return: True for available cameras or False for None
    """
    cameras_info = QtMultimedia.QCameraInfo.availableCameras()
    if len(cameras_info) > 0:
        return True
    return False


def get_cameras():
    """
    Get all cameras connecting to the host machine.

    :return: all available cameras using "Camera" Class's instance
    """
    cameras_info = QtMultimedia.QCameraInfo.availableCameras()
    cameras = []
    for item in cameras_info:
        cameras.append(Camera(QtMultimedia.QCamera(item)))
    return cameras


class Camera(QtMultimedia.QCamera):
    """
    Encapsulation for QCamera's object.

    Using QCamera for it's attributes and extends for simply getting cameras
    attributes.

    Attributes:
        camera: QCamera's instance
    """

    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def name(self):
        camera_info = QtMultimedia.QCameraInfo(self.camera)
        return camera_info.description()

    def id(self):
        camera_info = QtMultimedia.QCameraInfo(self.camera)
        return camera_info.deviceName()

    def is_open(self):
        if self.camera.state() == QtMultimedia.QCamera.ActiveState:
            return True
        return False

    def open(self):
        self.camera.start()

    def close(self):
        self.camera.stop()

    def setViewfinder(self, viewfinder):
        self.camera.setViewfinder(viewfinder)


class CameraViewFinder(object):

    def __init__(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    cameras = Camera.get_cameras()
    for item in cameras:
        print(item.name())
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
