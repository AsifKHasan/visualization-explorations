#!/usr/bin/env python3
'''
'''
import importlib
from copy import deepcopy
from pprint import pprint

from util.geometry import Point

from util.logger import *
from util.svg_util import *

from elements.bpmn_element import BpmnElement, EDGE_TYPE
from elements.svg_element import SvgElement

from elements.swims.swim_channel import SwimChannel, ChannelObject

from elements.flows.flow_object import EdgeObject
from elements.flows.pool_flow import PoolFlow

'''
    a channel collection is a vertical stack of channels
'''
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

                # create an appropriate flow object, use PoolFlow which manages flows inside a SwimPool
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


''' ----------------------------------------------------------------------------------------------------------------------------------
    collection of channel Lists
'''
class ChannelCollectionObject:

    def __init__(self, pool_id, theme):
        self.pool_id = pool_id
        self.theme = theme


    '''
        the points must be on same vertical line
    '''
    def channels_blocking_southward(self, north_point, south_point):
        channels_vertically_between = []
        channels_horizontally_between = []
        for channel_list in self.channel_lists:
            for channel in channel_list:
                west_x, east_x = min(north_point.x, south_point.x), max(north_point.x, south_point.x)
                if channel.is_vertically_between(north_point.x, north_point.y, south_point.y, padding=self.theme['dx-between-channels']):
                    channels_vertically_between.append(channel)

                if channel.is_horizontally_between(south_point.y, west_x, east_x, padding=self.theme['dx-between-channels']):
                    channels_horizontally_between.append(channel)

        return channels_vertically_between, channels_horizontally_between


    '''
        connects two points in a pool only through straight lines.
        a. The points are asumed to be outside a Channel's outer rectangle inside the routing area between channels
        b. point_from must be above point_to

        1. We start by trying to go straight to the same y position of *point_to* (let us call it *target_point*) so that we can draw a straight horizontal line from there to *point_to*
        2. but going straight to the *target_point* from *point_from* may not be possible as there may be a whole channel in between
        3. so, if there is a channel in between, we bypass the channel (by moving either to left or right) to the routing area east or west of the channel in the middle and now try to reach the *target_point* in a recursive manner
    '''
    def connect_southward(self, point_from, point_to):
        if point_from == point_to:
            return [point_from]

        # see if there is any channel (vertically or horizontally) between point_from and point_to
        channels_vertically_between, channels_horizontally_between = self.channels_blocking_southward(point_from, point_to)

        # first we bypass the channels which are obstructing the path vertically
        if len(channels_vertically_between) > 0:
            # debug('...vertically blocking channels')
            # for channel in channels_vertically_between:
            #     debug('......[{0}]:[{1}]'.format(channel.number, channel.name))

            # we bypass the northmost (first) channel
            channel_to_bypass = channels_vertically_between[0]
            margin_spec = self.margin_spec(channel_to_bypass)
            points_to_bypass_the_channel = channel_to_bypass.bypass_vertically(coming_from=point_from, going_to=point_to, margin_spec=margin_spec)
            # warn('I {0} am going to south to {1} bypassing channel {2} [{3}]'.format(point_from, point_to, channel_to_bypass.name, points_to_bypass_the_channel))

            points = [point_from] + points_to_bypass_the_channel + self.connect_southward(points_to_bypass_the_channel[-1], point_to)
            # warn('I {0} am going to south to {1} through [{2}]'.format(point_from, point_to, points))
            return points

        # next we handle the channels which are obstructing the path horizontally only when we have no vertical obstruction
        elif len(channels_horizontally_between) > 0:
            # debug('...horizontally blocking channels')
            # for channel in channels_horizontally_between:
            #     debug('......[{0}]:[{1}]'.format(channel.number, channel.name))

            # there may be a number of such obstructing channels, our target is to, find the channel closest to point_to (the last channel)
            channel_to_bypass = channels_horizontally_between[-1]
            margin_spec = self.margin_spec(channel_to_bypass)
            # debug('bypassing [{0}]:[{1}] from {2} towards {3}'.format(channel_to_bypass.number, channel_to_bypass.name, point_to, point_from))
            points_to_bypass_the_channel = channel_to_bypass.bypass_vertically(coming_from=point_to, going_to=point_from, margin_spec=margin_spec)
            points_to_bypass_the_channel.reverse()
            points = self.connect_southward(point_from, points_to_bypass_the_channel[0]) + points_to_bypass_the_channel + [point_to]
            return points

        else:
            # there is no channel in between, we can just return the intersection point
            if point_from.x == point_to.x or point_from.y == point_to.y:
                return [point_from, point_to]
            else:
                return [point_from, Point(point_from.x, point_to.y), point_to]


    def outside_the_pool(self, pool_boundary, channel_boundary, channel, node, side, position, role, approach_snap_point_from, peer, edge_type, pool_margin_spec):
        # first get outside the channel
        points_in_pool_coordinate = self.outside_the_channel(channel_boundary, channel, node, side, position, role, approach_snap_point_from, peer, edge_type)
        # warn('[{0}] role [{1}] points to channel boundary: [{2}]'.format(node.id, role, optimize_points(points_in_pool_coordinate)))

        # debug('pool boundary is {0} and channel-boundary is {1} for [{2}]'.format(pool_boundary.upper(), channel_boundary.upper(), node.id))
        # now get outside the pool (channel_collection) - to do so we we either go south or north depending on pool_boundary
        if pool_boundary == 'south':
            # we have to get to the southern boundary of the pool
            if role == 'from':
                the_point = Point(points_in_pool_coordinate[-1].x, self.element.height + pool_margin_spec['bottom'])
                the_points = self.connect_southward(points_in_pool_coordinate[-1], the_point)
            else:
                the_point = Point(points_in_pool_coordinate[0].x, self.element.height + pool_margin_spec['bottom'])
                the_points = self.connect_southward(points_in_pool_coordinate[0], the_point)
                the_points.reverse()

        elif pool_boundary == 'north':
            # we have to get to the northern boundary of the pool
            if role == 'from':
                the_point = Point(points_in_pool_coordinate[-1].x, -pool_margin_spec['top'])
                the_points = self.connect_southward(the_point, points_in_pool_coordinate[-1])
                the_points.reverse()
            else:
                the_point = Point(points_in_pool_coordinate[0].x, -pool_margin_spec['top'])
                the_points = self.connect_southward(the_point, points_in_pool_coordinate[0])

        elif pool_boundary == 'west':
            # we have to get to the western boundary of the pool
            if role == 'from':
                the_point = Point(-pool_margin_spec['left'], points_in_pool_coordinate[-1].y)
                the_points = self.connect_southward(points_in_pool_coordinate[-1], the_point)
            else:
                the_point = Point(-pool_margin_spec['left'], points_in_pool_coordinate[0].y)
                the_points = self.connect_southward(points_in_pool_coordinate[0], the_point)

        elif pool_boundary == 'east':
            # we have to get to the eastern boundary of the pool
            if role == 'from':
                the_point = Point(self.element.width + pool_margin_spec['right'], points_in_pool_coordinate[-1].y)
                the_points = self.connect_southward(points_in_pool_coordinate[-1], the_point)
            else:
                the_point = Point(self.element.width + pool_margin_spec['right'], points_in_pool_coordinate[0].y)
                the_points = self.connect_southward(points_in_pool_coordinate[0], the_point)

        else:
            # should never happen
            warn('pool boundary is unknown')
            return points_in_pool_coordinate

        # debug('{0} outside point for pool [{1}] xy: {2} ({3} x {4}) is at {5}'.format(pool_boundary, self.pool_id, self.element.xy, self.element.width, self.element.height, the_point))

        if role == 'to':
            points = the_points + points_in_pool_coordinate
        else:
            points = points_in_pool_coordinate + the_points

        # warn('[{0}] role [{1}] points to pool   boundary: [{2}]'.format(node.id, role, optimize_points(points)))
        return points


    '''
        the path connects node to the boundary point outside the channel in channel-collection (pool) coordinate.
        the path is for getting outside of the channel from a node or getting into a node from outside the channel
        boundary is the side through which the path should get out of the channel or get into the channel [north|south|east|west]
        approach_snap_point_from is the direction from which the path should approach the snap-point specially when the snap-point can not be approached directly due to the presence of a label (for north and south snap-points for gateway, event and data)
    '''
    def outside_the_channel(self, boundary, channel, node, side, position, role, approach_snap_point_from, peer, edge_type):
        # we need to calculate the margin_spec for this channel
        points_in_channel_coordinate = channel.outside_the_channel(boundary, node, side, position, role, approach_snap_point_from, peer, edge_type, margin_spec=self.margin_spec(channel))
        points_in_pool_coordinate = [channel.element.xy + p for p in points_in_channel_coordinate]
        return points_in_pool_coordinate


    '''
        we want a path to bypass the pool through the routing area
    '''
    def bypass_vertically(self, coming_from, going_to, margin_spec):

        # the coming_from point is north of going_to, so we have to reach a point south of the pool either through east or west or directly dpending on which direction we are going_to
        if coming_from.north_of(going_to):
            # if the coming_from point is already below the pool, we have no point
            if coming_from.y >= self.element.xy.y + self.element.height + margin_spec['bottom']:
                return []

            # if the coming_from point's x position is outside the pool, we can directly go south
            elif (self.element.xy.x - margin_spec['left']) >= coming_from.x or coming_from.x >= (self.element.xy.x + self.element.width + margin_spec['right']):
                return [Point(coming_from.x, self.element.xy.y + self.element.height + margin_spec['bottom'])]

            # if the coming_from point is properly above the pool, we make a path
            else:
                # to the pool north vertically below coming_from
                p1 = Point(coming_from.x, self.element.xy.y - margin_spec['top'])
                if going_to.east_of(coming_from):
                    # to the pool north-east
                    p2 = Point(self.element.xy.x + self.element.width + margin_spec['right'], p1.y)
                    # debug('southward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))
                else:
                    # to the pool north-west
                    p2 = Point(self.element.xy.x - margin_spec['left'] , p1.y)
                    # debug('northward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))

                # to the pool south vertically below p2
                p3 = Point(p2.x, self.element.xy.y + self.element.height + margin_spec['bottom'])

        # the coming_from point is south of pool, so we have to reach a point north of the pool either through east or west dpending on which direction we are going_to
        else:
            # if the coming_from point is already above the pool, we have no point
            if coming_from.y <= self.element.xy.y - margin_spec['top']:
                return []

            # if the coming_from point's x position is outside the pool, we can directly go north
            elif (self.element.xy.x - margin_spec['left']) >= coming_from.x or coming_from.x >= (self.element.xy.x + self.element.width + margin_spec['right']):
                return [Point(coming_from.x, self.element.xy.y - margin_spec['top'])]

            # if the coming_from point is properly below the pool, we make a path
            else:
                # to the pool south vertically above coming_from
                p1 = Point(coming_from.x, self.element.xy.y + self.element.height + margin_spec['bottom'])
                if going_to.east_of(coming_from):
                    # to the pool south-east
                    p2 = Point(self.element.xy.x + self.element.width + margin_spec['right'], p1.y)
                    # debug('southward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))
                else:
                    # to the pool south-west
                    p2 = Point(self.element.xy.x - margin_spec['left'] , p1.y)
                    # debug('northward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))

                # to the pool north vertically above p2
                p3 = Point(p2.x, self.element.xy.y - margin_spec['top'])

        return [p1, p2, p3]


    '''
        a chennel's margin spec is the margin outside the channel outer boundary through which the inter-channel edges are routed
        1. if it is a top-most channel within the channel-collection (pool) then we assume that 1/2 of pool's top pad-spec is the top margin, else it is 1/2 of dy-between-channels
        2. if it is a bottom-most channel within the channel-collection (pool) then we assume that 1/2 of pool's bottom pad-spec is the top margin, else it is 1/2 of dy-between-channels
        3. if it is a left-most channel within the channel-collection (pool) then we assume that 1/2 of pool's left pad-spec is the left margin, else it is 1/2 of dx-between-channels
        4. if it is a right-most channel within the channel-collection (pool) then we assume that 1/2 of pool's right pad-spec is the right margin, else it is 1/2 of dx-between-channels
    '''
    def margin_spec(self, channel):
        margin_spec = {'left': 12, 'top': 12, 'right': 12, 'bottom': 12}

        # is it the top-most channel?
        if channel.element.xy.y == self.theme['pad-spec']['top']:
            margin_spec['top'] = self.theme['pad-spec']['top']/2
        else:
            margin_spec['top'] = self.theme['dy-between-channels']/2

        # is it the bottom-most channel?
        if (self.element.height) - (channel.element.xy.y + channel.element.height) == self.theme['pad-spec']['bottom']:
            margin_spec['bottom'] = self.theme['pad-spec']['bottom']/2
        else:
            margin_spec['bottom'] = self.theme['dy-between-channels']/2

        # is it the left-most channel?
        if channel.element.xy.x == self.theme['pad-spec']['left']:
            margin_spec['left'] = self.theme['pad-spec']['left']/2
        else:
            margin_spec['left'] = self.theme['dx-between-channels']/2

        # is it the right-most channel?
        if (self.element.width) - (channel.element.xy.x + channel.element.width) == self.theme['pad-spec']['right']:
            margin_spec['right'] = self.theme['pad-spec']['right']/2
        else:
            margin_spec['right'] = self.theme['dx-between-channels']/2

        return margin_spec


    '''
        a given node's xy Point in pool coordinate
    '''
    def node_xy(self, node):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                if node.id in [*channel.nodes]:
                    return channel.element.xy + node.element.xy

        return None


    '''
        given a nodes returns its channel
    '''
    def channel_of_node(self, node):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                if node.id in [*channel.nodes]:
                    return channel

        return None


    '''
        given a node returns its channel and the node's ordinal position in the channel
    '''
    def channel_and_ordinal(self, node):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                node_ordinal = channel.node_ordinal(node)
                if node_ordinal != -1:
                    return channel, node_ordinal

        return None, -1


    '''
        given a node's id returns its channel number and the node
    '''
    def channel_number_and_node(self, node_id):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                if node_id in [*channel.nodes]:
                    return channel.number, channel.nodes[node_id]

        return -1, None


    '''
        given a channel's name returns the channel
    '''
    def channel_by_name(self, channel_name):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                if channel_name == channel.name:
                    return channel

        return None


    '''
        given to node id's, return the corresponding nodes only if the nodes are in different channels
    '''
    def get_if_from_different_channels(self, from_node_id, to_node_id):
        from_channel_number, from_node = self.channel_number_and_node(from_node_id)
        to_channel_number, to_node = self.channel_number_and_node(to_node_id)

        if from_channel_number != -1 and to_channel_number != -1 and from_channel_number != to_channel_number:
            if from_node is not None and to_node is not None:
                return from_node, to_node

        return None, None


    '''
        given a channel-list and node_id, returns the channel name and and the node if the node is in any channel within the channel-list
    '''
    def find_channel_in_list_with_node(self, channel_list, node_id):
        if not channel_list:
            return None, None

        for channel in channel_list:
            if node_id in [*channel.nodes]:
                return channel.name, channel.nodes[node_id]

        return None, None


    '''
        the str representation of a ChannelCollectionObject
    '''
    def __repr__(self):
        for channel_list in self.channel_lists:
            s = '\r\n----------------------------------'
            for channel in channel_list:
                s = '{0}\r\n  {1}'.format(s, channel)

        return s


    '''
        in a pool, nodes need to be processed (ordered and grouped)
        1. nodes that are connected with other nodes (in the same pool) should be ordered in a group so that they are in the same channel (a channel is vertical lines for node flow, a lane may have multiple channels if the edges are branched like a tree) and flow from left to right based or edge order (from node at left, to node at right)
        2. isolated nodes (nodes that do not connect to any other nodes) should be put in a separate group (in which channel they should go is a TODO)
        3. If any node connects to two or more nodes (in the same pool) a new group starts for each branch so that they can be placed into different channels
    '''
    def build(self, pool_nodes, pool_edges):
        # iterate the edges and discard edges where either from or to node is not inside the pool, in the same go remove duplicates also
        filtered_pool_edges = []
        edge_keys = []
        for edge in pool_edges:
            if edge['from'] in pool_nodes and edge['to'] in pool_nodes:
                edge_key = '{0}__#__{1}'.format(edge['from'], edge['to'])
                if edge_key not in edge_keys:
                    filtered_pool_edges.append(edge)
                    edge_keys.append(edge_key)

        # now we group and order the nodes in a root Channel to be returned
        root_channel = ChannelCollectionObject.Channel()
        for node_id, node_data in pool_nodes.items():
            # get the parent and child nodes of this node
            children = []
            parents = []
            for edge in filtered_pool_edges:
                if node_id == edge['from']:
                    children.append(edge['to'])

                if node_id == edge['to']:
                    parents.append(edge['from'])

            root_channel.add(node_id, node_data, parents, children, )

        root_channel.group_and_order()

        # pprint(root_channel.as_list())

        channels_as_list = root_channel.as_list()

        self.channel_lists = []
        self.edges = []

        # build the inner data structure
        channel_list = None
        channel_number = 0
        for node_id_list in channels_as_list:
            if len(node_id_list) > 0:
                parent_channel_name, _ = self.find_channel_in_list_with_node(channel_list, node_id_list[0])
                if not parent_channel_name:
                    # if the first node of the list is not in any channel created so far, this is a root channel
                    # create a new channel and append the {first_node: node_id_list} object
                    if channel_list: self.channel_lists.append(channel_list)
                    channel_list = []
                    nodes = {node_id: {} for node_id in node_id_list}
                    channel = ChannelObject(name=node_id_list[0], number=channel_number, is_root=True, parent_channel=None, nodes=nodes)
                    channel_list.append(channel)
                    channel_number = channel_number + 1
                else:
                    # this must be a sub channel of a previous channel, append in the current channel (the first node becomes the name and will not be in the channel_nodes)
                    nodes = {node_id: {} for node_id in node_id_list[1:]}
                    channel = ChannelObject(name=node_id_list[0], number=channel_number, is_root=False, parent_channel=parent_channel_name, nodes=nodes)
                    channel_list.append(channel)
                    channel_number = channel_number + 1

        # append the last open channel
        if channel_list: self.channel_lists.append(channel_list)

        # we need a special channel for islands
        if len(root_channel.islands):
            channel_list = []
            nodes = {node_id: {} for node_id in root_channel.islands}
            channel = ChannelObject(name='-', number=channel_number, is_root=False, parent_channel=None, nodes=nodes)
            channel_list.append(channel)
            channel_number = channel_number + 1
            self.channel_lists.append(channel_list)


    '''
        # a channel is a node and another channel which is the next node and so on. Basically this represents node -> node -> .......
        # a channel may have more than one next nodes if it has two or more branches
    '''
    class Channel:

        def __init__(self, node_id=None, child=None):
            self.children = []
            self.islands = []
            self.orphans = {}

            self.node_id = node_id
            self.add_children(child)

        def __repr__(self):
            if self.node_id:
                s = '[{0}]'.format(self.node_id)
            else:
                s = ''

            for child in self.children:
                s = '{0}->{1}'.format(s, child).strip('->')
                s = '{0}\n'.format(s).replace('\n\n', '\n')

            return s

        def as_list(self):
            if len(self.children) == 0:
                if self.node_id:
                    return [[self.node_id]]
                else:
                    return [[]]

            the_list_of_list = []
            for child in self.children:
                append_parent_node = True
                for child_list in child.as_list():
                    if append_parent_node and self.node_id:
                        child_list = [self.node_id] + child_list
                        append_parent_node = False

                    the_list_of_list.append(child_list)

            return the_list_of_list

        def as_full_list(self):
            if len(self.children) == 0:
                if self.node_id:
                    return [[self.node_id]]
                else:
                    return [[]]

            the_list_of_list = []
            for child in self.children:
                for child_list in child.as_full_list():
                    if self.node_id:
                        child_list = [self.node_id] + child_list

                    the_list_of_list.append(child_list)

            return the_list_of_list

        def add_children(self, child):
            if child:
                self.children.append(child)

        def group_and_order(self):
            while True:
                if len(self.orphans) == 0:
                    return

                newdict = deepcopy(self.orphans)
                keys = newdict.keys()
                for key in keys:
                    debug('  parent [{0}] has orphans [{1}]'.format(key, newdict[key]))

                    parent = self.find(key)
                    # parent found, we just add this as children for the parent
                    if parent:
                        # parent.add_children(Channel(node_id, self.orphans.pop(node_id, None)))
                        parent.add_children(self.orphans.pop(key))
                        debug('  orphans [{0}] under [{1}] moved as child'.format(newdict[key], parent.node_id))

        def add_orphans(self, parent_node_id, child_node_id):
            # find inside all orpahn values whether the parent is already there
            # print('[{0}] marked as orphan of [{1}]'.format(child_node_id, parent_node_id))
            found = False
            for key, orphan in self.orphans.items():
                parent = orphan.find(parent_node_id)
                if parent:
                    found = True
                    parent.add_children(ChannelCollectionObject.Channel(child_node_id))
                    # debug('[{0}] added as a descendant orphan to [{1}] under key [{2}]'.format(child_node_id, parent_node_id, key))

            if not found:
                if child_node_id in self.orphans:
                    self.orphans[parent_node_id] = ChannelCollectionObject.Channel(child_node_id, self.orphans.pop(child_node_id))
                else:
                    self.orphans[parent_node_id] = ChannelCollectionObject.Channel(child_node_id)

                # debug('[{0}] added as a direct orphan under key [{1}]'.format(child_node_id, parent_node_id))

        def find(self, node_id):
            if self.node_id == node_id:
                return self

            # if there are children, look into them
            for child in self.children:
                found_child = child.find(node_id)
                if found_child:
                    return found_child
                else:
                    pass

            # it was not found
            return None

        def add(self, node_id, node_data, parents, children):
            # no parent, no children, it is an island
            # debug('[{0}]'.format(node_id))
            if len(parents) == 0 and len(children) == 0:
                # debug('  [{0}] is an island'.format(node_id))
                self.islands.append(node_id)
                return

            # marked as wrap_here, it is a new child
            if 'wrap_here' in node_data['styles']:
                self.add_children(ChannelCollectionObject.Channel(node_id, self.orphans.pop(node_id, None)))
                return

            # no parent, but one or more children, it is a new child
            if len(parents) == 0 and len(children) > 0:
                # its children may already be stored as an orphans
                # debug('[{0}] has no parent, it is a root node'.format(node_id))
                self.add_children(ChannelCollectionObject.Channel(node_id, self.orphans.pop(node_id, None)))
                # self.add_children(Channel(node_id))
                return

            # we have parent(s), we just find the parent and put it as children
            if len(parents) > 0:
                for parent_node_id in parents:
                    parent = self.find(parent_node_id)
                    # parent found, we just add this as children for the parent
                    if parent:
                        # debug('[{0}] is child to [{1}]'.format(node_id, parent.node_id))
                        parent.add_children(ChannelCollectionObject.Channel(node_id, self.orphans.pop(node_id, None)))
                        # parent.add_children(Channel(node_id))
                        return

            # if (any of) the parent(s) do(es) not exist (yet), it is an orphan or a child to another orphan
            # debug('[{0}] none of the parents {1} processed yet, adding as an orphan'.format(node_id, parents))
            for parent_node_id in parents:
                self.add_orphans(parent_node_id, node_id)

            return
