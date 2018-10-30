#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/5/14
"""

# imports
import os
import shutil
import sys
import threading
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
from tvsupervision import image_proc
from tvsupervision import mainwindow
from tvsupervision import report
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
        self.supervision_started = False
        self.current_cam = None
        self.curr_result_dir = None
        self.camera_reports = []
        self.summary_report = None
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
        if camera_handler.check_camera_availability():
            self.refresh_camera_table()
        self.refresh_serial()  # TODO

    def closeEvent(self, QCloseEvent):
        if self.serial_port.is_open:
            log.debug('Close %s.' % self.serial_port.name)
            self.serial_port.close()
        for cam in self.cameras:
            if cam.is_open():
                log.debug('Close %s.' % cam.name())
                cam.close()
        if self.curr_result_dir is not None:
            shutil.move(conf.LOG_FILE, self.curr_result_dir)
        log.debug('Close App.')

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

    def capture_curr(self, id, image):
        self.current_cam.set_current_frame(image)
        log.debug("Capturing %s's current frame is finished" %
                  self.current_cam.name())

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
                                                                conf.BASE_OPEN_DIR,
                                                                QtWidgets.QFileDialog.ShowDirsOnly)
        self.resultdir_linedit.setText(result_dir)
        log.debug('Result directory is %s.' % result_dir)

    @QtCore.pyqtSlot()
    def start_supervision(self):
        if self.start_supervision_pushbutton.text() == "开始监控":
            log.debug('Start supervision, first check param configurations.')
            self.start()
            return
        self.pause()

    def start(self):
        self.supervision_started = True
        if not self.check_and_prepare():
            return
        self.start_supervision_pushbutton.setText('暂停监控')
        # if self.powertype_combobox.currentText() == '电源箱交流':
        #     pass
        if self.powertype_combobox.currentText() == '红外直流':
            log.debug('Start direct supervision.')
            self.start_direct_supervision()
        else:
            log.debug('Start cross supervision.')
            self.start_cross_supervision()
        # Move log file to result dir
        shutil.move(conf.LOG_FILE, self.curr_result_dir)

    def pause(self):
        self.supervision_started = False
        # Update log file to result dir.
        shutil.move(conf.LOG_FILE, self.curr_result_dir)
        log.debug('Pause supervision.')
        self.start_supervision_pushbutton.setText('开始监控')

    def start_direct_supervision(self):
        self.start_supervision_pushbutton.setText('暂停监控')
        while self.current_snap_times < int(
                self.directpower_count_lineedit.text()):
            if not self.supervision_started:
                return
                # Power off first and wait for some time
            off_time = int(self.directpower_offtime_lineedit.text())
            log.debug('Power off Tv after %s seconds.' % str(off_time))
            key_value = bytes.fromhex(self.directpower_keyvalue_lineedit.text())
            self.serial_port.write(key_value)
            self.current_snap_times += 1
            t = threading.Timer(off_time, self.start_compare)
            t.start()
            t.join()

    def start_cross_supervision(self):
        self.start_supervision_pushbutton.setText('暂停监控')
        # Set cross_power address
        power_address_key = self.crosspower_address_lineedit.text()
        key_value = bytes.fromhex(power_address_key)
        log.debug('Send %s to set cross power address.' % power_address_key)
        self.serial_port.write(key_value)
        time.sleep(5)
        while self.current_snap_times < int(
                self.crosspower_count_lineedit.text()):
            if not self.supervision_started:
                return
            # Power off first and wait for some time
            off_time = int(self.crosspower_offtime_lineedit.text())
            log.debug('Power off Tv after %s seconds.' % str(off_time))
            power_off_key = self.crosspower_off_keyvalue_lineedit.text()
            key_value = bytes.fromhex(power_off_key)
            log.debug('Send %s to cross power off.' % power_off_key)
            self.serial_port.write(key_value)
            self.current_snap_times += 1
            t = threading.Timer(off_time, self.start_compare)
            t.start()
            t.join()

    def start_compare(self):
        """
        Process all open cameras to diff current frame with standard img.
        :return:
        """
        if self.powertype_combobox.currentText() == '红外直流':
            power_on_key = self.directpower_keyvalue_lineedit.text()
            log.debug('Send %s to direct power on.' % power_on_key)
            key_value = bytes.fromhex(power_on_key)
            self.serial_port.write(key_value)
        elif self.powertype_combobox.currentText() == 'PRO800交流':
            power_on_key = self.crosspower_on_keyvalue_lineedit.text()
            log.debug('Send %s to cross power on.' % power_on_key)
            key_value = bytes.fromhex(power_on_key)
            self.serial_port.write(key_value)
        camera_diff_threads = []
        for cam in self.cameras:
            if not cam.is_open():
                continue
            t = threading.Thread(target=self.camera_diff, args=(cam,))
            camera_diff_threads.append(t)
        for t in camera_diff_threads:
            t.start()
        for t in camera_diff_threads:
            t.join()
        self.summary_report.update_summary_report()

    def camera_diff(self, cam):
        interval, times = self.crosspower_interval_lineedit.text().split('-')
        threads = []
        for i in range(int(times)):
            interval_time = int(interval) * (i + 1)
            t = threading.Timer(interval=interval_time,
                                function=self.image_diff, args=[cam, i + 1])
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def image_diff(self, cam, count):
        """
        Current camera to diff it's standard and current frame.

        :param cam: current camera
        :param count: current number of difference.
        :return:
        """
        self.current_cam = cam
        if not cam.get_image_capture().isReadyForCapture():
            return
        cam.get_image_capture().imageCaptured.connect(self.capture_curr)
        log.debug("Start %s's current frame capturing." % cam.name())
        cam.capture()
        standard_image = image_proc.qimage2cv(cam.standard_img())
        current_image = image_proc.qimage2cv(cam.current_frame())
        diff_result, diff_percent = image_proc.diff(standard_image,
                                                    current_image)
        log.debug("%s : %s's %s diff result is %s, different percent is %s" % (
            str(self.current_snap_times), cam.name(), str(count), diff_result,
            str(diff_percent)))
        for camera_report in self.camera_reports:
            if cam is not camera_report.camera():
                continue
            current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
            camera_report.camera_attr['currentTime'] = current_time
            current_image_name = '%s_%s.%s' % (current_time,
                                               self.current_snap_times,
                                               conf.IMG_POSTFIX)
            camera_report.camera_attr['snapTimes'] = self.current_snap_times
            camera_report.camera_attr['imgSrc'] = current_image_name
            camera_report.diff_state = diff_result
            camera_report.diff_percent = diff_percent
            if not diff_result:
                camera_report.fail_times += 1
                camera_report.update()
            camera_report.pass_times += 1
            log.debug('Save current image to %s' % camera_report.result_dir())
            camera_report.save_current_img()

    def look_result(self):
        if self.summary_report is None:
            log.warning("Test result doesn't exist.")
            warning(self, '提示', '测试结果未生成.')
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
        self.curr_result_dir = os.path.join(self.resultdir_linedit.text(),
                                            current_time)
        if not os.path.exists(self.curr_result_dir):
            os.mkdir(self.curr_result_dir)
        log.debug('Current result dir is %s' % self.curr_result_dir)
        for cam in self.cameras:
            if not cam.is_open():
                continue
            camera_report = report.CameraReport(cam)
            camera_report.set_result_dir(self.curr_result_dir)
            if not os.path.exists(camera_report.result_dir()):
                os.mkdir(camera_report.result_dir())
            log.debug("%s's result dir is %s" % (cam.name(),
                                                 camera_report.result_dir()))
            # Save standard img to cam's dir
            camera_report.save_standard_img()
            # Initialize each open camera's report
            camera_report.initialize()
            self.camera_reports.append(camera_report)
        # Initialize summary report
        self.summary_report = report.SummaryReport(self.camera_reports)
        self.summary_report.report_name = os.path.join(
            self.curr_result_dir, conf.SUMMARY_REPORT)
        self.summary_report.initialize_summary_report(current_time)
        return True


def main():
    """Module's main entrance, executed when not as imported."""
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
