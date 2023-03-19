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

from util.geometry import Point
from util.logger import *
from util.svg_util import *
from util.helper_util import *

from elements.bpmn_element import BpmnElement, SnapPoint
from elements.svg_element import SvgElement

''' a task activity is a rounded rectangle with a text inside
'''
class Activity(BpmnElement):
    def __init__(self, current_theme, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.current_theme = current_theme
        self.theme = self.current_theme['activities']['Activity']
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.group_id = 'N-{0}:{1}:{2}:{3}'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id)


    def to_svg(self):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # the rectangle element
        if self.node_data['label'] == '':
            label = id_to_label(self.node_id)
        else:
            label = self.node_data['label']

        rectangle_group, rectangle_group_width, rectangle_group_height = text_inside_a_rectangle(
                                    text=label,
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


    ''' activities have more snap points, in all sides in all positions we add at least two more so that edges do not overlap
    '''
    def snap_points(self, width, height):
        snaps = super().snap_points(width, height)

        # add two more (slight left and slight right) for north-middle)
        snaps['north']['middle'].append(SnapPoint(point=Point(width * 0.45, self.snap_point_offset * -1)))
        snaps['north']['middle'].append(SnapPoint(point=Point(width * 0.55, self.snap_point_offset * -1)))

        # add two more (slight left and slight right) for south-middle)
        snaps['south']['middle'].append(SnapPoint(point=Point(width * 0.45, height + self.snap_point_offset * 1)))
        snaps['south']['middle'].append(SnapPoint(point=Point(width * 0.55, height + self.snap_point_offset * 1)))

        # add two more (slight up and slight down) for east-middle)
        snaps['east']['middle'].append(SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.40)))
        snaps['east']['middle'].append(SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.60)))

        # add two more (slight up and slight down) for west-middle)
        snaps['west']['middle'].append(SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.40)))
        snaps['west']['middle'].append(SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.60)))

        # activities have snap-points in north-left - one in mid-left and two more (slight left and slight right)
        snaps['north']['left'] = [SnapPoint(point=Point(width * 0.25, self.snap_point_offset * -1))]
        snaps['north']['left'].append(SnapPoint(point=Point(width * 0.20, self.snap_point_offset * -1)))
        snaps['north']['left'].append(SnapPoint(point=Point(width * 0.30, self.snap_point_offset * -1)))

        # activities have snap-points in north-right - one in mid-right and two more (slight left and slight right)
        snaps['north']['right'] = [SnapPoint(point=Point(width * 0.75, self.snap_point_offset * -1))]
        snaps['north']['right'].append(SnapPoint(point=Point(width * 0.70, self.snap_point_offset * -1)))
        snaps['north']['right'].append(SnapPoint(point=Point(width * 0.80, self.snap_point_offset * -1)))

        # activities have snap-points in south-left - one in mid-left and two more (slight left and slight right)
        snaps['south']['left'] = [SnapPoint(point=Point(width * 0.25, height + self.snap_point_offset * 1))]
        snaps['south']['left'].append(SnapPoint(point=Point(width * 0.20, height + self.snap_point_offset * 1)))
        snaps['south']['left'].append(SnapPoint(point=Point(width * 0.30, height + self.snap_point_offset * 1)))

        # activities have snap-points in south-right - one in mid-right and two more (slight left and slight right)
        snaps['south']['right']  = [SnapPoint(point=Point(width * 0.75, height + self.snap_point_offset * 1))]
        snaps['south']['right'].append(SnapPoint(point=Point(width * 0.70, height + self.snap_point_offset * 1)))
        snaps['south']['right'].append(SnapPoint(point=Point(width * 0.80, height + self.snap_point_offset * 1)))

        # activities have snap-points in east-top - one in mid-top and two more (slight up and slight down)
        snaps['east']['top'] = [SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.25))]
        snaps['east']['top'].append(SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.15)))
        snaps['east']['top'].append(SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.35)))

        # activities have snap-points in east-bottom - one in mid-bottom and two more (slight up and slight down)
        snaps['east']['bottom'] = [SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.75))]
        snaps['east']['bottom'].append(SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.65)))
        snaps['east']['bottom'].append(SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.85)))

        # activities have snap-points in west-top - one in mid-top and two more (slight up and slight down)
        snaps['west']['top'] = [SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.25))]
        snaps['west']['top'].append(SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.15)))
        snaps['west']['top'].append(SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.35)))

        # activities have snap-points in west-bottom - one in mid-bottom and two more (slight up and slight down)
        snaps['west']['bottom'] = [SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.75))]
        snaps['west']['bottom'].append(SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.65)))
        snaps['west']['bottom'].append(SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.85)))

        return snaps


    def switch_label_position(self):
        pass


    def get_top_left_element(self):
        return None


    def get_bottom_center_element(self):
        return None
