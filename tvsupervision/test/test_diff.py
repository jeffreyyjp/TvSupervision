#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/17
"""
import unittest
from unittest import TestCase

from tvsupervision import image_proc

standard_img = 'StandardImg.jpeg'
current_img = '2017-12-03_08-41-14_0001.jpeg'
current_img_false = '2017-12-03_14-52-14_0319.jpeg'


class TestDiff(TestCase):
    def test_diff_true(self):
        result, diff_percent = image_proc.diff(standard_img, current_img)
        print(result, diff_percent)
        self.assertEqual(True, result)

    def test_diff_false(self):
        result, diff_percent = image_proc.diff(standard_img, current_img_false)
        print(result, diff_percent)
        self.assertEqual(False, result)


if __name__ == '__main__':
    unittest.main()
