#!/usr/bin/env python3
'''
'''
import pandas as pd
import pygsheets

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
    print(df)
    data = df.to_dict(orient='dict')

    return data
