#!/usr/bin/env python3

import importlib
from datetime import date, timedelta

from dot.dot_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Dot objects wrappers
#   ----------------------------------------------------------------------------------------------------------------
RANK_NODES = []
POOL_LIST = []
MAX_TIME = 1000
MIN_TIME = 0

THEME = None
DATA = None
VIEW = None
CONSIDER_HOLIDAYS = None
START_DATE = None


''' weekday in short format
'''
def long_date(day_number):
    global START_DATE

    the_date = START_DATE + timedelta(days=day_number)
    if START_DATE:
        return the_date.strftime('%a')[0], the_date.strftime('%b'), the_date.strftime('%d'), the_date.strftime('%y')
    else:
        return ''



''' is a day a holiday
'''
def is_holiday(day_number):
    global START_DATE
    global CONSIDER_HOLIDAYS

    if CONSIDER_HOLIDAYS == False:
        return False

    the_date = START_DATE + timedelta(days=day_number)
    date_str = the_date.strftime('%Y-%m-%d')

    # if the week-day is a holiday
    week_day = the_date.strftime('%a')
    if week_day in DATA['holiday-list']['weekdays']:
        return True

    # if this is a listed holiday
    if date_str in DATA['holiday-list']['dates']:
        return True

    return False



''' get the next working day
'''
def next_workday(day_number):
    next_work_day = day_number
    while True:
        next_work_day = next_work_day + 1
        if not is_holiday(day_number=next_work_day):
            return next_work_day



''' adjust for holidays
'''
def adjust_for_holidays(strt, endt):
    new_strt = strt
    new_endt = endt

    diff = endt - strt

    # strt day must not be a holiday
    if is_holiday(day_number=new_strt):
        new_strt = next_workday(day_number=new_strt)
        new_endt = new_strt + diff

    # we are assured that now the start is not on a holiday, we should validate the subsequent says sequentially
    current_day = new_strt + 1
    while current_day <= new_endt:

        if is_holiday(day_number=current_day):
            new_current_day = next_workday(day_number=current_day)
            days_added = (new_current_day - current_day)
            new_endt = new_endt + days_added
            current_day = current_day + days_added

        else:
            current_day = current_day + 1

    return new_strt, new_endt



''' item object
'''
class Item(object):
    ''' constructor
    '''
    def __init__(self, data, level):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        self._item_data = data
        self._levl = level
        self._time = 0
        self._strt = MAX_TIME
        self._endt = MIN_TIME
        self._spans = []
        self._items = []



    def process(self):
        global CONSIDER_HOLIDAYS

        self._hide = self._item_data.get('hide', False)
        self._hide_children = self._item_data.get('hide-children', False)

        # we may not have span for parent items
        if not 'hash' in self._item_data:
            warn(f"item has no value for [hash]")
            self._hash = 'NA'
        else:
            self._hash = self._item_data['hash']

        if not 'text' in self._item_data:
            warn(f"item has no value for [text]")
            self._text = 'MISSSING'
        else:
            self._text = self._item_data['text']


        if 'span' in self._item_data:
            # we have span, we need time, spans (list of strt, endt)
            span_text = str(self._item_data['span'])

            # spans are list (separated by ,) of number pairs (separated by -)
            span_list = span_text.split(',')
            for a_span in span_list:
                pair = a_span.split('-')
                if len(pair) !=2:
                    warn(f"span [{a_span}] is invalid for [{self._hash} {self._text}]")
                else:
                    strt, endt = int(pair[0]), int(pair[1])
                    # adjust for holidays
                    if CONSIDER_HOLIDAYS:
                        strt, endt = adjust_for_holidays(strt=strt, endt=endt)

                    self._spans.append({'strt': strt, 'endt': endt})
                    self._strt = min(self._strt, strt)
                    self._endt = max(self._endt, endt)


                    self._time = self._time + endt - strt + 1


        else:
            if 'items' in self._item_data:
                debug(f"[{self._item_data['hash']}] [{self._item_data['text']}] does not have any span. Calculating time, start, end from children")
            else:
                warn(f"[{self._item_data['hash']}] [{self._item_data['text']}] does not have any span and there is no child. Can not calculate time, start, end")

        # if the item has a pool, append to pool list
        if 'pool' in self._item_data:
            if self._item_data['pool'] != '':
                if self._item_data['pool'] not in POOL_LIST:
                    POOL_LIST.append(self._item_data['pool'])


        # process children if any
        if 'items' in self._item_data:
            for child_data in self._item_data['items']:
                child = Item(data=child_data, level=self._levl + 1)
                child.process()
                self._strt = min(self._strt, child._strt)
                self._endt = max(self._endt, child._endt)
                self._items.append(child)

            self._time = self._endt - self._strt + 1

            # we ignore the spans and calculate the spans based on children
            self._spans = []
            self._spans.append({'strt': self._strt, 'endt': self._endt})


        self._item_data['time'] = self._time
        self._item_data['strt'] = self._strt
        self._item_data['endt'] = self._endt



''' Dot base object
'''
class GraphObject(object):
    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        global THEME
        global DATA
        global CONSIDER_HOLIDAYS
        global START_DATE

        # self._config = config
        DATA = data
        THEME = config['theme']['theme-data']
        self._lines = []
        self._current_row = 0
        self._items = []

        self._collapsed_ranges = {}



    ''' parse the theme
    '''
    def parse_theme(self):
        # fixed nodes
        THEME['node-spec']['header-style'] = props_to_dict(text=THEME['node-spec']['header-style'])

        # how many levels we have defined?
        levels_defined = []
        for level, level_data in THEME['node-spec']['row-styles'].items():
            levels_defined.append(level)
            THEME['node-spec']['row-styles'][level] = props_to_dict(text=level_data)

        # fixed node columns
        fixed_nodes = THEME['node-spec']['fixed-nodes']
        for column, column_data in fixed_nodes['columns'].items():
            if 'header-style' in column_data:
                column_data['header-style'] = {**THEME['node-spec']['header-style'], **props_to_dict(text=column_data['header-style'])}
            else:
                # TODO: warn
                column_data['header-style'] = THEME['node-spec']['header-style']

            if 'row-style' in column_data:
                column_data['row-style'] = {**THEME['node-spec']['header-style'], **props_to_dict(text=column_data['row-style'])}
            else:
                # TODO: warn
                column_data['row-style'] = THEME['node-spec']['header-style']

            if 'level-styles' in column_data:
                for level in levels_defined:
                    if level in column_data['level-styles']:
                        column_data['level-styles'][level] = {**column_data['row-style'], **THEME['node-spec']['row-styles'][level], **props_to_dict(text=column_data['level-styles'][level])}
                    else:
                        column_data['level-styles'][level] = {**column_data['row-style'], **THEME['node-spec']['row-styles'][level]}

            else:
                # TODO: warn
                column_data['level-styles'] = {}
                for level in levels_defined:
                    column_data['level-styles'][level] = {**column_data['row-style'], **THEME['node-spec']['row-styles'][level]}

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
                self._pool_scheme = False

        else:
            warn(f"[fixed-nodes][pool-spec] not defined in theme, disabling [pool-scheme]")
            self._pool_scheme = False



        # time nodes
        time_nodes = THEME['node-spec']['time-nodes']
        time_nodes['head-row']['style'] = {**THEME['node-spec']['header-style'], **props_to_dict(text=time_nodes['head-row']['style'])}
        if 'holiday-style' in time_nodes['head-row'] and time_nodes['head-row']['holiday-style'] is not None:
            time_nodes['head-row']['holiday-style'] = props_to_dict(text=time_nodes['head-row']['holiday-style'])
        else:
            time_nodes['head-row']['holiday-style'] = {}

        if 'collapsed-style' in time_nodes['head-row'] and time_nodes['head-row']['collapsed-style'] is not None:
            time_nodes['head-row']['collapsed-style'] = props_to_dict(text=time_nodes['head-row']['collapsed-style'])
        else:
            time_nodes['head-row']['collapsed-style'] = {}

        # time node has data-rows
        time_nodes['data-row']['base-style'] = props_to_dict(text=time_nodes['data-row']['base-style'])
        if 'holiday-style' in time_nodes['data-row'] and time_nodes['data-row']['holiday-style'] is not None:
            time_nodes['data-row']['holiday-style'] = props_to_dict(text=time_nodes['data-row']['holiday-style'])
        else:
            time_nodes['data-row']['holiday-style'] = {}

        if 'collapsed-style' in time_nodes['data-row'] and time_nodes['data-row']['collapsed-style'] is not None:
            time_nodes['data-row']['collapsed-style'] = props_to_dict(text=time_nodes['data-row']['collapsed-style'])
        else:
            time_nodes['data-row']['collapsed-style'] = {}

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
                self._pool_scheme = False

        else:
            warn(f"[time-nodes][pool-spec] not defined in theme, disabling [pool-scheme]")
            self._pool_scheme = False



    ''' parse the data
    '''
    def parse_data(self):
        global VIEW
        global START_DATE
        global CONSIDER_HOLIDAYS
    
        self._time_count = 0

        self._visible_pools = DATA.get('visible-pools', [])
        self._pool_scheme = DATA.get('pool-scheme', False)

        VIEW = DATA.get('view')
        CONSIDER_HOLIDAYS = DATA.get('consider-holidays', False)
        START_DATE = DATA.get('start-date', None)

        # get start date if any
        if START_DATE:
            try:
                START_DATE = date.fromisoformat(START_DATE) - timedelta(days=1)
                debug(f"[start-date] is [{START_DATE.strftime('%a, %b %d, %Y')}]")
            except:
                warn(f"[start-date] is invalid, ignoring ...")
                START_DATE = None
                CONSIDER_HOLIDAYS = False
        else:
            warn(f"[start-date] is missing, ignoring ...")
            CONSIDER_HOLIDAYS = False


        if CONSIDER_HOLIDAYS:
            if 'holiday-list' in DATA:
                if 'weekdays' not in DATA['holiday-list'] or not DATA['holiday-list']['weekdays']:
                    DATA['holiday-list']['weekdays'] = []

                else:
                    debug(f"found {DATA['holiday-list']['weekdays']} as holidays")

                if 'dates' not in DATA['holiday-list'] or not DATA['holiday-list']['dates']:
                    DATA['holiday-list']['dates'] = {}

                else:
                    debug(f"found {len(DATA['holiday-list']['dates'].keys())} listed holiday(s)")
                    for k, v in DATA['holiday-list']['dates'].items():
                        debug(f"  [{k}] [{v}]")

            else:
                warn("[holiday-list] is not defined, will not consider holidays ...")
                CONSIDER_HOLIDAYS = False


        if 'collapsed-ranges' in DATA:
            # we have spans, we need satrt and end
            for span_text in DATA['collapsed-ranges']:
                # a span is a pair of numbers (separated by -)
                pair = span_text.split('-')
                if len(pair) != 2:
                    warn(f"span [{span_text}] is invalid for [collapsed-ranges]")
                else:
                    strt, endt = int(pair[0]), int(pair[1])
                    # add each t to collapsed ranges where value is the node_id
                    for t in range(strt, endt + 1):
                        self._collapsed_ranges[str(t)] = {'strt': strt}

        # print(self._collapsed_ranges)


        for item_data in DATA['items']:
            item = Item(data=item_data, level=0)
            item.process()
            self._items.append(item)
            self._time_count = max(self._time_count, item._endt)
            # print(f"time-count [{self._time_count}], [{item._text}]")



    ''' generates the dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # parse the theme
        self.parse_theme()

        # parse the data
        self.parse_data()

        # graph attributes
        self._lines = append_content(lines=self._lines, content=make_property_lines(THEME['graph']['attributes']))
        self._lines = append_content(lines=self._lines, content='')

        # node properties
        self._lines = append_content(lines=self._lines, content=f"node [ {make_property_list(THEME['graph']['node'])}; ]")

        # edge properties
        self._lines = append_content(lines=self._lines, content=f"edge [ {make_property_list(THEME['graph']['edge'])}; ]")

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

        for k, v in THEME['node-spec']['fixed-nodes']['columns'].items():
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

            if VIEW == 'day' and START_DATE:
                short_weekday, mmm, dd, yyyy = long_date(day_number=t)
                label = THEME['node-spec']['time-nodes']['head-row']['label'].format(f"{mmm}\\n{dd}\\n'{yyyy}\\n{short_weekday}\\n{t}")
            else:
                label = THEME['node-spec']['time-nodes']['head-row']['label'].format(t)
            
            props = THEME['node-spec']['time-nodes']['head-row']['style']

            # this could be a holiday
            if is_holiday(day_number=t):
                props = {**props, **THEME['node-spec']['time-nodes']['head-row']['holiday-style']}

            nodes.append({'id': id, 'label': label, 'props': props, 'day-number': t})


        # TODO: process collapsed ranges
        props_collapsed = THEME['node-spec']['time-nodes']['head-row']['collapsed-style']
        for n in range(len(nodes) - 1, -1, -1):
            if nodes[n]:
                if 'day-number' in nodes[n]:
                    day_number = nodes[n]['day-number']
                    collapsed_node = self._collapsed_ranges.get(str(day_number), None)
                    if collapsed_node:
                        # this is in a collapsed node, only the first node to be appended
                        if day_number == collapsed_node['strt']:
                            nodes[n]['label'] = '...'
                            nodes[n]['props'] = {**nodes[n]['props'], **props_collapsed}

                        else:
                            nodes[n] = {}


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
        for k in THEME['node-spec']['fixed-nodes']['columns'].keys():
            column = THEME['node-spec']['fixed-nodes']['columns'][k]
            props = column['level-styles'][f"L{item._levl}"]
            id = f"_{self._current_row:03}_{k}"

            if k in item._item_data:
                label = props['label'].format(item._item_data[k])
            else:
                # the key was not found in data, we need an empty node
                label = ''

            # HACK: sime/strt/endt columns should not have unwanted values
            if k in ['time', 'strt', 'endt']:
                if int(label) <= MIN_TIME or int(label) >= MAX_TIME:
                    label = '-'

            nodes.append({'type': 'fixed-node', 'id': id, 'label': label, 'props': props})


        # if the item is not in visible-pools list, do not do anything
        if 'pool' in item._item_data:
            if self._visible_pools and len(self._visible_pools) > 0 and not item._item_data['pool'] in self._visible_pools:
                return

        time_node_strt = len(nodes)

        # the time nodes
        nodes.append({})
        for t in range(1, self._time_count + 1):
            id = f"_{self._current_row:03}_{t:02}"
            label = ''
            props = THEME['node-spec']['time-nodes']['data-row']['base-style']
            nodes.append({'type': 'time-node', 'id': id, 'label': label, 'props': props, 'day-number': t})


        # print(f"time-node start at [{time_node_strt}], number-time-nodes [{self._time_count}]")

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
                props = THEME['node-spec']['time-nodes']['data-row']['level-styles'][f"L{item._levl}"]['tail']
                tail_node['label'] = props['label'].format(span_strt)
                tail_node['props'] = props

                head_node = nodes[time_node_strt + span_endt]
                props = THEME['node-spec']['time-nodes']['data-row']['level-styles'][f"L{item._levl}"]['head']
                head_node['label'] = props['label'].format(span_endt)
                head_node['props'] = props

                for pos in range(span_strt+1, span_endt):
                    node = nodes[time_node_strt + pos]
                    props = THEME['node-spec']['time-nodes']['data-row']['level-styles'][f"L{item._levl}"]['edge']
                    node['label'] = ''
                    node['props'] = props


        # apply pool specific styles
        if self._pool_scheme:
            # we select a pool style based on pool and apply to each node props
            if 'pool' not in item._item_data or item._item_data['pool'] is None or item._item_data['pool'] == '':
                pool_props_fixed = THEME['node-spec']['fixed-nodes']['pool-spec']['empty-pool']
                pool_props_time = THEME['node-spec']['time-nodes']['pool-spec']['empty-pool']
            else:
                # find the index of the pool in POOL_LIST
                index = POOL_LIST.index(item._item_data['pool'])

                index_fixed = index % len(THEME['node-spec']['fixed-nodes']['pool-spec']['pool-styles'])
                pool_props_fixed = THEME['node-spec']['fixed-nodes']['pool-spec']['pool-styles'][index_fixed]

                index_time = index % len(THEME['node-spec']['time-nodes']['pool-spec']['pool-styles'])
                pool_props_time = THEME['node-spec']['time-nodes']['pool-spec']['pool-styles'][index_time]

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


        # apply holiday styles
        props_holiday = THEME['node-spec']['time-nodes']['data-row']['holiday-style']
        for node in nodes:
            if node:
                if node['type'] == 'time-node':
                    if is_holiday(day_number=node['day-number']):
                        node['props'] = {**node['props'], **props_holiday}


        # TODO: process collapsed ranges
        props_collapsed = THEME['node-spec']['time-nodes']['data-row']['collapsed-style']
        for n in range(len(nodes) - 1, -1, -1):
            if nodes[n]:
                if 'day-number' in nodes[n]:
                    day_number = nodes[n]['day-number']
                    collapsed_node = self._collapsed_ranges.get(str(day_number), None)
                    if collapsed_node:
                        # this is in a collapsed node, only the first node to be appended
                        if day_number == collapsed_node['strt']:
                            nodes[n]['label'] = '...'
                            nodes[n]['props'] = {**nodes[n]['props'], **props_collapsed}
                        else:
                            nodes[n] = {}


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
