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

class DataObject(BpmnElement):
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.theme = self.current_theme['datas']['DataObject']
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.group_id = 'N-{0}:{1}:{2}:{3}'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id)

    def to_svg(self):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # the label element
        label_group, label_group_width, label_group_height = text_inside_a_rectangle(
                                    text=self.node_data['label'],
                                    min_width=self.theme['rectangle']['min-width'],
                                    max_width=self.theme['rectangle']['max-width'],
                                    rect_spec=self.theme['rectangle'],
                                    text_spec=self.theme['text'])

        # the folded rectangle
        folded_rectangle_group, folded_rectangle_group_width, folded_rectangle_group_height = a_folded_rectangle(width=self.theme['folded-rectangle']['width'], height=self.theme['folded-rectangle']['height'], spec=self.theme['folded-rectangle'])

        # top left element inside -------------------------------------------------------
        top_left_element = self.get_top_left_element()
        # position properly inside the folder rectangle at top left
        if top_left_element is not None:
            top_left_group, top_left_group_width, top_left_group_height = top_left_element.group, top_left_element.specs['width'], top_left_element.specs['height']
            top_left_group_xy = '{0},{1}'.format(self.theme['folded-rectangle']['pad-spec']['left'], self.theme['folded-rectangle']['pad-spec']['top'])
            transformer = TransformBuilder()
            transformer.setTranslation(top_left_group_xy)
            top_left_group.set_transform(transformer.getTransform())
            folded_rectangle_group.addElement(top_left_group)

        # bottom center element inside -------------------------------------------------------
        bottom_center_element = self.get_bottom_center_element()
        # position properly inside the folder rectangle at bottom center
        if bottom_center_element is not None:
            bottom_center_group, bottom_center_group_width, bottom_center_group_height = bottom_center_element.group, bottom_center_element.specs['width'], bottom_center_element.specs['height']
            bottom_center_group_xy = '{0},{1}'.format((folded_rectangle_group_width - bottom_center_group_width)/2, folded_rectangle_group_height - bottom_center_group_height - self.theme['folded-rectangle']['pad-spec']['bottom'])
            transformer = TransformBuilder()
            transformer.setTranslation(bottom_center_group_xy)
            bottom_center_group.set_transform(transformer.getTransform())
            folded_rectangle_group.addElement(bottom_center_group)

        # wrap them in a svg group -----------------------------------------------------------------
        svg_group = G(id=self.group_id)

        # the folded rectangle is below an empty space of the same height of the label
        folded_rectangle_group_xy = '{0},{1}'.format((label_group_width - folded_rectangle_group_width)/2, label_group_height)
        transformer = TransformBuilder()
        transformer.setTranslation(folded_rectangle_group_xy)
        folded_rectangle_group.set_transform(transformer.getTransform())

        # the label is vertically below the folded rectangle
        label_group_xy = '{0},{1}'.format(0, label_group_height + folded_rectangle_group_height)
        transformer = TransformBuilder()
        transformer.setTranslation(label_group_xy)
        label_group.set_transform(transformer.getTransform())

        # place the elements
        svg_group.addElement(folded_rectangle_group)
        svg_group.addElement(label_group)

        # extend the height so that a blank space of the same height as text is at the bottom so that the circle's left edge is at dead vertical center
        group_width = label_group_width
        group_height = label_group_height + folded_rectangle_group_height + label_group_height

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        return SvgElement({'width': group_width, 'height': group_height}, svg_group)

    def get_top_left_element(self):
        return None

    def get_bottom_center_element(self):
        return None
