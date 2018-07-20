#!/usr/bin/python  
# -*- coding: UTF-8 -*-

"""
author: Jeffrey
date: 2018/5/14
"""

import sys
import serial
import serial.tools.list_ports as list_ports
from PyQt5 import QtWidgets, QtMultimedia, QtMultimediaWidgets
from tvsupervisory.mainwindow import Ui_Form
from tvsupervisory.camera_page import Camera_Page

ser = serial.Serial()
camera_list = []


class MainWindow(QtWidgets.QWidget, Ui_Form):
    """
    Setup window
    """

    def __init__(self):
        """Constructor
        """

        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.refresh_camera_list_btn.clicked.connect(self.refresh_camera_list)
        self.add_camera_btn.clicked.connect(self.add_camera)
        self.capture_std_btn.clicked.connect(self.capture_std)
        self.refresh_port_btn.clicked.connect(self.refresh_port)
        self.open_port_btn.clicked.connect(self.open_port)
        self.start_supervision_btn.clicked.connect(self.start_supervision)

        self.init_data()

    def init_data(self):
        self.refresh_camera_list()
        # TODO

    def refresh_camera_list(self):
        self.camera_list.clearContents()
        cameras = QtMultimedia.QCameraInfo.availableCameras()
        if len(cameras) == 0:
            QtWidgets.QMessageBox.information(self, 'Camera Info', "Can't find any camera device")
            return

        self.camera_list.setRowCount(len(cameras))
        for i, item in enumerate(cameras):
            id = QtWidgets.QTableWidgetItem('camera%s' % i)
            name = QtWidgets.QTableWidgetItem(item.description())
            self.camera_list.setItem(i, 0, id)
            self.camera_list.setItem(i, 1, name)

    def add_camera(self):
        if self.camera_list.rowCount() == 0:
            QtWidgets.QMessageBox.information(self, 'Camera Info', "Can't find any camera device")
            return

        cameras = QtMultimedia.QCameraInfo.availableCameras()
        selected_row = self.camera_list.currentRow()
        for item in cameras:
            if self.camera_list.item(selected_row, 1).text() == item.description():
                camera_page = Camera_Page()
                self.camera_tab.addTab(camera_page, self.camera_list.item(selected_row, 0).text())
                self.camera = QtMultimedia.QCamera(item)
                self.viewfinder = QtMultimediaWidgets.QCameraViewfinder(camera_page.video_widget)
                self.camera.setViewfinder(self.viewfinder)
                self.camera.start()

    def capture_std(self):
        pass

    def refresh_port(self):
        self.port_lists_combox.clear()
        com_list = list_ports.comports()
        port_name_list = []
        for port_item in com_list:
            port_name_list.append(port_item[0])
        self.port_lists_combox.addItems(sorted(port_name_list))

    def open_port(self):
        port_name = self.port_lists_combox.currentText()
        if port_name == '':
            QtWidgets.QMessageBox.information(self, 'Invalid Port Name', 'Current selected port name is none')
            return

        ser.port = port_name
        if self.open_port_btn.text() == '关闭COM':
            ser.close()
            QtWidgets.QMessageBox.information(self, 'Close Com Port', '{} has been closed successful'.format(port_name))
            self.open_port_btn.setText('打开COM')
            self.refresh_port_btn.setEnabled(True)
            self.port_lists_combox.setEnabled(True)
        else:
            try:
                ser.open()
                QtWidgets.QMessageBox.information(self, 'Open Successful',
                                                  '{} has been opened successful'.format(port_name))
                self.open_port_btn.setText('关闭COM')
                self.refresh_port_btn.setEnabled(False)
                self.port_lists_combox.setEnabled(False)
            except serial.SerialException as e:
                QtWidgets.QMessageBox.information(self, 'Open Fail', e.__str__())

    def start_supervision(self):
        abc = Camera_Page()
        abc.show()
        self.camera_tab.addTab(abc, 'hello')


def run():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
