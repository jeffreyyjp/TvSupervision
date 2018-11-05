#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/15
"""

import os
import xml.dom.minidom as dom

from docs import conf

__all__ = ['SummaryReport', 'CameraReport']


def remove_empty(file_name):
    """
    This func is used for removing empty lines in xml file.
    :param file_name:
    :return: None
    """
    empty_line = '\t\n'
    result = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if empty_line in line:
                continue
            elif len(line) == 1:
                continue
            result.append(line)
    file_result = ''.join(result)
    with open(file_name, 'w') as f:
        f.write(file_result)


class SummaryReport(object):
    """
    Object that represents summary's report
    """

    def __init__(self, camera_reports, report_name, initialize_time):
        self.camera_reports = camera_reports
        self.report_name = report_name
        self.initialize(initialize_time)

    def initialize(self, initialize_time):
        report_doc = dom.Document()
        pi_node = report_doc.createProcessingInstruction(
            target='xml-stylesheet',
            data='type="text/xsl" '
                 'href="../utils/detail.xsl"')
        report_doc.appendChild(pi_node)
        root_element = report_doc.createElement('body')
        report_doc.appendChild(root_element)
        details_element = report_doc.createElement('Details')
        root_element.appendChild(details_element)
        details_element.setAttribute('time', initialize_time)
        for camera_report in self.camera_reports:
            detail_element = report_doc.createElement('Detail')
            details_element.appendChild(detail_element)
            for attr in camera_report.summary_attr:
                detail_element.setAttribute(attr,
                                            str(camera_report.summary_attr[
                                                    attr]))
        with open(self.report_name, 'w') as f:
            report_doc.writexml(f, indent='', addindent='\t', newl='\n',
                                encoding='UTF-8')

    def update(self):
        report_doc = dom.parse(self.report_name)
        detail_elements = report_doc.getElementsByTagName('Detail')
        for camera_report in self.camera_reports:
            camera_report.update_summary_details()
            for detail_element in detail_elements:
                if detail_element.getAttribute('cameraName') != \
                        camera_report.camera_name:
                    continue
                for attr in camera_report.summary_attr:
                    detail_element.setAttribute(attr,
                                                str(camera_report.summary_attr[
                                                        attr]))
        with open(self.report_name, 'w') as f:
            report_doc.writexml(f, indent='', addindent='\t', newl='\n',
                                encoding='UTF-8')
        remove_empty(self.report_name)


class CameraReport(object):
    """
    Object that represents camera's report
    """

    def __init__(self, camera, basedir):
        self.camera = camera
        self.camera_name = '_'.join([self.camera.tag(), self.camera.name()])
        self.result_dir = os.path.join(basedir, self.camera_name)
        self.report_name = os.path.join(self.result_dir, conf.DETAILS_REPORT)
        self.pass_times = 0
        self.fail_times = 0
        self.total_times = 0
        self.curr_supervision_time = 0
        self.snap_time = 0
        self.current_time = 0
        self.fileSrc = os.path.join('.', self.camera_name, conf.DETAILS_REPORT)
        self.img_src = None
        self.diff_state = False
        self.diff_percent = 0
        self.camera_attr = None
        self.summary_attr = {'cameraName': self.camera_name,
                             'passTimes': self.pass_times,
                             'failTimes': self.fail_times,
                             'totalTimes': self.total_times,
                             'fileSrc': self.fileSrc}
        self.initialize()

    def save_standard_img(self):
        self.camera.standard_img().save(os.path.join(self.result_dir,
                                                     conf.STANDARD_IMG))

    def save_current_img(self):
        self.camera.current_frame().save(os.path.join(self.result_dir,
                                                      self.img_src))
    def initialize(self):
        if not os.path.exists(self.result_dir):
            os.mkdir(self.result_dir)
        report_doc = dom.Document()
        pi_node = report_doc.createProcessingInstruction(
            target='xml-stylesheet',
            data='type="text/xsl" '
                 'href="../utils/detail.xsl"')
        report_doc.appendChild(pi_node)
        root_element = report_doc.createElement('body')
        report_doc.appendChild(root_element)
        results_element = report_doc.createElement('Results')
        root_element.appendChild(results_element)
        results_element.setAttribute('cameraName', self.camera_name)
        with open(self.report_name, 'w') as f:
            report_doc.writexml(f, indent='', addindent='\t', newl='\n',
                                encoding='UTF-8')

    def update_summary_details(self):
        self.total_times = self.pass_times + self.fail_times
        self.summary_attr = {'cameraName': self.camera_name,
                             'passTimes': self.pass_times,
                             'failTimes': self.fail_times,
                             'totalTimes': self.total_times,
                             'fileSrc': self.fileSrc}

    def update_camera_details(self):
        self.camera_attr = {'currSupervisionTime': self.curr_supervision_time,
                            'snapTime': self.snap_time,
                            'currentTime': self.current_time,
                            'diffPercent': self.diff_percent,
                            'state': self.diff_state,
                            'imgSrc': self.img_src}


    def update(self):
        self.update_camera_details()
        report_doc = dom.parse(self.report_name)
        results_element = report_doc.getElementsByTagName('Results')[0]
        result_element = report_doc.createElement('Result')
        results_element.appendChild(result_element)
        for attr in self.camera_attr:
            result_element.setAttribute(attr, str(self.camera_attr[attr]))
        with open(self.report_name, 'w') as f:
            report_doc.writexml(f, indent='', addindent='\t', newl='\n',
                                encoding='UTF-8')
        remove_empty(self.report_name)
