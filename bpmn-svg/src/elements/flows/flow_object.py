#!/usr/bin/env python3
'''
TODO: Udemy
https://www.udemy.com/course/mega-course-vmware-vsphere-67-bootcamp-100-hands-on-labs/
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

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

'''
    Edge rules
    #1  if the from-node and to-node are in the same channel and to-node is further east from from-node ([from-node] --> [to_node])
        a) from-node's snap-position is on EAST (MIDDLE)
        b) to-node's snap-position is on WEST (MIDDLE)

    #2  if the from-node and to-node are in the same channel and to-node is further west from from-node (that is behind, a back-flow) ([to-node] <-- [from_node])
        a) from-node's snap-position is on
            1   EAST-TOP for Activity
            2   EAST-MIDDLE for Gateway/Event/Data
        b) to-node's snap-position is on
            1   WEST-TOP for Activity
            2   NORTH-MIDDLE for Gateway/Event/Data (swicth label to bottom if necessary)

    #3  from-node's snap-position is always on EAST (TOP if present, else MIDDLE) if the to-node is in another channel and further north
    #4  from-node's snap-position is always on EAST (BOTTOM if present, else MIDDLE) if the to-node is in another channel and further south

    #5 -
'''

# snaps can not be approached from any direction, it is rather dependent on the side of the snap, so we define the next allowed approaching point offset so that any edges reach snap from that point
adhacent_point_offset = {
    'north': Point(0, -10),
    'south': Point(0, 10),
    'east': Point(10, 0),
    'west': Point(-10, 0),
}

class FlowObject(BpmnElement):
    def __init__(self, flow_type):
        self.theme = self.current_theme['flows'][flow_type]

    def calculate_path_along_north(self, p_from, p_to):
        points = [p_from]

        # TODO: we are hardcoding this, this should come from the value of channel outer pad-spec
        northmost_y = 10
        p_from_north = Point(p_from.x, northmost_y)
        points.append(p_from_north)

        p_to_north = Point(p_to.x, northmost_y)
        points.append(p_to_north)

        points.append(p_to)

        return points

    # implementation of Rule #2
    def calculate_complex_path(self, from_node, to_node):
        # TODO: this can cross label for ['Event', 'Gateway', 'Data'], so a label position swiching from top to bottom may be required
        # rule 2.a
        if from_node['category'] in ['Activity']:
            # rule 2.a.1
            snap_position_from = from_node['snap-points']['east']['top']
            point_from = from_node['xy'] + snap_position_from['point']
            point_from_adjacent_point = point_from + adhacent_point_offset['east']

        elif from_node['category'] in ['Event', 'Gateway', 'Data']:
            # rule 2.a.2
            snap_position_from = from_node['snap-points']['east']['middle']
            from_node['xy'] + snap_position_from['point']
            point_from_adjacent_point = point_from + adhacent_point_offset['east']

        # rule 2.b
        if to_node['category'] in ['Activity']:
            # rule 2.b.1
            snap_position_to = to_node['snap-points']['west']['top']
            point_to = to_node['xy'] + snap_position_to['point']
            point_to_adjacent_point = point_to + adhacent_point_offset['west']

        elif to_node['category'] in ['Event', 'Gateway', 'Data']:
            # rule 2.b.2
            snap_position_to = to_node['snap-points']['north']['middle']
            point_to = to_node['xy'] + snap_position_to['point']
            point_to_adjacent_point = point_to + adhacent_point_offset['north']

        # we now have two start points and two end points, so we calculate a northward path from the two points adjacent to the snap points
        points = [point_from] + self.calculate_path_along_north(point_from_adjacent_point, point_to_adjacent_point) + [point_to]

        return points

    # implementation of Rule #1
    def calculate_straight_path(self, from_node, to_node, from_snap_side, to_snap_side):
        # Rule 1.a
        snap_position_from = from_node['snap-points'][from_snap_side]['middle']

        # rule 1.b
        snap_position_to = to_node['snap-points'][to_snap_side]['middle']

        point_from = from_node['xy'] + snap_position_from['point']
        point_to = to_node['xy'] + snap_position_to['point']

        points = [point_from, point_to]
        return points

    def connect_within_channel(self, from_node, to_node, label):
        # decide which way we go
        if from_node['xy'].west_of(to_node['xy']):
            points = self.calculate_straight_path(from_node=from_node, to_node=to_node, from_snap_side='east', to_snap_side='west')
        elif from_node['xy'].east_of(to_node['xy']):
            points = self.calculate_complex_path(from_node=from_node, to_node=to_node)
        else:
            warn('from-node {0} and to-node {1} starts at same x position, they can not be connected inside a channel which is supposed to have all nodes on different x position on same y')
            return None

        # we have the points, now create and return the flow
        flow_svg, flow_width, flow_height = a_flow(points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)
