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

    #1  *from-node* channel is above the *to-node* channel
        a.  *to-node* is the first node of its Channel
            1) from-node's snap-position is on
                a   SOUTH-MIDDLE
            2) to-node's snap-position is on
                a   WEST-MIDDLE if to_node is further east to *from-node*
                b   NORTH-MIDDLE if to_node is further west to *from-node*
        b.  *to-node* is NOT the first node of its Channel
            1) from-node's snap-position is on
                a   SOUTH-MIDDLE
            2) to-node's snap-position is on
                a   NORTH-LEFT for Activity
                b   NORTH-MIDDLE for Gateway/Event/Data

    #2  *from-node* channel is below the *to-node* channel
        a)  *to-node* is to the left (west) of *from-node* in pool coordinate
            1)  from-node's snap-position is on
                a   NORTH-RIGHT for Activity
                b   NORTH-MIDDLE for Gateway/Event/Data
            2)   to-node's snap-position is on
                a   SOUTH-RIGHT for Activity
                b   SOUTH-MIDDLE for Gateway/Event/Data
        b)  *to-node* is to the right (east) of *from-node* in pool coordinate
            1)  from-node's snap-position is on
                a   NORTH-RIGHT for Activity
                b   NORTH-MIDDLE for Gateway/Event/Data
            2)   to-node's snap-position is on
                a   SOUTH-LEFT for Activity
                b   SOUTH-MIDDLE for Gateway/Event/Data

'''
class PoolFlow(FlowObject):

    def __init__(self, edge_type, channel_collection):
        super().__init__(edge_type)
        self.channel_collection = channel_collection

    '''
        implementation of rule 2.a - *to-node* is to the left (west) of *from-node* in pool coordinate
        going one channel southward from-node [{0}] and approaching to-node [{1}] from top
    '''
    def northward_north_to_south_westward(self, from_node, to_node, label):
        # rule 2.a.1 - from-node's snap-position is on
        from_node_channel = self.channel_collection.channel_of_node(from_node)
        if from_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.a.1.b - NORTH-MIDDLE for Gateway/Event/Data
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=from_node_channel, node=from_node, side='north', position='middle', role='from', direction_hint='east', peer=to_node, edge_type=self.edge_type)
        else:
            # rule 2.a.1.a - is on NORTH-RIGHT for Activity
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=from_node_channel, node=from_node, side='north', position='right', role='from', direction_hint=None, peer=to_node, edge_type=self.edge_type)

        # rule 2.a.2 - to-node's snap-position is on
        to_node_channel = self.channel_collection.channel_of_node(to_node)
        if to_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.a.2.b - SOUTH-MIDDLE for Gateway/Event/Data
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=to_node_channel, node=to_node, side='south', position='middle', role='to', direction_hint='east', peer=from_node, edge_type=self.edge_type)
        else:
            # rule 2.a.2.b - SOUTH-LEFT for Activity
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=to_node_channel, node=to_node, side='south', position='left', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)

        # get the connecting points
        joining_points = self.channel_collection.connecting_points(point_from=from_node_points_in_pool_coordinate[-1], point_to=to_node_points_in_pool_coordinate[0])

        # we have the points, now create and return the flow
        flow_points = from_node_points_in_pool_coordinate + joining_points + to_node_points_in_pool_coordinate
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        implementation of rule 2.b - *to-node* is to the right (east) of *from-node* in pool coordinate
        going one channel southward from-node [{0}] and approaching to-node [{1}] from top
    '''
    def northward_north_to_south_eastward(self, from_node, to_node, label):
        # rule 2.b.1 - from-node's snap-position
        from_node_channel = self.channel_collection.channel_of_node(from_node)
        if from_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.b.1.b - NORTH-MIDDLE for Gateway/Event/Data
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=from_node_channel, node=from_node, side='north', position='middle', role='from', direction_hint='east', peer=to_node, edge_type=self.edge_type)
        else:
            # rule 2.b.1.a -is on NORTH-RIGHT for Activity
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=from_node_channel, node=from_node, side='north', position='right', role='from', direction_hint='east', peer=to_node, edge_type=self.edge_type)

        # rule 2.b.2 - to-node's snap-position is on
        to_node_channel = self.channel_collection.channel_of_node(to_node)
        if to_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.b.2.b - SOUTH-MIDDLE for Gateway/Event/Data
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=to_node_channel, node=to_node, side='south', position='middle', role='to', direction_hint='west', peer=from_node, edge_type=self.edge_type)
        else:
            # rule 2.b.2.a - SOUTH-LEFT for Activity
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=to_node_channel, node=to_node, side='south', position='left', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)

        # get the connecting points
        joining_points = self.channel_collection.connecting_points(point_from=from_node_points_in_pool_coordinate[-1], point_to=to_node_points_in_pool_coordinate[0])

        # we have the points, now create and return the flow
        flow_points = from_node_points_in_pool_coordinate + joining_points + to_node_points_in_pool_coordinate
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        implementation of rule 1.b - *to-node* is NOT the first node of its channel
        going one channel southward from-node [{0}] and approaching to-node [{1}] from top
    '''
    def southward_south_to_north(self, from_node, to_node, label):
        # rule 1.b.1 - from-node's snap-position is on SOUTH-MIDDLE
        from_node_channel = self.channel_collection.channel_of_node(from_node)
        from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=from_node_channel, node=from_node, side='south', position='middle', role='from', direction_hint='east', peer=to_node, edge_type=self.edge_type)

        # rule 1.b.2 - to-node's snap-position is on
        to_node_channel = self.channel_collection.channel_of_node(to_node)
        if to_node.category in ['Event', 'Gateway', 'Data']:
            # rule 1.b.2.b NORTH-MIDDLE for Gateway/Event/Data
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=to_node_channel, node=to_node, side='north', position='middle', role='to', direction_hint='west', peer=from_node, edge_type=self.edge_type)
        else:
            # rule 1.b.2.a NORTH-LEFT for Activity
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=to_node_channel, node=to_node, side='north', position='left', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)

        # get the connecting points
        joining_points = self.channel_collection.connecting_points(point_from=from_node_points_in_pool_coordinate[-1], point_to=to_node_points_in_pool_coordinate[0])

        # we have the points, now create and return the flow
        flow_points = from_node_points_in_pool_coordinate + joining_points + to_node_points_in_pool_coordinate
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        implementation of rule 1.a - *to-node* is the first node of its Channel
        going one channel southward from-node [{0}] and approaching to-node [{1}] from left
    '''
    def southward_south_to_west(self, from_node, to_node, label):
        # rule 1.a.1 - get the path to boundary for *from-node* in pool coordinate
        from_node_channel = self.channel_collection.channel_of_node(from_node)
        from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=from_node_channel, node=from_node, side='south', position='middle', role='from', direction_hint='east', peer=to_node, edge_type=self.edge_type)

        # rule 1.a.2 - get the path to boundary for *to-node* in pool coordinate
        to_node_channel = self.channel_collection.channel_of_node(to_node)
        to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='west', edgeover='outside', channel=to_node_channel, node=to_node, side='west', position='middle', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)


        # get the connecting points
        joining_points = self.channel_collection.connecting_points(point_from=from_node_points_in_pool_coordinate[-1], point_to=to_node_points_in_pool_coordinate[0])

        # we have the points, now create and return the flow
        flow_points = from_node_points_in_pool_coordinate + joining_points + to_node_points_in_pool_coordinate
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        rule 2 - *from-node* channel is below the *to-node* channel
    '''
    def northward(self, from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal):
        if self.channel_collection.node_xy(to_node).west_of(self.channel_collection.node_xy(from_node)):
            # rule 2.a - *to-node* is to the left (west) of *from-node* in pool coordinate
            return self.northward_north_to_south_westward(from_node, to_node, label)
        else:
            # rule 2.b - *to-node* is to the right (east) of *from-node* in pool coordinate
            return self.northward_north_to_south_eastward(from_node, to_node, label)


    '''
        rule 1 - *from-node* channel is above the *to-node* channel
    '''
    def southward(self, from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal):
        if to_node_ordinal == 0:
            # rule 1.a - *to-node* is the first node of its Channel
            if self.channel_collection.node_xy(to_node).west_of(self.channel_collection.node_xy(from_node)):
                return self.southward_south_to_north(from_node, to_node, label)
            else:
                return self.southward_south_to_west(from_node, to_node, label)
        else:
            # Rule 1.b - *to-node* is NOT the first node of its channel
            return self.southward_south_to_north(from_node, to_node, label)


    '''
        the entry method that decides which rule to apply
    '''
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

        # decide which rule to apply
        if from_node_channel_number < to_node_channel_number:
            # rule #1 - *from-node* channel is above the *to-node* channel
            return self.southward(from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal)
        else:
            # rule #2 - *from-node* channel is below the *to-node* channel
            return self.northward(from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal)
