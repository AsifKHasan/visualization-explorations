#!/usr/bin/env python3
'''
'''
from pprint import pprint
from copy import deepcopy

from util.geometry import Point
from util.logger import *

''' ----------------------------------------------------------------------------------------------------------------------------------
    EdgeRole object for node snap-points
'''
class EdgeRole:
    def __init__(self, role, peer, type):
        self.role = role
        self.peer = peer
        self.type = type


''' ----------------------------------------------------------------------------------------------------------------------------------
    snap point for a node
'''
class SnapPoint:
    def __init__(self, point):
        self.point = point
        self.edge_roles = []


''' ----------------------------------------------------------------------------------------------------------------------------------
    Edge Object
'''
class EdgeObject:
    def __init__(self, edge, type, element):
        self.edge = edge
        self.type = type
        self.element = element


''' ----------------------------------------------------------------------------------------------------------------------------------
    Node Object
'''
class NodeObject:
    def __init__(self, id, category, type, styles, element, instance):
        self.id = id
        self.category = category
        self.type = type
        self.styles = styles
        self.element = element
        self.instance = instance


''' ----------------------------------------------------------------------------------------------------------------------------------
    collection of nodes
'''
class ChannelObject:
    def __init__(self, name, number, is_root, parent_channel, nodes):
        self.name = name
        self.number = number
        self.is_root = is_root
        self.parent_channel = parent_channel
        self.nodes = nodes

        self.instance = None
        self.element = None


    '''
        the string representation of the Channel
    '''
    def __repr__(self):
        s = 'number: {0}, root: {1}, name: {2}, parent: [{3}], nodes: {4}'.format(self.number, self.is_root, self.name, self.parent_channel, [*self.nodes])
        return s


    '''
        height of the node which has the maximum height among all nodes in the channel
    '''
    def max_node_height(self):
        max_height = 0
        for _, node_object in self.nodes.items():
            max_height = max(node_object.element.height, max_height)

        return max_height

    '''
        given a node od, returns the x position of the node in the channel
    '''
    def x_of_node(self, node_id):
        if node_id in self.nodes:
            return self.nodes[node_id].element.xy.x

        # we could not locate the node in the named channel
        return 0


    '''
        given a node, returns the ordinal position of the node in the channel
    '''
    def node_ordinal(self, node):
        ordinal = 0
        for node_id in [*self.nodes]:
            if node_id == node.id:
                return ordinal
            else:
                ordinal = ordinal + 1

        return -1


    '''
        (path from the snap point to the exact point of the node) or (path to the snap point from the exact point of the node) in channel coordinates
    '''
    def to_snap_point(self, node, side, position, role, direction_hint, peer, edge_type):
        points_in_node_coordinate = node.instance.to_snap_point(side, position, role, direction_hint, peer, edge_type)
        points_in_channel_coordinate = [node.element.xy + p for p in points_in_node_coordinate]
        return points_in_channel_coordinate


    '''
        the path connects node to the boundary of the channel in channel coordinate.
        the path may cross inner node-boundary depending on the value of boundary (if not None), but does not cross the channel boundary
        boundary - [north|south|east|west]
    '''
    def inside_the_channel(self, boundary, node, side, position, role, direction_hint, peer, edge_type):
        forbidden_combinations = [('north', 'south'), ('south', 'north'), ('east', 'west'), ('west', 'east')]

        points_in_node_coordinate = node.instance.to_snap_point(side, position, role, direction_hint, peer, edge_type)
        points_in_channel_coordinate = [node.element.xy + p for p in points_in_node_coordinate]

        # if boundary is None, we return this
        if boundary is None:
            return points_in_channel_coordinate

        if (boundary, side) in forbidden_combinations:
            warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed'.format(side, node.id, edgeover, boundary))
            return points_in_channel_coordinate

        if role == 'to':
            point_to_extend = points_in_channel_coordinate[0]
        else:
            point_to_extend = points_in_channel_coordinate[-1]

        if boundary == 'south':
            the_point = Point(point_to_extend.x, self.element.height - self.theme['channel-outer-rect']['pad-spec']['bottom']/2)

        elif boundary == 'north':
            the_point = Point(point_to_extend.x, self.theme['channel-outer-rect']['pad-spec']['top']/2)

        elif boundary == 'east':
            # allow only for east-most node
            if self.node_ordinal(node) == len(self.nodes) - 1:
                the_point = Point(self.element.width - self.theme['channel-outer-rect']['pad-spec']['right']/2, point_to_extend.y)
            else:
                warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed as it is not the {3}-most node'.format(side, node.id, edgeover, boundary))
                return points_in_channel_coordinate

        elif boundary == 'west':
            # allow only for west-most node
            if self.node_ordinal(node) == 0:
                the_point = Point(self.theme['channel-outer-rect']['pad-spec']['left']/2, point_to_extend.y)
            else:
                warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed as it is not the {3}-most node'.format(side, node.id, edgeover, boundary))
                return points_in_channel_coordinate

        if role == 'to':
            return [the_point] + points_in_channel_coordinate
        else:
            return points_in_channel_coordinate + [the_point]


    '''
        the path connects node to the boundary point outside the channel in channel coordinate.
        the path is for getting outside of the channel from a node or getting into a node from outside the channel
        boundary - [north|south|east|west]
    '''
    def outside_the_channel(self, boundary, node, side, position, role, direction_hint, peer, edge_type, margin_spec):
        forbidden_combinations = [('north', 'south'), ('south', 'north'), ('east', 'west'), ('west', 'east')]

        points_in_node_coordinate = node.instance.to_snap_point(side, position, role, direction_hint, peer, edge_type)
        points_in_channel_coordinate = [node.element.xy + p for p in points_in_node_coordinate]

        # if boundary is None, we return this
        if boundary is None:
            return points_in_channel_coordinate

        if (boundary, side) in forbidden_combinations:
            warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed'.format(side, node.id, edgeover, boundary))
            return points_in_channel_coordinate

        if role == 'to':
            point_to_extend = points_in_channel_coordinate[0]
        else:
            point_to_extend = points_in_channel_coordinate[-1]

        if boundary == 'south':
            the_point = Point(point_to_extend.x, self.element.height + margin_spec['bottom'])

        elif boundary == 'north':
            the_point = Point(point_to_extend.x, -margin_spec['top'])

        elif boundary == 'east':
            # allow only for east-most node
            if self.node_ordinal(node) == len(self.nodes) - 1:
                the_point = Point(self.element.width + margin_spec['right'], point_to_extend.y)
            else:
                warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed as it is not the {3}-most node'.format(side, node.id, edgeover, boundary))
                return points_in_channel_coordinate

        elif boundary == 'west':
            # allow only for west-most node
            if self.node_ordinal(node) == 0:
                the_point = Point(-margin_spec['left'], point_to_extend.y)
            else:
                warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed as it is not the {3}-most node'.format(side, node.id, edgeover, boundary))
                return points_in_channel_coordinate

        if role == 'to':
            return [the_point] + points_in_channel_coordinate
        else:
            return points_in_channel_coordinate + [the_point]


    '''
        given a vertical line segment, finds out whether any portion of the channel falls on the line segment
    '''
    def is_vertically_between(self, x, top_y, bottom_y, padding):
        result = False

        # we make sure we consider that the channel area includes edge routing area outside the outer-rect of the channel
        # west-most point of channel is
        channel_west_x = self.westmost_x() - 0
        channel_east_x = self.element.xy.x + self.element.width + 0

        if channel_west_x < x < channel_east_x:
            # the vertical line between Point(x, top_y) and Point(x, bottom_y) will fall inside the channel, unless it is vertically not between  Point(x, top_y) and Point(x, bottom_y)
            channel_north_y = self.element.xy.y - 0
            channel_south_y = self.element.xy.y + self.element.height + 0
            if (top_y < channel_north_y < bottom_y) or (top_y < channel_south_y < bottom_y):
                # channel falls in the path, testing with both north_y or south_y is required to eliminate the channels in between partially
                # debug('channel [{0}:{1}] N=[{2}] S=[{3}] W=[{4}] E=[{5}] is vertically between x: {6} and y: [{6} {8}]'.format(self.number, self.name, channel_north_y, channel_south_y, channel_west_x, channel_east_x, x, top_y, bottom_y))
                result = True

        return result


    '''
        given a horizontal line segment, finds out whether any portion of the channel falls on the line segment
    '''
    def is_horizontally_between(self, y, left_x, right_x, padding):
        result = False

        # we make sure we consider that the channel area includes edge routing area outside the outer-rect of the channel
        channel_west_x = self.westmost_x() - 0
        channel_east_x = self.element.xy.x + self.element.width + 0
        if (left_x < channel_east_x < right_x) or (left_x < channel_east_x < right_x):
            # the channel is horizontally between the left_x and right_x, now we need to make sure the point y is within the channel
            channel_north_y = self.element.xy.y - 0
            channel_south_y = self.element.xy.y + self.element.height + 0
            if channel_north_y < y < channel_south_y:
                # debug('channel [{0}:{1}] N=[{2}] S=[{3}] W=[{4}] E=[{5}] is horizontally between y: {6} and x: [{7} {8}]'.format(self.number, self.name, channel_north_y, channel_south_y, channel_west_x, channel_east_x, y, left_x, right_x))
                result = True

        return result

    '''
        a channel's westmost x position may not always be the xy.x of the channel - when the westmost node has a move_x displacement, the westmost point will also be displaced
        returns position in pool coordinate
    '''
    def westmost_x(self):
        # get the first node
        first_node = self.nodes[[*self.nodes][0]]
        return self.element.xy.x + first_node.element.xy.x - self.theme['channel-outer-rect']['pad-spec']['left']

    def east_of(self, channel):
        if self.element.xy.x + self.element.width >= channel.element.xy.x + channel.element.width:
            return True
        else:
            return False


    def west_of(self, channel):
        if self.element.xy.x <= channel.element.xy.x:
            return True
        else:
            return False


    def north_of(self, channel):
        if self.element.xy.y <= channel.element.xy.y:
            return True
        else:
            return False


    def south_of(self, channel):
        if self.element.xy.y + self.element.height >= channel.element.xy.y + channel.element.height:
            return True
        else:
            return False


''' ----------------------------------------------------------------------------------------------------------------------------------
    collection of edges and channel Lists
'''
class ChannelCollectionObject:

    def __init__(self, pool_id, theme):
        self.pool_id = pool_id
        self.theme = theme


    '''
        the points must be on same vertical line
    '''
    def channels_between(self, point_from, point_to):
        channels_vertically_between = []
        channels_horizontally_between = []
        for channel_list in self.channel_lists:
            for channel in channel_list:
                top_y, bottom_y = min(point_from.y, point_to.y), max(point_from.y, point_to.y)
                left_x, right_x = min(point_from.x, point_to.x), max(point_from.x, point_to.x)
                if channel.is_vertically_between(point_from.x, top_y, bottom_y, padding=self.theme['dx-between-channels']):
                    channels_vertically_between.append(channel)

                if channel.is_horizontally_between(point_to.y, left_x, right_x, padding=self.theme['dx-between-channels']):
                    channels_horizontally_between.append(channel)

        return channels_vertically_between, channels_horizontally_between


    '''
        connects two points in a pool only through straight lines. The points are asumed to be outside a Channel's outer rectangle inside the routing area between channels
        1. We start by trying to go straight to the same y position of *point_to* (let us call it *target_point*) so that we can draw a straight horizontal line from there to *point_to*
        2. but going straight to the *target_point* from *point_from* may not be possible as there may be a whole channel in between
        3. so, if there is a channel in between, we bypass the channel (by moving either to left or right) to the routing area east or west of the channel in the middle and now try to reach the *target_point* in a recursive manner
    '''
    def connecting_points(self, point_from, point_to):
        # see if there is any channel (vertically or horizontally) between point_from and point_to
        channels_vertically_between, channels_horizontally_between = self.channels_between(point_from, point_to)

        # first we bypass the channels which are obstructing the path vertically
        if len(channels_vertically_between) > 0:
            # debug('...vertically blocking channels')
            # for channel in channels_vertically_between:
            #     debug('......[{0}]:[{1}]'.format(channel.number, channel.name))

            # there may be a number of such obstructing channels, our target is to, find the channel closest to point_to
            northmost_channel = channels_vertically_between[0]
            southmost_channel = channels_vertically_between[0]
            for channel in channels_vertically_between:
                if channel.north_of(northmost_channel):
                    northmost_channel = channel

                if channel.south_of(southmost_channel):
                    southmost_channel = channel

            # if we are going towards south, the northhmost channel is the channel nearest to point_from
            if point_from.north_of(point_to):
                channel_to_bypass = northmost_channel
            else:
                channel_to_bypass = southmost_channel

            # if to_point_to is east to point_from, this channel should be bypassed through east side , so we target a new point_to at its eastearn outside boundary
            margin_spec = self.margin_spec(channel_to_bypass)
            if point_to.east_of(point_from):
                new_target_point = Point(channel_to_bypass.element.xy.x + channel_to_bypass.element.width + margin_spec['right'] , point_from.y)
                # debug('southward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))
            else:
                new_target_point = Point(channel_to_bypass.element.xy.x - margin_spec['left'] , point_from.y)
                # debug('northward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))

            return [point_from] + self.connecting_points(new_target_point, point_to)

        # next we handle the channels which are obstructing the path horizontally only when we have no vertical obstruction
        elif len(channels_horizontally_between) > 0:
            # debug('...horizontally blocking channels')
            # for channel in channels_horizontally_between:
            #     debug('......[{0}]:[{1}]'.format(channel.number, channel.name))

            # there may be a number of such obstructing channels, our target is to, find the channel closest to point_to
            eastmost_channel = channels_horizontally_between[0]
            westmost_channel = channels_horizontally_between[0]
            for channel in channels_horizontally_between:
                if channel.east_of(eastmost_channel):
                    eastmost_channel = channel

                if channel.west_of(westmost_channel):
                    westmost_channel = channel

            # if we are going towards west, the westmost channel is the channel nearest to point_to
            if point_from.east_of(point_to):
                channel_to_bypass = westmost_channel
            else:
                channel_to_bypass = eastmost_channel

            # if to_point_to is south to point_from, this channel should be approached from north, so we target a new point_to at its north outside boundary
            margin_spec = self.margin_spec(channel_to_bypass)
            if point_from.north_of(point_to):
                new_target_point = Point(point_to.x, channel_to_bypass.element.xy.y - margin_spec['top'])
                # debug('southward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))
            else:
                new_target_point = Point(point_to.x, channel_to_bypass.element.xy.y + channel_to_bypass.element.height + margin_spec['bottom'])
                # debug('northward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))

            return self.connecting_points(point_from, new_target_point) + [point_to]

        else:
            # there is no channel in between, we can just return the intersection point
            return [point_from, Point(point_from.x, point_to.y), point_to]


    '''
        the path connects node to the boundary point outside the channel in channel-collection (pool) coordinate.
        the path is for getting outside of the channel from a node or getting into a node from outside the channel
        boundary - [north|south|east|west]
    '''
    def outside_the_channel(self, boundary, channel, node, side, position, role, direction_hint, peer, edge_type):
        # we need to calculate the margin_spec for this channel
        points_in_channel_coordinate = channel.outside_the_channel(boundary, node, side, position, role, direction_hint, peer, edge_type, margin_spec=self.margin_spec(channel))
        points_in_pool_coordinate = [channel.element.xy + p for p in points_in_channel_coordinate]
        return points_in_pool_coordinate

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
        given a node returns its channel number and the node's ordinal position in the channel
    '''
    def channel_number_and_ordinal(self, node):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                ordinal = channel.node_ordinal(node)
                if ordinal != -1:
                    return channel.number, ordinal

        return -1, -1


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
