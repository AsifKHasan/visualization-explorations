#!/usr/bin/env python3
'''
'''
# import pandas as pd
import pygsheets

from helper.logger import *
from helper.gsheet.gsheet_util import *


def process_gsheet(gsheet, worksheet_title):
    ws = gsheet.worksheet('title', worksheet_title)
    if not ws:
        error(f"no worksheet [{worksheet_title}]")
        return None

    items = ws.get_values(start='A3', end=f"L{ws.rows}", returnas='matrix', majdim='ROWS', include_tailing_empty=True, include_tailing_empty_rows=False, value_render='FORMULA')
    toc_list = [toc for toc in toc_list if toc[2] == 'Yes' and toc[3] in [0, 1, 2, 3, 4, 5, 6]]

    section_index = 0
    for toc in toc_list:
        data['sections'].append(process_section(context=context, gsheet=gsheet, toc=toc, current_document_index=current_document_index, section_index=section_index, parent=parent))
        section_index = section_index + 1

    return data
