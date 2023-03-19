#!/usr/bin/env python3

import importlib

from svg.svg_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Dot objects wrappers
#   ----------------------------------------------------------------------------------------------------------------


''' Dot base object
'''
class DotObject(object):
    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config
        self._data = data
        self._lines = []
        self._hide_label = self._data.get('hide-label', False)
        self._class = None
        self._label = None




