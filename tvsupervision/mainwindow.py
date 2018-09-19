#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/8/13
"""
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class Ui_Form(object):
    def setupUi(self, form):
        """
        Construct all kinds of UI widget of the application.

        All UI objects are there and also include signals and slots declaration.

        :return:
        """
        form.setObjectName('Form')
        form.resize(854, 480)
        font = QtGui.QFont()
        font.setFamily('微软雅黑')
        form.setFont(font)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('../docs/images/tv.jpg'),
                       QtGui.QIcon.Normal, QtGui.QIcon.On)
        form.setWindowIcon(icon)

        # Global layout for application
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setObjectName('main_layout')

        # all widgets and layouts about the tool's control settings
        self.controlsettings_groupbox = QtWidgets.QGroupBox(form)
        self.controlsettings_groupbox.setObjectName('controlsettings_groupbox')
        self.controlsettings_layout = QtWidgets.QVBoxLayout(
            self.controlsettings_groupbox)
        self.controlsettings_layout.setObjectName('controlsettings_layout')
        self.controlsettings_tabwidget = QtWidgets.QTabWidget()
        self.controlsettings_tabwidget.setObjectName(
            'controlsettings_tabwidget')
        self.controlsettings_layout.addWidget(self.controlsettings_tabwidget)

        # Power type widget including child and layout
        self.powertype_widget = QtWidgets.QWidget()
        self.powertype_widget.setObjectName('powertype_widget')
        self.powertype_layout = QtWidgets.QVBoxLayout(self.powertype_widget)
        self.powertype_layout.setObjectName('powertype_layout')
        self.powertype_stackedwidget = QtWidgets.QStackedWidget()
        self.powertype_stackedwidget.setObjectName('powertype_stackedwidget')
        self.powertype_layout.addWidget(self.powertype_stackedwidget)
        # Power box widget including it's child widget and layout
        self.powerbox_widget = QtWidgets.QWidget()
        self.powerbox_widget.setObjectName('powerbox_widget')
        self.powerbox_layout = QtWidgets.QFormLayout(self.powerbox_widget)
        self.powerbox_layout.setObjectName('powerbox_layout')
        self.powerbox_count_label = QtWidgets.QLabel()
        self.powerbox_count_label.setObjectName('powerbox_count_label')
        self.powerbox_count_lineedit = QtWidgets.QLineEdit()
        self.powerbox_count_lineedit.setObjectName('powerbox_count_lineedit')
        self.powerbox_layout.addRow(self.powerbox_count_label,
                                    self.powerbox_count_lineedit)
        self.powerbox_interval_label = QtWidgets.QLabel()
        self.powerbox_interval_label.setObjectName('powerbox_interval_label')
        self.powerbox_interval_lineedit = QtWidgets.QLineEdit()
        self.powerbox_interval_lineedit.setObjectName(
            'powerbox_interval_lineedit')
        self.powerbox_layout.addRow(self.powerbox_interval_label,
                                    self.powerbox_interval_lineedit)
        self.powertype_stackedwidget.addWidget(self.powerbox_widget)
        # Direct power widget including it's child widget and layout
        self.directpower_widget = QtWidgets.QWidget()
        self.directpower_widget.setObjectName('directpower_widget')
        self.directpower_layout = QtWidgets.QFormLayout(self.directpower_widget)
        self.directpower_layout.setObjectName('directpower_layout')
        self.directpower_count_label = QtWidgets.QLabel()
        self.directpower_count_label.setObjectName('directpower_count_label')
        self.directpower_count_lineedit = QtWidgets.QLineEdit()
        self.directpower_count_lineedit.setObjectName(
            'directpower_count_lineedit')
        self.directpower_layout.addRow(self.directpower_count_label,
                                       self.directpower_count_lineedit)
        self.directpower_offtime_label = QtWidgets.QLabel()
        self.directpower_offtime_label.setObjectName(
            'directpower_offtime_label')
        self.directpower_offtime_lineedit = QtWidgets.QLineEdit()
        self.directpower_offtime_lineedit.setObjectName(
            'directpower_offtime_lineedit')
        self.directpower_layout.addRow(self.directpower_offtime_label,
                                       self.directpower_offtime_lineedit)
        self.directpower_keyvalue_label = QtWidgets.QLabel()
        self.directpower_keyvalue_label.setObjectName(
            'directpower_keyvalue_label')
        self.directpower_keyvalue_lineedit = QtWidgets.QLineEdit()
        self.directpower_keyvalue_lineedit.setObjectName(
            'directpower_keyvalue_lineedit')
        self.directpower_layout.addRow(self.directpower_keyvalue_label,
                                       self.directpower_keyvalue_lineedit)
        self.directpower_interval_label = QtWidgets.QLabel()
        self.directpower_interval_label.setObjectName(
            'pdirectpower_interval_label')
        self.directpower_interval_lineedit = QtWidgets.QLineEdit()
        self.directpower_interval_lineedit.setObjectName(
            'pdirectpower_interval_lineedit')
        self.directpower_layout.addRow(self.directpower_interval_label,
                                       self.directpower_interval_lineedit)
        self.powertype_stackedwidget.addWidget(self.directpower_widget)
        # PRO 800 cross power widget including it's child widget and layout
        self.crosspower_widget = QtWidgets.QWidget()
        self.crosspower_widget.setObjectName('crosspower_widget')
        self.crosspower_layout = QtWidgets.QFormLayout(self.crosspower_widget)
        self.crosspower_layout.setObjectName('crosspower_layout')
        self.crosspower_count_label = QtWidgets.QLabel()
        self.crosspower_count_label.setObjectName('crosspower_count_label')
        self.crosspower_count_lineedit = QtWidgets.QLineEdit()
        self.crosspower_count_lineedit.setObjectName(
            'crosspower_count_lineedit')
        self.crosspower_layout.addRow(self.crosspower_count_label,
                                      self.crosspower_count_lineedit)
        self.crosspower_address_label = QtWidgets.QLabel()
        self.crosspower_address_label.setObjectName('crosspower_address_labe')
        self.crosspower_address_lineedit = QtWidgets.QLineEdit()
        self.crosspower_address_lineedit.setObjectName(
            'crosspower_address_lineedit')
        self.crosspower_layout.addRow(self.crosspower_address_label,
                                      self.crosspower_address_lineedit)
        self.crosspower_on_keyvalue_label = QtWidgets.QLabel()
        self.crosspower_on_keyvalue_label.setObjectName(
            'crosspower_on_keyvalue_label')
        self.crosspower_on_keyvalue_lineedit = QtWidgets.QLineEdit()
        self.crosspower_on_keyvalue_lineedit.setObjectName(
            'crosspower_on_keyvalue_lineedit')
        self.crosspower_layout.addRow(self.crosspower_on_keyvalue_label,
                                      self.crosspower_on_keyvalue_lineedit)
        self.crosspower_off_keyvalue_label = QtWidgets.QLabel()
        self.crosspower_off_keyvalue_label.setObjectName(
            'crosspower_off_keyvalue_label')
        self.crosspower_off_keyvalue_lineedit = QtWidgets.QLineEdit()
        self.crosspower_off_keyvalue_lineedit.setObjectName(
            'crosspower_off_keyvalue_lineedit')
        self.crosspower_layout.addRow(self.crosspower_off_keyvalue_label,
                                      self.crosspower_off_keyvalue_lineedit)
        self.crosspower_interval_label = QtWidgets.QLabel()
        self.crosspower_interval_label.setObjectName(
            'crosspower_interval_label')
        self.crosspower_interval_lineedit = QtWidgets.QLineEdit()
        self.crosspower_interval_lineedit.setObjectName(
            'crosspower_interval_lineedit')
        self.crosspower_layout.addRow(self.crosspower_interval_label,
                                      self.crosspower_interval_lineedit)
        self.powertype_stackedwidget.addWidget(self.crosspower_widget)
        # Power type combobox including it's child and layout
        self.powertype_combobox = QtWidgets.QComboBox()
        self.powertype_combobox.setObjectName('powertype_combobox')
        self.powertype_layout.addWidget(self.powertype_combobox)
        self.powertype_combobox.addItem('')
        self.powertype_combobox.addItem('')
        self.powertype_combobox.addItem('')
        self.controlsettings_tabwidget.addTab(self.powertype_widget, '')

        # Camera Setting's widget including it's child and layout
        self.camerasettings_widget = QtWidgets.QWidget()
        self.camerasettings_widget.setObjectName('camerasettings_widget')
        # self.main_layout.addWidget(self.camerasetting_groupbox)
        self.camerasetting_layout = QtWidgets.QVBoxLayout(
            self.camerasettings_widget)
        self.camerasetting_layout.setObjectName('camerasetting_layout')
        self.cameratable_tablewidget = QtWidgets.QTableWidget()
        self.cameratable_tablewidget.setObjectName('cameratable_tablewidget')
        self.cameratable_tablewidget.setColumnCount(3)
        self.cameratable_tablewidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.cameratable_tablewidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cameratable_tablewidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.cameratable_tablewidget.setHorizontalHeaderItem(2, item)
        self.cameratable_tablewidget.hideColumn(2)
        self.camerasetting_layout.addWidget(self.cameratable_tablewidget)
        # Camera buttons using QHBoxLayout
        self.camerabuttons_layout = QtWidgets.QHBoxLayout()
        self.camerabuttons_layout.setObjectName('camerabuttons_layout')
        self.refreshcamera_pushbutton = QtWidgets.QPushButton()
        self.refreshcamera_pushbutton.setObjectName(
            'refreshcameratable_pushbutton')
        self.camerabuttons_layout.addWidget(self.refreshcamera_pushbutton)
        self.opencamera_pushbutton = QtWidgets.QPushButton()
        self.opencamera_pushbutton.setObjectName('opencamera_pushbutton')
        self.camerabuttons_layout.addWidget(self.opencamera_pushbutton)
        self.capturestd_pushbutton = QtWidgets.QPushButton()
        self.capturestd_pushbutton.setObjectName('capturestd_pushbutton')
        self.camerabuttons_layout.addWidget(self.capturestd_pushbutton)
        self.camerasetting_layout.addLayout(self.camerabuttons_layout)
        self.controlsettings_tabwidget.addTab(self.camerasettings_widget, '')

        # Widgets including comport settings
        self.comportsettings_widget = QtWidgets.QWidget()
        self.comportsettings_widget.setObjectName('comportsettings_widget')
        self.comportsettings_layout = QtWidgets.QHBoxLayout(
            self.comportsettings_widget)
        self.comportsettings_layout.setObjectName('comportsettings_layout')
        self.refreshcomport_pushbutton = QtWidgets.QPushButton()
        self.refreshcomport_pushbutton.setObjectName('refreshport_pushbutton')
        self.comportsettings_layout.addWidget(self.refreshcomport_pushbutton)
        self.comport_combobox = QtWidgets.QComboBox()
        self.comport_combobox.setObjectName('comport_combobox')
        self.comportsettings_layout.addWidget(self.comport_combobox)
        self.opencomport_pushbutton = QtWidgets.QPushButton()
        self.opencomport_pushbutton.setObjectName('opencomport_pushbutton')
        self.comportsettings_layout.addWidget(self.opencomport_pushbutton)
        self.controlsettings_tabwidget.addTab(self.comportsettings_widget, '')

        # Widgets including test result directory setting
        self.resultdir_widget = QtWidgets.QWidget()
        self.resultdir_widget.setObjectName('resultdir_widget')
        self.resultdir_layout = QtWidgets.QHBoxLayout(self.resultdir_widget)
        self.resultdir_layout.setObjectName('resultdir_layout')
        self.resultdir_pushbutton = QtWidgets.QPushButton()
        self.resultdir_pushbutton.setObjectName('resultdir_pushbutton')
        self.resultdir_layout.addWidget(self.resultdir_pushbutton)
        self.resultdir_linedit = QtWidgets.QLineEdit()
        self.resultdir_linedit.setObjectName('resultdir_linedit')
        self.resultdir_layout.addWidget(self.resultdir_linedit)
        self.controlsettings_tabwidget.addTab(self.resultdir_widget, '')

        # Widget about start supervision and look test result
        self.start_supervision_layout = QtWidgets.QHBoxLayout()
        self.start_supervision_layout.setObjectName('start_supervision_layout')
        self.start_supervision_pushbutton = QtWidgets.QPushButton()
        self.start_supervision_layout.addStretch()
        self.start_supervision_pushbutton.setObjectName(
            'start_supervision_pushbutton')
        self.start_supervision_layout.addWidget(
            self.start_supervision_pushbutton)
        self.start_supervision_layout.addStretch()
        self.look_result_pushbutton = QtWidgets.QPushButton()
        self.look_result_pushbutton.setObjectName('look_result_pushbutton')
        self.start_supervision_layout.addWidget(self.look_result_pushbutton)
        self.start_supervision_layout.addStretch()

        self.controlsettings_layout.addLayout(self.start_supervision_layout)

        self.main_layout.addWidget(self.controlsettings_groupbox, 0, 0, 1, 1)

        # Display standard image widgets
        self.standardimg_tabwidget = QtWidgets.QTabWidget()
        self.standardimg_tabwidget.setObjectName('standardimg_tabwidget')

        self.main_layout.addWidget(self.standardimg_tabwidget, 0, 1, 1, 1)

        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 2)

        form.setLayout(self.main_layout)
        self.retranslateUi(form)
        self.powertype_stackedwidget.setCurrentIndex(0)
        self.powertype_combobox.currentIndexChanged.connect(
            self.powertype_stackedwidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate('Form', 'TvSupervision'))
        self.controlsettings_groupbox.setTitle(_translate('Form', '设置'))

        self.controlsettings_tabwidget.setTabText(0, _translate('Form',
                                                                '开关机类型'))
        self.controlsettings_tabwidget.setTabText(1, _translate('Form',
                                                                '摄像头'))
        self.controlsettings_tabwidget.setTabText(2, _translate('Form',
                                                                '串口'))
        self.controlsettings_tabwidget.setTabText(3, _translate('Form',
                                                                '结果路径'))

        self.powerbox_count_label.setText(_translate('Form', '开关机次数'))
        self.powerbox_interval_label.setText(_translate('Form', '拍摄时间间隔'))
        self.directpower_count_label.setText(_translate('Form', '开关机次数'))
        self.directpower_offtime_label.setText(_translate('Form', '关机时间'))
        self.directpower_keyvalue_label.setText(_translate('Form', '电源键值'))
        self.directpower_interval_label.setText((_translate('Form', '拍摄时间间隔')))
        self.crosspower_count_label.setText((_translate('Form', '开关机次数')))
        self.crosspower_address_label.setText((_translate('Form', '继电器地址')))
        self.crosspower_on_keyvalue_label.setText((_translate('Form', '开机键值')))
        self.crosspower_off_keyvalue_label.setText((_translate('Form', '关机键值')))
        self.crosspower_interval_label.setText(_translate('Form', '拍摄时间间隔'))
        self.powertype_combobox.setItemText(0, _translate('Form', '电源箱交流'))
        self.powertype_combobox.setItemText(1, _translate('Form', '红外直流'))
        self.powertype_combobox.setItemText(2, _translate('Form', 'PRO800交流'))

        item = self.cameratable_tablewidget.horizontalHeaderItem(0)
        item.setText(_translate('Form', 'Tag'))
        item = self.cameratable_tablewidget.horizontalHeaderItem(1)
        item.setText(_translate('Form', 'Name'))
        item = self.cameratable_tablewidget.horizontalHeaderItem(2)
        item.setText(_translate('Form', 'ID'))
        self.refreshcamera_pushbutton.setText(_translate('Form', '刷新列表'))
        self.opencamera_pushbutton.setText(_translate('Form', '打开摄像头'))
        self.capturestd_pushbutton.setText(_translate('Form', '拍摄标准图'))

        self.refreshcomport_pushbutton.setText(_translate('Form', '刷新'))
        self.opencomport_pushbutton.setText(_translate('Form', '打开COM'))

        self.resultdir_pushbutton.setText(_translate('Form', '选择路径'))
        self.start_supervision_pushbutton.setText(_translate('Form', '开始监控'))
        self.look_result_pushbutton.setText(_translate('Form', '查看报告'))
