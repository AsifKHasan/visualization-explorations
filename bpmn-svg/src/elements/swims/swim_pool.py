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
    def __init__(self):
        self.theme = self.current_theme['SwimPool']

    def to_svg(self, bpmn_id, lane_id, pool_id, pool_data):
        info('....processing pool [{0}:{1}:{2}] ...'.format(bpmn_id, lane_id, pool_id))

        # a horizontal pool is a narrow rectangle having a center-aligned text 90 degree anti-clockwise rotated at left and another adjacent rectangle () on its right containing nodes and edges

        # get the block group
        block_group_svg_element = self.get_block_group_svg_element(bpmn_id, lane_id, pool_id, pool_data)

        # get the lane text rect, its min_width and max_width is the block group's height
        pool_text_svg_element = self.get_pool_text_svg_element(bpmn_id, lane_id, pool_id, pool_data, block_group_svg_element.specs['height'], block_group_svg_element.specs['height'])

        # assemble the lane svg element
        svg_element = self.assemble_element(bpmn_id, lane_id, pool_id, pool_text_svg_element, block_group_svg_element)

        info('....processing pool [{0}:{1}:{2}] DONE ...'.format(bpmn_id, lane_id, pool_id))
        return svg_element

    def get_block_group_svg_element(self, bpmn_id, lane_id, pool_id, pool_data):
        block_group = BlockGroup()
        block_group_svg_element = block_group.to_svg(bpmn_id, lane_id, pool_id, pool_data['nodes'], pool_data['edges'], self.theme['pool-rect']['default-width'])
        return block_group_svg_element

    def get_pool_text_svg_element(self, bpmn_id, lane_id, pool_id, pool_data, min_width, max_width):
        # wrap in a svg group
        group_id = '{0}:{1}:{2}-text'.format(bpmn_id, lane_id, pool_id)
        svg_group = G(id=group_id)

        # get the svg list of the text, first elemnt is the rect, second element is the text
        svg_list = rect_with_text(text=pool_data['label'],
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

    def assemble_element(self, bpmn_id, lane_id, pool_id, pool_text_svg_element, block_group_svg_element):
        # wrap it in a svg group
        group_id = '{0}:{1}:{2}'.format(bpmn_id, lane_id, pool_id)
        svg_group = G(id=group_id)

        # a pool's width is pool text width + block group width + some padding
        group_height = block_group_svg_element.specs['height'] + self.theme['pool-rect']['pad-spec']['top'] + self.theme['pool-rect']['pad-spec']['bottom']
        group_width = pool_text_svg_element.specs['width'] + block_group_svg_element.specs['width'] + self.theme['pool-rect']['pad-spec']['left'] + self.theme['pool-rect']['pad-spec']['right']

        # add the pool ractangle
        pool_rect_svg = Rect(width=group_width, height=group_height)
        pool_rect_svg.set_style(StyleBuilder(self.theme['pool-rect']['style']).getStyle())

        pool_text_svg = pool_text_svg_element.group
        block_group_svg = block_group_svg_element.group

        # add the pool text svg
        pool_text_svg_xy = '{0},{1}'.format(self.theme['pool-rect']['pad-spec']['left'], self.theme['pool-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(pool_text_svg_xy)
        pool_text_svg.set_transform(transformer.getTransform())

        # add the block group svg
        block_group_svg_xy = '{0},{1}'.format(self.theme['pool-rect']['pad-spec']['left'] + pool_text_svg_element.specs['width'], self.theme['pool-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(block_group_svg_xy)
        block_group_svg.set_transform(transformer.getTransform())

        svg_group.addElement(pool_rect_svg)
        svg_group.addElement(pool_text_svg)
        svg_group.addElement(block_group_svg)

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}
        return SvgElement(group_specs, svg_group)
