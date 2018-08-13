#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/8/13
"""

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
        form.resize(640, 480)
        font = QtGui.QFont()
        font.setFamily('微软雅黑')
        form.setFont(font)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('../docs/images/tv.jpg'),
                       QtGui.QIcon.Normal, QtGui.QIcon.On)
        form.setWindowIcon(icon)

        # Power type including widgets and layout.
        self.powertype_groupbox = QtWidgets.QGroupBox(form)
        self.powertype_groupbox.setObjectName('powertype_groupbox')
        self.powertype_layout = QtWidgets.QVBoxLayout(self.powertype_groupbox)
        self.powertype_layout.setObjectName('powertype_layout')
        self.powertype_stackedwidget = QtWidgets.QStackedWidget(
            self.powertype_groupbox)
        self.powertype_stackedwidget.setObjectName('powertype_stackedwidget')
        # Power box widget including it's child widget and layout
        self.powerbox_widget = QtWidgets.QWidget()
        self.powerbox_widget.setObjectName('powerbox_widget')
        self.powerbox_layout = QtWidgets.QFormLayout(self.powerbox_widget)
        self.powerbox_layout.setObjectName('powerbox_layout')
        self.powerbox_count_label = QtWidgets.QLabel(self.powerbox_widget)
        self.powerbox_count_label.setObjectName('powerbox_count_label')
        self.powerbox_count_lineedit = QtWidgets.QLineEdit(
            self.powerbox_widget)
        self.powerbox_count_lineedit.setObjectName('powerbox_count_lineedit')
        self.powerbox_layout.addRow(self.powerbox_count_label,
                                    self.powerbox_count_lineedit)
        self.powerbox_interval_label = QtWidgets.QLabel(self.powerbox_widget)
        self.powerbox_interval_label.setObjectName('powerbox_interval_label')
        self.powerbox_interval_lineedit = QtWidgets.QLineEdit(
            self.powerbox_widget)
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
        self.directpower_count_label = QtWidgets.QLabel(self.directpower_widget)
        self.directpower_count_label.setObjectName('directpower_count_label')
        self.directpower_count_lineedit = QtWidgets.QLineEdit(
            self.directpower_widget)
        self.directpower_count_lineedit.setObjectName(
            'directpower_count_lineedit')
        self.directpower_layout.addRow(self.directpower_count_label,
                                       self.directpower_count_lineedit)
        self.directpower_offtime_label = QtWidgets.QLabel(
            self.directpower_widget)
        self.directpower_offtime_label.setObjectName(
            'directpower_offtime_label')
        self.directpower_offtime_lineedit = QtWidgets.QLineEdit(
            self.directpower_widget)
        self.directpower_offtime_lineedit.setObjectName(
            'directpower_offtime_lineedit')
        self.directpower_layout.addRow(self.directpower_offtime_label,
                                       self.directpower_offtime_lineedit)
        self.directpower_keyvalue_label = QtWidgets.QLabel(self.directpower_widget)
        self.directpower_keyvalue_label.setObjectName('directpower_keyvalue_label')

