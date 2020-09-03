#!/usr/bin/env python3
'''
python bpmn_script.py < ../data/bpmn-sample.json > ../data/bpmn-sample.bpmn
'''
import sys, json;

from util.logger import *

def repr_bpmn(bpmn_id, bpmn_data):
    s = 'graph {0} {{\n'.format(bpmn_id)
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
    with open(output_script_file_path, mode='w') as f:
        f.write(script)

    info('Output at {0}'.format(output_script_file_path))
