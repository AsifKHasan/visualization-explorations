#!/usr/bin/env python3

''' BPMN wrapper objects
'''
from bpmn.bpmn_api import BpmnRoot
from bpmn.bpmn_util import *
from svg.svg_api import SvgObject
from helper.theme import *
from helper.logger import *

class BpmnHelper(object):

    ''' constructor
    '''
    def __init__(self, config, theme):
        self._config = config
        self._source_theme = theme


    ''' generate and save the SVG
    '''
    def generate_and_save(self, bpmn_data):
        # parse the theme
        self._theme = parse_theme(theme=self._source_theme)

        # create BPMN root
        bpmn_object = BpmnRoot()

        # parse BPMN data
        bpmn_object.parse(source_data=bpmn_data)

        # create SVG object
        svg_object = SvgObject(config=self._config, theme=self._theme)

        # generate svg from bpmn root
        svg_object.to_svg(bpmn_object=bpmn_object)
