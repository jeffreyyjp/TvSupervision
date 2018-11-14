#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/11/1
"""

import time

from PyQt5 import QtCore
from PyQt5 import QtGui

from docs import conf
from tvsupervision import image_proc
from tvsupervision.log_handler import logger as log


class BaseWorker(QtCore.QObject):
    diff_finished = QtCore.pyqtSignal(str, str, str, str, str)
    supervision_finished = QtCore.pyqtSignal()

    def __init__(self):
        super(BaseWorker, self).__init__()
        self.cameras = None
        self.current_cam = None
        self.supervision_count = None
        self.curr_supervision_count = 0
        self.snap_count = 3
        self.snap_interval = 15
        self.image_diff_rate = 0.01
        self.camera_reports = None
        self.summary_report = None
        self.supervision_control = False

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

    @QtCore.pyqtSlot(int, QtGui.QImage)
    def capture_curr(self, id, image):
        self.current_cam.set_current_frame(image)
        self.current_cam.get_image_capture().imageCaptured.disconnect(
            self.capture_curr)

    def diff(self, snap_time):
        standard_image = image_proc.qimage2cv(self.current_cam.standard_img())
        current_image = image_proc.qimage2cv(self.current_cam.current_frame())
        diff_result, diff_percent = image_proc.diff(standard_image,
                                                    current_image,
                                                    self.image_diff_rate)
        diff_percent = str(round(diff_percent, 2)) + '%'
        self.diff_finished.emit(self.current_cam.name(),
                                str(self.curr_supervision_count),
                                str(snap_time),
                                str(diff_result), str(diff_percent))
        log.debug("%s's %s_%s diff result is %s, diff percent is %s" % (
            self.current_cam.name(), self.curr_supervision_count, snap_time,
            diff_result, diff_percent))
        self.save_report(diff_result, diff_percent, snap_time)

    def save_report(self, diff_result, diff_percent, snap_time):
        for camera_report in self.camera_reports:
            if self.current_cam is not camera_report.camera:
                continue
            current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
            camera_report.current_time = current_time
            current_image_name = '%s_%s.%s' % (current_time,
                                               self.curr_supervision_count,
                                               conf.IMG_POSTFIX)
            camera_report.curr_supervision_count = self.curr_supervision_count
            camera_report.snap_time = snap_time
            camera_report.img_src = current_image_name
            camera_report.diff_state = diff_result
            camera_report.diff_percent = diff_percent
            if diff_result:
                camera_report.pass_times += 1

            else:
                camera_report.fail_times += 1
                camera_report.update()
            camera_report.save_current_img()


class CrossWorker(BaseWorker):

    def __init__(self):
        super(CrossWorker, self).__init__()
        self.serial_port = None
        self.off_time = 15
        self.power_on_key = None
        self.power_off_key = None

    @QtCore.pyqtSlot()
    def start_supervision(self):
        while self.curr_supervision_count < self.supervision_count:
            if not self.supervision_control:
                break
            self.curr_supervision_count += 1
            log.debug('Power off and sleep %ss.' % self.off_time)
            self.serial_port.write(self.power_off_key)
            self.thread().sleep(self.off_time)
            log.debug('Power on and start snap.')
            self.serial_port.write(self.power_on_key)
            for i in range(self.snap_count):
                self.thread().sleep(self.snap_interval)
                for cam in self.cameras:
                    if not cam.is_open():
                        continue
                    self.snap_and_diff(cam, i + 1)
        self.summary_report.update()
        self.supervision_finished.emit()


class DirectWorker(BaseWorker):

    def __init__(self):
        super(DirectWorker, self).__init__()
        self.serial_port = None
        self.off_time = 15
        self.power_key = None

    @QtCore.pyqtSlot()
    def start_supervision(self):
        while self.curr_supervision_count < self.supervision_count:
            if not self.supervision_control:
                break
            self.curr_supervision_count += 1
            log.debug('Power off and sleep %ss.' % self.off_time)
            self.serial_port.write(self.power_key)
            self.thread().sleep(self.off_time)
            log.debug('Power on and start snap.')
            self.serial_port.write(self.power_key)
            for i in range(self.snap_count):
                self.thread().sleep(self.snap_interval)
                for cam in self.cameras:
                    if not cam.is_open():
                        continue
                    self.snap_and_diff(cam, i + 1)
        self.summary_report.update()
        self.supervision_finished.emit()


class PowerboxWorker(BaseWorker):

    def __init__(self):
        super(PowerboxWorker, self).__init__()
        self.onoff_interval = 60

    @QtCore.pyqtSlot()
    def start_supervision(self):
        pass
