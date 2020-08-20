#!/usr/bin/env python3
'''
'''
from elements.svg_element import SvgElement
from elements.flows.flow_object import FlowObject

from util.logger import *
from util.geometry import Point
from util.svg_util import *

'''
    Class to handle a flows/edges inside the channel which means between nodes inside a specific channel.

    A channel is by definition a straight horizontal stack of nodes, so edges are mostly straight lines from left to right (west to east) except when there is a loop back from a child to a previous node towards left (west).

    The rules are defined in SNAP_RULES
    1. The first key is the direction from from_node to to_node (east/west)
    2. the second key is the node's distance (adjacent/apart/*)
'''

SNAP_RULES = {
    'east': {
        'adjacent' : {
            'from-node': {
                'activity': {'side': 'east',    'position': 'middle',   'cross-through-boundary': None,    'approach-snap-point-from': None},
                'gateway':  {'side': 'east',    'position': 'middle',   'cross-through-boundary': None,    'approach-snap-point-from': None},
                'event':    {'side': 'east',    'position': 'middle',   'cross-through-boundary': None,    'approach-snap-point-from': None},
                'data':     {'side': 'east',    'position': 'middle',   'cross-through-boundary': None,    'approach-snap-point-from': None},
            },
            'to-node': {
                'activity': {'side': 'west',    'position': 'middle',   'cross-through-boundary': None,    'approach-snap-point-from': None},
                'gateway':  {'side': 'west',    'position': 'middle',   'cross-through-boundary': None,    'approach-snap-point-from': None},
                'event':    {'side': 'west',    'position': 'middle',   'cross-through-boundary': None,    'approach-snap-point-from': None},
                'data':     {'side': 'west',    'position': 'middle',   'cross-through-boundary': None,    'approach-snap-point-from': None},
            }
        },
        'apart' : {
            'from-node': {
                'activity': {'side': 'east',    'position': 'bottom',   'cross-through-boundary': 'south', 'approach-snap-point-from': None},
                'gateway':  {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': None},
                'event':    {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': None},
                'data':     {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': None},
            },
            'to-node': {
                'activity': {'side': 'west',    'position': 'bottom',   'cross-through-boundary': 'south', 'approach-snap-point-from': None},
                'gateway':  {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': None},
                'event':    {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': None},
                'data':     {'side': 'west',    'position': 'middle',   'cross-through-boundary': 'south', 'approach-snap-point-from': None},
            },
        },
    },
    'west': {
        '*' : {
            'from-node': {
                'activity': {'side': 'east',    'position': 'top',      'cross-through-boundary': 'north', 'approach-snap-point-from': None},
                'gateway':  {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': None},
                'event':    {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': None},
                'data':     {'side': 'east',    'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': None},
            },
            'to-node': {
                'activity': {'side': 'west',    'position': 'top',      'cross-through-boundary': 'north', 'approach-snap-point-from': None},
                'gateway':  {'side': 'north',   'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': 'west'},
                'event':    {'side': 'north',   'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': 'west'},
                'data':     {'side': 'north',   'position': 'middle',   'cross-through-boundary': 'north', 'approach-snap-point-from': 'west'},
            }
        },
    },
}

class ChannelFlow(FlowObject):

    def __init__(self, edge_type, channel):
        super().__init__(edge_type)
        self.channel = channel
        self.snap_rules = SNAP_RULES


    '''
        the entry method that decides which rule to apply
    '''
    def create_flow(self, from_node, to_node, label):
        # first we need the diection from from_node to to_node
        if from_node.element.xy.west_of(to_node.element.xy):
            direction = 'east'
            # are they adjacent or apart
            if (self.channel.node_ordinal(to_node) - self.channel.node_ordinal(from_node)) == 1:
                distance = 'adjacent'
            else:
                distance = 'apart'
        elif from_node.element.xy.east_of(to_node.element.xy):
            direction = 'west'
            distance = '*'
        else:
            warn('from-node [{0}] and to-node [{1}] starts at same x position, they can not be connected inside a channel which is supposed to have all nodes on different x position on same y')
            return None

        # now we know the rule to chose for snapping and routing for the *from* and *to* node
        from_node_spec = self.snap_rules[direction][distance]['from-node'][from_node.category]
        to_node_spec = self.snap_rules[direction][distance]['to-node'][to_node.category]

        from_node_points_in_channel = self.channel.inside_the_channel(
                                        boundary=from_node_spec['cross-through-boundary'],
                                        node=from_node,
                                        side=from_node_spec['side'],
                                        position=from_node_spec['position'],
                                        role='from',
                                        approach_snap_point_from=from_node_spec['approach-snap-point-from'],
                                        peer=to_node,
                                        edge_type=self.edge_type)

        if from_node_points_in_channel is None:
            warn('could not calculate snap points for from-node [{0}]'.format(from_node.id))
            return None

        to_node_points_in_channel = self.channel.inside_the_channel(
                                        boundary=to_node_spec['cross-through-boundary'],
                                        node=to_node,
                                        side=to_node_spec['side'],
                                        position=to_node_spec['position'],
                                        role='to',
                                        approach_snap_point_from=to_node_spec['approach-snap-point-from'],
                                        peer=to_node,
                                        edge_type=self.edge_type)

        if to_node_points_in_channel is None:
            warn('could not calculate snap points for to-node [{0}]'.format(to_node.id))
            return None

        # we now have two segments we connect the last point of *from-segment* to the first point of *to-segment* through a north-ward path
        flow_points = from_node_points_in_channel + to_node_points_in_channel

        # we have the points, now create and return the flow
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)
