#!/usr/bin/env python3

import importlib

from dot.dot_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Dot objects wrappers
#   ----------------------------------------------------------------------------------------------------------------

RANK_NODES = []

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


    '''
    '''
    def parse_theme(self):
        # fixed nodes
        self._header_nodes = {}

        common_header_props = props_to_dict(text=self._theme['node-spec']['header-style'])

        row_common_styles = {}
        for level, level_data in self._theme['node-spec']['row-styles'].items():
            row_common_styles[level] = props_to_dict(text=level_data)

        for header in self._theme['node-spec']['fixed-nodes']:
            props = {**common_header_props, **props_to_dict(text=header['header-style'])}
            self._header_nodes[header['column']] = {'label': header['label'], 'header-style': props, 'row-styles': {}}

            common_row_props = props_to_dict(text=header['row-style'])
            for k, v in header['row-styles'].items():
                props = {**row_common_styles[k], **common_row_props, **props_to_dict(text=v)}
                self._header_nodes[header['column']]['row-styles'][k] = props

        # time nodes
        self._time_nodes = self._theme['node-spec']['time-nodes']
        self._time_nodes['header-style'] = {**common_header_props, **props_to_dict(text=self._time_nodes['header-style'])}
        self._time_nodes['row-style'] = props_to_dict(text=self._time_nodes['row-style'])

        # iterate over types
        for level, level_data in self._time_nodes['levels'].items():
            level_props = props_to_dict(text=level_data['style'])
            self._time_nodes['levels'][level]['style'] = level_props
            # iterate over types
            for ntype, ntype_data in level_data['types'].items():
                type_props = {**self._time_nodes['row-style'], **level_props, **props_to_dict(text=ntype_data)}
                self._time_nodes['levels'][level]['types'][ntype] = type_props


    ''' parse the data
    '''
    def parse_data(self):
        self._time_count = 0

        for item in self._data['items']:
            self.parse_item(data=item, level=0)
            self._time_count = max(self._time_count, item['time'])

        self._data['time'] = self._time_count


    ''' parse the data items

    '''
    def parse_item(self, data, level):
        # we have span, we need time, spans (list of strt, endt)
        span_text = data['span']
        span_list = span_text.split(',')
        data['levl'] = level
        data['span'] = []
        time_span = 0
        min_strt = 1000
        max_endt = 0
        for a_span in span_list:
            pair = a_span.split('-')
            strt, endt = int(pair[0]), int(pair[1])
            min_strt = min(min_strt, strt)
            max_endt = max(max_endt, endt)
            data['span'].append({'strt': strt, 'endt': endt})
            time_span = time_span + endt - strt + 1

            # process children if any
            if 'items' in data:
                for child in data['items']:
                    self.parse_item(data=child, level=level + 1)

        data['time'] = time_span
        data['strt'] = min_strt
        data['endt'] = max_endt

        # print(f"{data['hash']} [time={data['time']}, strt={data['strt']}, endt={data['endt']}]")



    ''' generates the dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # parse the theme
        self.parse_theme()

        # parse the data
        self.parse_data()

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

        for k, v in self._header_nodes.items():
            id = f"_{self._current_row:03}_{k}"
            nodes.append({'id':id, 'label': v['label'], 'props': v['header-style']})

        self._lines = append_content(lines=self._lines, content='')

        # now the time headers
        time_header_prefix = self._time_nodes['header-label']
        time_header_props = self._time_nodes['header-style']

        # add a blank 00 time node 
        nodes.append({})
        for t in range(1, self._time_count + 1):
            id = f"_{self._current_row:03}_{t:02}"
            label = time_header_prefix.format(t)
            nodes.append({'id': id, 'label': label, 'props': time_header_props})

        for node in nodes:
            if node:
                self._lines = append_content(lines=self._lines, content=make_a_node(id=node['id'], label=node['label'], props=node['props']))

        # put nodes in same rank
        self.same_rank(nodes=nodes)


    ''' data row - 1.....
    '''
    def process_rows(self):
        self._lines = append_content(lines=self._lines, content='')

        for item in self._data['items']:
            self._current_row = self._current_row + 1
            self.process_data_row(data=item)


    ''' process a data row
    '''
    def process_data_row(self, data):
        level = data['levl']

        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# row {self._current_row}")
        nodes = []


        # the data nodes
        for k, v in data.items():
            if k in self._header_nodes:
                column = self._header_nodes[k]
                id = f"_{self._current_row:03}_{k}"
                # header_props = column['header-style']
                props = column['row-styles'][f"L{level}"]
                # props = {**header_props, **props}
                label = props['label'].format(v)
                nodes.append({'id':id, 'label': label, 'props': props})
    
        time_node_strt = len(nodes)

        # the time nodes
        # add a blank 00 time node 
        nodes.append({})
        for t in range(1, self._time_count + 1):
            id = f"_{self._current_row:03}_{t:02}"
            label = ''
            nodes.append({'id':id, 'label': label, 'props': self._time_nodes['row-style']})


        # shape the time nodes so that they fill the time line
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# time line(s) row {self._current_row}")

        # actual headers
        for span in data['span']:
            span_strt = span['strt']
            span_endt = span['endt']

            tail_node = nodes[time_node_strt + span_strt]
            props = self._time_nodes['levels'][f"L{data['levl']}"]['types']['tail']
            tail_node['label'] = props['label'].format(span_strt)
            tail_node['props'] = props

            head_node = nodes[time_node_strt + span_endt]
            props = self._time_nodes['levels'][f"L{data['levl']}"]['types']['head']
            head_node['label'] = props['label'].format(span_endt)
            head_node['props'] = props

            for pos in range(span_strt+1, span_endt):
                node = nodes[time_node_strt + pos]
                props = self._time_nodes['levels'][f"L{data['levl']}"]['types']['edge']
                node['label'] = ''
                node['props'] = props


            # self._lines = append_content(lines=self._lines, content=make_an_edge(head_node=head_node['id'], tail_node=tail_node['id'], props=edge_style))


        # generate the nodes
        for node in nodes:
            if node:
                self._lines = append_content(lines=self._lines, content=make_a_node(id=node['id'], label=node['label'], props=node['props']))

        # put nodes in same rank
        self.same_rank(nodes=nodes)


        # process children if any
        if 'items' in data:
            for item in data['items']:
                self._current_row = self._current_row + 1
                self.process_data_row(data=item)



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
        node_ids =  [n['id'] for n in nodes if 'id' in n]
        self._lines = append_content(lines=self._lines, content=f"{{ rank=same; {' -> '.join(node_ids)} }}")
