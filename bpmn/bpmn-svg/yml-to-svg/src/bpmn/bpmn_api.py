#!/usr/bin/env python3

import importlib

from bpmn.bpmn_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   BPMN objects wrappers
#   ----------------------------------------------------------------------------------------------------------------


''' BPMN base object
'''
class BpmnObject(object):
    ''' constructor
    '''
    def __init__(self, config):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config
        self._prepared_data = {}


    ''' prepare the output data
    '''
    def prepare_data(self, source_data):
        self._source_data = source_data

        # TODO: 
        self._prepared_data = self._source_data

        # finally return the prepared data
        return self._prepared_data




