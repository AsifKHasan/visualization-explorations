#!/usr/bin/env python3
'''
python bpmn_script.py < ../out/pizza-order.json > ../out/pizza-order-test.bpmn
'''
import sys, json;
import textwrap

from util.logger import *

def quote(s):
    return '"{0}"'.format(s.replace('"', '"""'))

def repr_label_and_style(label, styles):
    s = '['

    s = '{0}label={1}; '.format(s, quote(label))
    for style in styles:
        s = '{0}{1}={2}; '.format(s, style, quote(styles[style]))

    s = '{0}]'.format(s.strip())

    return s

def repr_styles(styles):
    s = '['

    for style in styles:
        s = '{0}{1}={2}; '.format(s, style, quote(styles[style]))

    s = '{0}]'.format(s.strip())

    return s

def repr_edge(edge):
    s = '{0:<32}{1} {2:<32}{3}'.format(edge['from'], edge['type'], edge['to'], repr_label_and_style(edge['label'], edge['styles']))
    return s.strip()

def repr_node(node_id, node_data):
    s = '{0:<32}{1:<36}{2}'.format(node_data['type'], node_id, repr_label_and_style(node_data['label'], node_data['styles']))
    return s.strip()

def repr_pool(pool_id, pool_data):
    indent = ' ' * 4

    s = '\npool {0} {{\n'.format(pool_id)
    s = '{0}{1} {2}\n'.format(s, textwrap.indent('label =', indent), quote(pool_data['label']))
    s = '{0}{1} {2}\n\n'.format(s, textwrap.indent('_', indent), repr_styles(pool_data['styles']))

    # nodes
    for node_id, node_data in pool_data['nodes'].items():
        s = '{0}{1}\n'.format(s, textwrap.indent(repr_node(node_id, node_data), indent))

    # edges
    for edge in pool_data['edges']:
        s = '{0}\n{1}'.format(s, textwrap.indent(repr_edge(edge), indent))

    if len(pool_data['edges']) > 0:
        s = '{0}\n'.format(s)

    s = '{0}}}\n'.format(s)

    return s

def repr_lane(lane_id, lane_data):
    indent = ' ' * 4

    s = '\nlane {0} {{\n'.format(lane_id)
    s = '{0}{1} {2}\n'.format(s, textwrap.indent('label =', indent), quote(lane_data['label']))
    s = '{0}{1} {2}\n'.format(s, textwrap.indent('_', indent), repr_styles(lane_data['styles']))

    # pools
    for pool_id, pool_data in lane_data['pools'].items():
        s = '{0}{1}'.format(s, textwrap.indent(repr_pool(pool_id, pool_data), indent))

    # edges
    for edge in lane_data['edges']:
        s = '{0}\n{1}'.format(s, textwrap.indent(repr_edge(edge), indent))

    if len(lane_data['edges']) > 0:
        s = '{0}\n'.format(s)

    s = '{0}}}\n'.format(s)

    return s

def repr_bpmn(bpmn_id, bpmn_data):
    indent = ' ' * 4

    s = 'graph {0} {{\n'.format(bpmn_id)
    s = '{0}{1} {2}\n'.format(s, textwrap.indent('label =', indent), quote(bpmn_data['label']))
    s = '{0}{1} {2}\n'.format(s, textwrap.indent('_', indent), repr_styles(bpmn_data['styles']))

    # lanes
    for lane_id, lane_data in bpmn_data['lanes'].items():
        s = '{0}{1}'.format(s, textwrap.indent(repr_lane(lane_id, lane_data), indent))

    # edges
    for edge in bpmn_data['edges']:
        s = '{0}\n{1}'.format(s, textwrap.indent(repr_edge(edge), indent))

    if len(bpmn_data['edges']) > 0:
        s = '{0}\n'.format(s)

    s = '{0}}}'.format(s)

    return s

def to_script(bpmn_json_data):
    # we process only the first key and value (in case there are more which should not be) where key is bpmn id, and value is bpmn data
    for bpmn_id, bpmn_data in bpmn_json_data.items():
        script = repr_bpmn(bpmn_id, bpmn_data)
        return script, bpmn_id

if __name__ == "__main__":
    bpmn_json_data = json.load(sys.stdin)
    script, bpmn_id = to_script(bpmn_json_data)

    output_script_file_path = '../data/{0}.bpmn'.format(bpmn_id)
    print(script)

    info('Output at {0}'.format(output_script_file_path))
