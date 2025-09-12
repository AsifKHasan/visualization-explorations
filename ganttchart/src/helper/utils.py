#!/usr/bin/env python3

import re

from helper.logger import *

COLUMN_TO_LETTER = [
    '-', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
]

LETTER_TO_COLUMN = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,
    'AA': 27, 'AB': 28, 'AC': 29, 'AD': 30, 'AE': 31, 'AF': 32, 'AG': 33, 'AH': 34, 'AI': 35, 'AJ': 36, 'AK': 37, 'AL': 38, 'AM': 39, 'AN': 40, 'AO': 41, 'AP': 42, 'AQ': 43, 'AR': 44, 'AS': 45, 'AT': 46, 'AU': 47, 'AV': 48, 'AW': 49, 'AX': 50, 'AY': 51, 'AZ': 52,
}


''' get height and width of a list of list
'''
def matrix_dimension(matrix):
    height, width = None, None
    if isinstance(matrix, list):
        height = len(matrix)
        if all(isinstance(el, list) for el in matrix):
            width = len(matrix[0])
        else:
            width = 1

    return height, width



''' addSheetRequest builder
'''
def build_add_worksheet_request(worksheet_name, sheet_index, num_rows, num_cols, frozen_rows, frozen_cols):
    return {
        'addSheet': {
            'properties': {
                'title': worksheet_name,
                'index': sheet_index,
                'gridProperties': {
                    'rowCount': num_rows,
                    'columnCount': num_cols,
                    'frozenRowCount': frozen_rows,
                    'frozenColumnCount': frozen_cols,
                },
            }
        }
    }



''' build a repeatCell from work_spec
'''
def build_repeatcell_from_work_spec(range, work_spec, gsheet):
    fields = []

    # textFormatRuns/values
    text_format_runs = []
    formatted_value = ''
    if 'values' in work_spec:
        start_index = 0
        for value in work_spec['values']:
            # buld the text
            if value['text'].startswith('='):
                resolved_values = gsheet.get_range_values(value['text'][1:])
                resolved_value = resolved_values['values'][0][0]
                # print(resolved_values)
            else:
                resolved_value = value['text']

            formatted_value = f"{formatted_value}{resolved_value}"

            # TextFormat
            text_format = value['format']


            # fgcolor
            fg_color = None
            if 'fgcolor' in text_format:
                fg_color = text_format['fgcolor']
                fields.append('textFormatRuns.format.foregroundColor')


            # font-family
            font_family = None
            if 'font-family' in text_format:
                font_family = text_format['font-family']
                fields.append('textFormatRuns.format.fontFamily')


            # font-size
            font_size = None
            if 'font-size' in text_format:
                font_size = text_format['font-size']
                fields.append('textFormatRuns.format.fontSize')


            # bold
            bold = False
            if 'bold' in text_format:
                bold = text_format['bold']
                fields.append('textFormatRuns.format.bold')


            # italic
            italic = False
            if 'italic' in text_format:
                italic = text_format['italic']
                fields.append('textFormatRuns.format.italic')


            # strikethrough
            strikethrough = False
            if 'strikethrough' in text_format:
                strikethrough = text_format['strikethrough']
                fields.append('textFormatRuns.format.strikethrough')


            # underline
            underline = False
            if 'underline' in text_format:
                underline = text_format['underline']
                fields.append('textFormatRuns.format.underline')

            # build the text_format_run
            text_format_run = {
                'startIndex': start_index,
                'format' : {
                    'foregroundColor': None if fg_color is None else hex_to_rgba(fg_color),
                    'fontFamily': font_family,
                    'fontSize': font_size,
                    'bold': bold,
                    'italic': italic,
                    'strikethrough': strikethrough,
                    'underline': underline,
                }
            }

            # update start_index
            start_index = len(formatted_value)

            # append the text_format_run into the list
            text_format_runs.append(text_format_run)

        # update fields
        fields.append('userEnteredValue.stringValue')
        fields.append('textFormatRuns')


    # valign
    valign = None
    if 'valign' in work_spec:
        valign = work_spec['valign']
        fields.append('userEnteredFormat.verticalAlignment')


    # halign
    halign = None
    if 'halign' in work_spec:
        halign = work_spec['halign']
        fields.append('userEnteredFormat.horizontalAlignment')


    # wrap
    wrap_strategy = None
    if 'wrap' in work_spec:
        if work_spec['wrap'] == True:
            wrap_strategy = 'WRAP'
        else:
            wrap_strategy = 'CLIP'

        fields.append('userEnteredFormat.wrapStrategy')


    number_format = None
    # number-format
    if 'number-format' in work_spec:
        number_format = {'type': 'NUMBER', 'pattern': work_spec['number-format']}
        fields.append('userEnteredFormat.numberFormat')


    # date-format
    if 'date-format' in work_spec:
        number_format = {'type': 'DATE', 'pattern': work_spec['date-format']}
        fields.append('userEnteredFormat.numberFormat')


    # bgcolor
    bg_color = None
    if 'bgcolor' in work_spec:
        bg_color = work_spec['bgcolor']
        fields.append('userEnteredFormat.backgroundColor')


    # fgcolor
    fg_color = None
    if 'fgcolor' in work_spec:
        fg_color = work_spec['fgcolor']
        fields.append('userEnteredFormat.textFormat.foregroundColor')


    # font-family
    font_family = None
    if 'font-family' in work_spec:
        font_family = work_spec['font-family']
        fields.append('userEnteredFormat.textFormat.fontFamily')


    # font-size
    font_size = None
    if 'font-size' in work_spec:
        font_size = work_spec['font-size']
        fields.append('userEnteredFormat.textFormat.fontSize')


    # bold
    bold = False
    if 'bold' in work_spec:
        bold = work_spec['bold']
        fields.append('userEnteredFormat.textFormat.bold')


    # italic
    italic = False
    if 'italic' in work_spec:
        italic = work_spec['italic']
        fields.append('userEnteredFormat.textFormat.italic')


    # strikethrough
    strikethrough = False
    if 'strikethrough' in work_spec:
        strikethrough = work_spec['strikethrough']
        fields.append('userEnteredFormat.textFormat.strikethrough')


    # underline
    underline = False
    if 'underline' in work_spec:
        underline = work_spec['underline']
        fields.append('userEnteredFormat.textFormat.underline')


    # note
    note = None
    if 'note' in work_spec:
        note = work_spec['note']
        fields.append('note')



    if len(fields) == 0:
        return None

    return {
      'repeatCell': {
        'range': range,
        'cell': {
            'userEnteredValue': {'stringValue': formatted_value},
            'userEnteredFormat': {
                'verticalAlignment': valign,
                'horizontalAlignment': halign,
                'wrapStrategy': wrap_strategy,
                'numberFormat': number_format,
                'backgroundColor': None if bg_color is None else hex_to_rgba(bg_color),
                'textFormat': {
                    'foregroundColor': None if fg_color is None else hex_to_rgba(fg_color),
                    'fontFamily': font_family,
                    'fontSize': font_size,
                    'bold': bold,
                    'italic': italic,
                    'strikethrough': strikethrough,
                    'underline': underline,
                },
            },
            'textFormatRuns': text_format_runs,
            'note': note,
        },
        'fields': ','.join(fields)
      }
    }



''' appendDimensionRequest builder
'''
def build_append_dimension_request(worksheet_id, dimension, length, inherit_from_before):
    return {'appendDimension': {'sheetId': worksheet_id, 'dimension': dimension, 'length': length}}



''' insertDimensionRequest builder
'''
def build_insert_dimension_request(worksheet_id, dimension, start_index, length, inherit_from_before):
    range = {'sheetId': worksheet_id, 'dimension': dimension, 'startIndex': start_index, 'endIndex': start_index + length}
    return {'insertDimension': {'range': range, 'inheritFromBefore': inherit_from_before}}



''' deleteDimensionRequest builder
'''
def build_delete_dimension_request(worksheet_id, dimension, start_index, end_index=None):
    range = {'sheetId': worksheet_id, 'dimension': dimension, 'startIndex': start_index}
    if end_index:
        range['endIndex'] = end_index

    return {'deleteDimension': {'range': range}}



''' gsheet border spec for border around a range
'''
def build_duplicate_sheet_request(worksheet_id, new_worksheet_name, new_worksheet_index=None):
    request_body = {
        "duplicateSheet": {
            "sourceSheetId": worksheet_id,
            "newSheetName": new_worksheet_name
        }
    }

    if new_worksheet_index:
        request_body['duplicateSheet'][insertSheetIndex] = new_worksheet_index

    return request_body



''' find and replace request builder
'''
def build_find_replace_request(worksheet_id, search_for, replace_with, regex=False, include_formulas=False, entire_cell=False):
    return {
        "findReplace": {
            "find": search_for,
            "replacement": replace_with,
            "matchCase": True,
            "matchEntireCell": entire_cell,
            "searchByRegex": regex,
            "includeFormulas": include_formulas,
            "sheetId": worksheet_id,
        }
    }



''' gsheet border spec for border around a range
'''
def build_border_around_spec(border_list, border_color, border_style='SOLID', inner_border=True):
    color = hex_to_rgba(border_color)
    border = {
        "style": border_style,
        "colorStyle": {
            "rgbColor": color
        }
    }

    borders = {
        "innerHorizontal": border if inner_border else None,
        "innerVertical": border if inner_border else None,
    }

    for side in border_list:
        borders[side] = border

    return borders



''' build a boolean conditional format rule
    ranges is a list
    condition_type is enum (https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#ConditionType)
    condition_values is a list of strings
    format is a dict
'''
def build_conditional_format_rule(ranges, condition_type, condition_values, format):
    rule = {"addConditionalFormatRule": {
                "rule": {
                    "ranges" : ranges,
                    "booleanRule": {
                        "condition": {
                            "type": condition_type,
                            "values": [{"userEnteredValue": v} for v in condition_values]
                        },
                        "format": format
                    }
                },
                "index": 0
            }
        }

    return rule



''' build format string from conditional-format format object
    format is a dict which needs to be manipulated
    backgroundColor -> hex_to_rgba(backgroundColor)
'''
def conditional_format_from_object(format):
    new_format = {}
    if 'backgroundColor' in format:
        new_format['backgroundColor'] = hex_to_rgba(format['backgroundColor'])

    return new_format



''' build a data validation rule
    condition_values is a list of strings
'''
def build_data_validation_rule(range, condition_type, condition_values, input_message=None):
    values = [{'userEnteredValue': v} for v in condition_values]
    rule = {"setDataValidation": {
                "range" : range,
                "rule": {
                    "condition": {
                        "type": condition_type,
                        "values": values,
                    },
                    "inputMessage": input_message,
                    "strict": True,
                    "showCustomUi": True
                }
            }
        }

    return rule



''' build a no data validation rule
'''
def build_no_data_validation_rule(range):
    rule = {"setDataValidation": {
                "range" : range,
                "rule": None
            }
        }

    return rule



''' gets the value from workspec
'''
def build_value_from_work_spec(work_spec, worksheets_dict={}, google_service=None):
    value = ''
    if 'value' in work_spec:
        value = work_spec['value']

    if value != '':
        # it may be hyperlink to another worksheet
        if 'ws-name-to-link' in work_spec:
            # is it a valid worksheet
            if work_spec['ws-name-to-link'] in worksheets_dict:
                value = f'=HYPERLINK("#gid={worksheets_dict[work_spec["ws-name-to-link"]]}", "{value}")'.lstrip("'")
            else:
                error(f".... No Worksheet named {work_spec['ws-name-to-link']}")

        # it may be hyperlink to another drive file
        elif 'file-name-to-link' in work_spec:
            # we need the id of the drive file
            drive_file = google_service.get_drive_file(drive_file_name=work_spec['file-name-to-link'])
            if drive_file:
                # print(drive_file)
                value = f'=HYPERLINK("{drive_file["webViewLink"]}", "{value}")'.lstrip("'")
            else:
                error(f".... No Drive File named {work_spec['file-name-to-link']}")

    return value



''' build dimension autosize request
    note: index is 0 based
'''
def build_dimension_autosize_request(sheet_id, dimension, start_index, end_index):
    range_spec = {
        "sheetId": sheet_id,
        "dimension": dimension,
        "startIndex": start_index - 1,
        "endIndex": end_index
    }

    dimension_autosize_request = {
      "autoResizeDimensions": {
        "dimensions": range_spec,
      },
    }

    return dimension_autosize_request



''' build dimension size update request
    note: index is 0 based
'''
def build_dimension_size_update_request(sheet_id, dimension, index, size):
    range_spec = {
        "sheetId": sheet_id,
        "dimension": dimension,
        "startIndex": index - 1,
        "endIndex": index
    }

    update_dimension_properties = {
      "updateDimensionProperties": {
        "range": range_spec,
        "properties": {
          "pixelSize": size
        },
        "fields": "pixelSize"
      }
    }

    return update_dimension_properties



''' build dimension visibility update request
    note: index is 0 based
'''
def build_dimension_visibility_update_request(sheet_id, dimension, start_index, end_index, hide):
    range_spec = {
        "sheetId": sheet_id,
        "dimension": dimension,
        "startIndex": start_index,
        "endIndex": end_index
    }

    update_dimension_properties = {
      "updateDimensionProperties": {
        "range": range_spec,
        "properties": {
          "hiddenByUser": hide
        },
        "fields": "hiddenByUser"
      }
    }

    return update_dimension_properties



''' build sheet property update request for frozen rows
'''
def build_row_freeze_request(sheet_id, frozen_rows):
    update_sheet_properties = {
      "updateSheetProperties": {
        "properties": {
          "sheetId": sheet_id,
          "gridProperties": {
            "frozenRowCount": frozen_rows,
          }
        },
        "fields": "gridProperties.frozenRowCount"
      }
    }

    return update_sheet_properties



''' build sheet property update request for frozen columns
'''
def build_column_freeze_request(sheet_id, frozen_cols):
    update_sheet_properties = {
      "updateSheetProperties": {
        "properties": {
          "sheetId": sheet_id,
          "gridProperties": {
            "frozenColumnCount": frozen_cols,
          }
        },
        "fields": "gridProperties.frozenColumnCount"
      }
    }

    return update_sheet_properties



''' column number to letter
'''
def column_to_letter(col_num):
    return COLUMN_TO_LETTER[col_num]



''' split text into lines and remove spaces and any special character from the begining
'''
def split_and_dress(value):
    lines = value.split('\n')
    regex = r'^[-\s•]+'
    lines = [re.sub(regex, '', s) for s in lines]
    regex = r'[\s]+$'
    lines = [re.sub(regex, '', s) for s in lines]

    return lines



''' hex string to RGB color tuple
'''
def hex_to_color(hex):
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))



''' hex string to RGBA
'''
def hex_to_rgba(hex):
    h = hex.lstrip('#')
    if len(h) == 6:
        h = h + '00'

    color = tuple(int(h[i:i+2], 16) for i in (0, 2, 4, 6))
    return {"red": color[0]/255, "green": color[1]/255, "blue": color[2]/255, "alpha": color[3]/255}
