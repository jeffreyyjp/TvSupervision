#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/12
"""

import cv2 as cv
import numpy as np
from PyQt5 import QtGui


def qimage2cv(image):
    """
    Construct height*width and 3 channels matrix, default pixel is 0.
    :param image:
    :return:
    """
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


def diff(standard_image, target_image, diff_rate=0.01):
    count_num = 0
    result = True
    if type(standard_image) == str:
        standard_image = cv.imread(standard_image)
    if type(target_image) == str:
        target_image = cv.imread(target_image)
    blur_image = cv.GaussianBlur(target_image, (3, 3), 0)
    diff_image = cv.absdiff(blur_image, standard_image)
    gray_image = cv.cvtColor(diff_image, cv.COLOR_BGR2GRAY)
    ret, threshold_image = cv.threshold(gray_image, 50, 255, cv.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    erode_image = cv.erode(threshold_image, kernel, iterations=3)
    dilate_image = cv.dilate(erode_image, kernel, iterations=2)
    rows, columns = dilate_image.shape
    diff_num = rows * columns * diff_rate
    for row in range(rows):
        for col in range(columns):
            pixel_value = dilate_image[row, col]
            if pixel_value != 255:
                continue
            count_num += 1
    diff_percent = count_num * 100 / (rows * columns)
    if count_num > diff_num:
        result = False
    return result, diff_percent
