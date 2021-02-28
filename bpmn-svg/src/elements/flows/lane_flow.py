#!/usr/bin/env python3
'''
'''
from elements.svg_element import SvgElement
from elements.flows.flow_object import FlowObject

from util.logger import *
from util.geometry import Point
from util.svg_util import *

'''
    Class to handle a flows/edges between pools of a lane
    Criteria - from-node and to-node must be in in two different pools under the same lane
'''
SNAP_RULES = {
    'south': {
        'from-node': {
            'east-most': {
                'activity': {'side': 'east',  'position': 'middle', 'channel-boundary': 'east',  'approach-snap-point-from': None},
                'gateway':  {'side': 'south', 'position': 'middle', 'channel-boundary': 'south', 'approach-snap-point-from': None},
                'event':    {'side': 'south', 'position': 'middle', 'channel-boundary': 'south', 'approach-snap-point-from': None},
                'data':     {'side': 'south', 'position': 'middle', 'channel-boundary': 'south', 'approach-snap-point-from': None},
            },
            '*': {
                'activity': {'side': 'south', 'position': 'middle', 'channel-boundary': 'south', 'approach-snap-point-from': None},
                'gateway':  {'side': 'south', 'position': 'middle', 'channel-boundary': 'south', 'approach-snap-point-from': 'east'},
                'event':    {'side': 'south', 'position': 'middle', 'channel-boundary': 'south', 'approach-snap-point-from': 'east'},
                'data':     {'side': 'south', 'position': 'middle', 'channel-boundary': 'south', 'approach-snap-point-from': 'east'},
            },
        },
        'to-node': {
            'west-most': {
                'activity': {'side': 'west',  'position': 'middle', 'channel-boundary': 'west',  'approach-snap-point-from': None},
                'gateway':  {'side': 'west',  'position': 'middle', 'channel-boundary': 'west',  'approach-snap-point-from': None},
                'event':    {'side': 'west',  'position': 'middle', 'channel-boundary': 'west',  'approach-snap-point-from': None},
                'data':     {'side': 'north', 'position': 'middle', 'channel-boundary': 'north', 'approach-snap-point-from': None},
            },
            '*': {
                'activity': {'side': 'north', 'position': 'left',   'channel-boundary': 'north', 'approach-snap-point-from': None},
                'gateway':  {'side': 'west',  'position': 'middle', 'channel-boundary': 'north', 'approach-snap-point-from': 'west'},
                'event':    {'side': 'west',  'position': 'middle', 'channel-boundary': 'north', 'approach-snap-point-from': 'west'},
                'data':     {'side': 'north', 'position': 'middle', 'channel-boundary': 'north', 'approach-snap-point-from': 'west'},
            },
        },
    },
    'north': {
        'from-node': {
            'east-most': {
                'activity': {'side': 'east',  'position': 'top',    'channel-boundary': 'east',  'approach-snap-point-from': None},
                'gateway':  {'side': 'east',  'position': 'middle', 'channel-boundary': 'east',  'approach-snap-point-from': None},
                'event':    {'side': 'east',  'position': 'middle', 'channel-boundary': 'east',  'approach-snap-point-from': None},
                'data':     {'side': 'east',  'position': 'middle', 'channel-boundary': 'east',  'approach-snap-point-from': None},
            },
            '*': {
                'activity': {'side': 'north', 'position': 'right',  'channel-boundary': 'north', 'approach-snap-point-from': None},
                'gateway':  {'side': 'north', 'position': 'middle', 'channel-boundary': 'north', 'approach-snap-point-from': 'east'},
                'event':    {'side': 'north', 'position': 'middle', 'channel-boundary': 'north', 'approach-snap-point-from': 'east'},
                'data':     {'side': 'north', 'position': 'middle', 'channel-boundary': 'north', 'approach-snap-point-from': 'east'},
            },
        },
        'to-node': {
            'west-most': {
                'activity': {'side': 'west',  'position': 'middle', 'channel-boundary': 'west',  'approach-snap-point-from': None},
                'gateway':  {'side': 'west',  'position': 'middle', 'channel-boundary': 'west',  'approach-snap-point-from': None},
                'event':    {'side': 'west',  'position': 'middle', 'channel-boundary': 'west',  'approach-snap-point-from': None},
                'data':     {'side': 'west',  'position': 'middle', 'channel-boundary': 'west',  'approach-snap-point-from': None},
            },
            '*': {
                'activity': {'side': 'south', 'position': 'left',   'channel-boundary': 'south', 'approach-snap-point-from': None},
                'gateway':  {'side': 'south', 'position': 'middle', 'channel-boundary': 'south', 'approach-snap-point-from': 'east'},
                'event':    {'side': 'south', 'position': 'middle', 'channel-boundary': 'south', 'approach-snap-point-from': 'east'},
                'data':     {'side': 'south', 'position': 'middle', 'channel-boundary': 'south', 'approach-snap-point-from': 'east'},
            },
        },
    },
}

class LaneFlow(FlowObject):

    def __init__(self, edge_type, pool_collection):
        super().__init__(edge_type)
        self.pool_collection = pool_collection
        self.snap_rules = SNAP_RULES
        self.flow_scope = 'LaneFlow'


    def validate(self, from_node_pool_number, to_node_pool_number, from_node, to_node):
        if from_node_pool_number is None:
            warn('this should not happen: from_node [{0}] can not be found in any pool'.format(from_node.id))
            return False

        if to_node_pool_number is None:
            warn('this should not happen: to_node [{0}] can not be found in any pool'.format(to_node.id))
            return False

        if from_node_pool_number == to_node_pool_number:
            warn('this should not happen: from_node [{0}] and to_node [{1}] both are in same pool [{2}]'.format(from_node.id, to_node.id, from_node_pool_number))
            return False


    '''
        the entry method that decides which rule to apply
    '''
    def create_flow(self, from_node, to_node, label, label_style):
        from_node_pool_number, from_node_pool_id = self.pool_collection.pool_number_and_id(from_node)
        to_node_pool_number, to_node_pool_id = self.pool_collection.pool_number_and_id(to_node)

        if self.validate(from_node_pool_number, to_node_pool_number, from_node, to_node) == False: return None

        # debug('LANE [{0}] - [{1}:{2}:{3}] --> [{4}:{5}:{6}]'.format(self.pool_collection.lane_id, from_node_pool_number, from_node_pool_id, from_node.id, to_node_pool_number, to_node_pool_id, to_node.id))

        # first we need the diection from from_node to to_node
        if from_node_pool_number < to_node_pool_number:
            direction = 'south'
            from_node_pool_boundary = 'south'
            to_node_pool_boundary = 'north'
        else:
            direction = 'north'
            from_node_pool_boundary = 'north'
            to_node_pool_boundary = 'south'

        # node-positions
        from_node_channel, from_node_ordinal = self.pool_collection.channel_and_ordinal(from_node)
        if from_node_ordinal == len(from_node_channel.nodes) - 1:
            from_node_position = 'east-most'
        else:
            from_node_position = '*'

        to_node_channel, to_node_ordinal = self.pool_collection.channel_and_ordinal(to_node)
        if to_node_ordinal == 0:
            to_node_position = 'west-most'
        else:
            to_node_position = '*'


        # now we know the rule to chose for snapping and routing for the *from* and *to* node
        from_node_spec = self.snap_rules[direction]['from-node'][from_node_position][from_node.category]
        to_node_spec = self.snap_rules[direction]['to-node'][to_node_position][to_node.category]

        from_node_pool_boundary = from_node_spec['channel-boundary']
        to_node_pool_boundary = to_node_spec['channel-boundary']

        from_node_points_in_lane_coordinate = self.pool_collection.outside_the_pool(
                                                pool_boundary=from_node_pool_boundary,
                                                pool_number=from_node_pool_number,
                                                channel_boundary=from_node_spec['channel-boundary'],
                                                channel=from_node_channel,
                                                node=from_node,
                                                side=from_node_spec['side'],
                                                position=from_node_spec['position'],
                                                role='from',
                                                approach_snap_point_from=from_node_spec['approach-snap-point-from'],
                                                peer=to_node,
                                                edge_type=self.edge_type)

        if from_node_points_in_lane_coordinate is None:
            warn('could not calculate snap points for from-node [{0}]'.format(from_node.id))
            return None

        # warn('from_node points: [{0}]'.format(optimize_points(from_node_points_in_lane_coordinate)))


        to_node_points_in_lane_coordinate = self.pool_collection.outside_the_pool(
                                                pool_boundary=to_node_pool_boundary,
                                                pool_number=to_node_pool_number,
                                                channel_boundary=to_node_spec['channel-boundary'],
                                                channel=to_node_channel,
                                                node=to_node,
                                                side=to_node_spec['side'],
                                                position=to_node_spec['position'],
                                                role='to',
                                                approach_snap_point_from=to_node_spec['approach-snap-point-from'],
                                                peer=to_node,
                                                edge_type=self.edge_type)

        if to_node_points_in_lane_coordinate is None:
            warn('could not calculate snap points for to-node [{0}]'.format(to_node.id))
            return None

        # we always connect from the north point to the south point
        if from_node_points_in_lane_coordinate[-1].north_of(to_node_points_in_lane_coordinate[0]):
            north_point = from_node_points_in_lane_coordinate[-1]
            south_point = to_node_points_in_lane_coordinate[0]
            joining_points = self.pool_collection.connect_southward(from_pool_number=from_node_pool_number, point_from=north_point, to_pool_number=to_node_pool_number, point_to=south_point)
        else:
            north_point = to_node_points_in_lane_coordinate[0]
            south_point = from_node_points_in_lane_coordinate[-1]
            joining_points = self.pool_collection.connect_southward(from_pool_number=to_node_pool_number, point_from=north_point, to_pool_number=from_node_pool_number, point_to=south_point)
            joining_points.reverse()

        # self.mark_points(from_node_points_in_lane_coordinate, self.pool_collection.element.svg, 'red')
        # self.mark_points(to_node_points_in_lane_coordinate, self.pool_collection.element.svg, 'green')

        # we have the points, now create and return the flow
        flow_points = from_node_points_in_lane_coordinate + joining_points + to_node_points_in_lane_coordinate
        # warn('flow points: [{0}]'.format(optimize_points(flow_points)))

        # determine the placement of the label
        label_data = None
        if label is not None and label != '':
            label_data = {}
            label_data['text'] = label
            # get the first vertical line segment having a min-length
            point_from, point_to = first_vertical_line_segment_longer_than(flow_points, 30)
            # the main connecting line for ChannelFlow is a horizontal line
            label_data['line-points'] = {'from': point_from, 'to': point_to}
            label_data['line-direction'] = 'north-south'
            # the text should be placed on top of the line
            label_data['placement'] = label_style.get('placement', 'east')
            label_data['move-x'] = float(label_style.get('move_x', 0))
            label_data['move-y'] = float(label_style.get('move_y', 20))

        flow_svg, flow_width, flow_height = a_flow(flow_points, label_data, self.theme, self.flow_scope)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)
