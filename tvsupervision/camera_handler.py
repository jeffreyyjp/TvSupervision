#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/7/12
"""

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


# class CameraDevice(QtMultimedia.QCamera):
#
#     def __init__(self, camera_id):
#         super(CameraDevice, self).__init__()
#         self.camera_id = bytearray(camera_id, encoding='ascii')
#
#     @staticmethod
#     def get_available_devices():
#         cameras_info = QtMultimedia.QCameraInfo.availableCameras()
#         cameras = []
#         for item in cameras_info:
#             cameras.append(CameraDevice(item.deviceName()))
#         return cameras
#
#     def camera_name(self):
#         camera_info = QtMultimedia.QCameraInfo(self)
#         print(self)
#         return camera_info.description()
#
#     def camera_id(self):
#         return self.camera_id
#
#     def is_opened(self):
#         pass
#
#     def start(self):
#         self.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # print(get_camera_count())
    cameras = get_all_cameras()
    for item in cameras:
        print(get_camera_description(item))
