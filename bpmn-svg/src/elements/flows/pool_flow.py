#!/usr/bin/env python3
'''
'''
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
                a   EAST-TOP for Activity
                b   EAST-MIDDLE for Gateway/Event/Data
            2)   to-node's snap-position is on
                a   SOUTH-RIGHT for Activity
                b   SOUTH-MIDDLE for Gateway/Event/Data
        b)  *to-node* is to the right (east) of *from-node* in pool coordinate
            1)  from-node's snap-position is on
                a   EAST-TOP for Activity
                b   EAST-MIDDLE for Gateway/Event/Data
            2)   to-node's snap-position is on
                a   SOUTH-LEFT for Activity
                b   SOUTH-MIDDLE for Gateway/Event/Data
'''
SNAP_RULES = {
    'south': {
        'from-node': {
            'east-most': {
                'activity': {'side': 'east',    'position': 'bottom',   'route-direction': 'east',  'direction-hint': None},
                'gateway':  {'side': 'east',    'position': 'middle',   'route-direction': 'east',  'direction-hint': None},
                'event':    {'side': 'east',    'position': 'middle',   'route-direction': 'east',  'direction-hint': None},
                'data':     {'side': 'east',    'position': 'middle',   'route-direction': 'east',  'direction-hint': None},
            },
            '*': {
                'activity': {'side': 'south',   'position': 'right',    'route-direction': 'south', 'direction-hint': None},
                'gateway':  {'side': 'south',   'position': 'middle',   'route-direction': 'south', 'direction-hint': 'east'},
                'event':    {'side': 'south',   'position': 'middle',   'route-direction': 'south', 'direction-hint': 'east'},
                'data':     {'side': 'south',   'position': 'middle',   'route-direction': 'south', 'direction-hint': 'east'},
            },
        },
        'to-node': {
            'west-most': {
                'activity': {'side': 'west',    'position': 'middle',   'route-direction': 'west',  'direction-hint': None},
                'gateway':  {'side': 'west',    'position': 'middle',   'route-direction': 'west',  'direction-hint': None},
                'event':    {'side': 'west',    'position': 'middle',   'route-direction': 'west',  'direction-hint': None},
                'data':     {'side': 'west',    'position': 'middle',   'route-direction': 'west',  'direction-hint': None},
            },
            '*': {
                'activity': {'side': 'north',   'position': 'left',     'route-direction': 'north', 'direction-hint': None},
                'gateway':  {'side': 'west',    'position': 'middle',   'route-direction': 'north', 'direction-hint': 'west'},
                'event':    {'side': 'west',    'position': 'middle',   'route-direction': 'north', 'direction-hint': 'west'},
                'data':     {'side': 'west',    'position': 'middle',   'route-direction': 'north', 'direction-hint': 'west'},
            },
        },
    },
    'north': {
        'from-node': {
            'east-most': {
                'activity': {'side': 'east',    'position': 'top',      'route-direction': 'east',  'direction-hint': None},
                'gateway':  {'side': 'east',    'position': 'middle',   'route-direction': 'east',  'direction-hint': None},
                'event':    {'side': 'east',    'position': 'middle',   'route-direction': 'east',  'direction-hint': None},
                'data':     {'side': 'east',    'position': 'middle',   'route-direction': 'east',  'direction-hint': None},
            },
            '*': {
                'activity': {'side': 'north',   'position': 'right',    'route-direction': 'north', 'direction-hint': None},
                'gateway':  {'side': 'north',   'position': 'middle',   'route-direction': 'north', 'direction-hint': 'east'},
                'event':    {'side': 'north',   'position': 'middle',   'route-direction': 'north', 'direction-hint': 'east'},
                'data':     {'side': 'north',   'position': 'middle',   'route-direction': 'north', 'direction-hint': 'east'},
            },
        },
        'to-node': {
            'west-most': {
                'activity': {'side': 'west',    'position': 'middle',   'route-direction': 'west',  'direction-hint': None},
                'gateway':  {'side': 'west',    'position': 'middle',   'route-direction': 'west',  'direction-hint': None},
                'event':    {'side': 'west',    'position': 'middle',   'route-direction': 'west',  'direction-hint': None},
                'data':     {'side': 'west',    'position': 'middle',   'route-direction': 'west',  'direction-hint': None},
            },
            '*': {
                'activity': {'side': 'south',   'position': 'left',     'route-direction': 'south', 'direction-hint': None},
                'gateway':  {'side': 'south',   'position': 'middle',   'route-direction': 'south', 'direction-hint': 'east'},
                'event':    {'side': 'south',   'position': 'middle',   'route-direction': 'south', 'direction-hint': 'east'},
                'data':     {'side': 'south',   'position': 'middle',   'route-direction': 'south', 'direction-hint': 'east'},
            },
        },
    },
}

class PoolFlow(FlowObject):

    def __init__(self, edge_type, channel_collection):
        super().__init__(edge_type)
        self.channel_collection = channel_collection
        self.snap_rules = SNAP_RULES

    '''
        the entry method that decides which rule to apply
    '''
    def create_flow(self, from_node, to_node, label):
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

        from_node_channel = self.channel_collection.channel_of_node(from_node)
        to_node_channel = self.channel_collection.channel_of_node(to_node)

        # first we need the diection from from_node to to_node
        if from_node_channel_number < to_node_channel_number:
            direction = 'south'
        else:
            direction = 'north'

        # node-positions
        if from_node_ordinal == len(from_node_channel.nodes) - 1:
            from_node_position = 'east-most'
        else:
            from_node_position = '*'

        if to_node_ordinal == 0:
            to_node_position = 'west-most'
        else:
            to_node_position = '*'


        # now we know the rule to chose for snapping and routing for the *from* and *to* node
        from_node_spec = self.snap_rules[direction]['from-node'][from_node_position][from_node.category]
        to_node_spec = self.snap_rules[direction]['to-node'][to_node_position][to_node.category]

        from_node_points_in_pool_coordinate = self.channel_collection.outside_the_channel(
                                                boundary=from_node_spec['route-direction'],
                                                channel=from_node_channel,
                                                node=from_node,
                                                side=from_node_spec['side'],
                                                position=from_node_spec['position'],
                                                role='from',
                                                direction_hint=from_node_spec['direction-hint'],
                                                peer=to_node,
                                                edge_type=self.edge_type)

        if from_node_points_in_pool_coordinate is None:
            warn('could not calculate snap points for from-node [{0}]'.format(from_node.id))
            return None

        to_node_points_in_pool_coordinate = self.channel_collection.outside_the_channel(
                                                boundary=to_node_spec['route-direction'],
                                                channel=to_node_channel,
                                                node=to_node,
                                                side=to_node_spec['side'],
                                                position=to_node_spec['position'],
                                                role='to',
                                                direction_hint=to_node_spec['direction-hint'],
                                                peer=to_node,
                                                edge_type=self.edge_type)

        if to_node_points_in_pool_coordinate is None:
            warn('could not calculate snap points for to-node [{0}]'.format(to_node.id))
            return None


        # get the connecting points
        # warn('-------------------------------------------------------------------------------------------------------------------------')
        # warn('{0}-ward = [{1}:{2}-{3}]::{4} --> [{5}:{6}-{7}]::{8}'.format(direction, from_node.id, from_node_spec['side'], from_node_spec['position'], from_node_spec['route-direction'], to_node.id, to_node_spec['side'], to_node_spec['position'], to_node_spec['route-direction']))
        # warn('-------------------------------------------------------------------------------------------------------------------------\n')
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
        from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', side='south', position='middle', direction_hint='east')

        # rule 1.b.2 - to-node's snap-position is on
        if to_node.category in ['event', 'gateway', 'data']:
            # rule 1.b.2.b NORTH-MIDDLE for Gateway/Event/Data
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', side='north', position='middle', direction_hint='west')
        else:
            # rule 1.b.2.a NORTH-LEFT for Activity
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='north', side='north', position='left', direction_hint=None)


    '''
        implementation of rule 1.a - *to-node* is the first node of its Channel
        going one channel southward from-node [{0}] and approaching to-node [{1}] from left
    '''
    def southward_south_to_west(self, from_node, to_node, label):
        # rule 1.a.1 - get the path to boundary for *from-node* in pool coordinate
        from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', side='south', position='middle', direction_hint='east')

        # rule 1.a.2 - get the path to boundary for *to-node* in pool coordinate
        to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='west', side='west', position='middle', direction_hint=None)


    '''
        implementation of rule 2.a - *to-node* is to the left (west) of *from-node* in pool coordinate
        going one channel southward from-node [{0}] and approaching to-node [{1}] from top
    '''
    def northward_north_to_south_westward(self, from_node, to_node, label):
        # rule 2.a.1 - from-node's snap-position is on
        if from_node.category in ['event', 'gateway', 'data']:
            # rule 2.a.1.b - NORTH-MIDDLE for Gateway/Event/Data
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='east', side='east', position='middle', direction_hint='east')
        else:
            # rule 2.a.1.a - is on NORTH-RIGHT for Activity
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='east', side='east', position='top', direction_hint=None)

        # rule 2.a.2 - to-node's snap-position is on
        if to_node.category in ['event', 'gateway', 'data']:
            # rule 2.a.2.b - SOUTH-MIDDLE for Gateway/Event/Data
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', side='south', position='middle', direction_hint='east')
        else:
            # rule 2.a.2.b - SOUTH-LEFT for Activity
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', side='south', position='left', direction_hint=None)


    '''
        implementation of rule 2.b - *to-node* is to the right (east) of *from-node* in pool coordinate
        going one channel southward from-node [{0}] and approaching to-node [{1}] from top
    '''
    def northward_north_to_south_eastward(self, from_node, to_node, label):
        # rule 2.b.1 - from-node's snap-position
        if from_node.category in ['event', 'gateway', 'data']:
            # rule 2.b.1.b - EAST-MIDDLE for Gateway/Event/Data
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='east', side='east', position='middle', direction_hint='east')
        else:
            # rule 2.b.1.a -is on EAST-RIGHT for Activity
            from_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='east', side='east', position='top', direction_hint='east')

        # rule 2.b.2 - to-node's snap-position is on
        if to_node.category in ['event', 'gateway', 'data']:
            # rule 2.b.2.b - SOUTH-MIDDLE for Gateway/Event/Data
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', side='south', position='middle', direction_hint='west')
        else:
            # rule 2.b.2.a - SOUTH-LEFT for Activity
            to_node_points_in_pool_coordinate = self.channel_collection.to_boundary(boundary='south', side='south', position='left', direction_hint=None)
