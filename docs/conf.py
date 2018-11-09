#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/8/24
"""

# imports
import os

from PyQt5 import QtCore

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_OPEN_DIR = QtCore.QStandardPaths.writableLocation(
    QtCore.QStandardPaths.DocumentsLocation)
STANDARD_IMG = 'standard.jpg'
IMG_POSTFIX = 'jpg'
SUMMARY_REPORT = 'summary_report.xml'
CAMERA_REPORT = 'camera_report.xml'
SUMMARY_REPORT_XSL = os.path.join(base_dir, 'docs/report/summary_report.xsl')
CAMERA_REPORT_XSL = os.path.join(base_dir, 'docs/report/camera_report.xsl')
STYLE_CSS = os.path.join(base_dir, 'docs/report/style.css')
LOG_FILE = 'log.txt'
