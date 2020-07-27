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

class ActivityEventSubprocess(BpmnElement):
    # a subprocess activity is a rounded rectangle with text inside and a + at the bottom floor of the rectangle below the text
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.theme = self.current_theme['ActivityEventSubprocess']
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.group_id = 'N-{0}:{1}:{2}:{3}'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id)

    def to_svg(self):
        # collect the node elements/svgs
        self.collect_elements()

        # tune the node
        self.tune_elements()

        # assemble the elements/svgs into a final one
        svg_element = self.assemble_elements()
        return svg_element

    def collect_elements(self):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # get the inner svg elements in a list
        self.node_elements = []

        # the label element
        label_group, group_width, group_height = rectangle_with_text_inside(
                                    text=self.node_data['label'],
                                    min_width=self.theme['text-rect']['min-width'],
                                    max_width=self.theme['text-rect']['max-width'],
                                    specs=self.theme['text-rect'])
        self.node_elements.append(SvgElement({'width': group_width, 'height': group_height}, label_group))

        rect_group, group_width, group_height = rectangle_with_cross_inside(
                                                    width=self.theme['inner-rect']['width'],
                                                    height=self.theme['inner-rect']['height'],
                                                    rx=self.theme['inner-rect']['rx'],
                                                    ry=self.theme['inner-rect']['ry'],
                                                    style=self.theme['inner-rect']['style'],
                                                    x_style=self.theme['inner-rect']['style'])
        self.node_elements.append(SvgElement({'width': group_width, 'height': group_height}, rect_group))

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

    def assemble_elements(self):
        info('......assembling node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # wrap it in a svg group
        svg_group = G(id=self.group_id)

        # get the elements
        label_svg_element = self.node_elements[0]
        label_svg = label_svg_element.group

        rect_svg_element = self.node_elements[1]
        rect_svg = rect_svg_element.group

        # place the elements
        svg_group.addElement(label_svg)

        # the rect is inside teh label, we keep a gap betwwen the bottom edge of the label and the botto edge of the rect
        gap_between_label_and_rect_bootom_edges = 5
        rect_svg_xy = '{0},{1}'.format((label_svg_element.specs['width'] - rect_svg_element.specs['width'])/2, label_svg_element.specs['height'] - rect_svg_element.specs['height'] - gap_between_label_and_rect_bootom_edges)
        transformer = TransformBuilder()
        transformer.setTranslation(rect_svg_xy)
        rect_svg.set_transform(transformer.getTransform())

        # place the elements
        svg_group.addElement(label_svg)
        svg_group.addElement(rect_svg)

        group_width = label_svg_element.specs['width']
        group_height = label_svg_element.specs['height']

        info('......assembling node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        return SvgElement({'width': group_width, 'height': group_height}, svg_group)

    def tune_elements(self):
        info('......tuning node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        info('......tuning node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
