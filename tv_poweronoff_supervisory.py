#!/usr/bin/env python
# encoding: utf-8

'''
author: Jeffrey
date: 2018/4/10
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraInfo
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from mainwindow import Ui_Form



class MainWindow(QWidget, Ui_Form):
    '''
    Setup window
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(MainWindow, self).__init__()
        self.setupUi(self)

        camera = QCamera(self)
        viewfinder = QCameraViewfinder(self)

        camera.setViewfinder(viewfinder)
        imagecapture = QCameraImageCapture(camera)

        self.imageview.addWidget(viewfinder)
        self.imagecapture.setScaledContents(True)

        camera.start()

        camerinfo = QCameraInfo(camera)
        print(camerinfo.deviceName())

        print(camera.status())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())