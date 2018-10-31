#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/31
"""

from PyQt5 import QtCore

from tvsupervision import image_proc


class BaseWorker(QtCore.QObject):
    curr_diff_finished = QtCore.pyqtSignal(str, str, str, str, str)

    def __init__(self):
        super(BaseWorker, self).__init__()
        self.cameras = None
        self.serial_port = None
        self.current_cam = None
        self.supervision_count = None
        self.curr_supervision_time = 0
        self.off_time = 15
        self.snap_count = 3
        self.snap_interval = 15

    def snap_and_diff(self, cam, snap_time):
        event_loop = QtCore.QEventLoop()
        self.current_cam = cam
        if cam.get_image_capture().isReadyForCapture():
            cam.get_image_capture().imageCaptured.connect(self.capture_curr)
            cam.get_image_capture().imageCaptured.connect(event_loop.quit)
            cam.capture()
            event_loop.exec()
        self.diff(snap_time)

    # @QtCore.pyqtSlot(int, QtGui.QImage)
    def capture_curr(self, id, image):
        print('debug')
        self.current_cam.set_current_frame(image)
        self.current_cam.get_image_capture().imageCaptured.disconnect(
            self.capture_curr)

    def diff(self, snap_time):
        standard_image = image_proc.qimage2cv(
            self.current_cam.standard_img())
        current_image = image_proc.qimage2cv(
            self.current_cam.current_frame())
        diff_result, diff_percent = image_proc.diff(standard_image,
                                                    current_image)
        print(diff_result)
        self.curr_diff_finished.emit(self.current_cam.name(),
                                     str(self.curr_supervision_time),
                                     str(snap_time),
                                     str(diff_result), str(diff_percent))
