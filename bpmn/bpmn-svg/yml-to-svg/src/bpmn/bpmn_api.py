#!/usr/bin/env python3

import importlib

from bpmn.bpmn_util import *
from helper.util import *
from helper.exception import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   BPMN objects wrappers
#   ----------------------------------------------------------------------------------------------------------------


''' BPMN base object
'''
class BpmnObject(object):
    ''' constructor
    '''
    def __init__(self, config, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config
        self._theme = theme
        self._prepared_data = {}

        # BpmnObject may have nodes
        self._nodes = {}

        # BpmnObject may have edges
        self._edges = []

        # BpmnObject may have pools
        self._pools = {}

        # BpmnObject may have lanes
        self._lanes = {}

        # BpmnObject may have bands
        self._bands = {}

        self._label = None
        self._hide_label = False



''' BPMN root object
'''
class BpmnRoot(BpmnObject):
    ''' constructor
    '''
    def __init__(self, config, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, theme=theme)


    ''' prepare the output data
    '''
    def parse(self, source_data):
        # TODO: 
        if 'bpmn' in source_data:
            self._label = source_data.get('bpmn')
        else:
            raise BpmnDataMissing('BPMN', 'bpmn')

        self._hide_label = source_data.get('hide-label', False)



