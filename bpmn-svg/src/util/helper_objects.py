#!/usr/bin/env python3
'''
'''
from pprint import pprint
from copy import deepcopy

from util.logger import *

# ---------------------------------------------------------------------------------------------------------
# object classes
# ---------------------------------------------------------------------------------------------------------
'''
    EdgeRole object for node snap-points
'''
class EdgeRole:
    def __init__(self, role, peer, type):
        self.role = role
        self.peer = peer
        self.type = type


'''
    snap point for a node
'''
class SnapPoint:
    def __init__(self, point):
        self.point = point
        self.edge_roles = []


'''
    Edge Object
'''
class EdgeObject:
    def __init__(self, edge, type, element):
        self.edge = edge
        self.type = type
        self.element = element


'''
    Node Object
'''
class NodeObject:
    def __init__(self, id, category, type, element, instance):
        self.id = id
        self.category = category
        self.type = type
        self.element = element
        self.instance = instance


'''
    collection of nodes
'''
class ChannelObject:
    def __init__(self, name, number, is_root, parent_channel, nodes):
        self.name = name
        self.number = number
        self.is_root = False
        self.parent_channel = parent_channel
        self.nodes = nodes

        self.intance = None
        self.element = None

    def node_ordinal(self, node):
        ordinal = 0
        for node_id in [*self.nodes]:
            if node_id == node.id:
                return ordinal
            else:
                ordinal = ordinal + 1

        return -1

    def __repr__(self):
        s = 'number: {0}, name: {1}, nodes: {2}'.format(self.number, self.name, [*self.nodes])
        return s


'''
    collection of edges and channel Lists
'''
class ChannelCollectionObject:

    def __init__(self, pool_id):
        self.pool_id = pool_id

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

    def get_swim_channel_instance_by_name(self, channel_name):
        for channel_list in self.channel_lists:
            for channel in channel_list:
                if channel_name == channel.name:
                    return channel.instance

        return None

    def get_if_from_different_channels(self, from_node_id, to_node_id):
        from_node, to_node = None, None
        for channel_list in self.channel_lists:
            from_node_channel, from_node = self.find_channel_in_list_with_node(channel_list, from_node_id)
            if from_node_channel is not None:
                break

        if from_node_channel is None:
            return None, None

        for channel_list in self.channel_lists:
            to_node_channel, to_node = self.find_channel_in_list_with_node(channel_list, to_node_id)
            if to_node_channel is not None:
                break

        if to_node_channel is None:
            return None, None

        if from_node_channel == to_node_channel:
            return None, None

        return from_node, to_node

    def find_channel_in_list_with_node(self, channel_list, node_id):
        if not channel_list:
            return None, None

        for channel in channel_list:
            if node_id in channel.nodes:
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

            root_channel.add(node_id, parents, children)

        root_channel.group_and_order()

        self.channel_lists = []
        self.edges = []

        # build the inner data structure
        channel_list = None
        channel_number = 0
        for node_id_list in root_channel.as_list():
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

        def add(self, node_id, parents, children):
            # no parent, no children, it is an island
            # debug('[{0}]'.format(node_id))
            if len(parents) == 0 and len(children) == 0:
                # debug('  [{0}] is an island'.format(node_id))
                self.islands.append(node_id)
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
