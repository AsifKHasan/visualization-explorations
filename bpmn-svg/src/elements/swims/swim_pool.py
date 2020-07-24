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

from elements.blocks.block_group import BlockGroup

class SwimPool(BpmnElement):
    # a horizontal pool is a narrow rectangle having a center-aligned text 90 degree anti-clockwise rotated at left and another adjacent rectangle () on its right containing nodes and edges
    def __init__(self, bpmn_id, lane_id, pool_id, pool_data):
        self.theme = self.current_theme['SwimPool']
        self.bpmn_id, self.lane_id, self.pool_id, self.pool_data = bpmn_id, lane_id, pool_id, pool_data

    def tune_elements(self, tune_spec):
        info('....tuning pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        # pool_text_svg_element width may need some tuning
        pool_text_element_target_width = tune_spec['pool-text-element-target-width']
        self.adjust_width_pool_text_element(pool_text_element_target_width)

        # block_group_svg_element width may need some tuning
        pool_block_group_target_width = tune_spec['pool-block-group-target-width']
        self.adjust_width_pool_block_group(pool_block_group_target_width)

        info('....tuning pool [{0}:{1}:{2}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id))

    def collect_elements(self):
        info('....processing pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        # get the block group
        self.block_group_svg_element = self.get_block_group_svg_element()

        # get the lane text rect, its min_width and max_width is the block group's height
        self.pool_text_svg_element = self.get_pool_text_svg_element()

        info('....processing pool [{0}:{1}:{2}] DONE ...'.format(self.bpmn_id, self.lane_id, self.pool_id))

    def assemble_elements(self):
        info('....assembling pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        # wrap it in a svg group
        group_id = '{0}:{1}:{2}'.format(self.bpmn_id, self.lane_id, self.pool_id)
        svg_group = G(id=group_id)

        # a pool's width is pool text width + block group width + some padding
        group_height = self.block_group_svg_element.specs['height'] + self.theme['pool-rect']['pad-spec']['top'] + self.theme['pool-rect']['pad-spec']['bottom']
        group_width = self.pool_text_svg_element.specs['width'] + self.block_group_svg_element.specs['width'] + self.theme['pool-rect']['pad-spec']['left'] + self.theme['pool-rect']['pad-spec']['right'] + self.theme['gap-between-text-and-block-group']

        # add the pool ractangle
        pool_outline_svg = Rect(width=group_width, height=group_height)
        pool_outline_svg.set_style(StyleBuilder(self.theme['pool-rect']['style']).getStyle())

        pool_text_svg = self.pool_text_svg_element.group
        block_group_svg = self.block_group_svg_element.group

        # add the pool text svg
        pool_text_svg_xy = '{0},{1}'.format(self.theme['pool-rect']['pad-spec']['left'], self.theme['pool-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(pool_text_svg_xy)
        pool_text_svg.set_transform(transformer.getTransform())

        # add the block group svg
        block_group_svg_xy = '{0},{1}'.format(self.theme['pool-rect']['pad-spec']['left'] + self.pool_text_svg_element.specs['width'] + self.theme['gap-between-text-and-block-group'], self.theme['pool-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(block_group_svg_xy)
        block_group_svg.set_transform(transformer.getTransform())

        svg_group.addElement(pool_outline_svg)
        svg_group.addElement(pool_text_svg)
        svg_group.addElement(block_group_svg)

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}

        info('....assembling pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))
        return SvgElement(group_specs, svg_group)

    def get_block_group_svg_element(self):
        block_group = BlockGroup(self.bpmn_id, self.lane_id, self.pool_id, self.pool_data['nodes'], self.pool_data['edges'])
        block_group_svg_element = block_group.to_svg(self.theme['pool-rect']['default-width'])
        return block_group_svg_element

    def get_pool_text_svg_element(self):
        # wrap in a svg group
        group_id = '{0}:{1}:{2}-text'.format(self.bpmn_id, self.lane_id, self.pool_id)
        svg_group = G(id=group_id)

        # get the svg list of the text, first elemnt is the rect, second element is the text
        svg_list = rect_with_text(text=self.pool_data['label'],
                                    min_width=self.block_group_svg_element.specs['height'],
                                    max_width=self.block_group_svg_element.specs['height'],
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
        debug('lane [{0}] text rect ({1}, {2})'.format(self.lane_id, group_width, group_height))
        return SvgElement(group_specs, svg_group)

    def adjust_width_pool_text_element(self, pool_text_element_target_width):
        # this is a group with a rect and an svg, we just add the differential in width to both elements
        group = self.pool_text_svg_element.group
        # we know that the rect is the first child and svg is the second child
        rect = group.getElementAt(0)
        svg = group.getElementAt(1)

        if pool_text_element_target_width > rect.get_width():
            width_to_increase = pool_text_element_target_width - rect.get_width()
            rect.set_width(rect.get_width() + width_to_increase)
            svg.set_width(svg.get_width() + width_to_increase)
            self.pool_text_svg_element.specs['width'] = self.pool_text_svg_element.specs['width'] + width_to_increase

    def adjust_width_pool_block_group(self, pool_block_group_target_width):
        # this is a group with a rect and one or more element groups, we just add the differential in width to the rect
        group = self.block_group_svg_element.group
        width_to_increase = pool_block_group_target_width - self.block_group_svg_element.specs['width']
        if width_to_increase > 0:
            # we know that the rect is the first child
            rect = group.getElementAt(0)
            rect.set_width(rect.get_width() + width_to_increase)
            self.block_group_svg_element.specs['width'] = pool_block_group_target_width

    def get_height(self):
        return self.block_group_svg_element.specs['height'] + self.theme['pool-rect']['pad-spec']['top'] + self.theme['pool-rect']['pad-spec']['bottom']

    def get_max_width_of_elements_of_children(self):
        return self.pool_text_svg_element.specs['width'], self.block_group_svg_element.specs['width']
