#!/usr/bin/env python3

import importlib

from dot.dot_util import *
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
        self._id = None



''' Dot graph object
'''
class GraphObject(DotObject):

    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config, data)

        self._class = 'graph'
        self._theme = self._config['theme']['theme-data'][self._class]

        self._label = self._data.get('bpmn')
        self._id = f"{self._class}_{text_to_identifier(text=self._label)}"



    ''' append single line or list of lines to _lines
    '''
    def append_content(self, content):
        if content is None:
            return

        if isinstance(content, str):
            self._lines.append(content)

        elif isinstance(content, list):
            self._lines = self._lines + content


    ''' generates the dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        if not self._hide_label:
            self._lines.append(make_a_property(prop_key='label', prop_value=self._label))
            self._lines.append('')

        # graph attributes
        self._lines = self._lines + make_property_lines(self._theme['attributes'])
        self._lines.append('')

        # node properties
        self._lines.append(f"node [ {make_property_list(self._theme['node'])} ]")

        # edge properties
        self._lines.append(f"edge [ {make_property_list(self._theme['edge'])} ]")

        # elements
        if self._data['elements']:
            for node in self._data['elements']:
                pass

        # pools
        if self._data['pools']:
            for node in self._data['pools']:
                pass

        # edges
        if self._data['edges']:
            for node in self._data['edges']:
                pass

        # wrap as a digraph
        self._lines = indent_and_wrap(self._lines, wrap_keyword='digraph ', object_name=self._id)

        return self._lines
