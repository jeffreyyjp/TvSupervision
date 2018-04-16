#!/usr/bin/env python
# encoding: utf-8

"""
author: Jeffrey
date: 2018/4/10
"""
import sys
import serial.tools.list_ports as list_ports
from PyQt5.QtWidgets import QApplication, QWidget
from mainwindow import Ui_Form


class MainWindow(QWidget, Ui_Form):
    """
    Setup window
    """

    def __init__(self):
        """Constructor
        """

        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.refresh_port_btn.clicked.connect(self.refresh_port)
        self.open_port_btn.clicked.connect(self.open_port)

    def refresh_port(self):
        self.port_lists_combox.clear()
        com_list = list_ports.comports()
        com_name_list = []
        for com_item in com_list:
            com_name_list.append(com_item[0])
        self.port_lists_combox.addItems(sorted(com_name_list))

    # TODO(Jeffrey): Will finish as soon as possible
    def open_port(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_()) 