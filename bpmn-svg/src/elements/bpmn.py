#!/usr/bin/env python3
'''
'''
from pysvg.builders import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *

from util.logger import *
from util.svg_util import *

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement
from elements.swims.lane_group import LaneGroup

class Bpmn(BpmnElement):
    def __init__(self):
        self.theme = self.current_theme['Bpmn']

    def to_svg(self, bpmn_id, bpmn_data):
        lane_group_id = 'lanes'
        lane_group = LaneGroup().to_svg(lane_group_id, bpmn_data['lanes'])
        lane_group_svg = lane_group.group

        # Bpmn is a text rectangle on top of another rectangle containing the lane groups

        # a bpmn's width is the width of inner lane group + margins + padding
        bpmn_width = lane_group.specs['width'] + self.theme['pad-left'] + self.theme['pad-right']

        # a bpmn's height is the sum of the heights of its pools + some padding
        bpmn_height = lane_group.specs['height'] + self.theme['pad-top'] + self.theme['pad-bottom']


        # text rect
        text_rect_width = bpmn_width
        text_rect_height = self.theme['text-rect']['default-height']
        text_rect = G()
        svg_rect = Rect(width=text_rect_width, height=text_rect_height)
        text_rect.addElement(svg_rect)
        # render the text
        text_svg = center_text(bpmn_data['label'], svg_rect, self.theme['text-rect']['text-style'], vertical_text=self.theme['text-rect']['vertical-text'], text_wrap_at=self.theme['text-rect']['text-wrap-at'])
        text_rect.addElement(text_svg)
        text_rect.set_style(StyleBuilder(self.theme['text-rect']['style']).getStyle())


        # pool rect
        bpmn_rect_width = bpmn_width
        bpmn_rect_height = bpmn_height
        bpmn_rect = G()
        bpmn_rect.addElement(Rect(width=bpmn_rect_width, height=bpmn_rect_height))

        # pool rect is to be placed just right of text rect
        transformer = TransformBuilder()
        transformer.setTranslation("{0},{1}".format(0, text_rect_height))
        bpmn_rect.set_transform(transformer.getTransform())
        bpmn_rect.set_style(StyleBuilder(self.theme['bpmn-rect']['style']).getStyle())

        # add lane_group inside bpmn rect with a tranformation by margin
        transformer = TransformBuilder()
        transformer.setTranslation("{0},{1}".format(self.theme['pad-left'], self.theme['pad-top']))
        lane_group_svg.set_transform(transformer.getTransform())
        lane_group_svg.set_style(StyleBuilder(self.theme['bpmn-rect']['style']).getStyle())
        bpmn_rect.addElement(lane_group_svg)

        # group text rect and pool rect
        svg_group = G()
        transformer = TransformBuilder()
        transformer.setTranslation("{0},{1}".format(self.theme['margin-left'], self.theme['margin-top']))
        svg_group.set_transform(transformer.getTransform())
        svg_group.addElement(text_rect)
        svg_group.addElement(bpmn_rect)


        # wrap in canvas
        canvas_width = bpmn_width + self.theme['margin-left'] + self.theme['margin-right']
        canvas_height = text_rect_height + bpmn_height + self.theme['margin-top'] + self.theme['margin-bottom']
        svg = Svg(0, 0, width=canvas_width, height=canvas_height)
        svg.addElement(svg_group)

        return svg
