#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/5/14
"""

# imports
import sys

import serial
from PyQt5 import QtCore
from PyQt5 import QtMultimediaWidgets
from PyQt5 import QtWidgets

from tvsupervision import camera_handler
from tvsupervision import comport_handler
from tvsupervision import mainwindow


class MainWindow(QtWidgets.QWidget, mainwindow.Ui_Form):
    """
    Setup window
    """

    def __init__(self):

        self.serial_port = serial.Serial()
        self.cameras = camera_handler.Camera.get_cameras()

        super(MainWindow, self).__init__()
        self.setupUi(self)

        # self.setMinimumSize(400, 300)

        # All connections between signals and slots are defined here.
        self.refreshcamera_pushbutton.clicked.connect(self.refresh_camera_table)
        self.opencamera_pushbutton.clicked.connect(self.open_camera)
        self.capturestd_pushbutton.clicked.connect(self.capture_std)
        self.refreshcomport_pushbutton.clicked.connect(self.refresh_port)
        self.opencomport_pushbutton.clicked.connect(self.open_port)
        self.resultdir_pushbutton.clicked.connect(self.choose_resultdir)
        self.start_supervision_pushbutton.clicked.connect(
            self.start_supervision)
        self.look_result_pushbutton.clicked.connect(self.look_result)

        self.init_data()

    def eventFilter(self, obj, event):
        if obj == self.viewfinder:
            if event.type() == QtCore.QEvent.Close:
                print('hello123')
                return True
            else:
                return False
        else:
            # pass the event on to the parent class.
            return MainWindow.eventFilter(self, obj, event)

    def init_data(self):
        """Initialize main window.

        Get camera, comport, and test result dir info.
        """

        if camera_handler.check_camera_availability():
            self.refresh_camera_table()
        self.refresh_port()
        # TODO

    def refresh_camera_table(self):
        self.cameratable_tablewidget.clearContents()
        if not camera_handler.check_camera_availability():
            QtWidgets.QMessageBox.information(self, '提示', "无可用摄像头")
            return

        self.cameratable_tablewidget.setRowCount(
            camera_handler.get_camera_count())
        for i, cam in enumerate(self.cameras):
            tag = QtWidgets.QTableWidgetItem('camera%s' % i)
            camera_name = QtWidgets.QTableWidgetItem(cam.name())
            camera_id = QtWidgets.QTableWidgetItem(cam.id())
            self.cameratable_tablewidget.setItem(i, 0, tag)
            self.cameratable_tablewidget.setItem(i, 1, camera_name)
            self.cameratable_tablewidget.setItem(i, 2, camera_id)

    def open_camera(self):
        if self.cameratable_tablewidget.rowCount() == 0:
            QtWidgets.QMessageBox.information(self, '提示', "无可用摄像头")
            return

        selected_row = self.cameratable_tablewidget.currentRow()
        if selected_row == -1:
            selected_row = 0
        selected_camera_tag = self.cameratable_tablewidget.item(selected_row,
                                                                0).text()
        selected_camera_id = self.cameratable_tablewidget.item(selected_row,
                                                               2).text()
        for cam in self.cameras:
            if selected_camera_id == cam.id():
                if cam.is_open():
                    QtWidgets.QMessageBox.information(self, '提示', '%s已打开' %
                                                      selected_camera_tag)
                    return

                self.viewfinder = QtMultimediaWidgets.QCameraViewfinder()
                self.viewfinder.setWindowTitle(selected_camera_tag)
                # self.viewfinder.setObjectName()
                # self.viewfinder.installEventFilter(self)
                self.viewfinder.show()
                cam.setViewfinder(self.viewfinder)
                cam.open()

    def capture_std(self):
        if self.camera_tab.count() == 0:
            QtWidgets.QMessageBox.information(self, '提示 ', '')
            return
        current_camera_tag = self.camera_tab.tabText(
            self.camera_tab.currentIndex())
        print(current_camera_tag)
        # current_camera_id = self.camera_table.fin

    def refresh_port(self):
        self.comport_combobox.clear()
        self.comport_combobox.addItems(comport_handler.get_comports_name())

    def open_port(self):
        port_name = self.comport_combobox.currentText()
        if port_name == '':
            QtWidgets.QMessageBox.information(self, '提示', '无效的串口名')
            return

        self.serial_port.port = port_name  # configure initialized port
        if self.opencomport_pushbutton.text() == '关闭COM':
            self.serial_port.close()
            QtWidgets.QMessageBox.information(self, '提示', '成功关闭{}'.format(
                port_name))
            self.opencomport_pushbutton.setText('打开COM')
            self.refreshcomport_pushbutton.setEnabled(True)
            self.comport_combobox.setEnabled(True)
        else:
            try:
                self.serial_port.open()
                QtWidgets.QMessageBox.information(self, '提示', '成功打开{}'.format(
                    port_name))
                self.opencomport_pushbutton.setText('关闭COM')
                self.refreshcomport_pushbutton.setEnabled(False)
                self.comport_combobox.setEnabled(False)
            except serial.SerialException as e:
                QtWidgets.QMessageBox.information(self, '提示',
                                                  str(e))

    def choose_resultdir(self):
        pass

    def start_supervision(self):
        if not self.check_conditions():
            return
        else:
            pass

    def look_result(self):
        pass

    def check_conditions(self):
        """Check preconditions is ready.

        Check:
            1. Camera is open.
            2. Comport is open.
            3. Test result dir is valid.
            4. Any config parm is ready for use.
            ...

        :return: bool
        """
        pass


def main():
    """Module's main entrance, executed when not as imported."""

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
