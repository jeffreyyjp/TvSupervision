#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/8/10
"""

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='tvsupervision',
    version = '0.0.1',
    author = 'Jeffrey Yang',
    author_email = '',
    description = 'Python tools for Tv power on and off supervisory',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url='https://github.com/messi-yang/TvSupervision',
    packages = setuptools.find_packages(),
    classifiers = {
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    }
)
