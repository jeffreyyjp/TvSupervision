# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1041, 594)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        Form.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../.designer/backup/res/tv.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.capture_std_btn = QtWidgets.QPushButton(self.groupBox)
        self.capture_std_btn.setObjectName("capture_std_btn")
        self.gridLayout.addWidget(self.capture_std_btn, 1, 3, 1, 1)
        self.camera_list = QtWidgets.QTableWidget(self.groupBox)
        self.camera_list.setColumnCount(2)
        self.camera_list.setObjectName("camera_list")
        self.camera_list.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.camera_list.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.camera_list.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.camera_list, 0, 0, 1, 4)
        self.refresh_camera_list_btn = QtWidgets.QPushButton(self.groupBox)
        self.refresh_camera_list_btn.setObjectName("refresh_camera_list_btn")
        self.gridLayout.addWidget(self.refresh_camera_list_btn, 1, 1, 1, 1)
        self.add_camera_btn = QtWidgets.QPushButton(self.groupBox)
        self.add_camera_btn.setObjectName("add_camera_btn")
        self.gridLayout.addWidget(self.add_camera_btn, 1, 2, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_22 = QtWidgets.QLabel(Form)
        self.label_22.setText("")
        self.label_22.setObjectName("label_22")
        self.verticalLayout_2.addWidget(self.label_22)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_24 = QtWidgets.QLabel(Form)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_3.addWidget(self.label_24)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_23 = QtWidgets.QLabel(Form)
        self.label_23.setText("")
        self.label_23.setObjectName("label_23")
        self.verticalLayout_3.addWidget(self.label_23)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.label_25 = QtWidgets.QLabel(Form)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_4.addWidget(self.label_25)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 1, 2, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.stackedWidget = QtWidgets.QStackedWidget(self.groupBox_2)
        self.stackedWidget.setObjectName("stackedWidget")
        self.power_box = QtWidgets.QWidget()
        self.power_box.setObjectName("power_box")
        self.formLayout = QtWidgets.QFormLayout(self.power_box)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.power_box)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txt_box_num = QtWidgets.QLineEdit(self.power_box)
        self.txt_box_num.setObjectName("txt_box_num")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_box_num)
        self.label_2 = QtWidgets.QLabel(self.power_box)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.txt_box_interval = QtWidgets.QLineEdit(self.power_box)
        self.txt_box_interval.setObjectName("txt_box_interval")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_box_interval)
        self.stackedWidget.addWidget(self.power_box)
        self.direct_power = QtWidgets.QWidget()
        self.direct_power.setObjectName("direct_power")
        self.formLayout_2 = QtWidgets.QFormLayout(self.direct_power)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(self.direct_power)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.txt_direct_num = QtWidgets.QLineEdit(self.direct_power)
        self.txt_direct_num.setObjectName("txt_direct_num")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_direct_num)
        self.label_4 = QtWidgets.QLabel(self.direct_power)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.txt_direct_off_time = QtWidgets.QLineEdit(self.direct_power)
        self.txt_direct_off_time.setObjectName("txt_direct_off_time")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_direct_off_time)
        self.label_5 = QtWidgets.QLabel(self.direct_power)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.txt_direct_power_key = QtWidgets.QLineEdit(self.direct_power)
        self.txt_direct_power_key.setObjectName("txt_direct_power_key")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_direct_power_key)
        self.label_6 = QtWidgets.QLabel(self.direct_power)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.txt_direct_interval = QtWidgets.QLineEdit(self.direct_power)
        self.txt_direct_interval.setObjectName("txt_direct_interval")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.txt_direct_interval)
        self.stackedWidget.addWidget(self.direct_power)
        self.pro800_power = QtWidgets.QWidget()
        self.pro800_power.setObjectName("pro800_power")
        self.formLayout_3 = QtWidgets.QFormLayout(self.pro800_power)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_7 = QtWidgets.QLabel(self.pro800_power)
        self.label_7.setObjectName("label_7")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.txt_cross_num = QtWidgets.QLineEdit(self.pro800_power)
        self.txt_cross_num.setObjectName("txt_cross_num")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_cross_num)
        self.label_8 = QtWidgets.QLabel(self.pro800_power)
        self.label_8.setObjectName("label_8")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.txt_cross_address = QtWidgets.QLineEdit(self.pro800_power)
        self.txt_cross_address.setObjectName("txt_cross_address")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_cross_address)
        self.label_9 = QtWidgets.QLabel(self.pro800_power)
        self.label_9.setObjectName("label_9")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.txt_cross_on_key = QtWidgets.QLineEdit(self.pro800_power)
        self.txt_cross_on_key.setObjectName("txt_cross_on_key")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_cross_on_key)
        self.label_10 = QtWidgets.QLabel(self.pro800_power)
        self.label_10.setObjectName("label_10")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.txt_cross_off_key = QtWidgets.QLineEdit(self.pro800_power)
        self.txt_cross_off_key.setObjectName("txt_cross_off_key")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.txt_cross_off_key)
        self.label_21 = QtWidgets.QLabel(self.pro800_power)
        self.label_21.setObjectName("label_21")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_21)
        self.txt_cross_interval = QtWidgets.QLineEdit(self.pro800_power)
        self.txt_cross_interval.setObjectName("txt_cross_interval")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.txt_cross_interval)
        self.stackedWidget.addWidget(self.pro800_power)
        self.gridLayout_5.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_5.addWidget(self.comboBox, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.result_dir_txt = QtWidgets.QLineEdit(self.groupBox_3)
        self.result_dir_txt.setObjectName("result_dir_txt")
        self.gridLayout_6.addWidget(self.result_dir_txt, 0, 0, 1, 2)
        self.result_dir_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.result_dir_btn.setObjectName("result_dir_btn")
        self.gridLayout_6.addWidget(self.result_dir_btn, 0, 2, 1, 2)
        self.refresh_port_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.refresh_port_btn.setObjectName("refresh_port_btn")
        self.gridLayout_6.addWidget(self.refresh_port_btn, 1, 0, 1, 1)
        self.port_lists_combox = QtWidgets.QComboBox(self.groupBox_3)
        self.port_lists_combox.setObjectName("port_lists_combox")
        self.gridLayout_6.addWidget(self.port_lists_combox, 1, 1, 1, 2)
        self.open_port_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.open_port_btn.setObjectName("open_port_btn")
        self.gridLayout_6.addWidget(self.open_port_btn, 1, 3, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_6.addWidget(self.pushButton_2)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_6.addWidget(self.pushButton_3)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 2, 1, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 3)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        self.comboBox.currentIndexChanged['int'].connect(self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "TvPowerOnOffSupervisory"))
        self.groupBox.setTitle(_translate("Form", "CameraSetting"))
        self.capture_std_btn.setText(_translate("Form", "拍摄标准图"))
        item = self.camera_list.horizontalHeaderItem(0)
        item.setText(_translate("Form", "ID"))
        item = self.camera_list.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Name"))
        self.refresh_camera_list_btn.setText(_translate("Form", "刷新列表"))
        self.add_camera_btn.setText(_translate("Form", "添加摄像头"))
        self.label_24.setText(_translate("Form", "标准图"))
        self.label_25.setText(_translate("Form", "对比图"))
        self.groupBox_2.setTitle(_translate("Form", "PowerType"))
        self.label.setText(_translate("Form", "开关机次数"))
        self.label_2.setText(_translate("Form", "拍摄时间间隔"))
        self.label_3.setText(_translate("Form", "开关机次数"))
        self.label_4.setText(_translate("Form", "关机时间"))
        self.label_5.setText(_translate("Form", "电源键值"))
        self.label_6.setText(_translate("Form", "拍摄时间间隔"))
        self.label_7.setText(_translate("Form", "开关机次数"))
        self.label_8.setText(_translate("Form", "继电器地址"))
        self.label_9.setText(_translate("Form", "开机键值"))
        self.label_10.setText(_translate("Form", "关机键值"))
        self.label_21.setText(_translate("Form", "拍摄时间间隔"))
        self.comboBox.setItemText(0, _translate("Form", "电源箱交流"))
        self.comboBox.setItemText(1, _translate("Form", "红外直流"))
        self.comboBox.setItemText(2, _translate("Form", "PRO800交流"))
        self.groupBox_3.setTitle(_translate("Form", "BasicSetting"))
        self.result_dir_btn.setText(_translate("Form", "结果路径"))
        self.refresh_port_btn.setText(_translate("Form", "刷新"))
        self.open_port_btn.setText(_translate("Form", "打开COM"))
        self.pushButton_2.setText(_translate("Form", "开始监控"))
        self.pushButton_3.setText(_translate("Form", "查看报告"))

