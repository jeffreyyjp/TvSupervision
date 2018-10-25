#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/19
"""

import logging

from docs import conf

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fh = logging.FileHandler(conf.LOG_FILE)
fh.setLevel(logging.WARNING)

ch_formatter = logging.Formatter('%(module)s:%(lineno)4s %(levelname)8s - %('
                                 'message)s')
fh_formatter = logging.Formatter('%(asctime)s - %(levelname)8s - %(message)s')

ch.setFormatter(ch_formatter)
fh.setFormatter(fh_formatter)

logger.addHandler(ch)
logger.addHandler(fh)
