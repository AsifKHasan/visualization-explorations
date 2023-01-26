#!/usr/bin/env python3

import importlib

from dot.dot_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Dot objects wrappers
#   ----------------------------------------------------------------------------------------------------------------

''' Dot graph object
'''
class DotObject(object):

    ''' constructor
    '''
    def __init__(self, config, data, level=0):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config

        self._data = data
        self._level = level
        self._children = []

        self._theme = self._config['theme']['theme-data'][str(self._level)]
        self._lines = []

        self._label = prep_for_dot(text=self._data['label'])
        self._id = text_to_identifier(text=self._label)


    ''' append single line or list of lines to _lines
    '''
    def append_content(self, content):
        if content is None:
            return

        if isinstance(content, str):
            self._lines.append(content)

        elif isinstance(content, list):
            self._lines = self._lines + content


    ''' generates the Dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # set the attributes only if we are in a new level
        if self._level != self._config['previous-level']:
            # print(self._label)
            # self.append_content(content='')
            self.append_content(content=make_property_list(name='graph', prop_dict=self._theme.get('graph', {})))
            self.append_content(content='')
            self._config['previous-level'] = self._level


        # make the node
        self.append_content(content=make_a_node(id=self._id, label=self._label, prop_dict=self._theme.get('node', {})))


        # traverse children
        for child in self._data.get('children', []):
            child_object = DotObject(config=self._config, data=child, level=self._level+1)
            self.append_content(content=child_object.to_dot())

            # make the edges between parent and child
            self.append_content(content=make_en_edge(from_node=self._id, to_node=child_object._id, prop_dict=self._theme.get('edge', {})))


        # wrap as a digraph
        if self._level == 0:
            self._lines = indent_and_wrap(self._lines, wrap_keyword='digraph', object_name='G')

        return self._lines
