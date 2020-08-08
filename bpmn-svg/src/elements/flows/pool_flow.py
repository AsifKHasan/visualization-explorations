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
    Class to handle a flows/edges between channels of a pool where from-node is in one channel and to-node is in another channel within the same ChabnnelCollection  (pool).

    Criteria - from-node and to-node must be in same ChannelCollection, but not in same Channel. The possible scenarios are

    #1  *from-node* channel is just above the *to-node* channel and *to-node* is the first node of its Channel
        a) from-node's snap-position is on
            1   SOUTH-MIDDLE
        b) to-node's snap-position is on
            1   WEST-MIDDLE

    #2  *from-node* channel is just above the *to-node* channel and *to-node* is not the first node of its Channel
        a) from-node's snap-position is on
            1   SOUTH-MIDDLE
        b) to-node's snap-position is on
            1   NORTH-LEFT for Activity
            2   NORTH-MIDDLE for Gateway/Event/Data

    #2  *from-node* channel is two or more Channels above the *to-node* channel (there are channels in between) and *to-node* IS the first node of its Channel

    #3  *from-node* channel is two or more Channels above the *to-node* channel (there are channels in between) and *to-node* IS NOT the first node of its Channel

'''
class PoolFlow(FlowObject):

    def __init__(self, edge_type, channel_collection):
        super().__init__(edge_type)
        self.channel_collection = channel_collection


    '''
        implementation of rule #2
        going downward single channel from-node [{0}] and approaching to-node [{1}] from top as it is in the middle of its channel
    '''
    def single_channel_downward_approach_from_top(self, from_node, to_node, label):
        # get the snap points for nodes in pool coordinate
        from_node_points_in_pool = self.snap_points_in_pool_coordinate(node=from_node, snap_side='south', snap_position='middle', role='from', peer_node=to_node, direction_hint='east')
        if from_node_points_in_pool is None:
            warn('could not calculate snap points for from-node [{0}]'.format(from_node.id))
            return None

        to_node_points_in_pool = self.snap_points_in_pool_coordinate(node=to_node, snap_side='west', snap_position='middle', role='to', peer_node=from_node, direction_hint='west')
        if to_node_points_in_pool is None:
            warn('could not calculate snap points for to-node [{0}]'.format(to_node.id))
            return None



        from_node_channel = self.channel_collection.channel_of_node(from_node)
        to_node_channel = self.channel_collection.channel_of_node(to_node)
        from_node_channel_bottom = from_node_channel.element.xy.y + from_node_channel.element.height
        to_node_channel_top = to_node_channel.element.xy.y


        # we extend the from-node last point vertically down to the center of the inter-channel gap area
        # we extend the to-node first point vertically  up to the center of the inter-channel gap area
        y_of_gap_between_channels = from_node_channel_bottom - (to_node_channel_top - from_node_channel_bottom)/2
        from_node_extended_point = Point(from_node_points_in_pool[-1].x, y_of_gap_between_channels)
        to_node_extended_point = Point(to_node_points_in_pool[0].x, y_of_gap_between_channels)


        # we have the points, now create and return the flow
        flow_points = from_node_points_in_pool + [from_node_extended_point, to_node_extended_point] + to_node_points_in_pool
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        implementation of rule #1
        going downward single channel from-node [{0}] and approaching to-node [{1}] from left as it is the left-most node of its channel
    '''
    def single_channel_downward_approach_from_left(self, from_node, to_node, label):
        # get the snap points for nodes in pool coordinate
        from_node_points_in_pool = self.snap_points_in_pool_coordinate(node=from_node, snap_side='south', snap_position='middle', role='from', peer_node=to_node, direction_hint='east')
        if from_node_points_in_pool is None:
            warn('could not calculate snap points for from-node [{0}]'.format(from_node.id))
            return None

        to_node_points_in_pool = self.snap_points_in_pool_coordinate(node=to_node, snap_side='west', snap_position='middle', role='to', peer_node=from_node, direction_hint=None)
        if to_node_points_in_pool is None:
            warn('could not calculate snap points for to-node [{0}]'.format(to_node.id))
            return None


        # we just extend the from-node last point vertically down to the same y position of to-node's first point
        joining_point = Point(from_node_points_in_pool[-1].x, to_node_points_in_pool[0].y)


        # we have the points, now create and return the flow
        flow_points = from_node_points_in_pool + [joining_point] + to_node_points_in_pool
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    def create_flow(self, from_node, to_node, label):
        # decide which edge rule we should apply
        from_node_channel_number, from_node_ordinal = self.channel_collection.channel_number_and_ordinal(from_node)
        if from_node_channel_number == -1 or from_node_ordinal == -1:
            warn('this should not happen: from_node [{0}] can not be found in any channel'.format(from_node.id))
            return None

        to_node_channel_number, to_node_ordinal = self.channel_collection.channel_number_and_ordinal(to_node)
        if to_node_channel_number == -1 or to_node_ordinal == -1:
            warn('this should not happen: to_node [{0}] can not be found in any channel'.format(to_node.id))
            return None

        if from_node_channel_number == to_node_channel_number:
            warn('this should not happen: from_node [{0}] and to_node [{1}] both are in same channel [{2}]'.format(from_node.id, to_node.id, from_node_channel_number))
            return None

        # debug('from-node [{0}] found in channel [{1}] ordinal [{2}]'.format(from_node.id, from_node_channel_number, from_node_ordinal))
        # debug('to-node [{0}] found in channel [{1}] ordinal [{2}]'.format(to_node.id, to_node_channel_number, to_node_ordinal))

        if from_node_channel_number < to_node_channel_number:
            # from-node is above to-node
            if (to_node_channel_number - from_node_channel_number) == 1:
                # from-node channel is just above the to-node channel
                if to_node_ordinal == 0:
                    # to-node IS the first node of its channel, Rule #1
                    return self.single_channel_downward_approach_from_left(from_node, to_node, label)
                else:
                    # to-node is NOT the first node of its channel, Rule #2
                    return self.single_channel_downward_approach_from_top(from_node, to_node, label)
            else:
                # from-node is two or more channels above the to-node
                warn('NOT IMPLEMENTED: from-node [{0}] is {1} channels above to-node [{2}]'.format(from_node.id, (to_node_channel_number - from_node_channel_number), to_node.id))
                return None

        else:
            # from-node is below to-node
            warn('NOT IMPLEMENTED: from-node [{0}] is below to-node [{1}]'.format(from_node.id, to_node.id))
            return None

        return None


    '''
        calculate points at node's snap end and tanslate them into pool's coordinate
    '''
    def snap_points_in_pool_coordinate(self, node, snap_side, snap_position, role, peer_node, direction_hint=None):
        node_channel = self.channel_collection.channel_of_node(node)
        if node_channel is None:
            warn('this should not happen: node [{0}] should be in some channel, but it can not be found in any channel'.format(node.id))
            return None

        # now that we have found both channels, we get their snap_points
        node_snap_side, node_snap_position = snap_side, snap_position
        node_snap_point = node.element.snap_points[node_snap_side][node_snap_position]

        # see if the snap points are occupied or not
        if len(node_snap_point.edge_roles) > 0:
            # TODO: occupied, do something
            warn('snap-point [{0}-{1}] for node [{2}] is occupied ... we may want to do something about it'.format(node_snap_side, node_snap_position, node.id))

        # this snap point is getting a new edge-role
        node_snap_point.edge_roles.append(EdgeRole(role=role, peer=peer_node.id, type=self.edge_type))

        # get the inner snap points
        node_inner_points = node.instance.inner_points_for_snapping(side=node_snap_side, position=node_snap_position, role=role, direction_hint=direction_hint)

        # points are in node coordinate, translate into channel coordinate
        node_points_in_channel = [node.element.xy + p for p in node_inner_points]

        # translate into pool coordinate
        node_points_in_pool = [node_channel.element.xy + p for p in node_points_in_channel]

        return node_points_in_pool
