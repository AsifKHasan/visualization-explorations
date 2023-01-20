#!/usr/bin/env python3

'''
various utilities for generating (GraphViz) dot code
'''
import re
import random
import string

from helper.logger import *


''' make a dot Node
'''
def make_a_property(prop_key, prop_value):
    prop_str = f'{prop_key}="{prop_value}"; '

    return prop_str


''' make a dot Node
'''
def make_a_node(node_key, label):
    node_str = f"{node_key} [ {make_a_property(prop_key='label', prop_value=label)} ]"

    return node_str


''' wrap with BEGIN/END comments
'''
def wrap_with_comment(lines, object_type=None, object_id=None, comment_prefix_start='BEGIN', comment_prefix_stop='END  ', begin_suffix=None, indent_level=0):
    indent = "\t" * indent_level
    output_lines =  list(map(lambda x: f"{indent}{x}", lines))

    if object_type:
        if object_id:
            comment = f"{object_type}: [{object_id}]"

        else:
            comment = f"{object_type}"

        # BEGIN comment
        begin_comment = f"% {comment_prefix_start} {comment}"
        if begin_suffix:
            begin_comment = f"{begin_comment} {begin_suffix}"

        output_lines = [begin_comment] + output_lines

        # END comment
        end_comment = f"% {comment_prefix_stop} {comment}"
        output_lines.append(end_comment)


    return output_lines



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
