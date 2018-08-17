#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/8/1
"""

# import
import serial.tools.list_ports as list_ports


def get_comports_name():
    com_list = list_ports.comports()
    port_name_list = []
    for port_item in com_list:
        port_name_list.append(port_item[0])
    return sorted(port_name_list)


if __name__ == '__main__':
    print(get_comports_name())
