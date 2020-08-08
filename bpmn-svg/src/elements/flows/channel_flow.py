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

from elements.svg_element import SvgElement
from elements.flows.flow_object import FlowObject

from util.logger import *
from util.geometry import Point
from util.svg_util import *
from util.helper_objects import EdgeRole

'''
    Class to handle a flows/edges inside the channel which means between nodes inside a specific channel. The rules are

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
'''
class ChannelFlow(FlowObject):

    def __init__(self, edge_type, channel_width, channel_height, channel_pad_spec):
        super().__init__(edge_type)
        self.channel_width = channel_width
        self.channel_height = channel_height
        self.channel_pad_left = channel_pad_spec['left']
        self.channel_pad_right = channel_pad_spec['right']
        self.channel_pad_top = channel_pad_spec['top']
        self.channel_pad_bottom = channel_pad_spec['bottom']

    def create_flow(self, from_node, to_node, label):
        # decide which edge rule we should apply
        if from_node.element.xy.west_of(to_node.element.xy):
            # rule #1
            points = self.calculate_straight_path(from_node=from_node, to_node=to_node, from_snap_side='east', to_snap_side='west')
        elif from_node.element.xy.east_of(to_node.element.xy):
            # rule #2
            points = self.calculate_complex_path(from_node=from_node, to_node=to_node)
        else:
            warn('from-node {0} and to-node {1} starts at same x position, they can not be connected inside a channel which is supposed to have all nodes on different x position on same y')
            return None

        # we have the points, now create and return the flow
        flow_svg, flow_width, flow_height = a_flow(points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)

    # implementation of Rule #1
    def calculate_straight_path(self, from_node, to_node, from_snap_side, to_snap_side):
        # select from-node's snap-point, Rule 1.a
        from_snap_position = 'middle'
        snap_position_from = from_node.element.snap_points[from_snap_side][from_snap_position]

        # see if the snap point is occupied or not
        if len(snap_position_from.edge_roles) > 0:
            # TODO: occupied, do something
            pass

        # this snap point is getting a new edge-role
        snap_position_from.edge_roles.append(EdgeRole(role='from', peer=to_node.id, type=self.edge_type))


        # select to-node's snap-point, rule 1.b
        to_snap_position = 'middle'
        snap_position_to = to_node.element.snap_points[to_snap_side][to_snap_position]

        # see if the snap point is occupied or not
        if len(snap_position_to.edge_roles) > 0:
            # TODO: occupied, do something
            pass

        # this snap point is getting a new edge-role
        snap_position_to.edge_roles.append(EdgeRole(role='to', peer=from_node.id, type=self.edge_type))


        # get the flow points
        points_from = from_node.instance.inner_points_for_snapping(side=from_snap_side, position=from_snap_position, role='from', direction_hint=None)
        points_from = [from_node.element.xy + p for p in points_from]
        points_to = to_node.instance.inner_points_for_snapping(side=to_snap_side, position=to_snap_position, role='to', direction_hint=None)
        points_to = [to_node.element.xy + p for p in points_to]

        return points_from + points_to

    # implementation of Rule #2
    def calculate_complex_path(self, from_node, to_node):
        # TODO: this can cross label for ['Event', 'Gateway', 'Data'], so a label position swiching from top to bottom may be required
        # rule 2.a
        if from_node.category in ['Activity']:
            # rule 2.a.1
            from_snap_side = 'east'
            from_snap_position = 'top'
        elif from_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.a.2
            from_snap_side = 'east'
            from_snap_position = 'middle'

        snap_position_from = from_node.element.snap_points[from_snap_side][from_snap_position]
        # this snap point is getting a new edge-role
        snap_position_from.edge_roles.append(EdgeRole(role='from', peer=to_node.id, type=self.edge_type))


        # rule 2.b
        if to_node.category in ['Activity']:
            # rule 2.b.1
            to_snap_side = 'west'
            to_snap_position = 'top'

        elif to_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.b.2
            to_snap_side = 'north'
            to_snap_position = 'middle'

        snap_position_to = from_node.element.snap_points[to_snap_side][to_snap_position]
        # this snap point is getting a new edge-role
        snap_position_to.edge_roles.append(EdgeRole(role='to', peer=from_node.id, type=self.edge_type))


        # get the points of internal segment
        points_from = from_node.instance.inner_points_for_snapping(side=from_snap_side, position=from_snap_position, role='from', direction_hint=None)
        points_from = [from_node.element.xy + p for p in points_from]
        points_to = to_node.instance.inner_points_for_snapping(side=to_snap_side, position=to_snap_position, role='to', direction_hint=None)
        points_to = [to_node.element.xy + p for p in points_to]


        # we now have two segments we connect the last point of *from-segment* to the first point of *to-segment*
        points_middle = self.calculate_path_along_north(points_from[-1], points_to[0])
        points = points_from + points_middle + points_to

        return points

    def calculate_path_along_north(self, p_from, p_to):
        points = [p_from]

        # TODO: we are hardcoding this, this should come from the value of channel outer pad-spec
        northmost_y = min(self.channel_pad_top/2, p_from.y, p_to.y)
        p_from_north = Point(p_from.x, northmost_y)
        points.append(p_from_north)

        p_to_north = Point(p_to.x, northmost_y)
        points.append(p_to_north)

        points.append(p_to)

        return points
