#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/5/14
"""

# imports
import os
import sys

import serial
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtMultimediaWidgets
from PyQt5 import QtWidgets

from docs import conf
from tvsupervision import camera_handler
from tvsupervision import comport_handler
from tvsupervision import mainwindow

information = QtWidgets.QMessageBox.information
warning = QtWidgets.QMessageBox.warning
critical = QtWidgets.QMessageBox.critical


class MainWindow(QtWidgets.QWidget, mainwindow.Ui_Form):
    """
    Setup window
    """

    def __init__(self):

        self.serial_port = serial.Serial()
        self.cameras = camera_handler.get_cameras()

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

    def init_data(self):
        """Initialize main window.

        Get camera, comport, and test result dir info.
        """

        if camera_handler.check_camera_availability():
            self.refresh_camera_table()
        self.refresh_port()
        # TODO

    def eventFilter(self, obj, event):
        """
        Object obj installed event filter and is watched by main window.

        :param obj: installed event filter and by watched.
        :param event: obj's event type
        :return: stop being handled further return True, otherwise return False.
        """
        # for item in self.cameras:
        #     if obj == item.get_viewfinder():
        #         if event.type() == QtCore.QEvent.Close:
        #             item.close()
        #             return True
        #         else:
        #             return False
        #     else:
        #         # pass the event on to the parent class.
        #         return MainWindow.eventFilter(self, obj, event)
        #         # return False
        if type(obj) == QtMultimediaWidgets.QCameraViewfinder:
            if event.type() == QtCore.QEvent.Close:
                for item in self.cameras:
                    if obj == item.get_viewfinder():
                        item.close()
                        return True
            else:
                return False
        return MainWindow.eventFilter(self, obj, event)

    def refresh_camera_table(self):
        """
        Refresh main window's camera table.

        Warning: Once camera is open or supervision starts, Adding new camera
        devices will cause app crash which means the application doesn't
        support hot plug.
        :return: None
        """
        self.cameras = camera_handler.get_cameras()
        self.cameratable_tablewidget.clearContents()
        if not camera_handler.check_camera_availability():
            warning(self, '提示', '无可用摄像头')
            return

        self.cameratable_tablewidget.setRowCount(len(self.cameras))
        for i, cam in enumerate(self.cameras):
            tag = QtWidgets.QTableWidgetItem('camera%s' % i)
            camera_name = QtWidgets.QTableWidgetItem(cam.name())
            camera_id = QtWidgets.QTableWidgetItem(cam.id())
            self.cameratable_tablewidget.setItem(i, 0, tag)
            self.cameratable_tablewidget.setItem(i, 1, camera_name)
            self.cameratable_tablewidget.setItem(i, 2, camera_id)

    def open_camera(self):
        if self.cameratable_tablewidget.rowCount() == 0:
            warning(self, '提示', '无可用摄像头')
            return

        for cam in self.cameras:
            if self.get_table_camera_info()[2] == cam.id():
                if cam.is_open():
                    information(self, '提示', '%s已打开' %
                                self.get_table_camera_info()[0])
                    return

                cam.get_viewfinder().setWindowTitle(
                    self.get_table_camera_info()[0])
                cam.get_viewfinder().installEventFilter(self)
                cam.show_camera_window()
                cam.open()

    def capture_std(self):
        if self.cameratable_tablewidget.rowCount() == 0:
            warning(self, '提示', '无可用摄像头')
            return

        for cam in self.cameras:
            if self.get_table_camera_info()[2] == cam.id():
                if not cam.is_open():
                    warning(self, '提示', '请先打开摄像头%s' %
                            self.get_table_camera_info()[0])
                    return

                if not os.path.exists(self.resultdir_linedit.text()):
                    warning(self, '提示', '结果路径不存在或格式错误')
                    return

                if cam.get_image_catpture().isReadyForCapture():
                    cam.get_image_catpture().imageCaptured.connect(
                        self.display_image)
                    cam.capture()

    def display_image(self, id, image):
        tab_text = self.get_table_camera_info()[0]
        for i in range(self.standardimg_tabwidget.count()):
            if self.standardimg_tabwidget.tabText(i) == tab_text:
                self.standardimg_tabwidget.widget(i).setPixmap(
                    QtGui.QPixmap.fromImage(image))
                return
        image_label = QtWidgets.QLabel()
        image_label.setPixmap(QtGui.QPixmap.fromImage(image))
        self.standardimg_tabwidget.addTab(image_label, tab_text)

        # Save image to disk
        file_name = '_'.join([*(self.get_table_camera_info()[0:2]),
                              conf.STANDARD_IMG])
        img_file = os.path.join(self.resultdir_linedit.text(), file_name)
        image.save(img_file)

    def get_table_camera_info(self):
        """
        Get all information of current camera.

        :return: list of camera's tag, name and id.
        """
        selected_row = self.cameratable_tablewidget.currentRow()
        if selected_row == -1:
            selected_row = 0
        selected_camera_tag = self.cameratable_tablewidget.item(
            selected_row, 0).text()
        selected_camera_name = self.cameratable_tablewidget.item(
            selected_row, 1).text()
        selected_camera_id = self.cameratable_tablewidget.item(
            selected_row, 2).text()
        return [selected_camera_tag, selected_camera_name, selected_camera_id]

    def refresh_port(self):
        self.comport_combobox.clear()
        self.comport_combobox.addItems(comport_handler.get_comports_name())

    def open_port(self):
        port_name = self.comport_combobox.currentText()
        if port_name == '':
            critical(self, '提示', '无效的串口名')
            return

        self.serial_port.port = port_name  # configure initialized port
        if self.opencomport_pushbutton.text() == '关闭COM':
            self.serial_port.close()
            information(self, '提示', '成功关闭%s' % port_name)
            self.opencomport_pushbutton.setText('打开COM')
            self.refreshcomport_pushbutton.setEnabled(True)
            self.comport_combobox.setEnabled(True)
        else:
            try:
                self.serial_port.open()
                information(self, '提示', '成功打开%s' % port_name)
                self.opencomport_pushbutton.setText('关闭COM')
                self.refreshcomport_pushbutton.setEnabled(False)
                self.comport_combobox.setEnabled(False)
            except serial.SerialException as e:
                critical(self, '提示', str(e))

    def choose_resultdir(self):
        result_dir = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                '选择结果路径',
                                                                conf.BASE_OPEN_DIR,
                                                                QtWidgets.QFileDialog.ShowDirsOnly)
        self.resultdir_linedit.setText(result_dir)

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
            4. Any config parm is ready to use.
            ...

        :return: True for all conditions are ready, False for not.
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
