#!/usr/bin/env python3
'''
'''
import importlib
from pprint import pprint

from pysvg.builders import *
from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *

from util.geometry import Point

from util.logger import *
from util.svg_util import *
from util.helper_objects import ChannelCollectionObject, EdgeObject

from elements.bpmn_element import BpmnElement, EDGE_TYPE
from elements.svg_element import SvgElement

from elements.swims.swim_channel import SwimChannel
from elements.flows.pool_flow import PoolFlow

class ChannelCollection(BpmnElement):
    def __init__(self, bpmn_id, lane_id, pool_id, nodes, edges):
        self.bpmn_id, self.lane_id, self.pool_id, self.nodes, self.edges = bpmn_id, lane_id, pool_id, nodes, edges
        self.theme = self.current_theme['swims']['ChannelCollection']

    def lay_edges(self):
        # first lay the intra-channel edges
        for channel_list in self.channel_collection.channel_lists:
            for channel in channel_list:
                channel.instance.lay_edges()

        # lay inter-channel edges - get a filtered list of edges containing only those where from-node and to-node both are in this channel-collection but are in different channels
        for edge in self.edges:
            from_node, to_node = self.channel_collection.get_if_from_different_channels(edge['from'], edge['to'])
            if from_node is not None and to_node is not None:
                edge_type = EDGE_TYPE[edge['type']]
                edge_label = edge.get('label', None)

                # create an appropriate flow object, use ChannelFlow which manages flows inside a SwimChannel
                flow_object = PoolFlow(edge_type, self.channel_collection)
                flow_svg_element = flow_object.create_flow(from_node, to_node, edge_label)

                # add to channel svg group
                if flow_svg_element is not None and flow_svg_element.svg is not None:
                    self.channel_collection.element.svg.addElement(flow_svg_element.svg)

                    # store object for future reference
                    self.channel_collection.edges.append(EdgeObject(edge=edge, type=edge_type, element=flow_svg_element))

    def assemble_elements(self):
        # channels are vertically stacked
        # root channels start at x=0
        # channels that are branch of some parent channel start horizontally after the node to which the first node is the to-node
        # TODO: how to horizontally shift channels based on to-node's relationship with from-node from other lane/pool
        # TODO: how and where to place the island channel?

        # wrap it in a svg group
        group_id = '{0}:{1}:{2}'.format(self.bpmn_id, self.lane_id, self.pool_id)
        svg_group = G(id=group_id)


        # lay the channels, channels are vertically stacked, but only the root channels start at left, branches ar horizontally positioned so that they fall to the right of their parent node's position
        group_width = 0
        current_y = self.theme['pad-spec']['top']
        transformer = TransformBuilder()
        for channel_list in self.channel_collection.channel_lists:
            for channel in channel_list:
                # if it is a root channel it, starts at left (0) x position
                if channel.is_root == True:
                    current_x = self.theme['pad-spec']['left']
                else:
                    # we find the parent node from which this channel is branched and position accordingly
                    if channel.parent_channel is not None:
                        parent_channel_object = self.channel_collection.channel_by_name(channel.parent_channel)
                        x_pos = parent_channel_object.element.xy.x + parent_channel_object.x_of_node(node_id=channel.name) + self.theme['dx-between-elements']
                    else:
                        x_pos = 0

                    if x_pos != 0:
                        current_x = self.theme['pad-spec']['left'] + x_pos + self.theme['dx-between-elements']
                    else:
                        current_x = self.theme['pad-spec']['left']

                # TODO: the channel may be moved up to just below of a previous channel if there is no part of any in between channels in the middle

                channel_element = channel.element
                channel_element_svg = channel_element.svg
                channel_element.xy = Point(current_x, current_y)

                transformer.setTranslation(channel_element.xy)
                channel_element_svg.set_transform(transformer.getTransform())
                svg_group.addElement(channel_element_svg)

                group_width = max(group_width, channel_element.xy.x + channel_element.width + self.theme['pad-spec']['right'])
                current_y = current_y + channel_element.height + self.theme['dy-between-channels']

        group_height = current_y - self.theme['dy-between-channels'] + self.theme['pad-spec']['bottom']

        # add the ractangle
        channel_collection_rect_svg = Rect(width=group_width, height=group_height)
        channel_collection_rect_svg.set_style(StyleBuilder(self.theme['style']).getStyle())
        svg_group.addElement(channel_collection_rect_svg)

        # wrap it in a svg element
        self.svg_element = SvgElement(svg=svg_group, width=group_width, height=group_height)

        # store the svg and dimensions for future reference
        self.channel_collection.element = self.svg_element

        return self.svg_element

    def collect_elements(self):
        # order and group nodes
        self.channel_collection = ChannelCollectionObject(pool_id=self.pool_id, theme=self.theme)
        self.channel_collection.build(pool_nodes=self.nodes, pool_edges=self.edges)
        # pprint(self.channel_collection)

        # create the swim channels
        for channel_list in self.channel_collection.channel_lists:
            for channel in channel_list:
                channel.instance = SwimChannel(self.bpmn_id, self.lane_id, self.pool_id, self.nodes, self.edges, channel)
                channel.instance.to_svg()
