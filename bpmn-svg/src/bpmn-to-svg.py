#!/usr/bin/env python3
'''
https://www.bpmnquickguide.com/view-bpmn-quick-guide/
cd C:\projects\asifhasan@github\visualization-explorations\bpmn-svg\src
python bpmn-to-svg.py < ../data/bpmn-sample.json
'''

import sys, json;

from util.logger import *

from elements.bpmn import Bpmn

if __name__ == "__main__":
    bpmn_json_data = json.load(sys.stdin)

    # we process only the first key and value (in case there are more which should not be) where key is bpmn id, and value is bpmn data
    for bpmn_id, bpmn_data in bpmn_json_data.items():
        info('processing bpmn [{0}] ...'.format(bpmn_id))
        svg = Bpmn().to_svg(bpmn_id, bpmn_data)
        output_svg_file_path = '../out/{0}.svg'.format(bpmn_id)
        svg.save(output_svg_file_path)
        info('processing bpmn [{0}] DONE. Output at {1}'.format(bpmn_id, output_svg_file_path))
