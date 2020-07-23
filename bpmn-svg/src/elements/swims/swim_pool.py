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

    def tune_elements(self):
        info('....processing pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))
        info('....processing pool [{0}:{1}:{2}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id))

    def collect_elements(self):
        info('....processing pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        # get the block group
        self.block_group_svg_element = self.get_block_group_svg_element()

        # get the lane text rect, its min_width and max_width is the block group's height
        self.pool_text_svg_element = self.get_pool_text_svg_element()

        info('....processing pool [{0}:{1}:{2}] DONE ...'.format(self.bpmn_id, self.lane_id, self.pool_id))

    def assemble_elements(self):
        # wrap it in a svg group
        group_id = '{0}:{1}:{2}'.format(self.bpmn_id, self.lane_id, self.pool_id)
        svg_group = G(id=group_id)

        # a pool's width is pool text width + block group width + some padding
        group_height = self.block_group_svg_element.specs['height'] + self.theme['pool-rect']['pad-spec']['top'] + self.theme['pool-rect']['pad-spec']['bottom']
        group_width = self.pool_text_svg_element.specs['width'] + self.block_group_svg_element.specs['width'] + self.theme['pool-rect']['pad-spec']['left'] + self.theme['pool-rect']['pad-spec']['right']

        # add the pool ractangle
        pool_rect_svg = Rect(width=group_width, height=group_height)
        pool_rect_svg.set_style(StyleBuilder(self.theme['pool-rect']['style']).getStyle())

        pool_text_svg = self.pool_text_svg_element.group
        block_group_svg = self.block_group_svg_element.group

        # add the pool text svg
        pool_text_svg_xy = '{0},{1}'.format(self.theme['pool-rect']['pad-spec']['left'], self.theme['pool-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(pool_text_svg_xy)
        pool_text_svg.set_transform(transformer.getTransform())

        # add the block group svg
        block_group_svg_xy = '{0},{1}'.format(self.theme['pool-rect']['pad-spec']['left'] + self.pool_text_svg_element.specs['width'], self.theme['pool-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(block_group_svg_xy)
        block_group_svg.set_transform(transformer.getTransform())

        svg_group.addElement(pool_rect_svg)
        svg_group.addElement(pool_text_svg)
        svg_group.addElement(block_group_svg)

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}
        return SvgElement(group_specs, svg_group)

    def get_block_group_svg_element(self):
        block_group = BlockGroup(self.bpmn_id, self.lane_id, self.pool_id, self.pool_data['nodes'], self.pool_data['edges'])
        block_group_svg_element = block_group.to_svg(self.theme['pool-rect']['default-width'])
        return block_group_svg_element

    def get_pool_text_svg_element(self):
        info('....tuning pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

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

        info('....tuning pool [{0}:{1}:{2}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id))
        return SvgElement(group_specs, svg_group)

    def get_height(self):
        return self.block_group_svg_element.specs['height']
