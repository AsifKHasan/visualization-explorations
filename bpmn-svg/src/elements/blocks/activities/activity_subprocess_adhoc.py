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

class ActivityAdhocSubprocess(BpmnElement):
    # a subprocess activity is a rounded rectangle with text inside and a + and a ~ side by side at the bottom floor of the rectangle below the text
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.theme = self.current_theme['ActivityAdhocSubprocess']
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

        wave_group, group_width, group_height = rectangle_with_text_inside(
                                                    text='~',
                                                    min_width=self.theme['wave-rect']['min-width'],
                                                    max_width=self.theme['wave-rect']['max-width'],
                                                    specs=self.theme['wave-rect'])
        self.node_elements.append(SvgElement({'width': group_width, 'height': group_height}, wave_group))

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

    def assemble_elements(self):
        info('......assembling node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # wrap it in a svg group
        svg_group = G(id=self.group_id)

        # get the elements
        label_svg_element = self.node_elements[0]
        label_svg = label_svg_element.group

        rect_svg_element = self.node_elements[1]
        wave_svg_element = self.node_elements[2]

        combined_svg, combined_svg_width, combined_svg_height = align_and_combine_horizontally([rect_svg_element, wave_svg_element])

        # the rect is inside the label, we keep a gap betwwen the bottom edge of the label and the botto edge of the rect
        gap_between_label_and_rect_bootom_edges = 5
        combined_svg_xy = '{0},{1}'.format((label_svg_element.specs['width'] - combined_svg_width)/2, label_svg_element.specs['height'] - combined_svg_height - gap_between_label_and_rect_bootom_edges)
        transformer = TransformBuilder()
        transformer.setTranslation(combined_svg_xy)
        combined_svg.set_transform(transformer.getTransform())

        # the wave is inside teh label, we keep a gap betwwen the bottom edge of the label and the bottom edge of the rect

        # place the elements
        svg_group.addElement(label_svg)
        svg_group.addElement(combined_svg)

        group_width = label_svg_element.specs['width']
        group_height = label_svg_element.specs['height']

        info('......assembling node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        return SvgElement({'width': group_width, 'height': group_height}, svg_group)

    def tune_elements(self):
        info('......tuning node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        info('......tuning node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
