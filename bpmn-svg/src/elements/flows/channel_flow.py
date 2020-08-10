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
    Class to handle a flows/edges inside the channel which means between nodes inside a specific channel.

    A channel is by definition a straight horizontal stack of nodes, so edges are mostly straight lines from left to right (west to east) except when there is a loop back from a child to a previous node towards left (west). The rules are

    #1  *to-node* is further right (east) from *from-node* ([from-node] --> [to_node]) and they are next to each other
        a) from-node's snap-position is on
            1   EAST (MIDDLE)
        b) to-node's snap-position is on
            1   WEST (MIDDLE)
    #2  *to-node* is further right (east) from *from-node* and they are NOT next to each other ([from-node] --> .... --> [to_node])
        a) from-node's snap-position is on
            1   EAST (BOTTOM) for Activity
            2   EAST (MIDDLE) for Gateway/Event/Data
        b) to-node's snap-position is on
            1   WEST (BOTTOM) for Activity
            2   WEST (MIDDLE) for Gateway/Event/Data
    #3  *to-node* is further left (west) from *from-node* (that is behind, a back-flow) ([to-node] <-- [from_node])
        a) from-node's snap-position is on
            1   EAST-TOP for Activity
            2   EAST-MIDDLE for Gateway/Event/Data
        b) to-node's snap-position is on
            1   WEST-TOP for Activity
            2   NORTH-MIDDLE for Gateway/Event/Data (swicth label to bottom if necessary)
'''
class ChannelFlow(FlowObject):

    def __init__(self, edge_type, channel):
        super().__init__(edge_type)
        self.channel = channel


    '''
        implementation of rule 1 - *to-node* is further right (east) from *from-node* ([from-node] --> [to_node]) and they are next to each other
        going eastward from from-node [{0}] and approaching to-node [{1}] from left (west) in a straight path
    '''
    def eastward_west_to_east(self, from_node, to_node, label):
        # rule 1.a - from-node's snap-position is on EAST (MIDDLE)
        from_node_points_in_channel = self.channel.to_snap_point(node=from_node, side='east', position='middle', role='from', direction_hint=None, peer=to_node, edge_type=self.edge_type)

        # rule 1.b - from-node's snap-position is on WEST (MIDDLE)
        to_node_points_in_channel = self.channel.to_snap_point(node=to_node, side='west', position='middle', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)


        # we have the points, now create and return the flow
        flow_points = from_node_points_in_channel + to_node_points_in_channel
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        implementation of rule 2 - *to-node* is further right (east) from *from-node* and they are NOT next to each other ([from-node] --> .... --> [to_node])
        going southward from from-node [{0}] and approaching to-node [{1}] from bottom (south)

        TODO: this can cross label for ['Event', 'Gateway', 'Data'], so a label position switching from top to bottom may be required
    '''
    def southward_west_to_east(self, from_node, to_node, label):
        # rule 2.a - from-node's snap-position is on
        if from_node.category in ['Activity']:
            # rule 2.a.1 - EAST-BOTTOM for Activity
            from_node_points_in_channel = self.channel.to_boundary(boundary='south', edgeover='inside', node=from_node, side='east', position='bottom', role='from', direction_hint=None, peer=to_node, edge_type=self.edge_type)
        elif from_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.a.2 - EAST-MIDDLE for Gateway/Event/Data
            from_node_points_in_channel = self.channel.to_boundary(boundary='south', edgeover='inside', node=from_node, side='east', position='middle', role='from', direction_hint=None, peer=to_node, edge_type=self.edge_type)

        if from_node_points_in_channel is None:
            warn('could not calculate snap points for from-node [{0}]'.format(from_node.id))
            return None

        # rule 2.b - to-node's snap-position is on
        if to_node.category in ['Activity']:
            # rule 2.b.1 - WEST-TOP for Activity
            to_node_points_in_channel = self.channel.to_boundary(boundary='south', edgeover='inside', node=to_node, side='west', position='bottom', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)
        elif to_node.category in ['Event', 'Gateway', 'Data']:
            # rule 2.b.2 - NORTH-MIDDLE for Gateway/Event/Data (swicth label to bottom if necessary)
            to_node_points_in_channel = self.channel.to_boundary(boundary='south', edgeover='inside', node=to_node, side='west', position='middle', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)

        if to_node_points_in_channel is None:
            warn('could not calculate snap points for to-node [{0}]'.format(to_node.id))
            return None


        # we now have two segments we connect the last point of *from-segment* to the first point of *to-segment* through a north-ward path
        flow_points = from_node_points_in_channel + to_node_points_in_channel

        # we have the points, now create and return the flow
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        implementation of rule 3 - *to-node* is further left (west) from *from-node* (that is behind, a back-flow) ([to-node] <-- [from_node])
        going north-ward from from-node [{0}] and approaching to-node [{1}] from top (north)

        TODO: this can cross label for ['Event', 'Gateway', 'Data'], so a label position switching from top to bottom may be required
    '''
    def westward_east_to_west(self, from_node, to_node, label):
        # rule 3.a - from-node's snap-position is on
        if from_node.category in ['Activity']:
            # rule 3.a.1 - EAST-TOP for Activity
            from_node_points_in_channel = self.channel.to_boundary(boundary='north', edgeover='inside', node=from_node, side='east', position='top', role='from', direction_hint=None, peer=to_node, edge_type=self.edge_type)
        elif from_node.category in ['Event', 'Gateway', 'Data']:
            # rule 3.a.2 - EAST-MIDDLE for Gateway/Event/Data
            from_node_points_in_channel = self.channel.to_boundary(boundary='north', edgeover='inside', node=from_node, side='east', position='middle', role='from', direction_hint=None, peer=to_node, edge_type=self.edge_type)

        if from_node_points_in_channel is None:
            warn('could not calculate snap points for from-node [{0}]'.format(from_node.id))
            return None

        # rule 3.b - to-node's snap-position is on
        if to_node.category in ['Activity']:
            # rule 3.b.1 - WEST-TOP for Activity
            to_node_points_in_channel = self.channel.to_boundary(boundary='north', edgeover='inside', node=to_node, side='west', position='top', role='to', direction_hint=None, peer=from_node, edge_type=self.edge_type)
        elif to_node.category in ['Event', 'Gateway', 'Data']:
            # rule 3.b.2 - NORTH-MIDDLE for Gateway/Event/Data (swicth label to bottom if necessary)
            to_node_points_in_channel = self.channel.to_boundary(boundary='north', edgeover='inside', node=to_node, side='north', position='middle', role='to', direction_hint='west', peer=from_node, edge_type=self.edge_type)

        if to_node_points_in_channel is None:
            warn('could not calculate snap points for to-node [{0}]'.format(to_node.id))
            return None


        # we now have two segments we connect the last point of *from-segment* to the first point of *to-segment* through a north-ward path
        flow_points = from_node_points_in_channel + to_node_points_in_channel

        # we have the points, now create and return the flow
        flow_svg, flow_width, flow_height = a_flow(flow_points, label, self.theme)

        return SvgElement(svg=flow_svg, width=flow_width, height=flow_height)


    '''
        the entry method that decides which rule to apply
    '''
    def create_flow(self, from_node, to_node, label):
        # decide which edge rule we should apply
        if from_node.element.xy.west_of(to_node.element.xy):
            if (self.channel.node_ordinal(to_node) - self.channel.node_ordinal(from_node)) == 1:
                # rule 1 - *to-node* is further right (east) from *from-node* ([from-node] --> [to_node]) and they are next to each other
                return self.eastward_west_to_east(from_node=from_node, to_node=to_node, label=label)
            else:
                # rule 2 - *to-node* is further right (east) from *from-node* ([from-node] --> [to_node]) and they are next to each other
                return self.southward_west_to_east(from_node=from_node, to_node=to_node, label=label)
        elif from_node.element.xy.east_of(to_node.element.xy):
            # rule 3 - *to-node* is further left (west) from *from-node* (that is behind, a back-flow) ([to-node] <-- [from_node])
            return self.westward_east_to_west(from_node=from_node, to_node=to_node, label=label)
        else:
            warn('from-node {0} and to-node {1} starts at same x position, they can not be connected inside a channel which is supposed to have all nodes on different x position on same y')
            return None
