#!/usr/bin/env python3

import gspread
from gspread.utils import *
from gspread.exceptions import *
from gspread_formatting import *

from helper.utils import *
from helper.logger import *
from pprint import pprint


''' Google worksheet wrapper
'''
class GoogleWorksheet(object):

    ''' constructor
    '''
    def __init__(self, google_service, gspread_worksheet, gsheet):
        self.service = google_service
        self.gspread_worksheet = gspread_worksheet
        self.gsheet = gsheet
        self.id = self.gspread_worksheet.id
        self.title = self.gspread_worksheet.title



    ''' get values for a column - column in A1 notation
    '''
    def get_col_values(self, col_a1):
        return self.gspread_worksheet.col_values(LETTER_TO_COLUMN[col_a1])



    ''' get values for a row - row starts with 1
    '''
    def get_row_values(self, row_num):
        return self.gspread_worksheet.row_values(row_num)



    ''' get values in batch
    '''
    def get_values_in_batch(self, ranges, major_dimension='ROWS', try_for=3):
        wait_for = 30
        for try_count in range(1, try_for+1):
            try:
                values = self.gspread_worksheet.batch_get(ranges, major_dimension=major_dimension, value_render_option=ValueRenderOption.formatted)
                # debug(f"get values in batch passed in [{try_count}] try", nesting_level=1)
                return values

            except Exception as e:
                print(e)
                if try_count < try_for:
                    warn(f"get values in batch failed in [{try_count}] try, trying again in {wait_for} seconds", nesting_level=1)
                    time.sleep(wait_for)
                else:
                    warn(f"get values in batch failed in [{try_count}] try", nesting_level=1)

        return None



    ''' get values from a1 notation
        get_values_in_batch is preferred
    '''
    def get_values(self, range_spec, try_for=3):
        wait_for = 30
        for try_count in range(1, try_for+1):
            try:
                values = self.gspread_worksheet.get_values(range_spec, value_render_option='ValueRenderOption.formatted')
                # debug(f"get values passed in [{try_count}] try", nesting_level=1)
                return values
            except Exception as e:
                print(e)
                if try_count < try_for:
                    warn(f"get values failed in [{try_count}] try, trying again in {wait_for} seconds", nesting_level=1)
                    time.sleep(wait_for)
                else:
                    warn(f"get values failed in [{try_count}] try", nesting_level=1)

        return None



    ''' get a range from a1 notation
    '''
    def get_range(self, range_spec, try_for=3):
        wait_for = 30
        for try_count in range(1, try_for+1):
            try:
                ws_range = self.gspread_worksheet.range(range_spec)
                # debug(f"get range passed in [{try_count}] try", nesting_level=1)
                return ws_range
            except Exception as e:
                print(e)
                if try_count < try_for:
                    warn(f"get range failed in [{try_count}] try, trying again in {wait_for} seconds", nesting_level=1)
                    time.sleep(wait_for)
                else:
                    warn(f"get range failed in [{try_count}] try", nesting_level=1)

        return None



    ''' copy worksheet to another gsheet
    '''
    def copy_worksheet_to_gsheet(self, destination_gsheet):
        try:
            info(f"copying worksheet        {self.title} to {destination_gsheet.title}")
            response = self.gspread_worksheet.copy_to(destination_gsheet.id)
            # rename the newly copied worksheet
            if response:
                info(f"copied  worksheet        {self.title} to {destination_gsheet.title}")

                try:
                    new_gspread_worksheet = destination_gsheet.gspread_sheet.worksheet(response['title'])
                    info(f"renaming worksheet [{response['title']}] to [{self.title}]")
                    new_gspread_worksheet.update_title(self.title)
                    new_gspread_worksheet.title = self.title
                    info(f"renamed  worksheet [{response['title']}] to [{self.title}]")

                except:
                    error(f"worksheet          [{response['title']}] could not be renamed to [{self.title}]")

        except:
            error(f"could not copy worksheet {self.title} to {destination_gsheet.title}")



    ''' rename a worksheet
    '''
    def rename_worksheet(self, new_worksheet_name):
        old_worksheet_name = self.title
        try:
            info(f"renaming worksheet [{old_worksheet_name}] to [{new_worksheet_name}]")
            self.gspread_worksheet.update_title(new_worksheet_name)
            self.title = new_worksheet_name
            info(f"renamed  worksheet [{old_worksheet_name}] to [{new_worksheet_name}]")

        except:
            error(f"worksheet [{old_worksheet_name}] could not be renamed to [{new_worksheet_name}]")



    ''' get start_index of trailing blank rows from the worksheet
    '''
    def trailing_blank_row_start_index(self):
        # we first need to know what is the last row having some value
        values = self.gspread_worksheet.get_values()
        return len(values)



    ''' number of rows and columns of the worksheet
    '''
    def number_of_dimesnions(self):
        return self.gspread_worksheet.row_count, self.gspread_worksheet.col_count



    ''' number of rows of the worksheet
    '''
    def row_count(self):
        row_count, _ = self.number_of_dimesnions()
        return row_count



    ''' number of columns of the worksheet
    '''
    def col_count(self):
        _, col_count = self.number_of_dimesnions()
        return col_count




    ''' worksheet methods to be called by gsheet to return back requests, not doing the actual work
    '''

    ''' bulk create multiple worksheets by duplicating this worksheet request
    '''
    def duplicate_worksheet_requests(self, new_worksheet_names):
        request_list = []
        for worksheet_name in new_worksheet_names:
            info(f"duplicating worksheet {self.title} as {worksheet_name}")
            request_list.append(build_duplicate_sheet_request(worksheet_id=self.id, new_worksheet_name=worksheet_name))

        return request_list



    ''' remove extra columns request
    '''
    def remove_extra_columns_requests(self, cols_to_remove_from, cols_to_remove_to):
        request_list = self.dimension_remove_requests(cols_to_remove_from=cols_to_remove_from, cols_to_remove_to=cols_to_remove_to)
        info(f"columns(s) {cols_to_remove_from}-{cols_to_remove_to} to be removed", nesting_level=1)
        return request_list



    ''' remove trailing blank rows request
    '''
    def remove_trailing_blank_rows_requests(self):
        rows_to_remove_from, rows_to_remove_to = self.trailing_blank_row_start_index(), 'end'
        request_list = self.dimension_remove_requests(rows_to_remove_from=rows_to_remove_from, rows_to_remove_to=rows_to_remove_to)
        info(f"rows {rows_to_remove_from}-{rows_to_remove_to} to be removed", nesting_level=1)
        return request_list



    ''' dimensions add request
    '''
    def dimension_add_requests(self, cols_to_add_at=None, cols_to_add=0, rows_to_add_at=None, rows_to_add=0):
        requests = []
        if cols_to_add_at and cols_to_add:
            # columns to be added
            if cols_to_add_at == 'end':
                # columns to be appended at the end
                requests.append(build_append_dimension_request(worksheet_id=self.id, dimension='COLUMNS', length=cols_to_add, inherit_from_before=False))

            else:
                # columns to be inserted at some index
                start_index = LETTER_TO_COLUMN[cols_to_add_at]-1
                requests.append(build_insert_dimension_request(worksheet_id=self.id, dimension='COLUMNS', start_index=start_index, length=cols_to_add, inherit_from_before=False))

        if rows_to_add_at and rows_to_add:
            # rows to be added
            if rows_to_add_at == 'end':
                # rows to be appended at the end
                requests.append(build_append_dimension_request(worksheet_id=self.id, dimension='ROWS', length=rows_to_add, inherit_from_before=False))

            else:
                # rows to be inserted at some index
                requests.append(build_insert_dimension_request(worksheet_id=self.id, dimension='ROWS', start_index=rows_to_add_at, length=rows_to_add, inherit_from_before=False))

        return requests



    ''' dimensions remove request
    '''
    def dimension_remove_requests(self, cols_to_remove_from=None, cols_to_remove_to=None, rows_to_remove_from=None, rows_to_remove_to=None):
        requests = []
        if cols_to_remove_from and cols_to_remove_to:
            # columns to be removed
            if cols_to_remove_to == 'end':
                # columns to be removed till end
                requests.append(build_delete_dimension_request(worksheet_id=self.id, dimension='COLUMNS', start_index=LETTER_TO_COLUMN[cols_to_remove_from]-1))

            else:
                # columns to be removed from the middle
                requests.append(build_delete_dimension_request(worksheet_id=self.id, dimension='COLUMNS', start_index=LETTER_TO_COLUMN[cols_to_remove_from]-1, end_index=LETTER_TO_COLUMN[cols_to_remove_to]))

        if rows_to_remove_from and rows_to_remove_to:
            # rows to be removed
            if rows_to_remove_to == 'end':
                # rows to be removed till end
                requests.append(build_delete_dimension_request(worksheet_id=self.id, dimension='ROWS', start_index=rows_to_remove_from))

            else:
                # rows to be removed from the middle
                requests.append(build_delete_dimension_request(worksheet_id=self.id, dimension='ROWS', start_index=rows_to_remove_from, end_index=rows_to_remove_to))

        return requests



    ''' link cells of a worksheet to drive-file/worksheet based type request
        type is valid only if the range has two columns
        if the range has only one column default to worksheet link
    '''
    def cell_link_based_on_type_requests(self, range_specs_for_cells_to_link, worksheets_dict):
        nesting_level = 2
        range_work_specs = {}
        for range_spec in range_specs_for_cells_to_link:
            grid_range_spec = a1_range_to_grid_range(range_spec)
            range_start_col, range_start_row, range_end_col = grid_range_spec['startColumnIndex']+1, grid_range_spec['startRowIndex']+1, grid_range_spec['endColumnIndex']+1
            values = self.get_values_in_batch(ranges=[range_spec])[0]
            num_columns = range_end_col - range_start_col
            r = 0
            for row_value in values:
                # make sure the row has num_columns elements, if not extend with empty string elements
                if len(row_value) < num_columns:
                    row_value.extend([''] * (num_columns - len(row_value)))

                # print(row_value)

                if len(row_value) == 1:
                    # no type defined, it is a worksheet link
                    cell_value = row_value[0]
                    cell_address = rowcol_to_a1(row=range_start_row+r, col=range_start_col)
                    if cell_value == '':
                        warn(f"cell [{cell_address:>5}] is empty .. skipping", nesting_level=nesting_level)
                    else:
                        info(f"cell [{cell_address:>5}] to be linked with worksheet [{cell_value}]", nesting_level=nesting_level)
                        range_work_specs[cell_address] = {'value': cell_value, 'ws-name-to-link': cell_value}

                elif len(row_value) > 1:
                    type_value, cell_value = row_value[0], row_value[1]
                    type_cell_address = rowcol_to_a1(row=range_start_row+r, col=range_start_col)
                    cell_address = rowcol_to_a1(row=range_start_row+r, col=range_start_col+1)

                    if type_value in ['gsheet', 'pdf']:
                        # it is a drive-file link
                        debug(f"type [{type_cell_address:>5}] is [{type_value}] .. link to drive file", nesting_level=nesting_level)
                        if cell_value == '':
                            warn(f"cell [{cell_address:>5}] is empty .. skipping", nesting_level=nesting_level)
                        else:
                            info(f"cell [{cell_address:>5}] to be linked with drive file [{cell_value}]", nesting_level=nesting_level)
                            range_work_specs[cell_address] = {'value': cell_value, 'file-name-to-link': cell_value}

                    elif type_value == 'table':
                        # it is a worksheet link
                        debug(f"type [{type_cell_address:>5}] is [{type_value}] .. link to worksheet", nesting_level=nesting_level)
                        if cell_value == '':
                            warn(f"cell [{cell_address:>5}] is empty .. skipping", nesting_level=nesting_level)
                        else:
                            info(f"cell [{cell_address:>5}] to be linked with worksheet [{cell_value}]", nesting_level=nesting_level)
                            range_work_specs[cell_address] = {'value': cell_value, 'ws-name-to-link': cell_value}

                    elif type_value == '':
                        warn(f"type [{cell_address:>5}] is empty .. skipping", nesting_level=nesting_level)

                    else:
                        warn(f"type [{type_cell_address:>5}] is [{type_value}] .. skipping", nesting_level=nesting_level)

                else:
                    debug(f"row  [{range_start_row+r:>5}] is empty .. skipping", nesting_level=nesting_level)

                r = r + 1

        return self.range_work_requests(range_work_specs=range_work_specs, worksheets_dict=worksheets_dict)



    ''' link cells to drive files request where cells values are names of drive files request
    '''
    def cell_to_drive_file_link_requests(self, range_specs_for_cells_to_link):
        range_work_specs = {}
        for range_spec in range_specs_for_cells_to_link:
            range_to_work_on = self.get_range(range_spec=range_spec)
            for cell in range_to_work_on:
                if cell.value == '':
                    warn(f"cell {cell.address:>5} is empty .. skipping")
                else:
                    info(f"cell {cell.address:>5} to be linked with drive file [{cell.value}]")
                    range_work_specs[cell.address] = {'value': cell.value, 'file-name-to-link': cell.value}

        return self.range_work_requests(range_work_specs=range_work_specs)



    ''' link cells to worksheets request where cells values are names of worksheets
    '''
    def cell_to_worksheet_link_requests(self, range_specs_for_cells_to_link, worksheets_dict={}):
        range_work_specs = {}
        for range_spec in range_specs_for_cells_to_link:
            range_to_work_on = self.get_range(range_spec=range_spec)
            for cell in range_to_work_on:
                if cell.value == '':
                    warn(f"cell {cell.address:>5} is empty .. skipping")
                else:
                    info(f"cell {cell.address:>5} to be linked with worksheet [{cell.value}]")
                    range_work_specs[cell.address] = {'value': cell.value, 'ws-name-to-link': cell.value}

        return self.range_work_requests(range_work_specs=range_work_specs, worksheets_dict=worksheets_dict)



    ''' format a worksheet according to spec defined in worksheet_def
    '''
    def format_worksheet_requests(self, worksheet_def, worksheets_dict):
        # work on the columns - size, alignemnts, fonts and wrapping
        range_work_specs = {}

        #  freeze rows and columns
        frozen_rows, frozen_columns = worksheet_def.get('frozen-rows', 0), worksheet_def.get('frozen-columns', 0)
        dimension_freeze_requests = self.dimension_freeze_requests(frozen_rows=frozen_rows, frozen_cols=frozen_columns)

        num_rows = self.row_count()

        # all rows to default-row-size if present
        row_defaultsize_requests = []
        if 'default-row-size' in worksheet_def:
            default_row_size = worksheet_def['default-row-size']
            default_size_work_requests = {}
            for r in range(1, num_rows+1):
                default_size_work_requests[str(r)] = {"size": default_row_size}

            row_defaultsize_requests = self.row_resize_requests(row_specs=default_size_work_requests)


        # autosize rows only if autosize-rows is true
        autosize_rows = worksheet_def.get('autosize-rows', False)
        row_autosize_requests = []
        if autosize_rows:
            row_autosize_request = self.row_autosize_request(start_index=1, end_index=num_rows)
            row_autosize_requests.append(row_autosize_request)

        if 'rows' in worksheet_def:
            # requests for row resizing
            row_resize_requests = self.row_resize_requests(row_specs=worksheet_def['rows'])

        else:
            row_resize_requests = []

        data_validation_requests = []
        if 'columns' in worksheet_def:
            # requests for column resizing
            column_resize_requests = self.column_resize_requests(column_specs=worksheet_def['columns'])

            #  requests for column formatting
            for col_a1, work_spec in worksheet_def['columns'].items():
                range_spec = f"{col_a1}:{col_a1}"
                range_work_specs[range_spec] = work_spec

                # set validation rules
                range_spec = f"{col_a1}3:{col_a1}"
                data_validation_requests = data_validation_requests + self.data_validation_clear_requests(range_spec)
                if ('validation-list' in work_spec):
                    data_validation_requests = data_validation_requests + self.data_validation_from_list_requests(range_spec, work_spec['validation-list'])

            values, column_format_requests = self.range_work_requests(range_work_specs=range_work_specs)

        else:
            column_resize_requests, values, column_format_requests = [], [], []

        # get the ranges and formatting requests
        if 'ranges' in worksheet_def:
            values, range_format_requests = self.range_work_requests(range_work_specs=worksheet_def['ranges'], worksheets_dict=worksheets_dict)
        else:
            values, range_format_requests = [], []

        # conditional formatting for blank cells
        if 'cell-empty-markers' in worksheet_def:
            conditional_format_requests = self.conditional_formatting_for_blank_cells_requests(range_specs=worksheet_def['cell-empty-markers'])
        else:
            conditional_format_requests = []

        # will there be review-notes in the worksheet
        if 'review-notes' in worksheet_def:
            if worksheet_def['review-notes']:
                num_cols = worksheet_def.get('num-columns', 26)
                review_notes_format_requests = self.conditional_formatting_for_review_notes_requests(num_cols=num_cols)
            else:
                review_notes_format_requests = []

        else:
            review_notes_format_requests = []

        # merge formats
        requests = dimension_freeze_requests + row_defaultsize_requests + row_autosize_requests + row_resize_requests + column_resize_requests + column_format_requests + data_validation_requests + range_format_requests + conditional_format_requests + review_notes_format_requests

        return values, requests



    ''' find and replace in worksheet
    '''
    def find_and_replace_requests(self, find_replace_patterns):
        find_replace_requests = []
        for pattern in find_replace_patterns:
            search_for = pattern['find']
            replace_with = pattern['replace-with']
            regex = pattern.get('regex', False)
            include_formulas = pattern.get('include-formulas', False)
            entire_cell = pattern.get('entire-cell', False)
            request = build_find_replace_request(worksheet_id=self.id, search_for=search_for, replace_with=replace_with, regex=regex, include_formulas=include_formulas, entire_cell=entire_cell)
            if request:
                find_replace_requests.append(request)

        return find_replace_requests



    ''' resize columns with the size mentioned in pixel number in row 1 for that column
    '''
    def resize_columns_from_values_in_row_requests(self, row_to_consult):
        values = []
        requests = []
        column_specs = {}

        # get the full row values
        row_values = self.get_row_values(row_num=row_to_consult)
        col_num = 1
        for row_value in row_values:
            col_a1 = COLUMN_TO_LETTER[col_num]
            if row_value.isnumeric():
                col_size = int(row_value)
                # print(f"[{self.title}] column [{col_a1}] will be resized to [{col_size}]")
                column_specs[col_a1] = {'size': col_size}

            else:
                # print(f"[{self.title}] column [{col_a1}] has a non-int value [{row_value}] will not be resized")
                pass

            col_num = col_num + 1
            requests = requests + self.column_resize_requests(column_specs=column_specs)

        return values, requests



    ''' put column size in pixels in row 1 for all columns except A
    '''
    def column_pixels_in_top_row_requests(self, column_sizes, row_to_update):
        # for coumns B to end
        range_work_specs = {}
        values = []
        requests = []

        for col_num in range(1, self.col_count()):
            cell_a1 = f"{column_to_letter(col_num + 1)}{row_to_update}"
            column_width = column_sizes[self.title][col_num]
            range_work_specs[cell_a1] = {'value': column_width, 'halign': 'center'}

        return self.range_work_requests(range_work_specs=range_work_specs, worksheets_dict={})



    ''' clear all conditional formats
    '''
    def clear_conditional_formats_requests(self, number_of_rules):
        request_list = []
        for i in range(0, number_of_rules):
            request = {"deleteConditionalFormatRule": {
                        "sheetId": self.id,
                        "index": 0
                    }
                }

            request_list.append(request)

        return request_list



    ''' conditional formatting request for blank cells
    '''
    def conditional_formatting_for_blank_cells_requests(self, range_specs):
        ranges = [a1_range_to_grid_range(range_spec, sheet_id=self.id) for range_spec in range_specs]
        rule = build_conditional_format_rule(ranges=ranges, condition_type="BLANK", condition_values=[], format={"backgroundColor": hex_to_rgba("#fff2cc")})

        return [rule]



    ''' conditional formatting request for blank cells
    '''
    def conditional_formatting_for_review_notes_requests(self, num_cols):
        range_spec = f"A3:{COLUMN_TO_LETTER[num_cols]}"
        range = a1_range_to_grid_range(range_spec, sheet_id=self.id)

        rule = build_conditional_format_rule(ranges=[range], condition_type="CUSTOM_FORMULA", condition_values=["=not(isblank($A:$A))"], format={"backgroundColor": hex_to_rgba("#f4cccc")})

        return [rule]



    ''' data validation from list request
    '''
    def data_validation_from_list_requests(self, range_spec, values, input_message=None):
        range = a1_range_to_grid_range(range_spec, sheet_id=self.id)

        rule = build_data_validation_rule(range=range, condition_type='ONE_OF_LIST', condition_values=values, input_message=input_message)

        return [rule]



    ''' boolean/checkbox data validation request
    '''
    def data_validation_boolean_requests(self, range_spec, input_message=None):
        range = a1_range_to_grid_range(range_spec, sheet_id=self.id)

        rule = build_data_validation_rule(range=range, condition_type='BOOLEAN', condition_values=[], input_message=input_message)

        return [rule]



    ''' clear data validation request
    '''
    def data_validation_clear_requests(self, range_spec):
        range = a1_range_to_grid_range(range_spec, sheet_id=self.id)

        rule = build_no_data_validation_rule(range=range)

        return [rule]



    ''' work on a range work specs requests for value and format updates
    '''
    def range_work_requests(self, range_work_specs={}, worksheets_dict={}):
        formats = []
        values = []
        merges = []
        borders = []
        data_validation_requests = []
        conditional_format_requests = []

        for range_spec, work_spec in range_work_specs.items():
            # value
            if 'value' in work_spec:
                values.append({'range': f"'{self.title}'!{range_spec}", 'values': [[build_value_from_work_spec(work_spec=work_spec, worksheets_dict=worksheets_dict, google_service=self.service)]]})

            # merge
            merge = False
            if 'merge' in work_spec:
                merge = work_spec['merge']

            merge_type = 'MERGE_ALL'
            if 'merge-type' in work_spec:
                merge_type = work_spec['merge-type']

            if merge:
                merges.append({'mergeCells': {'range': a1_range_to_grid_range(range_spec, sheet_id=self.id), 'mergeType': merge_type}})

            # formats
            repeat_cell = build_repeatcell_from_work_spec(range=a1_range_to_grid_range(range_spec, sheet_id=self.id), work_spec=work_spec, gsheet=self.gsheet)
            if repeat_cell:
                formats.append(repeat_cell)

            # borders
            update_border = False
            border_style = 'SOLID'

            no_border = True
            if 'no-border' in work_spec:
                update_border = True
                no_border = work_spec['no-border']

                if no_border:
                    border_style = 'NONE'

            if 'border-style' in work_spec:
                update_border = True
                border_style = work_spec['border-style']

            inner_border = True
            if 'inner-border' in work_spec:
                update_border = True
                inner_border = work_spec['inner-border']

            border_color = '#000000'
            if 'border-color' in work_spec:
                update_border = True
                border_color = work_spec['border-color']

            # borders may depend on the existence of another optional key (border-list). It may be absent which means all borders or a list with values from the set (left, top, right, bottom)
            if 'border-list' in work_spec:
                update_border = True
                border_list = work_spec['border-list']
            else:
                border_list = ['left', 'top', 'right', 'bottom']

            # should borders be updated
            if update_border:
                border_object = {'range': a1_range_to_grid_range(range_spec, sheet_id=self.id)}
                borders.append({'updateBorders': {**border_object, **build_border_around_spec(border_list=border_list, border_color=border_color, border_style=border_style, inner_border=inner_border)}})

            # there is a list validation
            if 'validation-list' in work_spec:
                data_validation_requests = data_validation_requests + self.data_validation_clear_requests(range_spec)
                data_validation_requests = data_validation_requests + self.data_validation_from_list_requests(range_spec, work_spec['validation-list'])

            # boolean value, to be rendered as checkbox
            if 'checkbox' in work_spec:
                data_validation_requests = data_validation_requests + self.data_validation_clear_requests(range_spec)
                if work_spec['checkbox']:
                    data_validation_requests = data_validation_requests + self.data_validation_boolean_requests(range_spec)

            # conditional formats are to be applied
            if 'conditional-formats' in work_spec:
                ranges = [a1_range_to_grid_range(range_spec, sheet_id=self.id)]
                for conditional_format in work_spec['conditional-formats']:
                    condition_type = conditional_format['type']
                    condition_values = conditional_format['values']
                    format = conditional_format_from_object(conditional_format['format'])

                    conditional_format_requests = conditional_format_requests + [build_conditional_format_rule(ranges=ranges, condition_type=condition_type, condition_values=condition_values, format=format)]

        return values, merges + formats + borders + data_validation_requests + conditional_format_requests



    ''' resize columns request as per spec
    '''
    def column_resize_requests(self, column_specs):
        dimension_update_requests = []
        for key, value in column_specs.items():
            # debug(f".. resizing column {key} to {value['size']}", nesting_level=2)
            # set_column_width(target_ws, key, value['size'])
            # dimension_update_request = build_dimension_size_update_request(sheet_id=worksheet.id, dimension='COLUMN', index=gspread.utils.column_letter_to_index(key), size=value['size'])
            dimension_update_request = build_dimension_size_update_request(sheet_id=self.id, dimension='COLUMNS', index=LETTER_TO_COLUMN[key], size=value['size'])
            dimension_update_requests.append(dimension_update_request)

        return dimension_update_requests



    ''' autosize rows request
    '''
    def row_autosize_request(self, start_index, end_index):
        dimension_autosize_requests = build_dimension_autosize_request(sheet_id=self.id, dimension='ROWS', start_index=start_index, end_index=end_index)

        return dimension_autosize_requests



    ''' resize rows request as per spec
    '''
    def row_resize_requests(self, row_specs):
        dimension_update_requests = []
        for key, value in row_specs.items():
            dimension_update_request = build_dimension_size_update_request(sheet_id=self.id, dimension='ROWS', index=int(key), size=value['size'])
            dimension_update_requests.append(dimension_update_request)

        return dimension_update_requests



    ''' unhide columns request
    '''
    def column_unhide_requests(self):
        dimension_update_requests = []
        col_count = self.gspread_worksheet.col_count

        # to unhide all columns we need to know the number of columns
        dimension_update_request = build_dimension_visibility_update_request(sheet_id=self.id, dimension='COLUMNS', start_index=0, end_index=col_count, hide=False)
        dimension_update_requests.append(dimension_update_request)

        return dimension_update_requests



    ''' hide columns request
    '''
    def column_hide_requests(self, column_keys):
        dimension_update_requests = []

        # to unhide all columns we need to know the number of columns
        for key in column_keys:
            end_index = LETTER_TO_COLUMN[key]
            start_index = end_index - 1
            dimension_update_request = build_dimension_visibility_update_request(sheet_id=self.id, dimension='COLUMNS', start_index=start_index, end_index=end_index, hide=True)
            dimension_update_requests.append(dimension_update_request)

        return dimension_update_requests



    ''' freeze row and column request
    '''
    def dimension_freeze_requests(self, frozen_rows=None, frozen_cols=None):
        requests = []

        if frozen_rows is not None:
            request = build_row_freeze_request(sheet_id=self.id, frozen_rows=frozen_rows)
            requests.append(request)

        if frozen_cols is not None:
            request = build_column_freeze_request(sheet_id=self.id, frozen_cols=frozen_cols)
            requests.append(request)

        return requests
