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
from elements.swims.lane_collection import LaneCollection

class Bpmn(BpmnElement):
    # Bpmn is a text rectangle on top of another rectangle containing the lane collections
    def __init__(self, bpmn_id, bpmn_data):
        self.theme = self.current_theme['bpmn']
        self.bpmn_id, self.bpmn_data = bpmn_id, bpmn_data

    def to_svg(self):
        # We go through a collect -> tune -> assemble flow

        # collect the svg elements, but do not assemble now. we need tuning before assembly
        self.collect_elements()

        # tune the svg elements as needed
        self.tune_elements()

        # finally assemble the svg into a final one
        final_svg = self.assemble_elements()
        return final_svg

    def tune_elements(self):
        info('tuning BPMN [{0}]'.format(self.bpmn_id))

        # tune the children
        self.child_element_class.tune_elements()

        info('tuning BPMN [{0}] DONE'.format(self.bpmn_id))

    def collect_elements(self):
        info('processing BPMN [{0}]'.format(self.bpmn_id))

        # process the lane collection
        self.child_element_class = LaneCollection(self.bpmn_id, self.bpmn_data['lanes'])
        self.child_element_class.collect_elements()

        info('processing BPMN [{0}] DONE'.format(self.bpmn_id))

    def assemble_elements(self):
        info('assembling BPMN [{0}]'.format(self.bpmn_id))

        # wrap it in a svg group
        svg_group = G(id=self.bpmn_id)

        bpmn_body_svg_element = self.get_body_element()
        bpmn_body_svg = bpmn_body_svg_element.group

        # get the svg element for the label on top
        bpmn_label_svg, label_width, label_height = text_inside_a_rectangle(
                                                    text=self.bpmn_data['label'],
                                                    min_width=bpmn_body_svg_element.specs['width'],
                                                    max_width=bpmn_body_svg_element.specs['width'],
                                                    rect_spec=self.theme['rectangle'],
                                                    text_spec=self.theme['text'],
                                                    debug_enabled=False)

        # assemble bpmn text and bpmn body. text stacked on top of body
        # bpmn has a margin, so the outer group needs a transformation
        svg_group_xy = '{0},{1}'.format(self.theme['margin-spec']['left'], self.theme['margin-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(svg_group_xy)
        svg_group.set_transform(transformer.getTransform())

        # place the bpmn body group just below the text group
        bpmn_body_svg_xy = '{0},{1}'.format(0, label_height)
        transformer = TransformBuilder()
        transformer.setTranslation(bpmn_body_svg_xy)
        bpmn_body_svg.set_transform(transformer.getTransform())

        # place the bpmn label
        svg_group.addElement(bpmn_label_svg)
        svg_group.addElement(bpmn_body_svg)

        # wrap in canvas
        canvas_width = bpmn_body_svg_element.specs['width'] + self.theme['margin-spec']['left'] + self.theme['margin-spec']['right']
        canvas_height = label_height + bpmn_body_svg_element.specs['height'] + self.theme['margin-spec']['top'] + self.theme['margin-spec']['bottom']
        svg = Svg(0, 0, width=canvas_width, height=canvas_height)
        svg.addElement(svg_group)

        info('assembling BPMN [{0}]'.format(self.bpmn_id))
        return svg

    def get_body_element(self):
        # wrap it in a svg group
        group_id = '{0}-body'.format(self.bpmn_id)
        svg_group = G(id=group_id)

        # bpmn's body is the lane collection
        lane_collection_svg_element = self.child_element_class.assemble_elements()
        lane_collection_svg = lane_collection_svg_element.group

        # a bpmn body's width is the width of inner lane collection + padding
        bpmn_body_width = lane_collection_svg_element.specs['width'] + self.theme['bpmn-rect']['pad-spec']['left'] + self.theme['bpmn-rect']['pad-spec']['right']

        # a bpmn body's height is the sum of the heights of its inner lane collection + some padding
        bpmn_body_height = lane_collection_svg_element.specs['height'] + self.theme['bpmn-rect']['pad-spec']['top'] + self.theme['bpmn-rect']['pad-spec']['bottom']

        body_rect_svg = Rect(width=bpmn_body_width, height=bpmn_body_height)
        body_rect_svg.set_style(StyleBuilder(self.theme['bpmn-rect']['style']).getStyle())
        svg_group.addElement(body_rect_svg)

        # add lane_collection inside bpmn rect with a tranformation by margin
        # bpmn body has padding, so the group needs a transformation
        lane_collection_svg_xy = '{0},{1}'.format(self.theme['bpmn-rect']['pad-spec']['left'], self.theme['bpmn-rect']['pad-spec']['top'])

        transformer = TransformBuilder()
        transformer.setTranslation(lane_collection_svg_xy)
        lane_collection_svg.set_transform(transformer.getTransform())
        svg_group.addElement(lane_collection_svg)

        # wrap it in a svg element
        return SvgElement({'width': bpmn_body_width, 'height': bpmn_body_height}, svg_group)
