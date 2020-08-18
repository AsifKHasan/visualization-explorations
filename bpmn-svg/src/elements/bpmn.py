#!/usr/bin/env python3
'''
'''
import re

from pprint import pprint

from pysvg.builders import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *

from util.geometry import Point
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

        # assemble the bpmn body
        self.assemble_elements()

        # lay edges
        self.lay_edges()

        # finally assemble the svg into a final one
        final_svg = self.create_svg()

        return final_svg

    def lay_edges(self):
        self.lane_collection_instance.lay_edges()

    def collect_elements(self):
        info('processing BPMN [{0}]'.format(self.bpmn_id))

        # process the lane collection
        self.lane_collection_instance = LaneCollection(self.bpmn_id, self.bpmn_data['lanes'])
        self.lane_collection_instance.collect_elements()

        info('processing BPMN [{0}] DONE'.format(self.bpmn_id))

    '''
        we are manipulating the svg directly
    '''
    def tune_labels(self):
        # get the width of the lane label having the maximum width
        max_lane_label_width = 0
        max_pool_label_width = 0
        for lane_group in self.label_element.svg.getAllElements():
            # the first child is a rect and the rect element's width is the width of lane-label
            lane_label_width = lane_group.getElementAt(0).getAttribute('width')
            # print('lane {0} width: {1}'.format(lane_group.getAttribute('id'), lane_label_width))
            max_lane_label_width = max(max_lane_label_width, lane_label_width)

            # the pool labels are in a group which is the third child
            for pool_group in lane_group.getElementAt(2).getAllElements():
                # the first child is a rect and the rect element's width is the width of pool-label
                pool_label_width = pool_group.getElementAt(0).getAttribute('width')
                # print('....pool {0} width: {1}'.format(pool_group.getAttribute('id'), pool_label_width))
                max_pool_label_width = max(max_pool_label_width, pool_label_width)

        # now we know the max width for lane and pool labels, we adjust them accordingly
        for lane_group in self.label_element.svg.getAllElements():
            # the first child is a rect and the rect element's width is the width of lane-label
            lane_label_width_diff = max_lane_label_width - lane_group.getElementAt(0).getAttribute('width')
            if lane_label_width_diff == 0:
                # we do nothing, this is already at the max width
                pass

            # change the rect's (first child) width
            lane_group.getElementAt(0).setAttribute('width', max_lane_label_width)

            # second child is an svg whose width needs to be adjusted by diff
            lane_label_svg_width = lane_group.getElementAt(1).getAttribute('width')
            lane_group.getElementAt(1).setAttribute('width', lane_label_svg_width + lane_label_width_diff)

            # third child is the pool label group, whose transform's translation's x position needs to be adjusted by diff
            transform = lane_group.getElementAt(2).getAttribute('transform')
            m = re.match('translate\((?P<x>.+),(?P<y>.+)\)', transform, re.IGNORECASE)
            if m and m.group('x') is not None and m.group('y') is not None:
                point = Point(float(m.group('x')) + lane_label_width_diff, float(m.group('y')))
                lane_group.getElementAt(2).setAttribute('transform', 'translate({0})'.format(point))

            # the pool labels are in a group which is the third child
            for pool_group in lane_group.getElementAt(2).getAllElements():
                # the first child is a rect and the rect element's width is the width of pool-label
                pool_label_width_diff = max_pool_label_width - pool_group.getElementAt(0).getAttribute('width')
                if pool_label_width_diff == 0:
                    # we do nothing, this is already at the max width
                    pass

                # change the rect's (first child) width
                pool_group.getElementAt(0).setAttribute('width', max_pool_label_width)

                # second child is an svg whose width needs to be adjusted by diff
                pool_label_svg_width = pool_group.getElementAt(1).getAttribute('width')
                pool_group.getElementAt(1).setAttribute('width', pool_label_svg_width + pool_label_width_diff)



    def assemble_elements(self):
        # bpmn's body is the lane collection
        self.body_element = self.lane_collection_instance.assemble_elements()
        self.label_element = self.lane_collection_instance.assemble_labels()
        self.tune_labels()

    def create_svg(self):
        info('assembling BPMN [{0}]'.format(self.bpmn_id))

        # wrap it in a svg group
        svg_group = G(id=self.bpmn_id)

        bpmn_width = self.theme['bpmn-rect']['pad-spec']['left'] + self.label_element.width + self.body_element.width + self.theme['bpmn-rect']['pad-spec']['right']

        # get the svg element for the label on top
        bpmn_label_svg, label_width, label_height = text_inside_a_rectangle(
                                                    text=self.bpmn_data['label'],
                                                    min_width=bpmn_width,
                                                    max_width=bpmn_width,
                                                    rect_spec=self.theme['rectangle'],
                                                    text_spec=self.theme['text'],
                                                    debug_enabled=False)

        bpmn_height = label_height + self.theme['bpmn-rect']['pad-spec']['top'] + self.body_element.height + self.theme['bpmn-rect']['pad-spec']['bottom']

        body_rect_svg = Rect(width=bpmn_width, height=bpmn_height)
        body_rect_svg.set_style(StyleBuilder(self.theme['bpmn-rect']['style']).getStyle())
        svg_group.addElement(body_rect_svg)

        # assemble bpmn text and bpmn body. text stacked on top of body
        # bpmn has a margin, so the outer group needs a transformation
        svg_group_xy = Point(self.theme['margin-spec']['left'], self.theme['margin-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(svg_group_xy)
        svg_group.set_transform(transformer.getTransform())

        if 'hide_labels' in self.bpmn_data['styles'] and self.bpmn_data['styles']['hide_labels'] == 'true':
            # place the bpmn body group just below the text group right to label
            body_element_xy = Point(self.theme['bpmn-rect']['pad-spec']['left'], label_height + self.theme['bpmn-rect']['pad-spec']['top'])
            transformer = TransformBuilder()
            transformer.setTranslation(body_element_xy)
            self.body_element.svg.set_transform(transformer.getTransform())

            # place the bpmn label
            svg_group.addElement(bpmn_label_svg)
            svg_group.addElement(self.body_element.svg)
        else:
            # place the lane-pool label just below the text to the laft
            label_element_xy = Point(self.theme['bpmn-rect']['pad-spec']['left'], label_height + self.theme['bpmn-rect']['pad-spec']['top'])
            transformer = TransformBuilder()
            transformer.setTranslation(label_element_xy)
            self.label_element.svg.set_transform(transformer.getTransform())

            # place the bpmn body group just below the text group right to label
            body_element_xy = Point(self.theme['bpmn-rect']['pad-spec']['left'] + self.label_element.width, label_height + self.theme['bpmn-rect']['pad-spec']['top'])
            transformer = TransformBuilder()
            transformer.setTranslation(body_element_xy)
            self.body_element.svg.set_transform(transformer.getTransform())

            # place the bpmn label
            svg_group.addElement(bpmn_label_svg)
            svg_group.addElement(self.label_element.svg)
            svg_group.addElement(self.body_element.svg)

        # wrap in canvas
        canvas_width = self.theme['margin-spec']['left'] + bpmn_width + self.theme['margin-spec']['right']
        canvas_height = self.theme['margin-spec']['top'] + bpmn_height + self.theme['margin-spec']['bottom']
        svg = Svg(0, 0, width=canvas_width, height=canvas_height)
        svg.addElement(svg_group)

        info('assembling BPMN [{0}]'.format(self.bpmn_id))
        return svg
