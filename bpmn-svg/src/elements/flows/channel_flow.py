#!/usr/bin/env python3
'''
'''
from elements.svg_element import SvgElement
from elements.flows.flow_object import FlowObject

from util.logger import *
from util.geometry import Point
from util.svg_util import *

'''
    Class to handle a flows/edges inside a channel
    A channel is by definition a straight horizontal stack of nodes, so edges are mostly straight lines from left to right (west to east) except when there is a loop back from a child to a previous node towards left (west).
    Criteria - from-node and to-node must be in the same channel
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

    def __init__(self, current_theme, edge_type, channel):
        super().__init__(current_theme, edge_type)
        self.channel = channel
        self.snap_rules = SNAP_RULES
        self.flow_scope = 'ChannelFlow'


    '''
        the entry method that decides which rule to apply
    '''
    def create_flow(self, from_node, to_node, label, label_style):
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
        flow_points = optimize_points(flow_points)

        # determine the placement of the label
        label_data = None
        if label is not None and label != '':
            label_data = {}
            label_data['text'] = label
            # get the longest horizontal line segment
            point_from, point_to = longest_horizontal_line_segment(flow_points)
            # the main connecting line for ChannelFlow is a horizontal line
            label_data['line-points'] = {'from': point_from, 'to': point_to}
            label_data['line-direction'] = 'east-west'
            # the text should be placed on top of the line
            label_data['placement'] = label_style.get('placement', 'north')
            label_data['move-x'] = float(label_style.get('move_x', 0))
            label_data['move-y'] = float(label_style.get('move_y', 0))

        # we have the points, now create and return the flow
        flow_svg, flow_width, flow_height = a_flow(flow_points, label_data, self.theme, self.flow_scope)


        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)
