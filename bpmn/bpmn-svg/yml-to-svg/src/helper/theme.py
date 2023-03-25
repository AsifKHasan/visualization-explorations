#!/usr/bin/env python3
from mergedeep import merge

from helper.util import *
from helper.exception import *

''' theme utils
'''

''' parse theme
'''
def parse_theme(theme):

    # get the defaults
    if 'defs' in theme:
        theme['defs'] = parse_theme_defs(data=theme['defs'])
    else:
        ThemeDataMissing(data='root', key='defs')

    # get the text attributes
    if 'text' in theme:
        theme['text'] = merge(theme['defs'], parse_theme_text(data=theme['text']))
    else:
        ThemeDataMissing(data='root', key='text')

    # get the bpmn attributes
    if 'bpmn' in theme:
        bpmn_attrs = parse_theme_bpmn(data=theme['bpmn'])
        theme['bpmn'] = merge(theme['defs'], bpmn_attrs)
    else:
        ThemeDataMissing(data='root', key='bpmn')

    return theme



''' parse defs in theme
'''
def parse_theme_defs(data):
    parsed_data = {}

    #  style
    if 'style' in data:
        parsed_data['style'] = props_to_dict(text=data['style'])
    else:
        parsed_data['style'] = {}

    #  shape defaults to rect
    parsed_data['shape'] = data.get('shape', 'rect')

    #  margin, defaults to 10 on all sides
    if 'margin' in data:
        parsed_data['margin'] = props_to_dict(text=data['margin'])
    else:
        # parsed_data['margin'] = {'north': 10, 'south': 10, 'west': 10, 'east': 10}
        parsed_data['margin'] = {}

    #  text-wrap defaults to 0
    parsed_data['text-wrap'] = int(data.get('text-wrap', 0))

    # pos defaults to 'in'
    parsed_data['pos'] = data.get('pos', 'in')

    # valign defaults to 'middle'
    parsed_data['valign'] = data.get('halign', 'middle')

    # halign defaults to 'center'
    parsed_data['halign'] = data.get('halign', 'center')

    #  rotation defaults to 0
    parsed_data['rotation'] = int(data.get('rotation', 0))

    #  min-width defaults to 20
    parsed_data['min-width'] = int(data.get('min-width', 20))

    #  min-width defaults to 20
    parsed_data['min-height'] = int(data.get('min-height', 20))

    #  rx defaults to 2
    parsed_data['rx'] = int(data.get('rx', 2))

    #  ry defaults to 2
    parsed_data['ry'] = int(data.get('rx', 2))

    return parsed_data



''' parse text in theme
'''
def parse_theme_text(data):
    # parse the common attributes
    parsed_data = parse_theme_defs(data=data)

    return parsed_data


''' parse bpmn in theme
'''
def parse_theme_bpmn(data):
    # parse the common attributes
    parsed_data = parse_theme_defs(data=data)

    # parse the text attributes
    parsed_data['text'] = parse_theme_text(data=data['text'])

    return parsed_data

