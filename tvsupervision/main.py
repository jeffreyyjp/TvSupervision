#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/5/14
"""

# imports
import os
import sys
import threading
import time

import serial
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtMultimediaWidgets
from PyQt5 import QtWidgets

from docs import conf
from tvsupervision import camera_handler
from tvsupervision import comport_handler
from tvsupervision import mainwindow
from tvsupervision import report

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
        self.current_times = 0
        self.supervision_started = False
        self.current_cam = None

        super(MainWindow, self).__init__()
        self.setupUi(self)

        # self.setMinimumSize(400, 300)

        # All connections between signals and slots are defined here.
        self.refreshcamera_pushbutton.clicked.connect(self.refresh_camera_table)
        self.opencamera_pushbutton.clicked.connect(self.open_camera)
        self.capturestd_pushbutton.clicked.connect(self.capture_std)
        self.refresh_serial_pushbutton.clicked.connect(self.refresh_serial)
        self.open_serial_pushbutton.clicked.connect(self.open_port)
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
        self.refresh_serial()  # TODO

    def eventFilter(self, obj, event):
        """
        Object obj installed event filter and is watched by main window.

        :param obj: installed event filter and by watched.
        :param event: obj's event type
        :return: stop being handled further return True, otherwise return False.
        """
        if type(obj) == QtMultimediaWidgets.QCameraViewfinder:
            if event.type() == QtCore.QEvent.Close:
                for item in self.cameras:
                    if obj == item.get_viewfinder():
                        item.close()
                        return True
            else:
                return False
        return MainWindow.eventFilter(self, obj, event)

    # def resizeEvent(self, QResizeEvent):
    #     """
    #     Resize standard image when main window is changed and keep image
    #     resize smoothly.
    #     :param QResizeEvent:
    #     :return:
    #     """
    #     # print('hello')
    #     if self.standardimg_tabwidget.count() == 0:
    #         return
    #
    #     curr_label = self.standardimg_tabwidget.currentWidget()
    #     curr_pixmap = curr_label.pixmap()
    #     scaled_size = curr_pixmap.size()
    #     scaled_size.scale(curr_label.size(), QtCore.Qt.KeepAspectRatio)
    #     # if not curr_pixmap or scaled_size != curr_pixmap.size():
    #     #     self.update_label_image(curr_label, curr_pixmap)
    #     self.update_label_image(curr_label, curr_pixmap)

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
            cam.set_tag('camera%s' % i)
            tag = QtWidgets.QTableWidgetItem(cam.tag())
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
                    information(self, '提示', '%s已打开' % cam.tag())
                    return

                cam.get_viewfinder().setWindowTitle(cam.tag())
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
                    warning(self, '提示', '请先打开摄像头%s' % cam.tag())
                    return

                if cam.get_image_capture().isReadyForCapture():
                    cam.get_image_capture().imageCaptured.connect(
                        self.display_image)
                    self.current_cam = cam
                    cam.capture()

    def caputre_curr(self, id, image):
        self.current_cam.set_current_frame(image)

    def display_image(self, id, image):
        # Hold standard img for cam
        # cam_id = self.get_table_camera_info()[2]
        # for cam in self.cameras:
        #     if cam_id == cam.id():
        #         cam.set_standard_img(image)
        self.current_cam.set_standard_img(image)

        tab_text = self.get_table_camera_info()[0]
        for i in range(self.standardimg_tabwidget.count()):
            if self.standardimg_tabwidget.tabText(i) == tab_text:
                self.standardimg_tabwidget.widget(i).setPixmap(
                    QtGui.QPixmap.fromImage(image))
                return
        image_label = QtWidgets.QLabel()
        image_label.setAlignment(QtCore.Qt.AlignCenter)
        image_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Expanding)
        screen_geometry = QtWidgets.QApplication.desktop().screenGeometry(self)
        image_label.setMinimumSize(screen_geometry.width() // 8,
                                   screen_geometry.height() // 8)
        self.standardimg_tabwidget.addTab(image_label, tab_text)
        self.update_label_image(image_label, QtGui.QPixmap.fromImage(image))
        # image_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def update_label_image(self, label, pixmap):
        label.setPixmap(pixmap.scaled(label.size(),
                                      QtCore.Qt.KeepAspectRatio,
                                      QtCore.Qt.SmoothTransformation))

    def get_table_camera_info(self):
        """
        Get all information of current camera.

        :return: list of camera's tag, name and id.
        """
        selected_row = self.cameratable_tablewidget.currentRow()
        if selected_row == -1:
            selected_row = 0
        selected_camera_tag = self.cameratable_tablewidget.item(selected_row,
                                                                0).text()
        selected_camera_name = self.cameratable_tablewidget.item(selected_row,
                                                                 1).text()
        selected_camera_id = self.cameratable_tablewidget.item(selected_row,
                                                               2).text()
        return [selected_camera_tag, selected_camera_name, selected_camera_id]

    def refresh_serial(self):
        self.serial_port_combobox.clear()
        self.serial_port_combobox.addItems(comport_handler.get_comports_name())
        self.serial_baudrate_combobox.setCurrentIndex(0)
        self.serial_databits_combobox.setCurrentIndex(3)
        self.serial_parity_combobox.setCurrentIndex(0)
        self.serial_stopbits_combobox.setCurrentIndex(0)

    def open_port(self):
        if self.open_serial_pushbutton.text() == '关闭COM':
            self.serial_port.close()
            information(self, '提示', '成功关闭%s' % self.serial_port.port)
            self.open_serial_pushbutton.setText('打开COM')
            self.refresh_serial_pushbutton.setEnabled(True)
            self.serial_port_combobox.setEnabled(True)
        else:
            try:
                port_name = self.serial_port_combobox.currentText()
                if port_name == '':
                    critical(self, '提示', '无效的串口名')
                    return
                self.serial_port.port = port_name  # configure initialized port
                self.serial_port.baudrate = int(
                    self.serial_baudrate_combobox.currentText())
                self.serial_port.bytesize = int(
                    self.serial_databits_combobox.currentText())
                parity = self.serial_parity_combobox.currentText()
                self.serial_port.parity = comport_handler.PARITY_NAME[parity]
                self.serial_port.stopbits = float(
                    self.serial_stopbits_combobox.currentText())
                self.serial_port.open()
                information(self, '提示', '成功打开%s' % port_name)
                self.open_serial_pushbutton.setText('关闭COM')
                self.refresh_serial_pushbutton.setEnabled(False)
                # self.serial_port_combobox.setEnabled(False)
            except serial.SerialException as e:
                critical(self, '提示', '无法打开串口，请检查参数配置')
            except Exception as e:
                print(str(e))

    def choose_resultdir(self):
        result_dir = QtWidgets.QFileDialog.getExistingDirectory(self, '选择结果路径',
                                                                conf.BASE_OPEN_DIR,
                                                                QtWidgets.QFileDialog.ShowDirsOnly)
        self.resultdir_linedit.setText(result_dir)

    def start_supervision(self):
        if self.start_supervision_pushbutton.text() == "开始监控":
            self.start()
            return
        self.pause()

    def start(self):
        if not self.check_and_prepare():
            return
        self.start_supervision_pushbutton.setText('暂停监控')
        if self.powertype_combobox.currentText() == '电源箱交流':
            pass
        elif self.powertype_combobox.currentText() == '红外直流':
            pass
        else:
            self.start_cross_supervision()

    def pause(self):
        pass

    def start_cross_supervision(self):
        # Set cross_power address
        self.serial_port.write(self.crosspower_address_lineedit)
        while self.current_times < int(self.crosspower_count_lineedit):
            if self.supervision_started:
                # Power off first and wait for some time
                self.serial_port.write(self.crosspower_off_keyvalue_lineedit)
                off_time = int(self.crosspower_offtime_lineedit)
                t = threading.Timer(off_time, self.start_compare)
                t.start()
                t.join()
                self.current_times += 1

    def start_compare(self):
        """
        Process all open cameras to diff current frame with standard img.
        :return:
        """
        self.serial_port.write(self.crosspower_on_keyvalue_lineedit)
        camera_diff_threads = []
        for cam in self.cameras:
            if cam.is_open():
                t = threading.Thread(target=self.camera_diff, args=(cam,))
                camera_diff_threads.append(t)
        for t in camera_diff_threads:
            t.start()

        for t in camera_diff_threads:
            t.join()

    def camera_diff(self, cam):
        interval, times = self.crosspower_interval_lineedit.split('-')
        threads = []
        for i in times:
            interval_time = int(interval) * (i + 1)
            t = threading.Timer(interval=interval_time,
                                function=self.image_diff, args=[cam])
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def image_diff(self, cam):
        if cam.get_image_capture().isReadyForCapture():
            cam.get_image_capture().imageCaptured.connect(
                self.capture_curr)
            self.current_cam = cam
            cam.capture()

    def look_result(self):
        pass

    def check_and_prepare(self):
        """Check preconditions is ready.

        Check:
            1. Camera is open.
            2. Comport is open.
            3. Test result dir is valid.
            4. Any config parm is ready to use.
            ...

        Prepare:
            1. Initialize current test result dir.

        :return: True for all conditions are ready, False for not.
        """
        # Check if any camera has open
        for cam in self.cameras:
            if cam.is_open():
                break
        else:
            critical(self, '提示', '未打开任何摄像头')
            return False

        # Check if standard image has been captured
        for cam in self.cameras:
            if cam.is_open():
                if cam.standard_img() is None:
                    critical(self, '提示', '未截取标准图')
                    return False

        # Check if com_port is open
        if not self.serial_port.is_open:
            critical(self, '提示', '未打开串口')
            return False

        # Check result dir is valid
        if not os.path.isdir(self.resultdir_linedit.text()):
            critical(self, '提示', '路径错误')
            return False

        # Check all parameters have been configured.
        for item in self.powertype_stackedwidget.currentWidget().children():
            if type(item) == QtWidgets.QLineEdit:
                if not item.text():
                    critical(self, '提示', '配置参数未填写')
                    return False


        # Initialize test result dir
        curr_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        curr_result_dir = os.path.join(self.resultdir_linedit.text(), curr_time)
        if not os.path.exists(curr_result_dir):
            os.mkdir(curr_result_dir)
        report.create_summary_report()
        for cam in self.cameras:
            if cam.is_open():
                cam.set_result_dir(curr_result_dir)
                if not os.path.exists(cam.result_dir()):
                    os.mkdir(cam.result_dir())
                # Save standard img to cam's dir
                cam.standard_img().save(os.path.join(cam.result_dir(),
                                                     conf.STANDARD_IMG))
        return True


def main():
    """Module's main entrance, executed when not as imported."""
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
