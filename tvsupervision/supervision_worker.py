#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/11/1
"""

from PyQt5 import QtCore

from tvsupervision import base_worker
from tvsupervision.log_handler import logger as log


class CrossWorker(base_worker.BaseWorker):

    def __init__(self):
        super(CrossWorker, self).__init__()
        self.power_on_key = None
        self.power_off_key = None

    @QtCore.pyqtSlot()
    def start_supervision(self):
        while self.curr_supervision_time < self.supervision_count:
            self.curr_supervision_time += 1
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
                    self.snap_and_diff(cam, i)
        # self.summary_report.update_summary_report()
        self.supervision_finished.emit()


class DirectWorker(base_worker.BaseWorker):

    def __init__(self):
        super(DirectWorker, self).__init__()
        self.power_key = None

    @QtCore.pyqtSlot()
    def start_supervision(self):
        while self.curr_supervision_time < self.supervision_count:
            self.curr_supervision_time += 1
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
                    self.snap_and_diff(cam, i)
        # self.summary_report.update_summary_report()
        self.supervision_finished.emit()
