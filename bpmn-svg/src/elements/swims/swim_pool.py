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

    def to_svg(self, pool_id, pool_data):
        debug('..processing pool [{0}] ...'.format(pool_id))

        # get the inner blocks as a group first, it will give us (actual calculated) width and height required for this pool
        block_group_id = '{0}_blocks'.format(pool_id)
        block_group_svg = BlockGroup().to_svg(block_group_id, pool_data['nodes'], pool_data['edges'], self.theme['pool-rect']['default-width'])

        # a horizontal pool is a narrow rectangle having a center-aligned text 90 degree anti-clockwise rotated at left and another adjacent rectangle () on its right containing nodes and edges

        # to get the width we need to calculate the text rendering function
        text_rendering_hint = break_text_inside_rect(pool_data['label'],
                                self.theme['text-rect']['text-style']['font-family'],
                                self.theme['text-rect']['text-style']['font-size'],
                                self.theme['text-rect']['max-lines'],
                                block_group_svg.specs['height'],
                                block_group_svg.specs['height'],
                                self.theme['text-rect']['pad-spec'])

        # text rect
        text_rect_width = text_rendering_hint[1]
        text_rect_height = block_group_svg.specs['height']
        text_rect_group = G()
        text_rect_svg = Rect(width=text_rect_width, height=text_rect_height)
        text_rect_svg.set_style(StyleBuilder(self.theme['text-rect']['style']).getStyle())
        text_rect_group.addElement(text_rect_svg)
        # render the text
        text_svg = center_text(text_rendering_hint[0],
                        text_rect_svg,
                        self.theme['text-rect']['text-style'],
                        vertical_text=self.theme['text-rect']['vertical-text'],
                        pad_spec=self.theme['text-rect']['pad-spec'])
        text_rect_group.addElement(text_svg)

        # pool rect
        pool_rect_width = block_group_svg.specs['width']
        pool_rect_height = block_group_svg.specs['height']
        pool_rect_group = G()
        pool_rect_svg = Rect(width=pool_rect_width, height=pool_rect_height)
        pool_rect_svg.set_style(StyleBuilder(self.theme['pool-rect']['style']).getStyle())
        # add the inner block group
        pool_rect_group.addElement(pool_rect_svg)
        pool_rect_group.addElement(block_group_svg.group)

        # pool rect is to be placed just right of text rect
        transformer = TransformBuilder()
        transformer.setTranslation("{0},{1}".format(text_rect_width, 0))
        pool_rect_group.set_transform(transformer.getTransform())

        # group text rect and pool rect
        svg_group = G(id=pool_id)
        svg_group.addElement(text_rect_group)
        svg_group.addElement(pool_rect_group)

        group_specs = {'width': text_rect_width + pool_rect_width, 'height': max(text_rect_height, pool_rect_height)}

        debug('..processing pool [{0}] DONE ...'.format(pool_id))

        return SvgElement(group_specs, svg_group)
