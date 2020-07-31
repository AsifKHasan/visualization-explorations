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
        self.theme = self.current_theme['swims']['SwimLane']
        self.bpmn_id, self.lane_id, self.lane_data = bpmn_id, lane_id, lane_data

    def tune_elements(self, tune_spec):
        info('..tuning lane [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # tune the children
        self.child_element_class.tune_elements(tune_spec)

        # label_svg_element width may need some tuning
        label_element_target_width = tune_spec['lane-text-element-target-width']
        self.tune_label_element(label_element_target_width)

        info('..tuning lane [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))

    def collect_elements(self):
        info('..processing lane [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # get the pool group
        self.child_element_class = PoolGroup(self.bpmn_id, self.lane_id, self.lane_data['pools'])
        self.child_element_class.collect_elements()

        # get the inner svg elements in a list
        self.node_elements = []

        # we need the height of the pool group
        pool_group_height = self.child_element_class.get_height()

        # get the lane label, its min_width and max_width is the pool group's height + all
        label_group, group_width, group_height = text_inside_a_rectangle(
                                                    text=self.lane_data['label'],
                                                    min_width=pool_group_height,
                                                    max_width=pool_group_height,
                                                    rect_spec=self.theme['rectangle'],
                                                    text_spec=self.theme['text'],
                                                    debug_enabled=False)
        self.node_elements.append(SvgElement({'width': group_width, 'height': group_height}, label_group))

        info('..processing lane [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))

    def assemble_elements(self):
        info('..assembling lane [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # wrap it in a svg group
        group_id = '{0}:{1}'.format(self.bpmn_id, self.lane_id)
        svg_group = G(id=group_id)

        pool_group_svg_element = self.child_element_class.assemble_elements()
        pool_group_svg = pool_group_svg_element.group

        label_svg_element = self.node_elements[0]
        label_svg = label_svg_element.group

        # a lane's width is lane text width + pool group width + some padding
        group_height = self.theme['lane-rect']['pad-spec']['top'] + pool_group_svg_element.specs['height'] + self.theme['lane-rect']['pad-spec']['bottom']
        group_width = self.theme['lane-rect']['pad-spec']['left'] + label_svg_element.specs['width'] + self.theme['gap-between-text-and-pool-group'] + pool_group_svg_element.specs['width'] + self.theme['lane-rect']['pad-spec']['right']

        # add the lane outline
        outline_svg, group_width, group_height = a_rectangle(width=group_width, height=group_height, spec=self.theme['lane-rect'])

        # the lane label
        label_svg_xy = '{0},{1}'.format(self.theme['lane-rect']['pad-spec']['left'], self.theme['lane-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(label_svg_xy)
        label_svg.set_transform(transformer.getTransform())

        # the pool group svg
        pool_group_svg_xy = '{0},{1}'.format(self.theme['lane-rect']['pad-spec']['left'] + label_svg_element.specs['width'] + self.theme['gap-between-text-and-pool-group'], self.theme['lane-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(pool_group_svg_xy)
        pool_group_svg.set_transform(transformer.getTransform())

        svg_group.addElement(outline_svg)
        svg_group.addElement(label_svg)
        svg_group.addElement(pool_group_svg)

        info('..assembling lane [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))
        return SvgElement({'width': group_width, 'height': group_height}, svg_group)

    def tune_label_element(self, label_element_target_width):
        label_svg_element = self.node_elements[0]

        # this is a group with a rect and an svg, we just add the differential in width to both elements
        group = label_svg_element.group
        # we know that the rect is the first child and svg is the second child
        rect = group.getElementAt(0)
        svg = group.getElementAt(1)

        if label_element_target_width > rect.get_width():
            width_to_increase = label_element_target_width - rect.get_width()
            rect.set_width(rect.get_width() + width_to_increase)
            svg.set_width(svg.get_width() + width_to_increase)
            label_svg_element.specs['width'] = label_svg_element.specs['width'] + width_to_increase

    def get_max_width_of_elements_of_children(self):
        label_svg_element = self.node_elements[0]
        pool_label_element_max_width, pool_block_group_max_width = self.child_element_class.get_max_width_of_elements_of_children()
        return label_svg_element.specs['width'], pool_label_element_max_width, pool_block_group_max_width
