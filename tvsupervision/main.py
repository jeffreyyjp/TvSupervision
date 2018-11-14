#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/5/14
"""

# imports
import os
import shutil
import sys
import time
import webbrowser

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
from tvsupervision import supervision_worker
from tvsupervision.log_handler import logger as log

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
        self.current_snap_times = 0
        self.current_cam = None
        self.base_dir = None
        self.camera_reports = []
        self.summary_report = None
        self.worker = None
        self.supervision_thread = QtCore.QThread()
        super(MainWindow, self).__init__()
        self.setupUi(self)
        log.debug('App starts.')
        log.debug('Window size: %s * %s.' % (self.width(), self.height()))

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
        self.powerbox_count_lineedit.setText('500')
        self.powerbox_onoff_interval_lineedit.setText('60')
        self.powerbox_snap_interval_lineedit.setText('10-3')
        self.directpower_count_lineedit.setText('500')
        self.directpower_offtime_lineedit.setText('15')
        self.directpower_keyvalue_lineedit.setText('AAA7BF0DE3')
        self.directpower_interval_lineedit.setText('15-3')
        self.crosspower_count_lineedit.setText('500')
        self.crosspower_offtime_lineedit.setText('15')
        self.crosspower_address_lineedit.setText('55010000f2aa')
        self.crosspower_on_keyvalue_lineedit.setText('55010001f0aa')
        self.crosspower_off_keyvalue_lineedit.setText('55010001f1aa')
        self.crosspower_interval_lineedit.setText('15-3')
        self.resultdir_linedit.setText(conf.BASE_OPEN_DIR)
        if camera_handler.check_camera_availability():
            self.refresh_camera_table()
        self.refresh_serial()  # TODO

    def closeEvent(self, event):
        if self.supervision_thread.isRunning():
            log.warning('Supervision is still running.')
            button = warning(self, '提示', '电视监控正在运行，确定要关闭？',
                             QtWidgets.QMessageBox.Yes |
                             QtWidgets.QMessageBox.No)
            if button == QtWidgets.QMessageBox.Yes:
                self.supervision_thread.quit()
            else:
                event.ignore()
                return
        if self.serial_port.is_open:
            log.debug('Close %s.' % self.serial_port.name)
            self.serial_port.close()
        for cam in self.cameras:
            if cam.is_open():
                log.debug('Close %s.' % cam.name())
                cam.get_viewfinder().close()
                cam.close()
        log.debug('Close App.')
        event.accept()

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
                    if obj != item.get_viewfinder():
                        continue
                    log.debug('%s has been closed.' % item.name())
                    item.close()
                    return True
            else:
                return False
        return MainWindow.eventFilter(self, obj, event)

    @QtCore.pyqtSlot()
    def refresh_camera_table(self):
        """
        Refresh main window's camera table.

        Warning: Once camera is open or supervision starts, Adding new camera
        devices will cause app crash which means the application don't
        support hot plug.
        :return: None
        """
        self.cameras = camera_handler.get_cameras()
        self.cameratable_tablewidget.clearContents()
        if not camera_handler.check_camera_availability():
            warning(self, '提示', '无可用摄像头')
            return
        camera_num = len(self.cameras)
        self.cameratable_tablewidget.setRowCount(camera_num)
        if camera_num > 1:
            log.debug('There are %s cameras available.' % camera_num)
        else:
            log.debug('There is 1 camera available.')
        for i, cam in enumerate(self.cameras):
            cam.set_tag('camera%s' % i)
            tag = QtWidgets.QTableWidgetItem(cam.tag())
            camera_name = QtWidgets.QTableWidgetItem(cam.name())
            camera_id = QtWidgets.QTableWidgetItem(cam.id())
            self.cameratable_tablewidget.setItem(i, 0, tag)
            self.cameratable_tablewidget.setItem(i, 1, camera_name)
            self.cameratable_tablewidget.setItem(i, 2, camera_id)

    @QtCore.pyqtSlot()
    def open_camera(self):
        if self.cameratable_tablewidget.rowCount() == 0:
            log.warning('Not available cameras.')
            warning(self, '提示', '无可用摄像头')
            return

        for cam in self.cameras:
            if self.get_table_camera_info()[2] != cam.id():
                continue
            if cam.is_open():
                log.warning('%s is already open' % cam.name())
                information(self, '提示', '%s已打开' % cam.tag())
                return
            cam.get_viewfinder().setWindowTitle(cam.tag())
            cam.get_viewfinder().installEventFilter(self)
            cam.show_camera_window()
            cam.open()
            log.debug('%s opened successfully.' % cam.name())

    @QtCore.pyqtSlot()
    def capture_std(self):
        for cam in self.cameras:
            if self.get_table_camera_info()[2] != cam.id():
                continue
            if not cam.is_open():
                log.warning('%s not opened yet.' % cam.tag())
                warning(self, '提示', '请先打开摄像头%s' % cam.tag())
                return
            if cam.get_image_capture().isReadyForCapture():
                cam.get_image_capture().imageCaptured.connect(
                    self.display_image)
                self.current_cam = cam
                cam.capture()
                log.debug("Start %s's standard image capturing..." % cam.name())

    def display_image(self, id, image):
        # Hold standard img for cam
        self.current_cam.set_standard_img(image)
        tab_text = self.current_cam.tag()
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
        log.debug("Capturing %s's standard image is finished." %
                  self.current_cam.name())
        self.current_cam.get_image_capture().imageCaptured.disconnect(
            self.display_image)

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

    @QtCore.pyqtSlot()
    def refresh_serial(self):
        self.serial_port_combobox.clear()
        self.serial_port_combobox.addItems(comport_handler.get_comports_name())
        self.serial_baudrate_combobox.setCurrentIndex(0)
        self.serial_databits_combobox.setCurrentIndex(3)
        self.serial_parity_combobox.setCurrentIndex(0)
        self.serial_stopbits_combobox.setCurrentIndex(0)

    @QtCore.pyqtSlot()
    def open_port(self):
        if self.open_serial_pushbutton.text() == '关闭COM':
            self.serial_port.close()
            log.debug('Close %s successfully.' % self.serial_port.port)
            information(self, '提示', '成功关闭%s' % self.serial_port.port)
            self.open_serial_pushbutton.setText('打开COM')
            self.refresh_serial_pushbutton.setEnabled(True)
            self.serial_port_combobox.setEnabled(True)
        else:
            try:
                port_name = self.serial_port_combobox.currentText()
                if port_name == '':
                    log.error('Invalid port name.')
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
                log.debug('Open %s successfully.' % port_name)
                information(self, '提示', '成功打开%s' % port_name)
                self.open_serial_pushbutton.setText('关闭COM')
                self.refresh_serial_pushbutton.setEnabled(False)
                # self.serial_port_combobox.setEnabled(False)
            except Exception as e:
                log.critical("Open port fail, please check configurations.")
                critical(self, '提示', '无法打开串口，请检查参数配置')

    @QtCore.pyqtSlot()
    def choose_resultdir(self):
        result_dir = QtWidgets.QFileDialog.getExistingDirectory(self, '选择结果路径',
                                                                self.resultdir_linedit.text(),
                                                                QtWidgets.QFileDialog.ShowDirsOnly)
        if result_dir == '':
            return
        else:
            self.resultdir_linedit.setText(result_dir)
        log.debug('Result directory is %s.' % result_dir)

    @QtCore.pyqtSlot(str, str, str, str, str)
    def update_result_table(self, cam_name, curr_supervision_time, snap_time,
                            diff_result, diff_percent):
        for i in range(self.result_tabwidget.count()):
            if self.result_tabwidget.tabText(i) == cam_name:
                widget = self.result_tabwidget.widget(i)
                row_count = widget.rowCount()
                widget.insertRow(row_count)
                curr_supervision_time = QtWidgets.QTableWidgetItem(
                    curr_supervision_time)
                snap_time = QtWidgets.QTableWidgetItem(snap_time)
                diff_result = QtWidgets.QTableWidgetItem(diff_result)
                diff_percent = QtWidgets.QTableWidgetItem(diff_percent)
                widget.setItem(row_count, 0, curr_supervision_time)
                widget.setItem(row_count, 1, snap_time)
                widget.setItem(row_count, 2, diff_result)
                widget.setItem(row_count, 3, diff_percent)

    @QtCore.pyqtSlot()
    def start_supervision(self):
        if self.start_supervision_pushbutton.text() == "开始监控":
            log.debug('Start supervision, first check param configurations.')
            self.start()
        else:
            self.stop()

    def start(self):
        if not self.check_and_prepare():
            return
        self.start_supervision_pushbutton.setText('结束监控')
        self.open_serial_pushbutton.setEnabled(False)
        self.look_result_pushbutton.setEnabled(False)
        # if self.powertype_combobox.currentText() == '电源箱交流':
        #     pass
        if self.powertype_combobox.currentText() == '电源箱交流':
            log.debug('Start powerbox supervision.')
            self.worker = supervision_worker.PowerboxWorker()
        if self.powertype_combobox.currentText() == '红外直流':
            log.debug('Start direct supervision.')
            self.worker = supervision_worker.DirectWorker()
        else:
            log.debug('Start cross supervision.')
            self.worker = supervision_worker.CrossWorker()
        self.init_worker(self.worker)
        self.worker.moveToThread(self.supervision_thread)
        self.supervision_thread.started.connect(self.worker.start_supervision)
        self.worker.diff_finished.connect(self.update_result_table)
        self.worker.supervision_finished.connect(self.supervision_thread.quit)
        self.worker.supervision_finished.connect(self.resume)
        self.supervision_thread.finished.connect(self.worker.deleteLater)
        self.supervision_thread.start()

    def stop(self):
        log.debug('Stop supervision.')
        self.worker.supervision_control = False

    def init_worker(self, worker):
        if self.powertype_combobox.currentText() == '电源箱交流':
            supervision_count = int(self.powerbox_count_lineedit.text())
            worker.supervision_count = supervision_count
            worker.onoff_interval = int(
                self.powerbox_onoff_interval_lineedit.text())
            interval_times = self.crosspower_interval_lineedit.text().split('-')
            interval, times = list(map(int, interval_times))
            worker.snap_interval = interval
            worker.snap_count = times
            return
        if self.powertype_combobox.currentText() == '红外直流':
            supervision_count = int(self.directpower_count_lineedit.text())
            off_time = int(self.directpower_offtime_lineedit.text())
            interval_times = self.directpower_interval_lineedit.text().split(
                '-')
            worker.power_key = bytes.fromhex(
                self.directpower_keyvalue_lineedit.text())
        else:

            supervision_count = int(self.crosspower_count_lineedit.text())
            off_time = int(self.crosspower_offtime_lineedit.text())
            interval_times = self.crosspower_interval_lineedit.text().split('-')
            worker.power_on_key = bytes.fromhex(
                self.crosspower_on_keyvalue_lineedit.text())
            worker.power_off_key = bytes.fromhex(
                self.crosspower_off_keyvalue_lineedit.text())
        worker.supervision_count = supervision_count
        worker.off_time = off_time
        interval, times = list(map(int, interval_times))
        worker.snap_interval = interval
        worker.snap_count = times
        worker.cameras = self.cameras
        worker.serial_port = self.serial_port
        worker.image_diff_rate = self.image_diff_spinbox.value() * 0.01
        worker.camera_reports = self.camera_reports
        worker.summary_report = self.summary_report
        worker.supervision_control = True

    def resume(self):
        log.debug('Supervision is finished.')
        self.start_supervision_pushbutton.setText('开始监控')
        self.open_serial_pushbutton.setEnabled(True)
        self.look_result_pushbutton.setEnabled(True)
        # Copy log.txt to result dir
        shutil.copy(conf.LOG_FILE, self.base_dir)

    def look_result(self):
        if self.summary_report is None:
            log.warning("Test result doesn't exist.")
            warning(self, '提示', '测试结果未生成.')
            return
        if self.supervision_thread.isRunning():
            warning(self, '提示', '监控正在进行，无法查看测试报告')
            return
        ie = webbrowser.get(webbrowser.iexplore)
        ie.open(self.summary_report.report_name)

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
            log.warning("Haven't opened any cameras.")
            critical(self, '提示', '未打开任何摄像头')
            return False

        # Check if standard image has been captured
        for cam in self.cameras:
            if not cam.is_open():
                continue
            if cam.standard_img() is None:
                log.warning("%s didn't capture standard image." % cam.name())
                critical(self, '提示', '未截取标准图')
                return False

        # Check if com_port is open
        if not self.serial_port.is_open:
            log.warning("Haven't opened cam port.")
            critical(self, '提示', '未打开串口')
            return False

        # Check result dir is valid
        if not os.path.isdir(self.resultdir_linedit.text()):
            log.warning('Result base dir is invalid.')
            critical(self, '提示', '路径错误')
            return False

        # Check all parameters have been configured.
        for item in self.powertype_stackedwidget.currentWidget().children():
            if type(item) != QtWidgets.QLineEdit:
                continue
            if not item.text():
                log.warning('Configuration params is missing.')
                critical(self, '提示', '配置参数未填写')
                return False

        # Initialize test result dir
        current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        self.base_dir = os.path.join(self.resultdir_linedit.text(),
                                     current_time)
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)
            shutil.copy(conf.SUMMARY_REPORT_XSL, self.base_dir)
            shutil.copy(conf.CAMERA_REPORT_XSL, self.base_dir)
            shutil.copy(conf.STYLE_CSS, self.base_dir)

        log.debug('Current base dir is %s' % self.base_dir)
        for cam in self.cameras:
            if not cam.is_open():
                continue
            camera_report = report.CameraReport(cam, self.base_dir)
            log.debug("%s's result dir is %s" % (cam.name(),
                                                 camera_report.result_dir))
            # Save standard img to cam's dir
            camera_report.save_standard_img()
            # Initialize each open camera's report
            self.camera_reports.append(camera_report)
        # Initialize summary report
        summary_report_name = os.path.join(self.base_dir, conf.SUMMARY_REPORT)
        self.summary_report = report.SummaryReport(self.camera_reports,
                                                   summary_report_name,
                                                   current_time)

        # Initialize result table
        for cam in self.cameras:
            if not cam.is_open():
                continue
            result_cam_table = QtWidgets.QTableWidget()
            result_cam_table.setColumnCount(4)
            result_cam_table.setHorizontalHeaderLabels(['当前轮次', '对比轮次',
                                                        '对比结果', '误差值'])
            self.result_tabwidget.addTab(result_cam_table, cam.name())
        return True


def main():
    """Module's main entrance, executed when not as imported."""
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
