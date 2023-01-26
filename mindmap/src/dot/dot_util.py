#!/usr/bin/env python3

'''
various utilities for generating (GraphViz) dot code
'''
import re
import random
import string

from helper.logger import *


''' make a property list
'''
def make_property_list(name, prop_dict):
    if prop_dict is None or prop_dict == {}:
        return None

    prop_list = []
    for k, v in prop_dict.items():
        prop_list.append(make_a_property(prop_key=k, prop_value=v))

    prop_str = '; '.join(prop_list)
    prop_str = f'[ {prop_str} ]'

    if not name is None:
        prop_str = f'{name} {prop_str}'

    return prop_str


''' make a property
'''
def make_a_property(prop_key, prop_value):
    prop_str = f'{prop_key}="{prop_value}"'

    return prop_str


''' make a dot Node
'''
def make_a_node(id, label, prop_dict):
    properies = {'label': label}
    if prop_dict:
        properies = {**properies, **prop_dict} 

    node_str = f"{id} {make_property_list(name=None, prop_dict=properies)}"

    return node_str


''' make a dot Edge
'''
def make_en_edge(from_node, to_node, prop_dict):
    prop_str = make_property_list(None, prop_dict=prop_dict)

    if prop_str:
        edge_str = f"{from_node} -> {to_node} {prop_str}"
    else:
        edge_str = f"{from_node} -> {to_node}"

    return edge_str


''' wrap (in start/stop) and indent dot lines
'''
def indent_and_wrap(lines, wrap_keyword, object_name, wrap_start='{', wrap_stop='}', indent_level=1):
    output_lines = []

    # subgraph's identifier must be prefixed with 'cluster_'
    if wrap_keyword == 'subgraph':
        object_name = f"cluster_{object_name}"
    
    # start wrap
    output_lines.append(f"{wrap_keyword} {object_name} {wrap_start}")

    # indent
    indent = "\t" * indent_level
    output_lines = output_lines + list(map(lambda x: f"{indent}{x}", lines))

    # stop wrap
    output_lines.append(f"{wrap_stop}")

    return output_lines



''' convert a text to a valid Dot identifier
'''
def text_to_identifier(text):
    # Remove invalid characters
    id = re.sub('[^0-9a-zA-Z_]', '', text)

    # Remove leading characters until we find a letter or underscore
    id = re.sub('^[^a-zA-Z_]+', '', id)

    return id



''' get a random string
'''
def random_string(length=12):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))



''' prep a text for dot
    remove spaces with \n
'''
def prep_for_dot(text):
    new_text = re.sub('\s+', r'\\n', text)

    return new_text