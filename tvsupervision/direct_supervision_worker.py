#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/31
"""

from PyQt5 import QtCore

from tvsupervision import base_supervision_worker


class DirectWorker(base_supervision_worker.BaseWorker):

    def __init__(self):
        super(DirectWorker, self).__init__()
        self.power_key = None

    @QtCore.pyqtSlot()
    def start_supervision(self):
        while self.curr_supervision_time < self.supervision_count:
            self.curr_supervision_time += 1
            self.serial_port.write(self.power_key)
            self.thread().sleep(self.off_time)
            self.serial_port.write(self.power_key)
            for i in range(self.snap_count):
                self.thread().sleep(self.snap_interval)
                for cam in self.cameras:
                    if not cam.is_open():
                        continue
                    self.snap_and_diff(cam, i)
