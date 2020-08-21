#!/usr/bin/env python3
'''
'''
from elements.bpmn_element import BpmnElement

from util.geometry import Point
from util.svg_util import *
from util.logger import *

class FlowObject(BpmnElement):
    def __init__(self, edge_type):
        self.edge_type = edge_type
        self.theme = self.current_theme['flows'][edge_type]

    def mark_points(self, points, svg, color):
        for point in points:
            svg_element, _, _ = a_snap_point(point, color)
            svg.addElement(svg_element)


''' ----------------------------------------------------------------------------------------------------------------------------------
    Edge Object
'''
class EdgeObject:
    def __init__(self, edge, type, element):
        self.edge = edge
        self.type = type
        self.element = element
