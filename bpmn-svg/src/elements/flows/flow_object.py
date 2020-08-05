#!/usr/bin/env python3
'''
'''
from pysvg.builders import *
from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *

from util.geometry import Point

from util.logger import *
from util.svg_util import *

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

class FlowObject(BpmnElement):
    def __init__(self, flow_type):
        self.theme = self.current_theme['flows'][flow_type]

    def connect_within_channel(self, head_node, tail_node, label):
        # TODO: it is a quick hack connecting head's right snap-point with tail's left snap-point
        east_of_head = head_node['xy'] + head_node['snaps']['east']
        west_of_tail = tail_node['xy'] + tail_node['snaps']['west']

        points = [east_of_head, west_of_tail]

        edge_svg, edge_width, edge_height = a_path_with_label(points=points, label=label, spec=self.theme)

        edge_spec = {'width': edge_width, 'height': edge_height}
        return SvgElement(edge_spec, edge_svg)
