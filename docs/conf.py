#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/8/24
"""

# imports
from PyQt5 import QtCore

BASE_OPEN_DIR = QtCore.QStandardPaths.writableLocation(
    QtCore.QStandardPaths.DocumentsLocation)
STANDARD_IMG = 'standard.jpg'
IMG_POSTFIX = 'jpg'
SUMMARY_REPORT = 'summary_report.xml'
DETAILS_REPORT = 'details_report.xml'
