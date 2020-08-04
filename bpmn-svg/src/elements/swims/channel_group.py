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

from util.logger import *
from util.svg_util import *
from util.block_util import *

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

def is_in_channel(node_id, channel_list):
    if not channel_list:
        return None

    for channel in channel_list:
        if node_id in channel['channel-nodes']:
            return channel['channel-name']

    return None

class ChannelGroup(BpmnElement):
    def __init__(self, bpmn_id, lane_id, pool_id, nodes, edges):
        self.theme = self.current_theme['swims']['ChannelGroup']
        self.bpmn_id, self.lane_id, self.pool_id, self.nodes, self.edges = bpmn_id, lane_id, pool_id, nodes, edges

    def assemble_channel(self, channel_name, channel_nodes):
        # wrap it in a svg group
        svg_group = G()

        # get the max height and cumulative width of all elements and adjust height and width accordingly
        max_element_height = self.get_max_height(channel_nodes)

        # we have found the bpmn elements, now render them within the group
        # start with the height width hints
        group_height = max_element_height

        # now we have height and width adjusted, we place the elements with proper displacement
        transformer = TransformBuilder()
        current_x = 0
        for node_id, node_object in channel_nodes.items():
            element_svg = node_object['svg']
            current_y = group_height/2 - node_object['height']/2

            # keep the x, y position and dimension for the node within the group for future reference
            node_object['x'] = current_x
            node_object['y'] = current_y

            transformation_xy = '{0},{1}'.format(current_x, current_y)
            transformer.setTranslation(transformation_xy)
            # debug('........tranforming to {0}'.format(transformation_xy))
            element_svg.set_transform(transformer.getTransform())
            svg_group.addElement(element_svg)
            current_x = current_x + node_object['width'] + self.theme['dx-between-elements']

        group_width = current_x - self.theme['dx-between-elements']

        # the group rect
        channel_rect_svg = Rect(width=group_width, height=group_height)
        channel_rect_svg.set_style(StyleBuilder(self.theme['channel-style']).getStyle())
        svg_group.addElement(channel_rect_svg)

        # wrap it in a svg element
        group_spec = {'width': group_width, 'height': group_height}
        return SvgElement(group_spec, svg_group)

    def collect_elements(self):
        # order and group nodes
        root_channel = group_nodes_inside_a_pool(
                                            bpmn_id=self.bpmn_id,
                                            lane_id=self.lane_id,
                                            pool_id=self.pool_id,
                                            pool_nodes=self.nodes,
                                            pool_edges=self.edges)

        # pprint(root_channel)
        # pprint(root_channel.as_list())

        # change the data structure a little bit - make it an array of root channels, where root channels are array of objects ()
        self.channels = []
        channel = None
        for node_id_list in root_channel.as_list():
            if len(node_id_list) > 0:
                parent_channel_name = is_in_channel(node_id_list[0], channel)
                if not parent_channel_name:
                    # if the first node of the list is not in any channel created so far, this is a root channel
                    # create a new channel and append the {first_node: node_id_list} object
                    if channel: self.channels.append(channel)
                    channel = []
                    channel.append({'channel-name': node_id_list[0], 'root-channel': True, 'channel-nodes': {node_id: {} for node_id in node_id_list}})
                else:
                    # this must be a sub channel of a previous channel, append in the current channel (the first node becomes the name and will not be in the channel_nodes)
                    channel.append({'channel-name': node_id_list[0], 'root-channel': False, 'parent-channel': parent_channel_name, 'channel-nodes': {node_id: {} for node_id in node_id_list[1:]}})

        # append the last open channel
        if channel: self.channels.append(channel)

        # we need a special channel for islands
        if len(root_channel.islands):
            channel = []
            channel.append({'channel-name': '-', 'root-channel': False, 'parent-channel': None, 'channel-nodes': {node_id: {} for node_id in root_channel.islands}})
            self.channels.append(channel)

        # pprint(self.channels)

        # now we have the channels defined, get the svg elements
        for channel_list in self.channels:
            for channel in channel_list:
                for node_id in channel['channel-nodes']:
                    node_data = self.nodes[node_id]
                    # we know the node type
                    if node_data['type'] in CLASSES:
                        # get the svg element
                        element_class = getattr(importlib.import_module(CLASSES[node_data['type']]['m']), CLASSES[node_data['type']]['c'])
                        element_instance = element_class(self.bpmn_id, self.lane_id, self.pool_id, node_id, node_data)
                        svg_element = element_instance.to_svg()
                        channel['channel-nodes'][node_id]['type'] = node_data['type']
                        channel['channel-nodes'][node_id]['svg'] = svg_element.group
                        channel['channel-nodes'][node_id]['width'] = svg_element.specs['width']
                        channel['channel-nodes'][node_id]['height'] = svg_element.specs['height']
                    else:
                        warn('node type [{0}] is not supported. skipping ..'.format(node_data['type']))

        # pprint(self.channels)

    def get_max_height(self, channel_nodes):
        max_element_height = 0
        for node_id, node_object in channel_nodes.items():
            max_element_height = max(node_object['height'], max_element_height)

        return max_element_height

    def x_of_node_in_channel(self, channel_name, node_id):
        for channel_list in self.channels:
            for channel in channel_list:
                if channel['channel-name'] == channel_name:
                    # get the node
                    if node_id in channel['channel-nodes']:
                        # we actually return the x position after the node
                        return channel['channel-nodes'][node_id]['x'] + channel['channel-nodes'][node_id]['width']

        # we could not locate the node in the named channel
        return 0
