#!/usr/bin/env python3

import importlib

from dot.dot_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Dot objects wrappers
#   ----------------------------------------------------------------------------------------------------------------

RANK_NODES = []

''' item object
'''
class Item(object):
    ''' constructor
    '''
    def __init__(self, data, level):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        self._data = data
        self._levl = level
        self._time = 0
        self._strt = 1000
        self._endt = 0
        self._spans = []
        self._items = []


    def process(self):
        # we may not have span for parent items
        if not 'hash' in self._data:
            warn(f"item has no value for [hash]")
            self._hash = 'NA'
        else:
            self._hash = self._data['hash']

        if not 'text' in self._data:
            warn(f"item has no value for [text]")
            self._text = 'MISSSING'
        else:
            self._text = self._data['text']


        if 'span' in self._data:
            # we have span, we need time, spans (list of strt, endt)
            span_text = self._data['span']

            # spans are list (separated by ,) of number pairs (separated by -)
            span_list = span_text.split(',')
            for a_span in span_list:
                pair = a_span.split('-')
                strt, endt = int(pair[0]), int(pair[1])
                self._spans.append({'strt': strt, 'endt': endt})
                self._strt = min(self._strt, strt)
                self._endt = max(self._endt, endt)
                self._time = self._time + endt - strt + 1

            # print(f"{data['hash']} [time={data['time']}, strt={data['strt']}, endt={data['endt']}]")

        else:
            if 'items' in self._data:
                debug(f"[{self._data['hash']}] [{self._data['text']}] does not have any span. Calculating time, start, end from children")
            else:
                warn(f"[{self._data['hash']}] [{self._data['text']}] does not have any span and there is no child. Can not calculate time, start, end")

        # process children if any
        if 'items' in self._data:
            for child_data in self._data['items']:
                child = Item(data=child_data, level=self._levl + 1)
                child.process()

        self._data['span'] = self._time
        self._data['strt'] = self._strt
        self._data['endt'] = self._endt


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
        self._items = []



    '''
    '''
    def parse_theme(self):
        # fixed nodes
        self._theme['node-spec']['header-style'] = props_to_dict(text=self._theme['node-spec']['header-style'])

        # how many levels we have defined?
        levels_defined = []
        for level, level_data in self._theme['node-spec']['row-styles'].items():
            levels_defined.append(level)
            self._theme['node-spec']['row-styles'][level] = props_to_dict(text=level_data)

        fixed_nodes = self._theme['node-spec']['fixed-nodes']
        for column, column_data in fixed_nodes.items():
            if 'header-style' in fixed_nodes[column]:
                fixed_nodes[column]['header-style'] = {**self._theme['node-spec']['header-style'], **props_to_dict(text=fixed_nodes[column]['header-style'])}
            else:
                # TODO warn
                fixed_nodes[column]['header-style'] = self._theme['node-spec']['header-style']

            if 'row-style' in fixed_nodes[column]:
                fixed_nodes[column]['row-style'] = {**self._theme['node-spec']['header-style'], **props_to_dict(text=fixed_nodes[column]['row-style'])}
            else:
                # TODO warn
                fixed_nodes[column]['row-style'] = self._theme['node-spec']['header-style']

            if 'level-styles' in column_data:
                for level, level_data in column_data['level-styles'].items():
                    column_data['level-styles'][level] = {**fixed_nodes[column]['row-style'], **props_to_dict(text=column_data['level-styles'][level])}
            else:
                # TODO warn
                column_data['level-styles'] = {}
                for level in levels_defined:
                    column_data['level-styles'][level] = {**self._theme['node-spec']['row-styles'][level], **fixed_nodes[column]['row-style']}



        # time nodes
        time_nodes = self._theme['node-spec']['time-nodes']
        time_nodes['head-row']['style'] = {**self._theme['node-spec']['header-style'], **props_to_dict(text=time_nodes['head-row']['style'])}


        # time node has data-rows
        time_nodes['data-row']['base-style'] = props_to_dict(text=time_nodes['data-row']['base-style'])

        # data rows have node types edge/head/tail
        for ntype in ['edge', 'tail', 'head']:
            if ntype in time_nodes['data-row']['type-styles']:
                time_nodes['data-row']['type-styles'][ntype] = {**time_nodes['data-row']['base-style'], **props_to_dict(text=time_nodes['data-row']['type-styles'][ntype])}

            else:
                warn(f"no [{ntype}] style defined for time nodes, using the base style")
                time_nodes['data-row']['type-styles'][ntype] = time_nodes['data-row']['base-style']


        # data-rows may differ by levels
        for level, level_data in time_nodes['data-row']['level-styles'].items():
            level_props = props_to_dict(text=level_data['style'])
            time_nodes['data-row']['level-styles'][level]['style'] = level_props

            # iterate over types
            for ntype in ['edge', 'tail', 'head']:
                if ntype in level_data:
                    time_nodes['data-row']['level-styles'][level][ntype] = {**level_props, **props_to_dict(time_nodes['data-row']['level-styles'][level][ntype])}

                else:
                    warn(f"no [{ntype}] style defined for level [{level}] time nodes, using the base style")
                    time_nodes['data-row']['level-styles'][level][ntype] = level_props



    ''' parse the data
    '''
    def parse_data(self):
        self._time_count = 0

        for item_data in self._data['items']:
            item = Item(data=item_data, level=0)
            item.process()
            self._items.append(item)
            self._time_count = max(self._time_count, item._time)

        # self._data['time'] = self._time_count



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
        self.process_header_row()

        # generate the data rows
        self.process_data_rows()

        # rank rows
        self.rank_rows()

        # wrap as a digraph
        self._lines = indent_and_wrap(self._lines, wrap_keyword='digraph ', object_name='G')

        return self._lines

    
    ''' the header row - 0
    '''
    def process_header_row(self):
        # the columns are to be found in theme['headers']
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content='# row 0 - header')
        nodes = []

        for k, v in self._theme['node-spec']['fixed-nodes'].items():
            id = f"_{self._current_row:03}_{k}"
            nodes.append({'id':id, 'label': v['label'], 'props': v['header-style']})

        self._lines = append_content(lines=self._lines, content='')

        # add a blank 00 time node 
        nodes.append({})
        for t in range(1, self._time_count + 1):
            id = f"_{self._current_row:03}_{t:02}"
            label = self._theme['node-spec']['time-nodes']['head-row']['label'].format(t)
            nodes.append({'id': id, 'label': label, 'props': self._theme['node-spec']['time-nodes']['head-row']['style']})

        for node in nodes:
            if node:
                self._lines = append_content(lines=self._lines, content=make_a_node(id=node['id'], label=node['label'], props=node['props']))

        # put nodes in same rank
        self.same_rank(nodes=nodes)


    ''' data row - 1.....
    '''
    def process_data_rows(self):
        self._lines = append_content(lines=self._lines, content='')

        for item in self._items:
            self._current_row = self._current_row + 1
            self.process_data_row(item=item)


    ''' process a data row
    '''
    def process_data_row(self, item):
        level = item._levl

        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# row {self._current_row}")
        nodes = []


        # the data nodes
        for k, v in item._data.items():
            if k in self._theme['node-spec']['fixed-nodes']:
                column = self._theme['node-spec']['fixed-nodes'][k]
                id = f"_{self._current_row:03}_{k}"
                props = column['level-styles'][f"L{level}"]
                label = props['label'].format(v)
                nodes.append({'id':id, 'label': label, 'props': props})
    
        time_node_strt = len(nodes)

        # the time nodes
        # add a blank 00 time node 
        nodes.append({})
        for t in range(1, self._time_count + 1):
            id = f"_{self._current_row:03}_{t:02}"
            label = ''
            nodes.append({'id':id, 'label': label, 'props': self._theme['node-spec']['time-nodes']['row-style']})


        # shape the time nodes so that they fill the time line
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# time line(s) row {self._current_row}")

        # actual headers
        for span in item._spans:
            span_strt = span['strt']
            span_endt = span['endt']

            tail_node = nodes[time_node_strt + span_strt]
            props = self._theme['node-spec']['time-nodes']['levels'][f"L{item._levl}"]['types']['tail']
            tail_node['label'] = props['label'].format(span_strt)
            tail_node['props'] = props

            head_node = nodes[time_node_strt + span_endt]
            props = self._theme['node-spec']['time-nodes']['levels'][f"L{item._levl}"]['types']['head']
            head_node['label'] = props['label'].format(span_endt)
            head_node['props'] = props

            for pos in range(span_strt+1, span_endt):
                node = nodes[time_node_strt + pos]
                props = self._theme['node-spec']['time-nodes']['levels'][f"L{item._levl}"]['types']['edge']
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
        for child_item in item._items:
            self._current_row = self._current_row + 1
            self.process_data_row(item=child_item)



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
