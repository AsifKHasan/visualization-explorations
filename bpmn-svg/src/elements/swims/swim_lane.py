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

    def to_svg(self, lane_id, lane_data):
        debug('processing lane [{0}] DONE ...'.format(lane_id))

        # a horizontal lane is a narrow rectangle having a center-aligned text 90 degree anti-clockwise rotated at left and another adjacent rectangle () on its right containing Pool elements stacked vertically
        pool_group_id = 'pools'
        pool_group = PoolGroup().to_svg(pool_group_id, lane_data['pools'])

        # a bpmn's width is the width of inner lane group + margins + padding
        lane_width = self.theme['text-rect']['default-width'] + pool_group.specs['width'] + self.theme['lane-rect']['pad-left'] + self.theme['lane-rect']['pad-right']

        # a lane's width is pool group width + some padding
        lane_height = pool_group.specs['height'] + self.theme['lane-rect']['pad-top'] + self.theme['lane-rect']['pad-bottom']

        # text rect
        text_rect_width = self.theme['text-rect']['default-width']
        text_rect_height = lane_height
        text_rect = G()
        svg_rect = Rect(width=text_rect_width, height=text_rect_height)
        text_rect.addElement(svg_rect)

        # render the text
        text_svg = center_text(lane_data['label'], svg_rect, self.theme['text-rect']['text-style'], vertical_text=self.theme['text-rect']['vertical-text'], text_wrap_at=self.theme['text-rect']['text-wrap-at'])
        text_rect.addElement(text_svg)
        text_rect.set_style(StyleBuilder(self.theme['text-rect']['style']).getStyle())

        # lane rect
        lane_rect_width = lane_width - text_rect_width
        lane_rect_height = lane_height
        lane_rect = G()
        lane_rect.addElement(Rect(width=lane_rect_width, height=lane_rect_height))

        # pool group to be added into the lane rect with a transformation
        transformer = TransformBuilder()
        transformer.setTranslation("{0},{1}".format(self.theme['lane-rect']['pad-left'], self.theme['lane-rect']['pad-top']))
        pool_group_svg = pool_group.group
        pool_group_svg.set_transform(transformer.getTransform())
        lane_rect.addElement(pool_group_svg)

        # lane rect is to be placed just right of text rect
        transformer = TransformBuilder()
        transformer.setTranslation("{0},{1}".format(self.theme['text-rect']['default-width'], 0))
        lane_rect.set_transform(transformer.getTransform())
        lane_rect.set_style(StyleBuilder(self.theme['lane-rect']['style']).getStyle())

        # group text rect and pool rect
        svg_group = G(id=lane_id)
        svg_group.addElement(text_rect)
        svg_group.addElement(lane_rect)

        group_specs = {'width': lane_width, 'height': lane_height}

        debug('processing lane [{0}] DONE ...'.format(lane_id))

        return SvgElement(group_specs, svg_group)
