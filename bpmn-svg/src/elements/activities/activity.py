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

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

class Activity(BpmnElement):
    # a task activity is a rounded rectangle with a text inside
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.theme = self.current_theme['activities']['Activity']
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.group_id = 'N-{0}:{1}:{2}:{3}'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id)

    def to_svg(self):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # the rectangle element
        rectangle_group, rectangle_group_width, rectangle_group_height = rectangle_with_text_inside(
                                    text=self.node_data['label'],
                                    min_width=self.theme['rectangle']['min-width'],
                                    max_width=self.theme['rectangle']['max-width'],
                                    rect_specs=self.theme['rectangle'],
                                    text_specs=self.theme['text'])

        # get the inside bottom center element
        bottom_center_element = self.get_bottom_center_element()

        # if an inside bottom center element is to be placed, the element should have a gap from the rectangle bottom
        if bottom_center_element is not None:
            bottom_center_group, bottom_center_group_width, bottom_center_group_height = bottom_center_element.group, bottom_center_element.specs['width'], bottom_center_element.specs['height']
            bottom_center_group_xy = '{0},{1}'.format((rectangle_group_width - bottom_center_group_width)/2, rectangle_group_height - bottom_center_group_height - self.theme['bottom-center-rectangle']['margin-spec']['bottom'])
            transformer = TransformBuilder()
            transformer.setTranslation(bottom_center_group_xy)
            bottom_center_group.set_transform(transformer.getTransform())
            rectangle_group.addElement(bottom_center_group)

        # get the inside bottom center element
        top_left_element = self.get_top_left_element()

        # if an inside bottom center element is to be placed, the element should have a gap from the rectangle bottom
        if top_left_element is not None:
            top_left_group, top_left_group_width, top_left_group_height = top_left_element.group, top_left_element.specs['width'], top_left_element.specs['height']
            top_left_group_xy = '{0},{1}'.format(self.theme['bottom-center-rectangle']['margin-spec']['left'], self.theme['bottom-center-rectangle']['margin-spec']['top'])
            transformer = TransformBuilder()
            transformer.setTranslation(top_left_group_xy)
            top_left_group.set_transform(transformer.getTransform())
            rectangle_group.addElement(top_left_group)

        # if there is an outer rectangle process that
        if 'outer-rectangle' in self.theme:
            rectangle_group, rectangle_group_width, rectangle_group_height = envelop_and_center_in_a_rectangle(svg=rectangle_group, svg_width=rectangle_group_width, svg_height=rectangle_group_height, rect_specs=self.theme['outer-rectangle'])

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        return SvgElement({'width': rectangle_group_width, 'height': rectangle_group_height}, rectangle_group)

    def get_top_left_element(self):
        return None

    def get_bottom_center_element(self):
        return None
