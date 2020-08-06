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
from util.channel_util import *

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

from elements.swims.swim_channel import SwimChannel

class ChannelCollection(BpmnElement):
    def __init__(self, bpmn_id, lane_id, pool_id, nodes, edges):
        self.theme = self.current_theme['swims']['ChannelCollection']
        self.bpmn_id, self.lane_id, self.pool_id, self.nodes, self.edges = bpmn_id, lane_id, pool_id, nodes, edges

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
        for channel_list in self.channel_collection:
            for channel in channel_list:
                # if it is a root channel it, starts at left (0) x position
                if channel['root-channel'] == True:
                    current_x = self.theme['pad-spec']['left']
                else:
                    # we find the parent node from which this channel is branched and position accordingly
                    if 'parent-channel' in channel and channel['parent-channel'] is not None:
                        parent_swim_channel = self.get_swim_channel_instance_by_name(channel['parent-channel'])
                        x_pos = parent_swim_channel.x_of_node(node_id=channel['channel-name'])
                    else:
                        x_pos = 0

                    if x_pos != 0:
                        current_x = self.theme['pad-spec']['left'] + x_pos + self.theme['dx-between-elements']
                    else:
                        current_x = self.theme['pad-spec']['left']

                channel_element = channel['channel-element']
                channel_element_svg = channel_element['svg']
                channel_element['x'] = current_x
                channel_element['y'] = current_y

                channel_xy = '{0},{1}'.format(current_x, current_y)
                transformer.setTranslation(channel_xy)
                channel_element_svg.set_transform(transformer.getTransform())
                svg_group.addElement(channel_element_svg)

                group_width = max(group_width, channel_element['x'] + channel_element['width'] + self.theme['pad-spec']['right'])
                current_y = current_y + channel_element['height'] + self.theme['dy-between-channels']

        group_height = current_y - self.theme['dy-between-channels'] + self.theme['pad-spec']['bottom']

        # add the ractangle
        channel_collection_rect_svg = Rect(width=group_width, height=group_height)
        channel_collection_rect_svg.set_style(StyleBuilder(self.theme['style']).getStyle())
        svg_group.addElement(channel_collection_rect_svg)

        # wrap it in a svg element
        return SvgElement(svg=svg_group, width=group_width, height=group_height)

    def collect_elements(self):
        # order and group nodes
        root_channel = group_nodes_inside_a_pool(
                                            bpmn_id=self.bpmn_id,
                                            lane_id=self.lane_id,
                                            pool_id=self.pool_id,
                                            pool_nodes=self.nodes,
                                            pool_edges=self.edges)

        # change the data structure a little bit - make it an array of root channels, where root channels are array of objects ()
        self.channel_collection = []
        channel_list = None
        for node_id_list in root_channel.as_list():
            if len(node_id_list) > 0:
                parent_channel_name = self.find_channel_in_list_with_node(node_id_list[0], channel_list)
                if not parent_channel_name:
                    # if the first node of the list is not in any channel created so far, this is a root channel
                    # create a new channel and append the {first_node: node_id_list} object
                    if channel_list: self.channel_collection.append(channel_list)
                    channel_list = []
                    channel_list.append({'channel-name': node_id_list[0], 'root-channel': True, 'channel-nodes': {node_id: {} for node_id in node_id_list}})
                else:
                    # this must be a sub channel of a previous channel, append in the current channel (the first node becomes the name and will not be in the channel_nodes)
                    channel_list.append({'channel-name': node_id_list[0], 'root-channel': False, 'parent-channel': parent_channel_name, 'channel-nodes': {node_id: {} for node_id in node_id_list[1:]}})

        # append the last open channel
        if channel_list: self.channel_collection.append(channel_list)

        # we need a special channel for islands
        if len(root_channel.islands):
            channel_list = []
            channel_list.append({'channel-name': '-', 'root-channel': False, 'parent-channel': None, 'channel-nodes': {node_id: {} for node_id in root_channel.islands}})
            self.channel_collection.append(channel_list)

        # create the swim channels
        for channel_list in self.channel_collection:
            for channel in channel_list:
                swim_channel = SwimChannel(self.bpmn_id, self.lane_id, self.pool_id, self.nodes, self.edges, channel)
                swim_channel.to_svg()
                channel['instance'] = swim_channel

    def to_svg(self):
        # We go through a collect -> tune -> assemble flow

        # collect the svg elements, but do not assemble now. we need tuning before assembly
        self.collect_elements()

        # finally assemble the svg elements into a final one
        final_svg_element = self.assemble_elements()
        return final_svg_element

    def get_swim_channel_instance_by_name(self, channel_name):
        for channel_list in self.channel_collection:
            for channel in channel_list:
                if channel_name == channel['channel-name']:
                    return channel['instance']

        return None

    def find_channel_in_list_with_node(self, node_id, channel_list):
        if not channel_list:
            return None

        for channel in channel_list:
            if node_id in channel['channel-nodes']:
                return channel['channel-name']

        return None
