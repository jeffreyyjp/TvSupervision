#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/5/14
"""

# imports
import os
import sys

from tvsupervision import main

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)
sys.path.append(base_dir)

if __name__ == '__main__':
    main.main()
