#!/usr/bin/env python3
import copy
from mergedeep import merge

from helper.util import *
from helper.exception import *

''' theme utils
'''

ALLOWED_VALUES = {
    'shape': {
        'allowed-values': ['none', 'rect', ],
        'default-value': 'rect'
    },
    'halign': {
        'allowed-values': ['center', 'west', 'east', ],
        'default-value': 'center'
    },
    'valign': {
        'allowed-values': ['middle', 'north', 'south', ],
        'default-value': 'middle'
    },
    'position': {
        'allowed-values': ['west', 'east', 'north', ],
        'default-value': 'in'
    },
    'rotation': {
        'allowed-values': ['left', 'right', 'none', ],
        'default-value': 'none'
    },
    
}


''' parse theme
'''
def parse_theme(theme):
    parsed_theme = {}

    # get the defaults
    if 'defs' in theme:
        parsed_theme['defs'] = parse_defs(defs=theme['defs'])
    else:
        ThemeDataMissing(data='root', key='defs')

    # get the object specific attributes
    # for object_type in ['bpmn', 'pool', 'lane', 'band', 'node', 'edge', 'head', 'tail']:
    for object_type in ['bpmn', 'pool', 'lane', 'band', 'node', ]:
        if object_type in theme and theme[object_type]:
            parsed_theme[object_type] = merge({}, parsed_theme['defs'], parse_defs(defs=theme[object_type]))

            if 'label' in theme[object_type]:
                parsed_theme[object_type]['label'] = merge({}, parsed_theme['defs'], parse_defs(defs=theme[object_type]['label']))
                
        else:
            raise ThemeDataMissing(data='root', key=object_type)

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
    parsed_defs['shape'] = defs.get('shape', ALLOWED_VALUES['shape']['default-value'])
    if parsed_defs['shape'] not in ALLOWED_VALUES['shape']['allowed-values']:
        parsed_defs['shape'] = ALLOWED_VALUES['shape']['default-value']

    #  margin, defaults to 10 on all sides
    if 'margin' in defs:
        parsed_defs['margin'] = props_to_dict(text=defs['margin'])
    else:
        parsed_defs['margin'] = {}

    #  text-wrap defaults to 0
    parsed_defs['text-wrap'] = int(defs.get('text-wrap', 0))

    # position defaults to 'in'
    parsed_defs['position'] = defs.get('position', ALLOWED_VALUES['position']['default-value'])
    if parsed_defs['position'] not in ALLOWED_VALUES['position']['allowed-values']:
        parsed_defs['position'] = ALLOWED_VALUES['position']['default-value']

    # valign defaults to 'middle'
    parsed_defs['valign'] = defs.get('valign', ALLOWED_VALUES['valign']['default-value'])
    if parsed_defs['valign'] not in ALLOWED_VALUES['valign']['allowed-values']:
        parsed_defs['valign'] = ALLOWED_VALUES['valign']['default-value']

    # halign defaults to 'center'
    parsed_defs['halign'] = defs.get('halign', ALLOWED_VALUES['halign']['default-value'])
    if parsed_defs['halign'] not in ALLOWED_VALUES['halign']['allowed-values']:
        parsed_defs['halign'] = ALLOWED_VALUES['halign']['default-value']

    #  rotation defaults to 0
    parsed_defs['rotation'] = defs.get('rotation', ALLOWED_VALUES['rotation']['default-value'])
    if parsed_defs['rotation'] not in ALLOWED_VALUES['rotation']['allowed-values']:
        parsed_defs['rotation'] = ALLOWED_VALUES['rotation']['default-value']

    #  min-width defaults to 20
    parsed_defs['min-width'] = int(defs.get('min-width', 20))

    #  min-width defaults to 20
    parsed_defs['min-height'] = int(defs.get('min-height', 20))

    #  rx defaults to 2
    parsed_defs['rx'] = int(defs.get('rx', 2))

    #  ry defaults to 2
    parsed_defs['ry'] = int(defs.get('ry', 2))

    return parsed_defs
