#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/5/14
"""

# imports
import serial
import sys

from PyQt5 import QtWidgets
from PyQt5 import QtMultimedia
from PyQt5 import QtMultimediaWidgets

# from PyQt5 import QtMultimediaWidgets

from tvsupervisory import camera_handler
from tvsupervisory import camera_window
from tvsupervisory import comport_handler
from tvsupervisory.ui import mainwindow


class MainWindow(QtWidgets.QWidget, mainwindow.Ui_Form):
    """
    Setup window
    """

    def __init__(self):

        self.serial_port = serial.Serial()
        self.cameras = camera_handler.get_all_cameras()

        super(MainWindow, self).__init__()
        self.setupUi(self)

        # self.setMinimumSize(400, 300)

        self.refresh_camera_table_btn.clicked.connect(self.refresh_camera_table)
        self.add_camera_btn.clicked.connect(self.add_camera)
        self.capture_std_btn.clicked.connect(self.capture_std)
        self.refresh_port_btn.clicked.connect(self.refresh_port)
        self.open_port_btn.clicked.connect(self.open_port)
        self.start_supervision_btn.clicked.connect(self.start_supervision)

        self.init_data()

    def init_data(self):
        """Initialize main window.

        Get camera, comport, and test result dir info.
        """

        if camera_handler.check_camera_availability():
            self.refresh_camera_table()
        self.refresh_port()
        # TODO

    def refresh_camera_table(self):
        self.camera_table.clearContents()
        if not camera_handler.check_camera_availability():
            QtWidgets.QMessageBox.information(self, 'Camera Info',
                                              "Can't find any camera device")
            return

        self.camera_table.setRowCount(camera_handler.get_camera_count())
        for i, cam in enumerate(self.cameras):
            tag = QtWidgets.QTableWidgetItem('camera%s' % i)
            camera_name = QtWidgets.QTableWidgetItem(
                camera_handler.get_camera_description(cam))
            camera_id = QtWidgets.QTableWidgetItem(
                camera_handler.get_camera_name(cam))
            self.camera_table.setItem(i, 0, tag)
            self.camera_table.setItem(i, 1, camera_name)
            self.camera_table.setItem(i, 2, camera_id)
            self.camera_table.hideColumn(2)

    def add_camera(self):
        if self.camera_table.rowCount() == 0:
            QtWidgets.QMessageBox.information(self, 'Camera Info',
                                              "Can't find any camera device")
            return

        # if self.camera_table.is

        selected_row = self.camera_table.currentRow()
        if selected_row == -1:
            selected_row = 0
        selected_camera_tag = self.camera_table.item(selected_row, 0).text()
        selected_camera_id = self.camera_table.item(selected_row, 2).text()

        for cam in self.cameras:
            if selected_camera_id == camera_handler.get_camera_name(cam):
                if cam.state() == QtMultimedia.QCamera.ActiveState:
                    QtWidgets.QMessageBox.information(self, 'Camera Info',
                                                      '%s is already opened'
                                                      % selected_camera_tag)
                    return

                camera_page = camera_window.CameraPage()
                self.camera_tab.addTab(camera_page, selected_camera_tag)
                self.viewfinder = QtMultimediaWidgets.QCameraViewfinder()
                self.viewfinder.show()
                cam.setViewfinder(self.viewfinder)
                cam.start()

    def capture_std(self):
        if self.camera_tab.count() == 0:
            QtWidgets.QMessageBox.information(self, 'Camera Info',
                                              'Please open camera device')
            return
        current_camera_tag = self.camera_tab.tabText(
            self.camera_tab.currentIndex())
        print(current_camera_tag)
        # current_camera_id = self.camera_table.fin

    def refresh_port(self):
        self.port_lists_combox.clear()
        self.port_lists_combox.addItems(comport_handler.get_comports_name())

    def open_port(self):
        port_name = self.port_lists_combox.currentText()
        if port_name == '':
            QtWidgets.QMessageBox.information(self, 'Invalid Port Name',
                                              'Current selected port name is '
                                              'none')
            return

        self.serial_port.port = port_name  # configure initialized port
        if self.open_port_btn.text() == '关闭COM':
            self.serial_port.close()
            QtWidgets.QMessageBox.information(self, 'Close Com Port',
                                              '{} has been closed '
                                              'successful'.format(
                                                  port_name))
            self.open_port_btn.setText('打开COM')
            self.refresh_port_btn.setEnabled(True)
            self.port_lists_combox.setEnabled(True)
        else:
            try:
                self.serial_port.open()
                QtWidgets.QMessageBox.information(self, 'Open Successful',
                                                  '{} has been opened '
                                                  'successful'.format(
                                                      port_name))
                self.open_port_btn.setText('关闭COM')
                self.refresh_port_btn.setEnabled(False)
                self.port_lists_combox.setEnabled(False)
            except serial.SerialException as e:
                QtWidgets.QMessageBox.information(self, 'Open Fail',
                                                  str(e))

    def start_supervision(self):
        if not self.check_conditions():
            return
        else:
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
    """Module's main entrance, """
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
