#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/15
"""

import os
import xml.dom.minidom as dom

from docs import conf


def reset_xml(file_name):
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

    def __init__(self, camera_reports):
        self.camera_reports = camera_reports
        self.report_name = None

    def initialize_summary_report(self, initialize_time):
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
        for item in self.camera_reports:
            detail_element = report_doc.createElement('Detail')
            details_element.appendChild(detail_element)
            for attr in item.summary_attr.keys():
                detail_element.setAttribute(attr, item.summary_attr[attr])
        with open(self.report_name, 'w') as f:
            report_doc.writexml(f, indent='', addindent='\t', newl='\n',
                                encoding='UTF-8')

    def update_summary_report(self):
        report_doc = dom.parse(self.report_name)
        detail_elements = report_doc.getElementsByTagName('Detail')
        for detail in detail_elements:
            for camera_report in self.camera_reports:
                if detail.getAttribute(
                        'cameraName') != camera_report.camera_name:
                    continue
                for attr in camera_report.summary_attr.keys():
                    detail.setAttribute(attr, camera_report.summary_attr[attr])
        with open(self.report_name, 'w') as f:
            report_doc.writexml(f, indent='', addindent='\t', newl='\n',
                                encoding='UTF-8')
        reset_xml(self.report_name)


class CameraReport(object):
    """
    Object that represents camera's report
    """

    def __init__(self, camera):
        self._camera = camera
        self.camera_name = '_'.join([self._camera.tag(), self._camera.name()])
        self.result_dir = None
        self.report_name = os.path.join(self._result_dir, conf.DETAILS_REPORT)
        self.pass_times = 0
        self.fail_times = 0
        self.total_times = self.pass_times + self.fail_times
        self.fileSrc = os.path.join('.', self.camera_name, conf.DETAILS_REPORT)
        self.diff_state = False
        self.diff_percent = 0
        self.summary_attr = {'cameraName': self.camera_name, 'passTimes':
            self.pass_times, 'failTimes': self.fail_times, 'totalTimes':
                                 self.total_times, 'fileSrc': self.fileSrc}
        self.camera_attr = {'snapTimes': '0', 'currentTime': '0',
                            'cameraName': self.camera_name, 'diffPercent':
                                self.diff_percent, 'state': self.diff_state,
                            'imgSrc': ''}

    def camera(self):
        return self._camera

    def set_result_dir(self, basedir):
        self._result_dir = os.path.join(basedir, self.camera_name)

    def result_dir(self):
        return self._result_dir

    def save_standard_img(self):
        self._camera.standard_img().save(os.path.join(self._result_dir,
                                                      conf.STANDARD_IMG))

    def save_current_img(self):
        self._camera.current_frame.save(os.path.join(self._result_dir,
                                                     self.fileSrc))

    def initialize(self):
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

    def update(self):
        report_doc = dom.parse(self.report_name)
        results_element = report_doc.getElementsByTagName('Results')[0]
        result_element = report_doc.createElement('Result')
        results_element.appendChild(result_element)
        for attr in self.camera_attr.keys():
            result_element.setAttribute(attr, self.camera_attr[attr])
        with open(self.report_name, 'w') as f:
            report_doc.writexml(f, indent='', addindent='\t', newl='\n',
                                encoding='UTF-8')
        reset_xml(self.report_name)
