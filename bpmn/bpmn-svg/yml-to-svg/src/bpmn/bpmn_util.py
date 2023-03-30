#!/usr/bin/env python3

import re

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
