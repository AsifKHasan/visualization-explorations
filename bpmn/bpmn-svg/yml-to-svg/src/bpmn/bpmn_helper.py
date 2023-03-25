#!/usr/bin/env python3

''' BPMN wrapper objects
'''

import time
import yaml
import datetime

from bpmn.bpmn_api import BpmnObject
from bpmn.bpmn_util import *
from svg.svg_api import SvgObject
from helper.logger import *

class BpmnHelper(object):

    ''' constructor
    '''
    def __init__(self, config):
        self._config = config


    ''' generate and save the SVG
    '''
    def generate_and_save(self, bpmn_data):
        # create BPMN object
        bpmn_object = BpmnObject(config=self._config)

        # prepare BPMN data
        prepared_data = bpmn_object.prepare_data(source_data=bpmn_data)

        # create SVG object
        svg_object = SvgObject(config=self._config)

        # generate svg from data
        svg_object.to_svg(bpmn_data=prepared_data)
