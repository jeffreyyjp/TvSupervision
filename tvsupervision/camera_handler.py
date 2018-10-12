#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/7/12
"""

# imports
import os
import sys

from PyQt5 import QtMultimedia
from PyQt5 import QtMultimediaWidgets
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
    cameras = [Camera(QtMultimedia.QCamera(item)) for item in cameras_info]
    return cameras


class Camera(object):
    """
    Encapsulation for QCamera's object.

    Using QCamera for it's attributes and extends for simply getting cameras
    attributes.

    Attributes:
        camera: QCamera's instance
    """

    def __init__(self, camera):
        super().__init__()
        self._camera = camera
        self._camera_viewfinder = QtMultimediaWidgets.QCameraViewfinder()
        self._camera.setCaptureMode(QtMultimedia.QCamera.CaptureStillImage)
        self._image_capture = QtMultimedia.QCameraImageCapture(self._camera)
        self._image_capture.setCaptureDestination(
            QtMultimedia.QCameraImageCapture.CaptureToFile)
        self._tag = None
        self._standard_img = None
        self._current_frame = None
        self._result_dir = None

    def set_tag(self, tag):
        self._tag = tag

    def tag(self):
        return self._tag

    def name(self):
        camera_info = QtMultimedia.QCameraInfo(self._camera)
        return camera_info.description()

    def id(self):
        camera_info = QtMultimedia.QCameraInfo(self._camera)
        return camera_info.deviceName()

    def is_open(self):
        return self._camera.state() == QtMultimedia.QCamera.ActiveState

    def open(self):
        self._camera.start()

    def close(self):
        self._camera.stop()

    def capture(self):
        self._image_capture.capture()

    def show_camera_window(self):
        self._camera_viewfinder.show()
        self._camera.setViewfinder(self._camera_viewfinder)

    def get_image_capture(self):
        return self._image_capture

    def get_viewfinder(self):
        return self._camera_viewfinder

    def set_standard_img(self, image):
        self._standard_img = image

    def standard_img(self):
        return self._standard_img

    def set_current_frame(self, image):
        self._current_frame = image

    def current_frame(self):
        return self._current_frame

    def set_result_dir(self, basedir):
        cam_folder_name = '_'.join([self.tag(), self.name()])
        self._result_dir = os.path.join(basedir, cam_folder_name)

    def result_dir(self):
        return self._result_dir

def main():
    app = QtWidgets.QApplication(sys.argv)
    cameras = get_cameras()
    for item in cameras:
        print(item.name())
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
