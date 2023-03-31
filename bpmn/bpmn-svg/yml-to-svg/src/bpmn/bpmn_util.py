#!/usr/bin/env python3

import re
from bigtree import list_to_tree_by_relation, print_tree

from helper.util import *

'''
various utilities for BPMN
'''


''' create node-id from node label
'''
def node_id_from_label(label):
    return f"node__{text_to_identifier(label)}"    


''' parse node
    Pay for the Pizza        [ width='1.5in'; ]
'''
def parse_node_from_text(text):
    # see if there are properties enclosed inside []
    node_str = text
    m = re.search(r"\[(.+)\]", text)
    if m:
        prop_str = m.group(1)
        prop_dict = props_to_dict(text=prop_str)

        node_str = text[:m.start(0)]

    else:
        prop_dict = {}

    # get the label
    label = node_str.strip()

    return label, prop_dict



''' parse edge
    Order a Pizza        -> Order Received           [ label='pizza order'; ]
'''
def parse_edge_from_text(text):
    # see if there are properties enclosed inside []
    edge_str = text
    m = re.search(r"\[(.+)\]", text)
    if m:
        prop_str = m.group(1)
        prop_dict = props_to_dict(text=prop_str)

        edge_str = text[:m.start(0)]

    else:
        prop_dict = {}

    # get the from and to nodes
    node_list = edge_str.split('->')
    tail_node = node_id_from_label(label=node_list[0].strip())
    head_node = node_id_from_label(label=node_list[1].strip())

    return tail_node, head_node, prop_dict



''' from list of edges create bands so that one branch from the edge tree is a band
    edge_list is a list of tuples (tail_node, head_node)
'''
def edges_to_bands(edge_list, node_list):
    # edge list needs to be curated
    pruned_edge_list = []
    for edge in edge_list:
        # head and tail nodes of an edge must be in the node_list
        if edge[0] in node_list and edge[1] in node_list:
            # if there is any edge (tail->head) it should be removed if there is another edge (head->tail) to remove cycles
            if (edge[1], edge[0]) not in pruned_edge_list:
                pruned_edge_list.append(edge)

    bands = []
    if len(pruned_edge_list) > 0:
        band = []
        root = list_to_tree_by_relation(pruned_edge_list)
        traverse_preorder(root=root, bands=bands, band=band)

    # we may have stray nodes which were not part of any edges, put those in a separate band
    connected_nodes = [ edge[0] for edge in edge_list] + [ edge[1] for edge in pruned_edge_list ]
    stray_nodes = [ node for node in node_list if not node in connected_nodes ]

    if len(stray_nodes) > 0:
        bands.append(stray_nodes)

    return bands


''' recusive function for preorder tree traversal
'''
def traverse_preorder(root, bands, band):
    if root:
        # it is going into the current band
        band.append(root.name)
        for node in root.children:
            # Then recur on this child
            traverse_preorder(root=node, bands=bands, band=band)
            if node.is_leaf:
                bands.append(band)
            
            band = []


