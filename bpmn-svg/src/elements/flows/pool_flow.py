#!/usr/bin/env python3
'''
'''
from elements.svg_element import SvgElement
from elements.flows.flow_object import FlowObject

from util.logger import *
from util.geometry import Point
from util.svg_util import *

'''
    Class to handle a flows/edges between channels of a pool
    Criteria - from-node and to-node must be in in two different channels under the same pool
'''
SNAP_RULES = {
    'south': {
        'from-node': {
            'east-most': {
                'activity': {'side': 'east',    'position': 'bottom',   'cross-through-boundary': 'east',  'approach-snap-point-from': None},
                'gateway':  {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'east',  'approach-snap-point-from': None},
                'event':    {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'east',  'approach-snap-point-from': None},
                'data':     {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'east',  'approach-snap-point-from': None},
            },
            '*': {
                'activity': {'side': 'south',   'position': 'right',    'cross-through-boundary': 'south', 'approach-snap-point-from': None},
                'gateway':  {'side': 'south',   'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': 'east'},
                'event':    {'side': 'south',   'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': 'east'},
                'data':     {'side': 'south',   'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': 'east'},
            },
        },
        'to-node': {
            'west-most': {
                'activity': {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'west',  'approach-snap-point-from': None},
                'gateway':  {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'west',  'approach-snap-point-from': None},
                'event':    {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'west',  'approach-snap-point-from': None},
                'data':     {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'west',  'approach-snap-point-from': None},
            },
            '*': {
                'activity': {'side': 'north',   'position': 'left',     'cross-through-boundary': 'north', 'approach-snap-point-from': None},
                'gateway':  {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': 'west'},
                'event':    {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': 'west'},
                'data':     {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': 'west'},
            },
        },
    },
    'north': {
        'from-node': {
            'east-most': {
                'activity': {'side': 'east',    'position': 'top',      'cross-through-boundary': 'east',  'approach-snap-point-from': None},
                'gateway':  {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'east',  'approach-snap-point-from': None},
                'event':    {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'east',  'approach-snap-point-from': None},
                'data':     {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'east',  'approach-snap-point-from': None},
            },
            '*': {
                'activity': {'side': 'north',   'position': 'right',    'cross-through-boundary': 'north', 'approach-snap-point-from': None},
                'gateway':  {'side': 'north',   'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': 'east'},
                'event':    {'side': 'north',   'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': 'east'},
                'data':     {'side': 'north',   'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': 'east'},
            },
        },
        'to-node': {
            'west-most': {
                'activity': {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'west',  'approach-snap-point-from': None},
                'gateway':  {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'west',  'approach-snap-point-from': None},
                'event':    {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'west',  'approach-snap-point-from': None},
                'data':     {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'west',  'approach-snap-point-from': None},
            },
            '*': {
                'activity': {'side': 'south',   'position': 'left',     'cross-through-boundary': 'south', 'approach-snap-point-from': None},
                'gateway':  {'side': 'south',   'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': 'east'},
                'event':    {'side': 'south',   'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': 'east'},
                'data':     {'side': 'south',   'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': 'east'},
            },
        },
    },
}

class PoolFlow(FlowObject):

    def __init__(self, edge_type, channel_collection):
        super().__init__(edge_type)
        self.channel_collection = channel_collection
        self.snap_rules = SNAP_RULES


    def validate(self, from_node_channel, to_node_channel, from_node, to_node):
        if from_node_channel is None:
            warn('this should not happen: from_node [{0}] can not be found in any channel'.format(from_node.id))
            return False

        if to_node_channel is None:
            warn('this should not happen: to_node [{0}] can not be found in any channel'.format(to_node.id))
            return False

        if from_node_channel.number == to_node_channel.number:
            warn('this should not happen: from_node [{0}] and to_node [{1}] both are in same channel [{2}]'.format(from_node.id, to_node.id, from_node_channel_number))
            return False


    '''
        the entry method that decides which rule to apply
    '''
    def create_flow(self, from_node, to_node, label):
        from_node_channel, from_node_ordinal = self.channel_collection.channel_and_ordinal(from_node)
        to_node_channel, to_node_ordinal = self.channel_collection.channel_and_ordinal(to_node)

        if self.validate(from_node_channel, to_node_channel, from_node, to_node) == False: return None

        # first we need the diection from from_node to to_node
        if from_node_channel.number < to_node_channel.number:
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
                                                boundary=from_node_spec['cross-through-boundary'],
                                                channel=from_node_channel,
                                                node=from_node,
                                                side=from_node_spec['side'],
                                                position=from_node_spec['position'],
                                                role='from',
                                                approach_snap_point_from=from_node_spec['approach-snap-point-from'],
                                                peer=to_node,
                                                edge_type=self.edge_type)

        if from_node_points_in_pool_coordinate is None:
            warn('could not calculate snap points for from-node [{0}]'.format(from_node.id))
            return None

        to_node_points_in_pool_coordinate = self.channel_collection.outside_the_channel(
                                                boundary=to_node_spec['cross-through-boundary'],
                                                channel=to_node_channel,
                                                node=to_node,
                                                side=to_node_spec['side'],
                                                position=to_node_spec['position'],
                                                role='to',
                                                approach_snap_point_from=to_node_spec['approach-snap-point-from'],
                                                peer=to_node,
                                                edge_type=self.edge_type)

        if to_node_points_in_pool_coordinate is None:
            warn('could not calculate snap points for to-node [{0}]'.format(to_node.id))
            return None

        # we always connect from the north point to the south point
        if from_node_points_in_pool_coordinate[-1].north_of(to_node_points_in_pool_coordinate[0]):
            north_point = from_node_points_in_pool_coordinate[-1]
            south_point = to_node_points_in_pool_coordinate[0]
            joining_points = self.channel_collection.connect_southward(point_from=north_point, point_to=south_point)
        else:
            north_point = to_node_points_in_pool_coordinate[0]
            south_point = from_node_points_in_pool_coordinate[-1]
            joining_points = self.channel_collection.connect_southward(point_from=north_point, point_to=south_point)
            joining_points.reverse()

        # self.mark_points(joining_points, self.channel_collection.element.svg)

        # we have the points, now create and return the flow
        flow_points = from_node_points_in_pool_coordinate + joining_points + to_node_points_in_pool_coordinate
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)
