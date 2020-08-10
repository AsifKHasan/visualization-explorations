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
from util.helper_objects import SnapPoint

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

class Activity(BpmnElement):
    # a task activity is a rounded rectangle with a text inside
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.theme = self.current_theme['activities']['Activity']
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.group_id = 'N-{0}:{1}:{2}:{3}'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id)

    def to_svg(self):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # the rectangle element
        rectangle_group, rectangle_group_width, rectangle_group_height = text_inside_a_rectangle(
                                    text=self.node_data['label'],
                                    min_width=self.theme['rectangle']['min-width'],
                                    max_width=self.theme['rectangle']['max-width'],
                                    rect_spec=self.theme['rectangle'],
                                    text_spec=self.theme['text'])

        # get the inside bottom center element
        bottom_center_element = self.get_bottom_center_element()

        # if an inside bottom center element is to be placed, the element should have a gap from the rectangle bottom
        if bottom_center_element is not None:
            bottom_center_group, bottom_center_group_width, bottom_center_group_height = bottom_center_element.svg, bottom_center_element.width, bottom_center_element.height
            bottom_center_group_xy = '{0},{1}'.format((rectangle_group_width - bottom_center_group_width)/2, rectangle_group_height - bottom_center_group_height - self.theme['rectangle']['inner-shape-margin-spec']['bottom'])
            transformer = TransformBuilder()
            transformer.setTranslation(bottom_center_group_xy)
            bottom_center_group.set_transform(transformer.getTransform())
            rectangle_group.addElement(bottom_center_group)

        # get the inside top left element
        top_left_element = self.get_top_left_element()

        # if an inside bottom center element is to be placed, the element should have a gap from the rectangle bottom
        if top_left_element is not None:
            top_left_group, top_left_group_width, top_left_group_height = top_left_element.svg, top_left_element.width, top_left_element.height
            top_left_group_xy = '{0},{1}'.format(self.theme['rectangle']['inner-shape-margin-spec']['left'], self.theme['rectangle']['inner-shape-margin-spec']['top'])
            transformer = TransformBuilder()
            transformer.setTranslation(top_left_group_xy)
            top_left_group.set_transform(transformer.getTransform())
            rectangle_group.addElement(top_left_group)

        # if there is an outer rectangle process that
        if 'outer-rectangle' in self.theme:
            rectangle_group, rectangle_group_width, rectangle_group_height = envelop_and_center_in_a_rectangle(
                                                                                svg=rectangle_group,
                                                                                svg_width=rectangle_group_width,
                                                                                svg_height=rectangle_group_height,
                                                                                rect_spec=self.theme['outer-rectangle'])

        # snap points
        snap_points = self.snap_points(rectangle_group_width, rectangle_group_height)
        self.snap_offset_x = self.snap_point_offset
        self.snap_offset_y = self.snap_point_offset
        # self.draw_snaps(snap_points, rectangle_group, x_offset=self.snap_offset_x, y_offset=self.snap_offset_y)
        label_pos = 'middle'

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        self.svg_element = SvgElement(svg=rectangle_group, width=rectangle_group_width, height=rectangle_group_height, snap_points=snap_points, label_pos=label_pos)
        return self.svg_element

    def snap_points(self, width, height):
        # activities have more snap points
        snaps = super().snap_points(width, height)
        snaps['north']['left']   = SnapPoint(point=Point(width * 0.25, self.snap_point_offset * -1))
        snaps['north']['right']  = SnapPoint(point=Point(width * 0.75, self.snap_point_offset * -1))
        snaps['south']['left']   = SnapPoint(point=Point(width * 0.25, height + self.snap_point_offset * 1))
        snaps['south']['right']  = SnapPoint(point=Point(width * 0.75, height + self.snap_point_offset * 1))
        snaps['east']['top']     = SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.25))
        snaps['east']['bottom']  = SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.75))
        snaps['west']['top']     = SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.25))
        snaps['west']['bottom']  = SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.75))

        return snaps

    def switch_label_position(self):
        pass

    def get_top_left_element(self):
        return None

    def get_bottom_center_element(self):
        return None
