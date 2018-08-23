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
    cameras_info = QtMultimedia.QCameraInfo.availableCameras()
    if len(cameras_info) > 0:
        return True
    return False


def get_camera_count():
    return len(QtMultimedia.QCameraInfo.availableCameras())


def get_all_cameras():
    cameras_info = QtMultimedia.QCameraInfo.availableCameras()
    cameras = []
    for item in cameras_info:
        cameras.append(QtMultimedia.QCamera(item))
    return cameras


def get_camera_name(camera):
    return QtMultimedia.QCameraInfo(camera).deviceName()


def get_camera_description(camera):
    return QtMultimedia.QCameraInfo(camera).description()


def is_open(camera):
    if camera.state() == QtMultimedia.QCamera.ActiveState:
        return True
    return False


class Camera(QtMultimedia.QCamera):

    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    @staticmethod
    def get_cameras():
        cameras_info = QtMultimedia.QCameraInfo.availableCameras()
        cameras = []
        for item in cameras_info:
            cameras.append(Camera(QtMultimedia.QCamera(item)))
        return cameras

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

    def setViewfinder(self, viewfinder):
        self.camera.setViewfinder(viewfinder)


def main():
    app = QtWidgets.QApplication(sys.argv)
    cameras = Camera.get_cameras()
    for item in cameras:
        print(item.name())
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
