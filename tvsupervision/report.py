#!/usr/bin/python  
# -*- coding: utf-8 -*-

"""
author: Jeffrey
date: 2018/10/15
"""

import xml.dom.minidom as dom


def create_summary_report(report_name, create_time):
    report = dom.Document()
    doc_pi = dom.ProcessingInstruction(target='xml-stylesheet',
                                       data='type="text/xsl" '
                                            'href="../utils/detail.xsl"')
    report.appendChild(doc_pi)
    root_element = report.createElement('body')
    report.appendChild(root_element)
    details = report.createElement('Details')
    root_element.appendChild(details)
    details.setAttribute('time', create_time)
    with open(report_name, 'w') as f:
        report.writexml(f, indent='\t', addindent='\t', newl='\n',
                        encoding='UTF-8')


create_summary_report('test.xml', 'abc')
