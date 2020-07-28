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

from elements.swims.block_group import BlockGroup

class SwimPool(BpmnElement):
    # a horizontal pool is a narrow rectangle having a center-aligned text 90 degree anti-clockwise rotated at left and another adjacent rectangle () on its right containing nodes and edges
    def __init__(self, bpmn_id, lane_id, pool_id, pool_data):
        self.theme = self.current_theme['swims']['SwimPool']
        self.bpmn_id, self.lane_id, self.pool_id, self.pool_data = bpmn_id, lane_id, pool_id, pool_data

    def tune_elements(self, tune_spec):
        info('....tuning pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        # label_svg_element width may need some tuning
        label_element_target_width = tune_spec['pool-text-element-target-width']
        self.tune_label_element(label_element_target_width)

        # block_group_svg_element width may need some tuning
        block_group_target_width = tune_spec['pool-block-group-target-width']
        self.tune_block_group_element(block_group_target_width)

        info('....tuning pool [{0}:{1}:{2}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id))

    def collect_elements(self):
        info('....processing pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        # get the inner svg elements in a list
        self.node_elements = []

        # get the block group
        block_group = BlockGroup(self.bpmn_id, self.lane_id, self.pool_id, self.pool_data['nodes'], self.pool_data['edges'])
        block_group_svg_element = block_group.to_svg(self.theme['pool-rect']['default-width'])
        self.node_elements.append(block_group_svg_element)

        # get the lane label, its min_width and max_width is the block group's height
        label_group, group_width, group_height = rectangle_with_text_inside(
                                                    text=self.pool_data['label'],
                                                    min_width=block_group_svg_element.specs['height'],
                                                    max_width=block_group_svg_element.specs['height'],
                                                    specs=self.theme['text-rect'],
                                                    debug_enabled=False)
        self.node_elements.append(SvgElement({'width': group_width, 'height': group_height}, label_group))

        info('....processing pool [{0}:{1}:{2}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id))

    def assemble_elements(self):
        info('....assembling pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        # wrap it in a svg group
        group_id = '{0}:{1}:{2}'.format(self.bpmn_id, self.lane_id, self.pool_id)
        svg_group = G(id=group_id)

        block_group_svg_element = self.node_elements[0]
        block_group_svg = block_group_svg_element.group
        label_svg_element = self.node_elements[1]
        label_svg = label_svg_element.group

        # a pool's width is pool text width + block group width + some padding
        group_height = block_group_svg_element.specs['height'] + self.theme['pool-rect']['pad-spec']['top'] + self.theme['pool-rect']['pad-spec']['bottom']
        group_width = label_svg_element.specs['width'] + block_group_svg_element.specs['width'] + self.theme['pool-rect']['pad-spec']['left'] + self.theme['pool-rect']['pad-spec']['right'] + self.theme['gap-between-text-and-block-group']

        # add the pool outline
        outline_svg, group_width, group_height = rectangle(width=group_width, height=group_height, rx=0, ry=0, style=self.theme['pool-rect']['style'])

        # add the label svg
        label_svg_xy = '{0},{1}'.format(self.theme['pool-rect']['pad-spec']['left'], self.theme['pool-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(label_svg_xy)
        label_svg.set_transform(transformer.getTransform())

        # add the block group svg
        block_group_svg_xy = '{0},{1}'.format(self.theme['pool-rect']['pad-spec']['left'] + label_svg_element.specs['width'] + self.theme['gap-between-text-and-block-group'], self.theme['pool-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(block_group_svg_xy)
        block_group_svg.set_transform(transformer.getTransform())

        svg_group.addElement(outline_svg)
        svg_group.addElement(label_svg)
        svg_group.addElement(block_group_svg)

        # wrap it in a svg element

        info('....assembling pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))
        return SvgElement({'width': group_width, 'height': group_height}, svg_group)

    def tune_label_element(self, label_element_target_width):
        label_svg_element = self.node_elements[1]

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

    def tune_block_group_element(self, block_group_target_width):
        block_group_svg_element = self.node_elements[0]

        # this is a group with a rect and one or more element groups, we just add the differential in width to the rect
        group = block_group_svg_element.group
        width_to_increase = block_group_target_width - block_group_svg_element.specs['width']
        if width_to_increase > 0:
            # we know that the rect is the first child
            rect = group.getElementAt(0)
            rect.set_width(rect.get_width() + width_to_increase)
            block_group_svg_element.specs['width'] = block_group_target_width

    def get_height(self):
        block_group_svg_element = self.node_elements[0]
        return block_group_svg_element.specs['height'] + self.theme['pool-rect']['pad-spec']['top'] + self.theme['pool-rect']['pad-spec']['bottom']

    def get_max_width_of_elements_of_children(self):
        label_svg_element = self.node_elements[1]
        block_group_svg_element = self.node_elements[0]
        return label_svg_element.specs['width'], block_group_svg_element.specs['width']
