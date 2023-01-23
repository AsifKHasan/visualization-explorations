#!/usr/bin/env python3
'''
'''
import json
import pandas as pd
import pygsheets
from collections import defaultdict

from helper.logger import *

ws_data_spec = {
    'start-col': 'A', 'end-col': 'N', 'start-row': 2, 'numerize': False
}

def process_gsheet(gsheet, worksheet_name):
    ws = gsheet.worksheet('title', worksheet_name)
    if not ws:
        error(f"no worksheet [{worksheet_name}]")
        return None

    start = f"{ws_data_spec['start-col']}{ws_data_spec['start-row']}"
    end = f"{ws_data_spec['end-col']}{ws.rows}"

    df = ws.get_as_df(has_header=True, index_colum=None, empty_value=None, numerize=ws_data_spec['numerize'], start=start, end=end)
    df.dropna(inplace=True)
    df = df.query('include == "Yes"')
    df = df.drop(['include'], axis=1)
    
    # TODO: just store for now
    # df.to_pickle('../../out/nbr.pickle')

    d = defaultdict(dict)
    for i, row in df.iterrows():
        if not row.house in d:
            d[row.house] = {}

        if not row.area in d[row.house]:
            d[row.house][row.area] = {}

        if not row.building in d[row.house][row.area]:
            d[row.house][row.area][row.building] = {}

        if not row.floor in d[row.house][row.area][row.building]:
            d[row.house][row.area][row.building][row.floor] = {}

        if not row.room in d[row.house][row.area][row.building][row.floor]:
            d[row.house][row.area][row.building][row.floor][row.room] = {}

        if not row.rack in d[row.house][row.area][row.building][row.floor][row.room]:
            d[row.house][row.area][row.building][row.floor][row.room][row.rack] = {}
        
        if not row.tag in d[row.house][row.area][row.building][row.floor][row.room][row.rack]:
            d[row.house][row.area][row.building][row.floor][row.room][row.rack][row.tag] = {'name': row['name'], 'type': row.type, 'make': row.make, 'model': row.model, 'ports': []}
        
        d[row.house][row.area][row.building][row.floor][row.room][row.rack][row.tag]['ports'].append(row.drop(['house', 'area', 'building', 'floor', 'room', 'rack', 'tag', 'name', 'type', 'make', 'model']).to_dict())

        # print(i, row.house)

    return dict(d)

