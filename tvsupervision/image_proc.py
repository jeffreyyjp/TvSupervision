#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/12
"""

import numpy as np
from PyQt5 import QtGui


def qimage2cv(image):
    # Construct height*width and 3 channels matrix, default pixel is 0.
    cv_image = np.zeros((image.height(), image.width(), 3), dtype=np.uint8)

    for row in range(image.height()):
        for col in range(image.width()):
            image_rgb = QtGui.QColor(image.pixel(col, row))
            r = image_rgb.red()
            g = image_rgb.green()
            b = image_rgb.blue()
            cv_image[row, col, 0] = b
            cv_image[row, col, 1] = g
            cv_image[row, col, 2] = r
    return cv_image
