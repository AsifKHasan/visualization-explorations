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

def load_theme(bpmn_data):
    # we should get the theme from the *theme* key of the root element
    theme_key = bpmn_data['theme']

    # there should be a theme_key.json in *themes* directory
    theme_path = './themes/{0}.json'.format(theme_key)
    try:
        with open(theme_path, 'r') as f:
            theme_data = json.load(f)
            return theme_data

    except Exception as e:
        warn('theme {0} not found or not a theme at path [{1}]. Using {2} theme'.format(theme_key, theme_path, 'default'))
        try:
            theme_path = './themes/{0}.json'.format('default')
            with open(theme_path, 'r') as f:
                theme_data = json.load(f)
                return theme_data

        except Exception as e:
            error('theme {0} not found or not a theme at path [{1}]. Exiting...'.format('default', theme_path))
            raise e


def to_svg(bpmn_json_data):
    # we process only the first key and value (in case there are more which should not be) where key is bpmn id, and value is bpmn data
    for bpmn_id, bpmn_data in bpmn_json_data.items():
        theme = load_theme(bpmn_data)
        svg = Bpmn(bpmn_id, bpmn_data).to_svg(theme)
        return svg, bpmn_id


if __name__ == "__main__":
    bpmn_json_data = json.load(sys.stdin)
    svg, bpmn_id = to_svg(bpmn_json_data)
    output_svg_file_path = '../out/{0}.svg'.format(bpmn_id)
    svg.save(output_svg_file_path)
    info('Output at {0}'.format(output_svg_file_path))
