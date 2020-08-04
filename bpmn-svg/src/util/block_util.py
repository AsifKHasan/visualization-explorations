#!/usr/bin/env python3
'''
'''
from pprint import pprint
from copy import deepcopy

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

from elements.svg_element import SvgElement

# a channel is a node and another channel which is the next node and so on. Basically this represents node -> node -> .......
# a channel may have more than one next nodes if it has two or more branches
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
                parent.add_children(Channel(child_node_id))
                # debug('[{0}] added as a descendant orphan to [{1}] under key [{2}]'.format(child_node_id, parent_node_id, key))

        if not found:
            if child_node_id in self.orphans:
                self.orphans[parent_node_id] = Channel(child_node_id, self.orphans.pop(child_node_id))
            else:
                self.orphans[parent_node_id] = Channel(child_node_id)

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
            self.add_children(Channel(node_id, self.orphans.pop(node_id, None)))
            # self.add_children(Channel(node_id))
            return

        # we have parent(s), we just find the parent and put it as children
        if len(parents) > 0:
            for parent_node_id in parents:
                parent = self.find(parent_node_id)
                # parent found, we just add this as children for the parent
                if parent:
                    # debug('[{0}] is child to [{1}]'.format(node_id, parent.node_id))
                    parent.add_children(Channel(node_id, self.orphans.pop(node_id, None)))
                    # parent.add_children(Channel(node_id))
                    return

        # if (any of) the parent(s) do(es) not exist (yet), it is an orphan or a child to another orphan
        # debug('[{0}] none of the parents {1} processed yet, adding as an orphan'.format(node_id, parents))
        for parent_node_id in parents:
            self.add_orphans(parent_node_id, node_id)

        return

'''
    in a pool, nodes need to be processed (ordered and grouped)
    1. nodes that are connected with other nodes (in the same pool) should be ordered in a group so that they are in the same channel (a channel is vertical lines for node flow, a lane may have multiple channels if the edges are branched like a tree) and flow from left to right based or edge order (head node at left, tail node at right)
    2. isolated nodes (nodes that do not connect to any other nodes) should be put in a separate group (in which channel they should go is a TODO)
    3. If any node connects to two or more nodes (in the same pool) a new group starts for each branch so that they can be placed into different channels
'''
def group_nodes_inside_a_pool(bpmn_id, lane_id, pool_id, pool_nodes, pool_edges):
    # iterate the edges and discard edges where either head or tail node is not inside the pool, in the same go remove duplicates also
    filtered_pool_edges = []
    edge_keys = []
    for edge in pool_edges:
        if edge['head'] in pool_nodes and edge['tail'] in pool_nodes:
            edge_key = '{0}__#__{1}'.format(edge['head'], edge['tail'])
            if edge_key not in edge_keys:
                filtered_pool_edges.append(edge)
                edge_keys.append(edge_key)

    # now we group and order the nodes in a root Channel to be returned
    root_channel = Channel()
    for node_id, node_data in pool_nodes.items():
        # get the parent and child nodes of this node
        children = []
        parents = []
        for edge in filtered_pool_edges:
            if node_id == edge['head']:
                children.append(edge['tail'])

            if node_id == edge['tail']:
                parents.append(edge['head'])

        root_channel.add(node_id, parents, children)

    root_channel.group_and_order()

    return root_channel

def group_nodes_across_pools(bpmn_id, lane_id, lane_nodes, lane_edges):
    pass

def group_nodes_across_lanes(bpmn_id, bpmn_nodes, bpmn_edges):
    pass

def assemble_channel(channel_name, channel_nodes, spec):
    # wrap it in a svg group
    svg_group = G()

    # get the max height and cumulative width of all elements and adjust height and width accordingly
    max_element_height = get_max_height(channel_nodes)

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
        current_x = current_x + node_object['width'] + spec['dx-between-elements']

    group_width = current_x - spec['dx-between-elements']

    # the group rect
    channel_rect_svg = Rect(width=group_width, height=group_height)
    channel_rect_svg.set_style(StyleBuilder(spec['channel-style']).getStyle())
    svg_group.addElement(channel_rect_svg)

    # wrap it in a svg element
    group_spec = {'width': group_width, 'height': group_height}
    return SvgElement(group_spec, svg_group)

def get_max_height(channel_nodes):
    max_element_height = 0
    for node_id, node_object in channel_nodes.items():
        max_element_height = max(node_object['height'], max_element_height)

    return max_element_height
