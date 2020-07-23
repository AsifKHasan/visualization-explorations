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

from elements.swims.pool_group import PoolGroup

class SwimLane(BpmnElement):
    # a horizontal lane is a narrow rectangle having a center-aligned text 90 degree anti-clockwise rotated at left and another adjacent rectangle () on its right containing Pool elements stacked vertically
    def __init__(self, bpmn_id, lane_id, lane_data):
        self.theme = self.current_theme['SwimLane']
        self.bpmn_id, self.lane_id, self.lane_data = bpmn_id, lane_id, lane_data

    def tune_elements(self):
        info('..tuning lane [{0}:{1}]'.format(self.bpmn_id, self.lane_id))
        info('..tuning lane [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))

    def collect_elements(self):
        info('..processing lane [{0}:{1}]'.format(self.bpmn_id, self.lane_id))
        # get the pool group
        self.child_element_class = PoolGroup(self.bpmn_id, self.lane_id, self.lane_data['pools'])
        self.child_element_class.collect_elements()

        # we need the height of the pool group
        pool_group_height = self.child_element_class.get_height()

        # get the lane text rect, its min_width and max_width is the pool group's height
        self.lane_text_svg_element = self.get_lane_text_svg_element(pool_group_height, pool_group_height)
        info('..processing lane [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))

    def assemble_elements(self):
        info('..assembling lane [{0}:{1}]'.format(self.bpmn_id, self.lane_id))
        # wrap it in a svg group
        group_id = '{0}:{1}'.format(self.bpmn_id, self.lane_id)
        svg_group = G(id=group_id)

        # a lane's width is lane text width + pool group width + some padding
        pool_group_svg_element = self.child_element_class.assemble_elements()

        group_height = pool_group_svg_element.specs['height'] + self.theme['lane-rect']['pad-spec']['top'] + self.theme['lane-rect']['pad-spec']['bottom']
        group_width = self.lane_text_svg_element.specs['width'] + pool_group_svg_element.specs['width'] + self.theme['lane-rect']['pad-spec']['left'] + self.theme['lane-rect']['pad-spec']['right']

        # add the lane ractangle
        lane_rect_svg = Rect(width=group_width, height=group_height)
        lane_rect_svg.set_style(StyleBuilder(self.theme['lane-rect']['style']).getStyle())

        lane_text_svg = self.lane_text_svg_element.group
        pool_group_svg = pool_group_svg_element.group

        # add the lane text svg
        lane_text_svg_xy = '{0},{1}'.format(self.theme['lane-rect']['pad-spec']['left'], self.theme['lane-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(lane_text_svg_xy)
        lane_text_svg.set_transform(transformer.getTransform())

        # add the pool group svg
        pool_group_svg_xy = '{0},{1}'.format(self.theme['lane-rect']['pad-spec']['left'] + self.lane_text_svg_element.specs['width'], self.theme['lane-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(pool_group_svg_xy)
        pool_group_svg.set_transform(transformer.getTransform())

        svg_group.addElement(lane_rect_svg)
        svg_group.addElement(lane_text_svg)
        svg_group.addElement(pool_group_svg)

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}

        info('..assembling lane [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))
        return SvgElement(group_specs, svg_group)

    def get_pool_group_svg_element(self):
        return pool_group_svg_element

    def get_lane_text_svg_element(self, min_width, max_width):
        # wrap in a svg group
        group_id = '{0}:{1}-text'.format(self.bpmn_id, self.lane_id)
        svg_group = G(id=group_id)

        # get the svg list of the text, first elemnt is the rect, second element is the text
        svg_list = rect_with_text(text=self.lane_data['label'],
                                    min_width=min_width,
                                    max_width=max_width,
                                    specs=self.theme['text-rect'])

        rect_svg = svg_list[0]
        text_svg = svg_list[1]

        # place the node rect
        svg_group.addElement(rect_svg)

        # place the node text
        svg_group.addElement(text_svg)

        group_width = rect_svg.get_width()
        group_height = rect_svg.get_height()

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}
        return SvgElement(group_specs, svg_group)
