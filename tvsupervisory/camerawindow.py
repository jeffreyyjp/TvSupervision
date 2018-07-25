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
        self.lbl_std_image = QtWidgets.QLabel(Video)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_std_image.sizePolicy().hasHeightForWidth())
        self.lbl_std_image.setSizePolicy(sizePolicy)
        self.lbl_std_image.setStyleSheet("QLabel {border: 1px solid blank; }")
        self.lbl_std_image.setText("")
        self.lbl_std_image.setObjectName("lbl_std_image")
        self.gridLayout.addWidget(self.lbl_std_image, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Video)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setStyleSheet("QLabel {border: 1px solid blank; }")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)
        self.video_window = QtWidgets.QWidget(Video)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_window.sizePolicy().hasHeightForWidth())
        self.video_window.setSizePolicy(sizePolicy)
        self.video_window.setStyleSheet("QWidget {border: 1px solid blank; }")
        self.video_window.setObjectName("video_window")
        self.gridLayout.addWidget(self.video_window, 1, 0, 1, 1)

        self.retranslateUi(Video)
        QtCore.QMetaObject.connectSlotsByName(Video)

    def retranslateUi(self, Video):
        _translate = QtCore.QCoreApplication.translate
        Video.setWindowTitle(_translate("Video", "Form"))
        self.label.setText(_translate("Video", "拍摄图像"))
        self.label_2.setText(_translate("Video", "标准图像"))
        self.label_3.setText(_translate("Video", "对比结果"))

