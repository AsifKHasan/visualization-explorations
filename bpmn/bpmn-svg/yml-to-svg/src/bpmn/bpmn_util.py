#!/usr/bin/env python3

import re
from bigtree import list_to_tree_by_relation, print_tree

from helper.util import *

'''
various utilities for BPMN
'''

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
    tail_node = text=node_list[0].strip()
    head_node = text=node_list[1].strip()

    return tail_node, head_node, prop_dict



''' from list of edges create bands so that one branch from the edge tree is a band
    edge_list is a list of tuples (tail_node, head_node)
'''
def edges_to_bands(edge_list, node_list):
    # head and tail nodes of an edge must be in the node_list
    pruned_edge_list = [ (edge[0], edge[1]) for edge in edge_list if edge[0] in node_list and edge[1] in node_list ]

    # eliminate edges where they make a cycle
    pruned_edge_list = [ (edge[0], edge[1]) for edge in pruned_edge_list if (edge[1], edge[0]) not in pruned_edge_list ]

    # for t in pruned_edge_list:
    #     print(f"{t[0]:40} -> {t[1]}")

    bands = []
    if len(pruned_edge_list) > 0:

        root = list_to_tree_by_relation(pruned_edge_list)
        print_tree(root)
        band = []
        traverse_preorder(root=root, bands=bands, band=band)
        if len(band) > 0:
            bands.append(band)

    # we may have stray nodes which were not part of any edges, put those in a separate band
    connected_nodes = [ edge[0] for edge in edge_list] + [ edge[1] for edge in pruned_edge_list ]
    stray_nodes = [ node for node in node_list if not node in connected_nodes ]

    if len(stray_nodes) > 0:
        bands.append(stray_nodes)

    return bands


def traverse_preorder(root, bands, band):
    if root:
        # it is going into the current band
        band.append(root.name)
        new_branch = False
        for node in root.children:
            if new_branch:
                bands.append(band)
                band = []
                print("new band")
                print(band)

            # Then recur on this child
            traverse_preorder(root=node, bands=bands, band=band)
            
            if new_branch == False:
                new_branch = True

            # the branch ends here


