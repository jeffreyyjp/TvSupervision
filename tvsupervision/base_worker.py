#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/31
"""

import time

from PyQt5 import QtCore

from docs import conf
from tvsupervision import image_proc
from tvsupervision.log_handler import logger as log


class BaseWorker(QtCore.QObject):
    diff_finished = QtCore.pyqtSignal(str, str, str, str, str)
    supervision_finished = QtCore.pyqtSignal()

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
        self.camera_reports = None
        self.summary_report = None

    def snap_and_diff(self, cam, snap_time):
        event_loop = QtCore.QEventLoop()
        self.current_cam = cam
        if cam.get_image_capture().isReadyForCapture():
            cam.get_image_capture().imageCaptured.connect(self.capture_curr)
            cam.get_image_capture().imageCaptured.connect(event_loop.quit)
            log.debug('Snap current image.')
            cam.capture()
            event_loop.exec()
        self.diff(snap_time)

    # @QtCore.pyqtSlot(int, QtGui.QImage)
    def capture_curr(self, id, image):
        self.current_cam.set_current_frame(image)
        self.current_cam.get_image_capture().imageCaptured.disconnect(
            self.capture_curr)

    def diff(self, snap_time):
        standard_image = image_proc.qimage2cv(self.current_cam.standard_img())
        current_image = image_proc.qimage2cv(self.current_cam.current_frame())
        diff_result, diff_percent = image_proc.diff(standard_image,
                                                    current_image)
        self.diff_finished.emit(self.current_cam.name(),
                                     str(self.curr_supervision_time),
                                     str(snap_time),
                                     str(diff_result), str(diff_percent))
        log.debug("%s's %s_%s diff result is %s, diff percent is %s" % (
            self.current_cam.name(), self.curr_supervision_time, snap_time,
            diff_result, diff_percent))
        self.save_report(diff_result, diff_percent, snap_time)

    def save_report(self, diff_result, diff_percent, snap_time):
        for camera_report in self.camera_reports:
            if self.current_cam is not camera_report.camera:
                continue
            current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
            camera_report.current_time = current_time
            current_image_name = '%s_%s.%s' % (current_time, snap_time,
                                               conf.IMG_POSTFIX)
            camera_report.curr_supervision_time = self.curr_supervision_time
            camera_report.snap_time = snap_time
            camera_report.img_src = current_image_name
            camera_report.diff_state = diff_result
            camera_report.diff_percent = diff_percent
            if not diff_result:
                camera_report.fail_times += 1
                camera_report.update()
            camera_report.pass_times += 1
            camera_report.save_current_img()
