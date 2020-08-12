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
    def __init__(self, id, category, type, element, instance):
        self.id = id
        self.category = category
        self.type = type
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
        height of the node with the maximum height in the channel
    '''
    def max_node_height(self):
        max_height = 0
        for _, node_object in self.nodes.items():
            max_height = max(node_object.element.height, max_height)

        return max_height

    '''
        x position of the node in the channel
    '''
    def x_of_node(self, node_id):
        if node_id in self.nodes:
            return self.nodes[node_id].element.xy.x

        # we could not locate the node in the named channel
        return 0


    '''
        the ordinal position of the node in the channel
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
        path from snap point to the exact point of the node in channel coordinates
    '''
    def to_snap_point(self, node, side, position, role, direction_hint, peer, edge_type):
        points_in_node_coordinate = node.instance.to_snap_point(side, position, role, direction_hint, peer, edge_type)
        points_in_channel_coordinate = [node.element.xy + p for p in points_in_node_coordinate]
        return points_in_channel_coordinate


    '''
        the path connects node to southern boundary of the channel in channel coordinate
        the path does not touch boundary but stops inside the channel's edge routing area
        do not allow a path from north of a node
        boundary - [north|south|east|west]
        edgeover - [inside|outside]
    '''
    def to_boundary(self, boundary, edgeover, node, side, position, role, direction_hint, peer, edge_type):
        forbidden_combinations = [('north', 'south'), ('south', 'north'), ('east', 'west'), ('west', 'east')]
        edgeover_dict = {'inside': 1, 'outside': -1}

        points_in_node_coordinate = node.instance.to_snap_point(side, position, role, direction_hint, peer, edge_type)
        points_in_channel_coordinate = [node.element.xy + p for p in points_in_node_coordinate]
        if (boundary, side) in forbidden_combinations:
            warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed'.format(side, node.id, edgeover, boundary))
            return points_in_channel_coordinate

        # debug('[{0}:{1}:{2}] -> [{3}] {4} {5}'.format(node.id, side, position, boundary, role, points_in_node_coordinate))
        if role == 'to':
            point_to_extend = points_in_channel_coordinate[0]
        else:
            point_to_extend = points_in_channel_coordinate[-1]

        if boundary == 'south':
            the_point = Point(point_to_extend.x, self.element.height - self.theme['channel-outer-rect']['pad-spec']['bottom']/2 * edgeover_dict[edgeover])
            # debug('[{0}] {1}-{2} to {3}: {4}'.format(node.id, side, position, boundary, the_point))

        elif boundary == 'north':
            the_point = Point(point_to_extend.x, self.theme['channel-outer-rect']['pad-spec']['bottom']/2 * edgeover_dict[edgeover])
            # debug('[{0}] {1}-{2} to {3}: {4}'.format(node.id, side, position, boundary, the_point))

        elif boundary == 'east':
            # allow only for east-most node
            if self.node_ordinal(node) == len(self.nodes) - 1:
                the_point = Point(self.element.width - self.theme['channel-outer-rect']['pad-spec']['right']/2 * edgeover_dict[edgeover], point_to_extend.y)
                # debug('[{0}] {1}-{2} to {3}: {4}'.format(node.id, side, position, boundary, the_point))
            else:
                warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed as it is not the {3}-most node'.format(side, node.id, edgeover, boundary))
                return points_in_channel_coordinate

        elif boundary == 'west':
            # allow only for west-most node
            if self.node_ordinal(node) == 0:
                the_point = Point(self.theme['channel-outer-rect']['pad-spec']['left']/2 * edgeover_dict[edgeover], point_to_extend.y)
                # debug('[{0}] {1}-{2} to {3}: {4}'.format(node.id, side, position, boundary, the_point))
            else:
                warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed as it is not the {3}-most node'.format(side, node.id, edgeover, boundary))
                return points_in_channel_coordinate

        if role == 'to':
            return [the_point] + points_in_channel_coordinate
        else:
            return points_in_channel_coordinate + [the_point]

    '''
        whether the channel is between the two points, the points must be on same vertical line
    '''
    def is_between(self, point_from, point_to, padding):
        # we make sure we consider that the channel area includes 1/2 of the edge routing area outside the outer-rect of the channel
        channel_north_west_x = self.element.xy.x - padding
        channel_north_east_x = self.element.xy.x + self.element.width + padding

        if point_from.x > channel_north_west_x and point_from.x < channel_north_east_x:
            # the vertical line between point_from and point_to will fall inside the channel, unless it is vertically not between point_from and point_to
            channel_north_y = self.element.xy.y - padding
            channel_south_y = self.element.xy.y + padding
            if channel_north_y > min(point_from.y, point_to.y) and channel_north_y < min(point_from.y, point_to.y):
                # channel falls in the path, testing with either north_y or south_y will do
                return True
            else:
                return False
        else:
            # the vertical line between point_from and point_to will fall outside the channel
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
    def channel_between(self, point_from, point_to):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                if channel.is_between(point_from, point_to, padding=self.theme['dx-between-channels']):
                    return channel

        return None

    '''
        connects two points in a pool only through straight lines. The points are asumed to be outside a Channel's outer rectangle inside the routing area between channels
        1. We start by trying to go straight to the same y position of *point_to* (let us call it *target_point*) so that we can draw a straight horizontal line from there to *point_to*
        2. but going straight to the *target_point* from *point_from* may not be possible as there may be a whole channel in between
        3. so, if there is a channel in between, we bypass the channel (by moving either to left or right) to the routing area east or west of the channel in the middle and now try to reach the *target_point* in a recursive manner
    '''
    def connecting_points(self, point_from, point_to):
        target_point = Point(point_from.x, point_to.y)
        # see if there is any channel between point_from and target_point
        channel_between = self.channel_between(point_from, point_to)
        if channel_between is None:
            # there is no channel in between, we can just return the target_point
            return [target_point]
        else:
            # there is a channel in between, we have to bypass the channel and set a new target point
            if point_from.north_of(point_to):
                # we are going southward
                if point_from.west_of(point_to):
                    # we need to go eastward to bypass the channel
                    # to north-east
                    new_point1 = Point(channel_between.element.xy.x + channel_between.element.width + self.theme['dx-between-channels']/2, point_from.y)
                    # to south-east
                    new_point2 = Point(new_point1.x, new_point1.y + channel_between.element.height + self.theme['dy-between-channels'])
                    new_target_point = (new_point2.x, target_point.y)
                    return [new_point1, new_point2] + self.connecting_points(new_point2, new_target_point)
                else:
                    # we need to go westward to bypass the channel
                    # to north-west
                    new_point1 = Point(channel_between.element.xy.x - self.theme['dx-between-channels']/2, point_from.y)
                    # to south-west
                    new_point2 = Point(new_point1.x, new_point1.y + channel_between.element.height + self.theme['dy-between-channels'])
                    new_target_point = (new_point2.x, target_point.y)
                    return [new_point1, new_point2] + self.connecting_points(new_point2, new_target_point)

            else:
                # we are going northhward
                if point_from.west_of(point_to):
                    # we need to go eastward to bypass the channel
                    # to south-east
                    new_point1 = Point(channel_between.element.xy.x + channel_between.element.width + self.theme['dx-between-channels']/2, point_from.y)
                    # to north-east
                    new_point2 = Point(new_point1.x, channel_between.element.xy.y - self.theme['dy-between-channels']/2)
                    new_target_point = (new_point2.x, target_point.y)
                    return [new_point1, new_point2] + self.connecting_points(new_point2, new_target_point)
                else:
                    # we need to go westward to bypass the channel
                    # to south-west
                    new_point1 = Point(channel_between.element.xy.x - self.theme['dx-between-channels']/2, point_from.y)
                    # to north-west
                    new_point2 = Point(new_point1.x, channel_between.element.xy.y - self.theme['dy-between-channels']/2)
                    new_target_point = (new_point2.x, target_point.y)

        return []


    def path_to_snap_point(self, channel, node, side, position, role, direction_hint, peer, edge_type):
        points_in_channel_coordinate = channel.path_to_snap_point(node, side, position, role, direction_hint, peer, edge_type)
        points_in_pool_coordinate = [channel.element.xy + p for p in points_in_channel_coordinate]
        return points_in_pool_coordinate


    def to_boundary(self, boundary, edgeover, channel, node, side, position, role, direction_hint, peer, edge_type):
        points_in_channel_coordinate = channel.to_boundary(boundary, edgeover, node, side, position, role, direction_hint, peer, edge_type)
        points_in_pool_coordinate = [channel.element.xy + p for p in points_in_channel_coordinate]
        return points_in_pool_coordinate


    def node_xy(self, node):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                if node.id in [*channel.nodes]:
                    return channel.element.xy + node.element.xy

        return None


    def channel_of_node(self, node):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                if node.id in [*channel.nodes]:
                    return channel

        return None


    def channel_number_and_ordinal(self, node):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                ordinal = channel.node_ordinal(node)
                if ordinal != -1:
                    return channel.number, ordinal

        return -1, -1


    def channel_number_and_node(self, node_id):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                if node_id in [*channel.nodes]:
                    return channel.number, channel.nodes[node_id]

        return -1, None


    def channel_by_name(self, channel_name):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                if channel_name == channel.name:
                    return channel

        return None


    def get_if_from_different_channels(self, from_node_id, to_node_id):
        from_channel_number, from_node = self.channel_number_and_node(from_node_id)
        to_channel_number, to_node = self.channel_number_and_node(to_node_id)

        if from_channel_number != -1 and to_channel_number != -1 and from_channel_number != to_channel_number:
            if from_node is not None and to_node is not None:
                return from_node, to_node

        return None, None


    def find_channel_in_list_with_node(self, channel_list, node_id):
        if not channel_list:
            return None, None

        for channel in channel_list:
            if node_id in [*channel.nodes]:
                return channel.name, channel.nodes[node_id]

        return None, None


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
            # warn('finding [{0}] in [{1}]'.format(node_id, self.node_id))
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
