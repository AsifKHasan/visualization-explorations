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
        a)  *from-node* channel is adjacent to *to-node* channel
            1. *to-node* is the first node of its Channel
                a) from-node's snap-position is on
                    1   SOUTH-MIDDLE
                b) to-node's snap-position is on
                    1   WEST-MIDDLE
            2. *to-node* is NOT the first node of its Channel
                a) from-node's snap-position is on
                    1   SOUTH-MIDDLE
                b) to-node's snap-position is on
                    1   NORTH-LEFT for Activity
                    2   NORTH-MIDDLE for Gateway/Event/Data
        b)  *from-node* channel is NOT adjacent to *to-node* channel

    #2  *from-node* channel is below the *to-node* channel
        a)  *from-node* channel is adjacent to *to-node* channel
            1)  *to-node* is to the left (west) of *from-node* in pool coordinate
                a)   from-node's snap-position is on
                    1   NORTH-LEFT for Activity
                    2   NORTH-MIDDLE for Gateway/Event/Data
                b)   to-node's snap-position is on
                    1   SOUTH-RIGHT for Activity
                    2   SOUTH-MIDDLE for Gateway/Event/Data
            2)  *to-node* is to the right (east) of *from-node* in pool coordinate
                a)   from-node's snap-position is on
                    1   NORTH-RIGHT for Activity
                    2   NORTH-MIDDLE for Gateway/Event/Data
                b)   to-node's snap-position is on
                    1   SOUTH-LEFT for Activity
                    2   SOUTH-MIDDLE for Gateway/Event/Data
        b)  *from-node* channel is NOT adjacent to *to-node* channel

'''
class PoolFlow(FlowObject):

    def __init__(self, edge_type, channel_collection):
        super().__init__(edge_type)
        self.channel_collection = channel_collection

    '''
        implementation of rule 2.a.1 - *to-node* is to the left (west) of *from-node* in pool coordinate
        going one channel southward from-node [{0}] and approaching to-node [{1}] from top
    '''
    def northward_adjacent_north_to_south_westward(self, from_node, to_node, label):
        # rule 2.a.1.a - from-node's snap-position is on
        from_node_channel = self.channel_collection.channel_of_node(from_node)
        if from_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.a.1.a.2 - NORTH-MIDDLE for Gateway/Event/Data
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=from_node_channel, node=from_node, side='north', position='middle', role='from', direction_hint='east', peer=to_node, edge_type=self.edge_type)
        else:
            # rule 2.a.1.a.1 - is on NORTH-LEFT for Activity
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=from_node_channel, node=from_node, side='north', position='left', role='from', direction_hint=None, peer=to_node, edge_type=self.edge_type)

        # rule 2.a.2.b - to-node's snap-position is on
        to_node_channel = self.channel_collection.channel_of_node(to_node)
        if to_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.a.2.b.2 - SOUTH-MIDDLE for Gateway/Event/Data
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=to_node_channel, node=to_node, side='south', position='middle', role='to', direction_hint='east', peer=from_node, edge_type=self.edge_type)
        else:
            # rule 2.a.2.b.1 - SOUTH-LEFT for Activity
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=to_node_channel, node=to_node, side='south', position='left', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)

        # get the connecting points
        joining_points = []

        # we have the points, now create and return the flow
        flow_points = from_node_points_in_pool_coordinate + joining_points + to_node_points_in_pool_coordinate
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        implementation of rule 2.a.2 - *to-node* is to the right (east) of *from-node* in pool coordinate
        going one channel southward from-node [{0}] and approaching to-node [{1}] from top
    '''
    def northward_adjacent_north_to_south_eastward(self, from_node, to_node, label):
        # rule 2.a.2.a - from-node's snap-position
        from_node_channel = self.channel_collection.channel_of_node(from_node)
        if from_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.a.2.b.2 - NORTH-MIDDLE for Gateway/Event/Data
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=from_node_channel, node=from_node, side='north', position='middle', role='from', direction_hint='east', peer=to_node, edge_type=self.edge_type)
        else:
            # rule 2.a.2.b.1 -is on NORTH-RIGHT for Activity
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=from_node_channel, node=from_node, side='north', position='right', role='from', direction_hint='east', peer=to_node, edge_type=self.edge_type)

        # rule 2.a.2.b - to-node's snap-position is on
        to_node_channel = self.channel_collection.channel_of_node(to_node)
        if to_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.a.2.b.2 - SOUTH-MIDDLE for Gateway/Event/Data
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=to_node_channel, node=to_node, side='south', position='middle', role='to', direction_hint='west', peer=from_node, edge_type=self.edge_type)
        else:
            # rule 2.a.2.b.1 - SOUTH-LEFT for Activity
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=to_node_channel, node=to_node, side='south', position='left', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)

        # get the connecting points
        joining_points = []

        # we have the points, now create and return the flow
        flow_points = from_node_points_in_pool_coordinate + joining_points + to_node_points_in_pool_coordinate
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        implementation of rule 1.a.2 - *to-node* is NOT the first node of its channel
        going one channel southward from-node [{0}] and approaching to-node [{1}] from top
    '''
    def southward_adjacent_south_to_north(self, from_node, to_node, label):
        # rule 1.a.2.a - from-node's snap-position is on SOUTH-MIDDLE
        from_node_channel = self.channel_collection.channel_of_node(from_node)
        from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=from_node_channel, node=from_node, side='south', position='middle', role='from', direction_hint='east', peer=to_node, edge_type=self.edge_type)

        # rule 1.a.2.b - to-node's snap-position is on
        to_node_channel = self.channel_collection.channel_of_node(to_node)
        if to_node.category in ['Event', 'Gateway', 'Data']:
            # rule 1.a.2.b.2 NORTH-MIDDLE for Gateway/Event/Data
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=to_node_channel, node=to_node, side='north', position='middle', role='to', direction_hint='west', peer=from_node, edge_type=self.edge_type)
        else:
            # rule 1.a.2.b.1 NORTH-LEFT for Activity
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', edgeover='outside', channel=to_node_channel, node=to_node, side='north', position='left', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)

        # get the connecting points
        joining_points = []

        # we have the points, now create and return the flow
        flow_points = from_node_points_in_pool_coordinate + joining_points + to_node_points_in_pool_coordinate
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        implementation of rule 1.a.1 - *to-node* is the first node of its Channel
        going one channel southward from-node [{0}] and approaching to-node [{1}] from left
    '''
    def southward_adjacent_south_to_west(self, from_node, to_node, label):
        # rule 1.a.1.a - get the path to boundary for *from-node* in pool coordinate
        from_node_channel = self.channel_collection.channel_of_node(from_node)
        from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', edgeover='outside', channel=from_node_channel, node=from_node, side='south', position='middle', role='from', direction_hint='east', peer=to_node, edge_type=self.edge_type)

        # rule 1.a.1.b - get the path to boundary for *to-node* in pool coordinate
        to_node_channel = self.channel_collection.channel_of_node(to_node)
        to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='west', edgeover='outside', channel=to_node_channel, node=to_node, side='west', position='middle', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)


        # get the connecting points
        joining_points = [Point(from_node_points_in_pool_coordinate[-1].x, to_node_points_in_pool_coordinate[0].y)]

        # we have the points, now create and return the flow
        flow_points = from_node_points_in_pool_coordinate + joining_points + to_node_points_in_pool_coordinate
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        rule 2.b - *from-node* channel is NOT adjacent to *to-node* channel
    '''
    def northward_detached(self, from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal):
        warn('NOT IMPLEMENTED: from-node [{0}] is multiple {1} channels above to-node [{2}]'.format(from_node.id, (to_node_channel_number - from_node_channel_number), to_node.id))
        return None


    '''
        rule 2.a - *from-node* channel is adjacent to *to-node* channel
    '''
    def northward_adjacent(self, from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal):
        if self.channel_collection.node_xy(to_node).west_of(self.channel_collection.node_xy(from_node)):
            # rule 2.a.1 - *to-node* is to the left (west) of *from-node* in pool coordinate
            return self.northward_adjacent_north_to_south_westward(from_node, to_node, label)
        else:
            # rule 2.a.2 - *to-node* is to the right (east) of *from-node* in pool coordinate
            return self.northward_adjacent_north_to_south_eastward(from_node, to_node, label)


    '''
        rule 1.b - *from-node* channel is NOT adjacent to *to-node* channel
    '''
    def southward_detached(self, from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal):
        # from-node is two or more channels above the to-node
        warn('NOT IMPLEMENTED: from-node [{0}] is multiple {1} channels above to-node [{2}]'.format(from_node.id, (to_node_channel_number - from_node_channel_number), to_node.id))
        return None


    '''
        rule 1.a - *from-node* channel is adjacent to *to-node* channel
    '''
    def southward_adjacent(self, from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal):
        if to_node_ordinal == 0:
            # rule 1.a.1 - *to-node* is the first node of its Channel
            return self.southward_adjacent_south_to_west(from_node, to_node, label)
        else:
            # Rule 1.a.2 - *to-node* is NOT the first node of its channel
            return self.southward_adjacent_south_to_north(from_node, to_node, label)


    '''
        rule 2 - *from-node* channel is below the *to-node* channel
    '''
    def northward(self, from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal):
        if (from_node_channel_number - to_node_channel_number) == 1:
            # rule 2.a - *from-node* channel is adjacent to *to-node* channel
            return self.northward_adjacent(from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal)
        else:
            # rule 2.b - *from-node* channel is NOT adjacent to *to-node* channel
            return self.northward_detached(from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal)


    '''
        rule 1 - *from-node* channel is above the *to-node* channel
    '''
    def southward(self, from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal):
        if (to_node_channel_number - from_node_channel_number) == 1:
            # rule 1.a - *from-node* channel is adjacent to *to-node* channel
            return self.southward_adjacent(from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal)
        else:
            # rule 1.b - *from-node* channel is NOT adjacent to *to-node* channel
            return self.southward_detached(from_node, to_node, label, from_node_channel_number, from_node_ordinal, to_node_channel_number, to_node_ordinal)


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
