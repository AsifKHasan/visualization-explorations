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

from util.logger import *
from util.svg_util import *

from elements.svg_element import SvgElement
from elements.datas.data_object import DataObject

class DataInputCollection(DataObject):
    # a task activity is a rounded rectangle with a text inside
    def __init__(self, current_theme, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(current_theme, bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['datas']['DataInputCollection']}

    def get_top_left_element(self):
        width = self.theme['top-left-inner-shape']['width']
        height = self.theme['top-left-inner-shape']['height']
        svg_group, group_width, group_height = a_right_arrow(width=width, height=height, spec=self.theme['top-left-inner-shape'])
        return SvgElement(svg=svg_group, width=group_width, height=group_height)

    def get_bottom_center_element(self):
        width = self.theme['bottom-center-inner-shape']['width']
        height = self.theme['bottom-center-inner-shape']['height']
        svg_group, group_width, group_height = three_bars(width=width, height=height, spec=self.theme['bottom-center-inner-shape'])
        return SvgElement(svg=svg_group, width=group_width, height=group_height)
