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
    def __init__(self, bpmn_id, bpmn_data):
        self.theme = self.current_theme['Bpmn']
        self.bpmn_id, self.bpmn_data = bpmn_id, bpmn_data

    def to_svg(self):
        # Bpmn is a text rectangle on top of another rectangle containing the lane groups

        # get the svg element for the bpmn content area
        bpmn_body_svg_element = self.get_bpmn_body_svg_element()

        # get the svg element for the text area on top
        bpmn_text_svg_element = self.get_bpmn_text_svg_element(bpmn_body_svg_element.specs['width'], bpmn_body_svg_element.specs['width'])

        # assemble the two svg's into a final one
        svg = self.assemble_bpmn(bpmn_text_svg_element, bpmn_body_svg_element)

        return svg

    def get_bpmn_body_svg_element(self):
        # wrap it in a svg group
        group_id = '{0}-body'.format(self.bpmn_id)
        svg_group = G(id=group_id)

        # bpmn's body is the lane group
        self.child_element_class = LaneGroup(self.bpmn_id, self.bpmn_data['lanes'])
        lane_group_svg_element = self.child_element_class.to_svg()
        lane_group_svg = lane_group_svg_element.group

        # a bpmn body's width is the width of inner lane group + padding
        bpmn_body_width = lane_group_svg_element.specs['width'] + self.theme['bpmn-rect']['pad-spec']['left'] + self.theme['bpmn-rect']['pad-spec']['right']

        # a bpmn body's height is the sum of the heights of its inner lane group + some padding
        bpmn_body_height = lane_group_svg_element.specs['height'] + self.theme['bpmn-rect']['pad-spec']['top'] + self.theme['bpmn-rect']['pad-spec']['bottom']

        body_rect_svg = Rect(width=bpmn_body_width, height=bpmn_body_height)
        body_rect_svg.set_style(StyleBuilder(self.theme['bpmn-rect']['style']).getStyle())
        svg_group.addElement(body_rect_svg)

        # add lane_group inside bpmn rect with a tranformation by margin
        # bpmn body has padding, so the group needs a transformation
        lane_group_svg_xy = '{0},{1}'.format(self.theme['bpmn-rect']['pad-spec']['left'], self.theme['bpmn-rect']['pad-spec']['top'])

        transformer = TransformBuilder()
        transformer.setTranslation(lane_group_svg_xy)
        lane_group_svg.set_transform(transformer.getTransform())
        svg_group.addElement(lane_group_svg)

        # wrap it in a svg element
        group_specs = {'width': bpmn_body_width, 'height': bpmn_body_height}
        return SvgElement(group_specs, svg_group)

    def get_bpmn_text_svg_element(self, min_width, max_width):
        # wrap in a svg group
        group_id = '{0}-text'.format(self.bpmn_id)
        svg_group = G(id=group_id)

        # get the svg list of the text, first elemnt is the rect, second element is the text
        svg_list = rect_with_text(text=self.bpmn_data['label'],
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

    def assemble_bpmn(self, bpmn_text_svg_element, bpmn_body_svg_element):
        # wrap it in a svg group
        svg_group = G(id=self.bpmn_id)

        # assemble bpmn text and bpmn body. text stacked on top of body
        # bpmn has a margin, so the outer group needs a transformation
        svg_group_xy = '{0},{1}'.format(self.theme['margin-spec']['left'], self.theme['margin-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(svg_group_xy)
        svg_group.set_transform(transformer.getTransform())

        # place the bpmn text group
        svg_group.addElement(bpmn_text_svg_element.group)

        # place the bpmn body group just below the text group
        bpmn_body_svg_xy = '{0},{1}'.format(0, bpmn_text_svg_element.specs['height'])
        bpmn_body_svg = bpmn_body_svg_element.group
        transformer = TransformBuilder()
        transformer.setTranslation(bpmn_body_svg_xy)
        bpmn_body_svg.set_transform(transformer.getTransform())

        svg_group.addElement(bpmn_body_svg)

        # wrap in canvas
        canvas_width = bpmn_body_svg_element.specs['width'] + self.theme['margin-spec']['left'] + self.theme['margin-spec']['right']
        canvas_height = bpmn_text_svg_element.specs['height'] + bpmn_body_svg_element.specs['height'] + self.theme['margin-spec']['top'] + self.theme['margin-spec']['bottom']
        svg = Svg(0, 0, width=canvas_width, height=canvas_height)
        svg.addElement(svg_group)

        return svg
