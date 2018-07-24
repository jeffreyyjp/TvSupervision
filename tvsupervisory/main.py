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
from tvsupervisory.camera_page import CameraPage

ser = serial.Serial()


class MainWindow(QtWidgets.QWidget, Ui_Form):
    """
    Setup window
    """

    def __init__(self):
        """Constructor
        """

        self.cameras = []
        self.cameras_info = QtMultimedia.QCameraInfo.availableCameras()

        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.refresh_camera_table_btn.clicked.connect(self.refresh_camera_table)
        self.add_camera_btn.clicked.connect(self.add_camera)
        self.capture_std_btn.clicked.connect(self.capture_std)
        self.refresh_port_btn.clicked.connect(self.refresh_port)
        self.open_port_btn.clicked.connect(self.open_port)
        self.start_supervision_btn.clicked.connect(self.start_supervision)

        self.init_data()

    def init_data(self):
        if self.check_camera_availability():
            self.refresh_camera_table()
        self.refresh_port()
        # TODO

    def check_camera_availability(self):
        if len(self.cameras_info) > 0:
            return True
        return False

    def refresh_camera_table(self):
        self.camera_table.clearContents()
        if len(self.cameras_info) == 0:
            QtWidgets.QMessageBox.information(self, 'Camera Info', "Can't find any camera device")
            return

        self.camera_table.setRowCount(len(self.cameras_info))
        for i, item in enumerate(self.cameras_info):
            tag = QtWidgets.QTableWidgetItem('camera%s' % i)
            camera_name = QtWidgets.QTableWidgetItem(item.description())
            camera_id = QtWidgets.QTableWidgetItem(item.deviceName())
            self.camera_table.setItem(i, 0, tag)
            self.camera_table.setItem(i, 1, camera_name)
            self.camera_table.setItem(i, 2, camera_id)
            self.camera_table.hideColumn(2)
            self.cameras.append(QtMultimedia.QCamera(item))

    def add_camera(self):
        if self.camera_table.rowCount() == 0:
            QtWidgets.QMessageBox.information(self, 'Camera Info', "Can't find any camera device")
            return

        selected_row = self.camera_table.currentRow()
        selected_camera_tag = self.camera_table.item(selected_row, 0).text()
        selected_camera_id = self.camera_table.item(selected_row, 2).text()
        for item_camera in self.cameras:
            if selected_camera_id == QtMultimedia.QCameraInfo(item_camera).deviceName():
                if item_camera.state() == QtMultimedia.QCamera.ActiveState:
                    QtWidgets.QMessageBox.information(self, 'Camera Info', 'Camera is already opened')
                    return
                camera_page = CameraPage()
                self.camera_tab.addTab(camera_page, selected_camera_tag)
                viewfinder = QtMultimediaWidgets.QCameraViewfinder(camera_page.video_window)
                item_camera.setViewfinder(viewfinder)
                # item_camera.setViewfinder(camera_page.viewfinder)
                item_camera.start()

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
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
