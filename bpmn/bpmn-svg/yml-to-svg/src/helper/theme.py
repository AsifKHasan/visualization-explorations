#!/usr/bin/env python3
from mergedeep import merge

from helper.util import *
from helper.exception import *

''' theme utils
'''

''' parse theme
'''
def parse_theme(theme):
    parsed_theme = {}

    # get the defaults
    if 'defs' in theme:
        parsed_theme['defs'] = parse_defs(defs=theme['defs'])
    else:
        ThemeDataMissing(data='root', key='defs')

    # get the bpmn attributes
    if 'bpmn' in theme:
        parsed_theme['bpmn'] = merge({}, parsed_theme['defs'], parse_defs(defs=theme['bpmn']))

        if 'label' in theme['bpmn']:
            parsed_theme['bpmn']['label'] = merge({}, parsed_theme['defs'], parse_defs(defs=theme['bpmn']['label']))
            
    else:
        ThemeDataMissing(data='root', key='bpmn')

    return parsed_theme



''' parse defs in theme
'''
def parse_defs(defs):
    parsed_defs = {}

    #  shape style
    if 'shape-style' in defs:
        parsed_defs['shape-style'] = props_to_dict(text=defs['shape-style'])
    else:
        parsed_defs['shape-style'] = {}

    #  label style
    if 'label-style' in defs:
        parsed_defs['label-style'] = props_to_dict(text=defs['label-style'])
    else:
        parsed_defs['label-style'] = {}

    #  shape defaults to rect
    parsed_defs['shape'] = defs.get('shape', 'rect')

    #  margin, defaults to 10 on all sides
    if 'margin' in defs:
        parsed_defs['margin'] = props_to_dict(text=defs['margin'])
    else:
        # parsed_defs['margin'] = {'north': 10, 'south': 10, 'west': 10, 'east': 10}
        parsed_defs['margin'] = {}

    #  text-wrap defaults to 0
    parsed_defs['text-wrap'] = int(defs.get('text-wrap', 0))

    # position defaults to 'in'
    parsed_defs['position'] = defs.get('position', 'in')

    # valign defaults to 'middle'
    parsed_defs['valign'] = defs.get('valign', 'middle')

    # halign defaults to 'center'
    parsed_defs['halign'] = defs.get('halign', 'center')

    #  rotation defaults to 0
    parsed_defs['rotation'] = defs.get('rotation', 'none')

    #  min-width defaults to 20
    parsed_defs['min-width'] = int(defs.get('min-width', 20))

    #  min-width defaults to 20
    parsed_defs['min-height'] = int(defs.get('min-height', 20))

    #  rx defaults to 2
    parsed_defs['rx'] = int(defs.get('rx', 2))

    #  ry defaults to 2
    parsed_defs['ry'] = int(defs.get('ry', 2))

    return parsed_defs
