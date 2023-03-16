#!/usr/bin/env python3

import importlib

from dot.dot_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Dot objects wrappers
#   ----------------------------------------------------------------------------------------------------------------

RANK_NODES = []
EDGE_PROPS = {}

NODE_DICT = {}


''' parse node properties
'''
def parse_node_props(node_props):
    for k, v in node_props.items():
        prop_dict = props_to_dict(text=v)
        NODE_PROPS[k] = prop_dict


''' parse edge properties
'''
def parse_edge_props(edge_props):
    for k, v in edge_props.items():
        prop_dict = props_to_dict(text=v)
        EDGE_PROPS[k] = prop_dict


''' Dot base object
'''
class GraphObject(object):
    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config
        self._data = data
        self._theme = self._config['theme']['theme-data']
        self._lines = []
        self._current_row = 0
        self._time_count = self._data['times']


    ''' generates the dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # graph attributes
        self._lines = append_content(lines=self._lines, content=make_property_lines(self._theme['graph']['attributes']))
        self._lines = append_content(lines=self._lines, content='')

        # node properties
        self._lines = append_content(lines=self._lines, content=f"node [ {make_property_list(self._theme['graph']['node'])}; ]")

        # edge properties
        self._lines = append_content(lines=self._lines, content=f"edge [ {make_property_list(self._theme['graph']['edge'])}; ]")

        # generate the header row
        self.header_row()

        # generate the data rows
        self.process_rows()

        # rank rows
        self.rank_rows()

        # wrap as a digraph
        self._lines = indent_and_wrap(self._lines, wrap_keyword='digraph ', object_name='G')

        return self._lines

    
    ''' the header row - 0
    '''
    def header_row(self):
        # the columns are to be found in theme['headers']
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content='# row 0 - header')
        nodes = []

        self._headers = {}
        for header in self._theme['headers']:
            self._headers[header['column']] = {'label': header['label'], 'style': props_to_dict(text=header['style'])}
            self._headers[header['column']]['row-styles'] = {}
            for k, v in header['row-styles'].items():
                self._headers[header['column']]['row-styles'][k] = props_to_dict(text=v)

        for k, v in self._headers.items():
            id = f"_{self._current_row:03}_{k}"
            self._lines = append_content(lines=self._lines, content=make_a_node(id=id, label=v['label'], prop_dict=v['style']))
            nodes.append(id)

        self._lines = append_content(lines=self._lines, content='')

        # now the time headers
        time_header_prefix = self._theme['time-headers']['label-format']
        time_header_style = props_to_dict(text=self._theme['time-headers']['style'])

        for t in range(1, self._time_count + 1):
            id = f"_{self._current_row:03}_{t:02}"
            label = time_header_prefix.format(t)
            self._lines = append_content(lines=self._lines, content=make_a_node(id=id, label=label, prop_dict=time_header_style))
            nodes.append(id)

        # put nodes in same rank
        self.same_rank(nodes=nodes)


    ''' data row - 1.....
    '''
    def process_rows(self):
        self._lines = append_content(lines=self._lines, content='')

        for item in self._data['items']:
            self._current_row = self._current_row + 1
            self.process_data_row(data=item, level=0)


    ''' process a data row
    '''
    def process_data_row(self, data, level):
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# row {self._current_row}")
        nodes = []

        # the data nodes
        for k, v in data.items():
            if k in self._headers:
                id = f"_{self._current_row:03}_{k}"
                style = self._headers[k]['row-styles'][f"L{level}"]
                label = style['label'].format(v)
                self._lines = append_content(lines=self._lines, content=make_a_node(id=id, label=label, prop_dict=style, properties_excluded=['label']))
                nodes.append(id)
    
        # the time nodes
        time_node_style = props_to_dict(text=self._theme['time-headers']['row-style'])
        self._time_count = self._data['times']
        for t in range(1, self._time_count + 1):
            id = f"_{self._current_row:03}_{t:02}"
            label = ''
            self._lines = append_content(lines=self._lines, content=make_a_node(id=id, label=label, prop_dict=time_node_style))
            nodes.append(id)

        # put nodes in same rank
        self.same_rank(nodes=nodes)

        # the edges for time
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# time edge for row {self._current_row}")
        from_node = f"_{self._current_row:03}_{data['strt']:02}"
        to_node = f"_{self._current_row:03}_{data['endt']:02}"
        edge_style = props_to_dict(text=self._theme['time-headers']['edge-styles'][f"L{level}"])
        self._lines = append_content(lines=self._lines, content=make_an_edge(from_node=from_node, to_node=to_node, prop_dict=edge_style))

        # process children if any
        if 'items' in data:
            for item in data['items']:
                self._current_row = self._current_row + 1
                self.process_data_row(data=item, level=level + 1)



    ''' generate node ranks
    '''
    def rank_rows(self):
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# edges to rank rows")
        for r in range(0, self._current_row + 1):
            RANK_NODES.append(f"_{r:03}_hash")
        
        self._lines = append_content(lines=self._lines, content=f"{' -> '.join(RANK_NODES)} [ constraint=true; ]")


    ''' generate same ranks
    '''
    def same_rank(self, nodes):
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# put nodes of rows in same rank")
        self._lines = append_content(lines=self._lines, content=f"{{ rank=same; {' -> '.join(nodes)} }}")
