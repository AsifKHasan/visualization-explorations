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
    def __init__(self):
        self.theme = self.current_theme['SwimLane']

    def to_svg(self, bpmn_id, lane_id, lane_data):
        info('..processing lane [{0}:{1}] DONE ...'.format(bpmn_id, lane_id))

        # a horizontal lane is a narrow rectangle having a center-aligned text 90 degree anti-clockwise rotated at left and another adjacent rectangle () on its right containing Pool elements stacked vertically

        # get the pool group
        pool_group_svg_element = self.get_pool_group_svg_element(bpmn_id, lane_id, lane_data)

        # get the lane text rect, its min_width and max_width is the pool group's height
        lane_text_svg_element = self.get_lane_text_svg_element(bpmn_id, lane_id, lane_data, pool_group_svg_element.specs['height'], pool_group_svg_element.specs['height'])

        # assemble the lane svg element
        svg_element = self.assemble_element(bpmn_id, lane_id, lane_text_svg_element, pool_group_svg_element)

        info('..processing lane [{0}:{1}] DONE ...'.format(bpmn_id, lane_id))
        return svg_element

    def get_pool_group_svg_element(self, bpmn_id, lane_id, lane_data):
        pool_group = PoolGroup()
        pool_group_svg_element = pool_group.to_svg(bpmn_id, lane_id, lane_data['pools'])
        return pool_group_svg_element

    def get_lane_text_svg_element(self, bpmn_id, lane_id, lane_data, min_width, max_width):
        # wrap in a svg group
        group_id = '{0}:{1}-text'.format(bpmn_id, lane_id)
        svg_group = G(id=group_id)

        # get the svg list of the text, first elemnt is the rect, second element is the text
        svg_list = rect_with_text(text=lane_data['label'],
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

    def assemble_element(self, bpmn_id, lane_id, lane_text_svg_element, pool_group_svg_element):
        # wrap it in a svg group
        group_id = '{0}:{1}'.format(bpmn_id, lane_id)
        svg_group = G(id=group_id)

        # a lane's width is lane text width + pool group width + some padding
        group_height = pool_group_svg_element.specs['height'] + self.theme['lane-rect']['pad-spec']['top'] + self.theme['lane-rect']['pad-spec']['bottom']
        group_width = lane_text_svg_element.specs['width'] + pool_group_svg_element.specs['width'] + self.theme['lane-rect']['pad-spec']['left'] + self.theme['lane-rect']['pad-spec']['right']

        # add the lane ractangle
        lane_rect_svg = Rect(width=group_width, height=group_height)
        lane_rect_svg.set_style(StyleBuilder(self.theme['lane-rect']['style']).getStyle())

        lane_text_svg = lane_text_svg_element.group
        pool_group_svg = pool_group_svg_element.group

        # add the lane text svg
        lane_text_svg_xy = '{0},{1}'.format(self.theme['lane-rect']['pad-spec']['left'], self.theme['lane-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(lane_text_svg_xy)
        lane_text_svg.set_transform(transformer.getTransform())

        # add the pool group svg
        pool_group_svg_xy = '{0},{1}'.format(self.theme['lane-rect']['pad-spec']['left'] + lane_text_svg_element.specs['width'], self.theme['lane-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(pool_group_svg_xy)
        pool_group_svg.set_transform(transformer.getTransform())

        svg_group.addElement(lane_rect_svg)
        svg_group.addElement(lane_text_svg)
        svg_group.addElement(pool_group_svg)

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}
        return SvgElement(group_specs, svg_group)
