#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/31
"""

from PyQt5 import QtCore

from tvsupervision import base_supervision_worker


class CrossWorker(base_supervision_worker.BaseWorker):
    curr_diff_finished = QtCore.pyqtSignal(str, str, str, str, str)

    def __init__(self):
        super(CrossWorker, self).__init__()
        self.power_on_key = None
        self.power_off_key = None

    @QtCore.pyqtSlot()
    def start_supervision(self):
        while self.curr_supervision_time < self.supervision_count:
            self.curr_supervision_time += 1
            self.serial_port.write(self.power_off_key)
            self.thread().sleep(self.off_time)
            self.serial_port.write(self.power_on_key)
            for i in range(self.snap_count):
                self.thread().sleep(self.snap_interval)
                for cam in self.cameras:
                    if not cam.is_open():
                        continue
                    self.snap_and_diff(cam, i)
