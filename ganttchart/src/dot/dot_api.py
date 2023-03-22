#!/usr/bin/env python3

import importlib
from datetime import date, timedelta

from dot.dot_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Dot objects wrappers
#   ----------------------------------------------------------------------------------------------------------------
HOLIDAYS = {}
RANK_NODES = []
POOL_LIST = []
MAX_TIME = 1000
MIN_TIME = 0

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
        self._strt = MAX_TIME
        self._endt = MIN_TIME
        self._spans = []
        self._items = []


    def process(self):
        self._hide = self._data.get('hide', False)
        self._hide_children = self._data.get('hide-children', False)

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
            span_text = str(self._data['span'])

            # spans are list (separated by ,) of number pairs (separated by -)
            span_list = span_text.split(',')
            for a_span in span_list:
                pair = a_span.split('-')
                if len(pair) !=2:
                    warn(f"span [{a_span}] is invalid for [{self._hash} {self._text}]")
                else:
                    strt, endt = int(pair[0]), int(pair[1])
                    self._spans.append({'strt': strt, 'endt': endt})
                    self._strt = min(self._strt, strt)
                    self._endt = max(self._endt, endt)
                    self._time = self._time + endt - strt + 1


        else:
            if 'items' in self._data:
                debug(f"[{self._data['hash']}] [{self._data['text']}] does not have any span. Calculating time, start, end from children")
            else:
                warn(f"[{self._data['hash']}] [{self._data['text']}] does not have any span and there is no child. Can not calculate time, start, end")

        # if the item has a pool, append to pool list
        if 'pool' in self._data:
            if self._data['pool'] != '':
                if self._data['pool'] not in POOL_LIST:
                    POOL_LIST.append(self._data['pool'])


        # process children if any
        if 'items' in self._data:
            for child_data in self._data['items']:
                child = Item(data=child_data, level=self._levl + 1)
                child.process()
                self._strt = min(self._strt, child._strt)
                self._endt = max(self._endt, child._endt)
                self._items.append(child)

            self._time = self._endt - self._strt + 1

            # we ignore the spans and calculate the spans based on children
            self._spans = []
            self._spans.append({'strt': self._strt, 'endt': self._endt})


        self._data['time'] = self._time
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



    ''' parse the theme
    '''
    def parse_theme(self):
        # fixed nodes
        self._theme['node-spec']['header-style'] = props_to_dict(text=self._theme['node-spec']['header-style'])

        # how many levels we have defined?
        levels_defined = []
        for level, level_data in self._theme['node-spec']['row-styles'].items():
            levels_defined.append(level)
            self._theme['node-spec']['row-styles'][level] = props_to_dict(text=level_data)

        # fixed node columns
        fixed_nodes = self._theme['node-spec']['fixed-nodes']
        for column, column_data in fixed_nodes['columns'].items():
            if 'header-style' in column_data:
                column_data['header-style'] = {**self._theme['node-spec']['header-style'], **props_to_dict(text=column_data['header-style'])}
            else:
                # TODO warn
                column_data['header-style'] = self._theme['node-spec']['header-style']

            if 'row-style' in column_data:
                column_data['row-style'] = {**self._theme['node-spec']['header-style'], **props_to_dict(text=column_data['row-style'])}
            else:
                # TODO warn
                column_data['row-style'] = self._theme['node-spec']['header-style']

            if 'level-styles' in column_data:
                for level in levels_defined:
                    if level in column_data['level-styles']:
                        column_data['level-styles'][level] = {**column_data['row-style'], **self._theme['node-spec']['row-styles'][level], **props_to_dict(text=column_data['level-styles'][level])}
                    else:
                        column_data['level-styles'][level] = {**column_data['row-style'], **self._theme['node-spec']['row-styles'][level]}

            else:
                # TODO warn
                column_data['level-styles'] = {}
                for level in levels_defined:
                    column_data['level-styles'][level] = {**column_data['row-style'], **self._theme['node-spec']['row-styles'][level]}

        # pool-spec
        if 'pool-spec' in fixed_nodes and fixed_nodes['pool-spec']:
            if 'empty-pool' in fixed_nodes['pool-spec'] and fixed_nodes['pool-spec']['empty-pool']:
                fixed_nodes['pool-spec']['empty-pool'] = props_to_dict(text=fixed_nodes['pool-spec']['empty-pool'])

                if 'pool-styles' in fixed_nodes['pool-spec'] and fixed_nodes['pool-spec']['pool-styles']:
                    for i in range(0, len(fixed_nodes['pool-spec']['pool-styles'])):
                        fixed_nodes['pool-spec']['pool-styles'][i] = props_to_dict(text=fixed_nodes['pool-spec']['pool-styles'][i])

                else:
                    fixed_nodes['pool-spec']['pool-styles'] = []

            else:
                warn(f"[empty-pool] in [fixed-nodes][pool-spec] not defined in theme, disabling [pool-scheme]")
                self._pool_scheme = false

        else:
            warn(f"[fixed-nodes][pool-spec] not defined in theme, disabling [pool-scheme]")
            self._pool_scheme = false



        # time nodes
        time_nodes = self._theme['node-spec']['time-nodes']
        time_nodes['head-row']['style'] = {**self._theme['node-spec']['header-style'], **props_to_dict(text=time_nodes['head-row']['style'])}
        time_nodes['head-row']['holiday-style'] = props_to_dict(text=time_nodes['head-row']['holiday-style'])

        # time node has data-rows
        time_nodes['data-row']['base-style'] = props_to_dict(text=time_nodes['data-row']['base-style'])
        time_nodes['data-row']['holiday-style'] = props_to_dict(text=time_nodes['data-row']['holiday-style'])

        # data rows have node types edge/head/tail
        for ntype in ['edge', 'tail', 'head']:
            if ntype in time_nodes['data-row']['type-styles']:
                time_nodes['data-row']['type-styles'][ntype] = props_to_dict(text=time_nodes['data-row']['type-styles'][ntype])

            else:
                warn(f"no [{ntype}] default style defined for time nodes")
                time_nodes['data-row']['type-styles'][ntype] = {}


        # data-rows may differ by levels
        for level, level_data in time_nodes['data-row']['level-styles'].items():
            time_nodes['data-row']['level-styles'][level]['style'] = {**time_nodes['data-row']['base-style'], **props_to_dict(text=level_data['style'])}

            # iterate over types
            for ntype in ['edge', 'tail', 'head']:
                if ntype in level_data:
                    time_nodes['data-row']['level-styles'][level][ntype] = {**time_nodes['data-row']['level-styles'][level]['style'], **time_nodes['data-row']['type-styles'][ntype], **props_to_dict(time_nodes['data-row']['level-styles'][level][ntype])}

                else:
                    warn(f"no [{ntype}] style defined for level [{level}] time nodes, using the base style")
                    time_nodes['data-row']['level-styles'][level][ntype] = {**time_nodes['data-row']['level-styles'][level]['style'], **time_nodes['data-row']['type-styles'][ntype]}

        # pool-spec
        if 'pool-spec' in time_nodes and time_nodes['pool-spec']:
            if 'empty-pool' in time_nodes['pool-spec'] and time_nodes['pool-spec']['empty-pool']:
                time_nodes['pool-spec']['empty-pool'] = props_to_dict(text=time_nodes['pool-spec']['empty-pool'])

                if 'pool-styles' in time_nodes['pool-spec'] and time_nodes['pool-spec']['pool-styles']:
                    for i in range(0, len(time_nodes['pool-spec']['pool-styles'])):
                        time_nodes['pool-spec']['pool-styles'][i] = props_to_dict(text=time_nodes['pool-spec']['pool-styles'][i])

                else:
                    time_nodes['pool-spec']['pool-styles'] = []

            else:
                warn(f"[empty-pool] in [time-nodes][pool-spec] not defined in theme, disabling [pool-scheme]")
                self._pool_scheme = false

        else:
            warn(f"[time-nodes][pool-spec] not defined in theme, disabling [pool-scheme]")
            self._pool_scheme = false



    ''' parse the data
    '''
    def parse_data(self):
        self._time_count = 0

        self._show_pools = self._data.get('show-pools', [])
        self._pool_scheme = self._data.get('pool-scheme', False)
        self._consider_holidays = self._data.get('consider-holidays', False)

        for item_data in self._data['items']:
            item = Item(data=item_data, level=0)
            item.process()
            self._items.append(item)
            self._time_count = max(self._time_count, item._time)

        # self._data['time'] = self._time_count
        # get start date if any
        self._start_date = self._data.get('start-date', None)
        if self._start_date:
            try:
                self._start_date = date.fromisoformat(self._start_date) - timedelta(days=1)
                debug(f"[start-date] is [{self._start_date.strftime('%a, %b %d, %Y')}]")
            except:
                warn("[start-date] is invalid, ignoring ...")
                self._start_date = None
                self._consider_holidays = False

        if self._consider_holidays:
            if 'holiday-list' in self._data:
                if 'weekdays' not in self._data['holiday-list'] or not self._data['holiday-list']['weekdays']:
                    self._data['holiday-list']['weekdays'] = []

                else:
                    debug(f"found {self._data['holiday-list']['weekdays']} as holidays")

                if 'dates' not in self._data['holiday-list'] or not self._data['holiday-list']['dates']:
                    self._data['holiday-list']['dates'] = {}

                else:
                    debug(f"found {len(self._data['holiday-list']['dates'].keys())} listed holiday(s)")
                    for k, v in self._data['holiday-list']['dates'].items():
                        debug(f"  [{k}] [{v}]")

            else:
                warn("[holiday-list] is not defined, will not consider holidays ...")
                self._consider_holidays = False



    ''' create holidays
    '''
    def is_holiday(self, day_number):
        if self._consider_holidays == False:
            return False

        if self._start_date is None:
            return False

        the_date = self._start_date + timedelta(days=day_number)

        # if the week-day is a holiday
        week_day = the_date.strftime('%a')
        if week_day in self._data['holiday-list']['weekdays']:
            date_str = the_date.strftime('%Y-%m-%d')
            return True

        # if this is a listed holiday
        date_str = the_date.strftime('%Y-%m-%d')
        if date_str in self._data['holiday-list']['dates']:
            return True

        return False
        



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
        RANK_NODES.append(f"_{0:03}_hash")
        
        nodes = []

        for k, v in self._theme['node-spec']['fixed-nodes']['columns'].items():
            id = f"_{self._current_row:03}_{k}"
            props = v['header-style']
            if 'label' in props:
                label = props['label'].format(v['label'])
            else:
                label = v['label']

            nodes.append({'id':id, 'label': label, 'props': props})

        self._lines = append_content(lines=self._lines, content='')

        # add a blank 00 time node 
        nodes.append({})
        for t in range(1, self._time_count + 1):
            id = f"_{self._current_row:03}_{t:02}"
            label = self._theme['node-spec']['time-nodes']['head-row']['label'].format(t)
            props = self._theme['node-spec']['time-nodes']['head-row']['style']

            # this could be a holiday
            if self.is_holiday(day_number=t):
                props = {**props, **self._theme['node-spec']['time-nodes']['head-row']['holiday-style']}

            nodes.append({'id': id, 'label': label, 'props': props})

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
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# row {self._current_row}")

        # if the item is hidden, do not do anything
        if item._hide == True:
            return

        nodes = []
        # the fixed nodes
        for k in self._theme['node-spec']['fixed-nodes']['columns'].keys():
            column = self._theme['node-spec']['fixed-nodes']['columns'][k]
            props = column['level-styles'][f"L{item._levl}"]
            id = f"_{self._current_row:03}_{k}"

            if k in item._data:
                label = props['label'].format(item._data[k])
            else:
                # the key was not found in data, we need an empty node
                label = ''

            # HACK: sime/strt/endt columns should not have unwanted values
            if k in ['time', 'strt', 'endt']:
                if int(label) <= MIN_TIME or int(label) >= MAX_TIME:
                    label = '-'

            nodes.append({'type': 'fixed-node', 'id': id, 'label': label, 'props': props})


        # if the item is not in show-pools list, do not do anything
        if 'pool' in item._data:
            if self._show_pools and len(self._show_pools) > 0 and not item._data['pool'] in self._show_pools:
                return

        time_node_strt = len(nodes)

        # the time nodes
        nodes.append({})
        for t in range(1, self._time_count + 1):
            id = f"_{self._current_row:03}_{t:02}"
            label = ''
            nodes.append({'type': 'time-node', 'id':id, 'label': label, 'props': self._theme['node-spec']['time-nodes']['data-row']['base-style']})


        # shape the time nodes so that they fill the time line
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# time line(s) row {self._current_row}")
        RANK_NODES.append(f"_{self._current_row:03}_hash")

        # actual headers
        for span in item._spans:
            span_strt = span['strt']
            span_endt = span['endt']

            if span_strt != MAX_TIME and span_endt != MIN_TIME:
                tail_node = nodes[time_node_strt + span_strt]
                props = self._theme['node-spec']['time-nodes']['data-row']['level-styles'][f"L{item._levl}"]['tail']
                tail_node['label'] = props['label'].format(span_strt)
                tail_node['props'] = props

                head_node = nodes[time_node_strt + span_endt]
                props = self._theme['node-spec']['time-nodes']['data-row']['level-styles'][f"L{item._levl}"]['head']
                head_node['label'] = props['label'].format(span_endt)
                head_node['props'] = props

                for pos in range(span_strt+1, span_endt):
                    node = nodes[time_node_strt + pos]
                    props = self._theme['node-spec']['time-nodes']['data-row']['level-styles'][f"L{item._levl}"]['edge']
                    node['label'] = ''
                    node['props'] = props


        # at this point apply the pool specific styles
        if self._pool_scheme:
            # we select a pool style based on pool and apply to each node props
            if 'pool' not in item._data or item._data['pool'] is None or item._data['pool'] == '':
                pool_props_fixed = self._theme['node-spec']['fixed-nodes']['pool-spec']['empty-pool']
                pool_props_time = self._theme['node-spec']['time-nodes']['pool-spec']['empty-pool']
            else:
                # find the index of the pool in POOL_LIST
                index = POOL_LIST.index(item._data['pool'])

                index_fixed = index % len(self._theme['node-spec']['fixed-nodes']['pool-spec']['pool-styles'])
                pool_props_fixed = self._theme['node-spec']['fixed-nodes']['pool-spec']['pool-styles'][index_fixed]

                index_time = index % len(self._theme['node-spec']['time-nodes']['pool-spec']['pool-styles'])
                pool_props_time = self._theme['node-spec']['time-nodes']['pool-spec']['pool-styles'][index_time]

            for node in nodes:
                if node:
                    if node['type'] == 'fixed-node':
                        node['props'] = {**node['props'], **pool_props_fixed}

                    elif node['type'] == 'time-node':
                        node['props'] = {**node['props'], **pool_props_time}

                    else:
                        pass

        else:
            pass


        # generate the nodes
        for node in nodes:
            if node:
                self._lines = append_content(lines=self._lines, content=make_a_node(id=node['id'], label=node['label'], props=node['props']))

        # put nodes in same rank
        self.same_rank(nodes=nodes)


        # process children if any
        if item._hide_children == False:
            for child_item in item._items:
                self._current_row = self._current_row + 1
                self.process_data_row(item=child_item)



    ''' generate node ranks
    '''
    def rank_rows(self):
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# edges to rank rows")
        
        self._lines = append_content(lines=self._lines, content=f"{' -> '.join(RANK_NODES)} [ constraint=true; ]")



    ''' generate same ranks
    '''
    def same_rank(self, nodes):
        self._lines = append_content(lines=self._lines, content='')
        self._lines = append_content(lines=self._lines, content=f"# put nodes of rows in same rank")
        node_ids =  [n['id'] for n in nodes if 'id' in n]
        self._lines = append_content(lines=self._lines, content=f"{{ rank=same; {' -> '.join(node_ids)} }}")
