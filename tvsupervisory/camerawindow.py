# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camerawindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Video(object):
    def setupUi(self, Video):
        Video.setObjectName("Video")
        Video.resize(774, 445)
        self.gridLayout = QtWidgets.QGridLayout(Video)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Video)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Video)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Video)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(Video)
        self.label_4.setStyleSheet("QLabel {border: 1px solid blank; }")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Video)
        self.label_5.setStyleSheet("QLabel {border: 1px solid blank; }")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)
        self.video_widget = QtWidgets.QWidget(Video)
        self.video_widget.setStyleSheet("QWidget {border: 1px solid blank; }")
        self.video_widget.setObjectName("video_widget")
        self.gridLayout.addWidget(self.video_widget, 1, 0, 1, 1)

        self.retranslateUi(Video)
        QtCore.QMetaObject.connectSlotsByName(Video)

    def retranslateUi(self, Video):
        _translate = QtCore.QCoreApplication.translate
        Video.setWindowTitle(_translate("Video", "Form"))
        self.label.setText(_translate("Video", "拍摄图像"))
        self.label_2.setText(_translate("Video", "标准图像"))
        self.label_3.setText(_translate("Video", "对比结果"))

