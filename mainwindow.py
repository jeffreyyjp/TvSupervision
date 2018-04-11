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
        Form.resize(975, 645)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        Form.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Res/tv.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(40, 20, 261, 191))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.cameralist = QtWidgets.QTableWidget(self.groupBox)
        self.cameralist.setColumnCount(2)
        self.cameralist.setObjectName("cameralist")
        self.cameralist.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.cameralist.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cameralist.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.cameralist, 0, 0, 1, 2)
        self.btn_add_camera = QtWidgets.QPushButton(self.groupBox)
        self.btn_add_camera.setObjectName("btn_add_camera")
        self.gridLayout.addWidget(self.btn_add_camera, 1, 0, 1, 1)
        self.btn_capture_std = QtWidgets.QPushButton(self.groupBox)
        self.btn_capture_std.setObjectName("btn_capture_std")
        self.gridLayout.addWidget(self.btn_capture_std, 1, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(50, 240, 381, 311))
        self.groupBox_2.setObjectName("groupBox_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.groupBox_2)
        self.stackedWidget.setGeometry(QtCore.QRect(30, 30, 291, 141))
        self.stackedWidget.setObjectName("stackedWidget")
        self.power_box = QtWidgets.QWidget()
        self.power_box.setObjectName("power_box")
        self.stackedWidget.addWidget(self.power_box)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(140, 260, 91, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "TvPowerOnOffSupervisory"))
        self.groupBox.setTitle(_translate("Form", "CameraSetting"))
        item = self.cameralist.horizontalHeaderItem(0)
        item.setText(_translate("Form", "ID"))
        item = self.cameralist.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Name"))
        self.btn_add_camera.setText(_translate("Form", "添加摄像头"))
        self.btn_capture_std.setText(_translate("Form", "拍摄标准图"))
        self.groupBox_2.setTitle(_translate("Form", "PowerType"))
        self.comboBox.setItemText(0, _translate("Form", "电源箱交流"))
        self.comboBox.setItemText(1, _translate("Form", "红外直流"))
        self.comboBox.setItemText(2, _translate("Form", "PRO800交流"))

