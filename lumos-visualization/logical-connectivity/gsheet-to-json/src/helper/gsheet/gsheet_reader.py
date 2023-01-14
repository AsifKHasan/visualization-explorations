#!/usr/bin/env python3
'''
'''
import json
import pandas as pd
import pygsheets
from collections import defaultdict

from helper.logger import *

ws_data_spec = {
    'start-col': 'A', 'end-col': 'L', 'start-row': 2, 'numerize': False
}

def process_gsheet(gsheet, worksheet_name):
    ws = gsheet.worksheet('title', worksheet_name)
    if not ws:
        error(f"no worksheet [{worksheet_name}]")
        return None

    start = f"{ws_data_spec['start-col']}{ws_data_spec['start-row']}"
    end = f"{ws_data_spec['end-col']}{ws.rows}"

    df = ws.get_as_df(has_header=True, index_colum=None, empty_value=None, numerize=ws_data_spec['numerize'], start=start, end=end)
    
    # TODO: just store for now
    # df.to_pickle('../../out/nbr.pickle')
    grouped = df.groupby(['house', 'area', 'building', 'floor', 'room', 'rack', 'tag', 'name', 'make', 'model'])

    # levels = len(grouped.index.levels)
    # levels = 10
    # dicts = [{} for i in range(levels)]
    # last_index = None
    # for index, value in grouped:
    #     if not last_index:
    #         last_index = index

    #     for (ii,(i,j)) in enumerate(zip(index, last_index)):
    #         if not i == j:
    #             ii = levels - ii -1
    #             dicts[:ii] =  [{} for _ in dicts[:ii]]
    #             break

    #     for i, key in enumerate(reversed(index)):
    #         dicts[i][key] = value
    #         value = dicts[i]

    #     last_index = index

    # result = json.dumps(dicts[-1])

    # data = df.to_dict(orient='dict')

    result = dict_from_enumerable(grouped.groups, 'port', 'house', 'area', 'building', 'floor', 'room', 'rack', 'tag', 'name', 'make', 'model')

    return result


def dict_from_enumerable(enumerable, final_value, *groups):
    d = defaultdict(lambda: defaultdict(dict))
    group_count = len(groups)

    for item in enumerable:
        nested = d
        item_result = final_value(item) if callable(final_value) else item.get(final_value)
        for i, group in enumerate(groups, start=1):
            group_val = str(group(item) if callable(group) else item.get(group))

            if i == group_count:
                nested[group_val] = item_result
            else:
                nested = nested[group_val]

    return d
