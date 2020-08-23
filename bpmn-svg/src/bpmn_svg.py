#!/usr/bin/env python3
'''
https://www.bpmnquickguide.com/view-bpmn-quick-guide/
cd C:\projects\asifhasan@github\visualization-explorations\bpmn-svg\src
python bpmn_svg.py < ../data/bpmn-sample.json
python bpmn_parser.py < ../data/grp__hrm__award-and-publication.bpmn | tee ../data/grp__hrm__award-and-publication.json | python bpmn_svg.py
'''
import sys, json;

from util.logger import *

from elements.bpmn import Bpmn

def to_svg(bpmn_json_data):
    # we process only the first key and value (in case there are more which should not be) where key is bpmn id, and value is bpmn data
    for bpmn_id, bpmn_data in bpmn_json_data.items():
        svg = Bpmn(bpmn_id, bpmn_data).to_svg()
        return svg, bpmn_id

if __name__ == "__main__":
    bpmn_json_data = json.load(sys.stdin)
    svg, bpmn_id = to_svg(bpmn_json_data)
    output_svg_file_path = '../out/{0}.svg'.format(bpmn_id)
    svg.save(output_svg_file_path)
    info('Output at {0}'.format(output_svg_file_path))
