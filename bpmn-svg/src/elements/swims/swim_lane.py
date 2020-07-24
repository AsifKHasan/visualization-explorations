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

    def get_max_width_of_elements_of_children(self):
        pool_text_element_max_width, pool_block_group_max_width = self.child_element_class.get_max_width_of_elements_of_children()
        return self.lane_text_svg_element.specs['width'], pool_text_element_max_width, pool_block_group_max_width

    def tune_elements(self, tune_spec):
        info('..tuning lane [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # tune the children
        self.child_element_class.tune_elements(tune_spec)

        # lane_text_svg_element width may need some tuning
        lane_text_element_target_width = tune_spec['lane-text-element-target-width']
        self.adjust_width_lane_text_element(lane_text_element_target_width)

        info('..tuning lane [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))

    def collect_elements(self):
        info('..processing lane [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # get the pool group
        self.child_element_class = PoolGroup(self.bpmn_id, self.lane_id, self.lane_data['pools'])
        self.child_element_class.collect_elements()

        # we need the height of the pool group
        pool_group_height = self.child_element_class.get_height()

        # get the lane text rect, its min_width and max_width is the pool group's height + all
        self.lane_text_svg_element = self.get_lane_text_svg_element(pool_group_height, pool_group_height)

        info('..processing lane [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))

    def assemble_elements(self):
        info('..assembling lane [{0}:{1}]'.format(self.bpmn_id, self.lane_id))
        # wrap it in a svg group
        group_id = '{0}:{1}'.format(self.bpmn_id, self.lane_id)
        svg_group = G(id=group_id)

        pool_group_svg_element = self.child_element_class.assemble_elements()

        # the lane outline
        # a lane's width is lane text width + pool group width + some padding
        group_height = self.theme['lane-rect']['pad-spec']['top'] + pool_group_svg_element.specs['height'] + self.theme['lane-rect']['pad-spec']['bottom']
        group_width = self.theme['lane-rect']['pad-spec']['left'] + self.lane_text_svg_element.specs['width'] + self.theme['gap-between-text-and-pool-group'] + pool_group_svg_element.specs['width'] + self.theme['lane-rect']['pad-spec']['right']
        lane_outline_svg = Rect(width=group_width, height=group_height)
        lane_outline_svg.set_style(StyleBuilder(self.theme['lane-rect']['style']).getStyle())

        # the lane text svg
        lane_text_svg = self.lane_text_svg_element.group
        lane_text_svg_xy = '{0},{1}'.format(self.theme['lane-rect']['pad-spec']['left'], self.theme['lane-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(lane_text_svg_xy)
        lane_text_svg.set_transform(transformer.getTransform())

        # the pool group svg
        pool_group_svg = pool_group_svg_element.group
        pool_group_svg_xy = '{0},{1}'.format(self.theme['lane-rect']['pad-spec']['left'] +
                                                    self.lane_text_svg_element.specs['width'] +
                                                    self.theme['gap-between-text-and-pool-group'],
                                                self.theme['lane-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(pool_group_svg_xy)
        pool_group_svg.set_transform(transformer.getTransform())

        svg_group.addElement(lane_outline_svg)
        svg_group.addElement(lane_text_svg)
        svg_group.addElement(pool_group_svg)

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}

        info('..assembling lane [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))
        return SvgElement(group_specs, svg_group)

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

    def adjust_width_lane_text_element(self, lane_text_element_target_width):
        # this is a group with a rect and an svg, we just add the differential in width to both elements
        group = self.lane_text_svg_element.group
        # we know that the rect is the first child and svg is the second child
        rect = group.getElementAt(0)
        svg = group.getElementAt(1)

        if lane_text_element_target_width > rect.get_width():
            width_to_increase = lane_text_element_target_width - rect.get_width()
            rect.set_width(rect.get_width() + width_to_increase)
            svg.set_width(svg.get_width() + width_to_increase)
            self.lane_text_svg_element.specs['width'] = self.lane_text_svg_element.specs['width'] + width_to_increase
