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

from elements.bpmn_element import BpmnElement, SnapPoint
from elements.svg_element import SvgElement

''' a Gateway is a diamond with label outside the diamond, either on the top or at the bottom
'''
class Gateway(BpmnElement):
    def __init__(self, current_theme, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.current_theme = current_theme
        self.theme = self.current_theme['gateways']['Gateway']
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.group_id = 'N-{0}:{1}:{2}:{3}'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id)
        if 'label_pos' in self.node_data['styles'] and self.node_data['styles']['label_pos'] in ['top', 'bottom']:
            self.label_pos = self.node_data['styles']['label_pos']
        else:
            self.label_pos = 'top'

        if self.node_data['label'] is None or self.node_data['label'] == '':
            self.label_pos = 'none'


    ''' gateways have more snap points, in all sides in all positions we add at least two more so that edges do not overlap
    '''
    def snap_points(self, width, height):
        snaps = super().snap_points(width, height)

        # add two more (slight left and slight right) for north-middle)
        distance = height/10
        p1 = snaps['north']['middle'][0].point.to_point(-45, distance)
        p2 = snaps['north']['middle'][0].point.to_point(-135, distance)
        snaps['north']['middle'].append(SnapPoint(point=p1))
        snaps['north']['middle'].append(SnapPoint(point=p2))

        # snaps['north']['middle'].append(SnapPoint(point=Point(width * 0.45, self.snap_point_offset * -1)))
        # snaps['north']['middle'].append(SnapPoint(point=Point(width * 0.55, self.snap_point_offset * -1)))

        # add two more (slight left and slight right) for south-middle)
        distance = height/10
        p1 = snaps['south']['middle'][0].point.to_point(45, distance)
        p2 = snaps['south']['middle'][0].point.to_point(135, distance)
        snaps['south']['middle'].append(SnapPoint(point=p1))
        snaps['south']['middle'].append(SnapPoint(point=p2))

        # snaps['south']['middle'].append(SnapPoint(point=Point(width * 0.45, height + self.snap_point_offset * 1)))
        # snaps['south']['middle'].append(SnapPoint(point=Point(width * 0.55, height + self.snap_point_offset * 1)))

        # add two more (slight up and slight down) for east-middle)
        distance = width/10
        p1 = snaps['east']['middle'][0].point.to_point(-135, distance)
        p2 = snaps['east']['middle'][0].point.to_point(135, distance)
        snaps['east']['middle'].append(SnapPoint(point=p1))
        snaps['east']['middle'].append(SnapPoint(point=p2))

        # snaps['east']['middle'].append(SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.40)))
        # snaps['east']['middle'].append(SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.60)))

        # add two more (slight up and slight down) for west-middle)
        distance = width/10
        p1 = snaps['west']['middle'][0].point.to_point(45, distance)
        p2 = snaps['west']['middle'][0].point.to_point(-45, distance)
        snaps['west']['middle'].append(SnapPoint(point=p1))
        snaps['west']['middle'].append(SnapPoint(point=p2))

        # snaps['west']['middle'].append(SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.40)))
        # snaps['west']['middle'].append(SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.60)))

        return snaps


    def to_svg(self):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # the label group
        label_group, label_group_width, label_group_height = text_inside_a_rectangle(
                                                                text=self.node_data['label'],
                                                                min_width=self.theme['rectangle']['min-width'],
                                                                max_width=self.theme['rectangle']['max-width'],
                                                                rect_spec=self.theme['rectangle'],
                                                                text_spec=self.theme['text'])

        # the diamond element
        diamond_group, diamond_group_width, diamond_group_height = a_diamond(
                                                                    diagonal_x=self.theme['diamond']['diagonal-x'],
                                                                    diagonal_y=self.theme['diamond']['diagonal-y'],
                                                                    spec=self.theme['diamond'])

        # the inside element
        inside_element = self.get_inside_element()

        # if an element is to be placed inside the diamond group, place it so that the inside object's center and the diamond's center is same
        if inside_element is not None:
            inside_group, inside_group_width, inside_group_height = inside_element.svg, inside_element.width, inside_element.height
            inside_group_xy = Point((diamond_group_width - inside_group_width)/2, (diamond_group_height - inside_group_height)/2)
            transformer = TransformBuilder()
            transformer.setTranslation(inside_group_xy)
            inside_group.set_transform(transformer.getTransform())
            diamond_group.addElement(inside_group)

        # wrap it in a svg group
        svg_group = G(id=self.group_id)

        # the diamond is to be positioned vertically after the rect_svg and center should be the center of the rect_svg
        diamond_group_xy = Point((label_group_width - diamond_group_width)/2, label_group_height + self.snap_point_offset)
        transformer = TransformBuilder()
        transformer.setTranslation(diamond_group_xy)
        diamond_group.set_transform(transformer.getTransform())

        # where the label will be positioned depends on the value of label_pos
        if self.label_pos == 'bottom':
            label_group_xy = Point(0, label_group_height + self.snap_point_offset + diamond_group_height + self.snap_point_offset)
            transformer = TransformBuilder()
            transformer.setTranslation(label_group_xy)
            label_group.set_transform(transformer.getTransform())

        # place the kabel and diamond
        svg_group.addElement(label_group)
        svg_group.addElement(diamond_group)

        # extend the height so that a blank space of the same height as text is at the bottom so that the diamond left edge is at dead vertical center
        group_width = label_group_width
        group_height = label_group_height + self.snap_point_offset + diamond_group_height + self.snap_point_offset + label_group_height

        # snap points
        snap_points = self.snap_points(group_width, group_height)
        self.snap_offset_x = (label_group_width - diamond_group_width)/2 + self.snap_point_offset
        self.snap_offset_y = label_group_height + self.snap_point_offset * 2
        # self.draw_snaps(snap_points, svg_group, x_offset=self.snap_offset_x, y_offset=self.snap_offset_y)

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        self.svg_element = SvgElement(svg=svg_group, width=group_width, height=group_height, snap_points=snap_points, label_pos=self.label_pos)
        return self.svg_element


    def get_inside_element(self):
        return None
