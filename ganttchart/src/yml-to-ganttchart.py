#!/usr/bin/env python3

import os
import sys
import time
import json
import yaml
import datetime
import argparse
from pathlib import Path
import pprint

from ggle.google_service import GoogleService

from dot.dot_helper import DotHelper
from dot.dot_util import *
from helper.logger import *
from helper import logger


def filter_columns(data, keep_first_n, keep_extra):
    """
    data         : list of lists
    keep_first_n : number of first columns to keep
    keep_extra   : list of additional column indices to keep (0-based)
    """
    result = []
    for row in data:
        new_row = row[:keep_first_n]  # take first N
        for idx in keep_extra:
            if idx < len(row):  # only keep if index exists
                new_row.append(row[idx])
        result.append(new_row)
    return result


def nested_list_from_data(data):

	result = []
	stack = []  # keeps track of last node seen at each level

	for row in data:
		# level = first non-blank column (excluding last column which is "span")
		level = next((i for i, val in enumerate(row[:-1]) if val.strip()), None)
		if level is None:
			continue  # skip empty row
		
		node = {
			"hash": row[level],
			"span": row[-1],
			"items": []
		}
		
		# Only add text if non-blank and not the same as hash
		if level + 1 < len(row) - 1 and row[level+1].strip():
			node["text"] = row[level+1]
		
		# Insert into tree
		if level == 0:  # top level
			result.append(node)
		else:  # child of previous level
			parent = stack[level-1]
			parent.setdefault("items", []).append(node)
		
		# Update stack for this level
		if len(stack) <= level:
			stack.extend([None] * (level - len(stack) + 1))
		stack[level] = node
		# Trim deeper levels (start fresh after this node)
		stack = stack[:level+1]

		# --- helper to prune empty children ---
		def prune(node):
			if "items" in node:
				if not node["items"]:
					del node["items"]
				else:
					node["items"] = [prune(child) for child in node["items"]]
			return node

	cleaned = [prune(item) for item in result]

	return cleaned


class GanttchartFromYml(object):

	def __init__(self, config, yml_name=None):
		self.start_time = int(round(time.time() * 1000))
		self._CONFIG = config
		self._data = {}
		self._yml_name = yml_name
		self._yml_name_only = self._yml_name.split('/')[-1]


	def run(self):
		self.set_up()
		self._CONFIG['files']['input-yml'] = f"{self._CONFIG['dirs']['data-dir']}/{self._yml_name}.yml"
		self._data = yaml.load(open(self._CONFIG['files']['input-yml'], 'r', encoding='utf-8'), Loader=yaml.FullLoader)

		# load theme
		self._CONFIG['theme']['theme-name'] = self._data.get('theme', 'task-week-default')
		self.load_theme()

		# dot-helper
		self._CONFIG['files']['output-dot'] = f"{self._CONFIG['dirs']['output-dir']}/{self._yml_name_only}.gv"

		# this is where we need to get the data, it may be in-yaml or in a gsheet
		if 'credential-json' in self._CONFIG:
			credential_json = self._CONFIG['credential-json']
			if 'gsheet' in self._data:
				gsheet_name = self._data['gsheet']
				debug(f"trying to access data from gsheet [{gsheet_name}], ignoring any in-yaml data")
				g_service = GoogleService(service_account_json_path=credential_json)
				info(f"processing gsheet {gsheet_name}")
				g_sheet = g_service.open(gsheet_name=gsheet_name)
				worksheet_name = self._data.get('worksheet', 'gantt-chart')
				start_row = self._data.get('start-row', 3)
				task_columns = self._data.get('task-columns', 3)
				span_column = self._data.get('span-column', 4)

				range_spec = f"{worksheet_name}!A{start_row}:Z"
				worksheet_data = g_sheet.get_range_values(range_spec=range_spec)
				worksheet_data = filter_columns(worksheet_data['values'], keep_first_n=task_columns, keep_extra=[span_column-1])
				

				# generate items from the data
				items = nested_list_from_data(data=worksheet_data)

				self._data['items'] = items

		else:
			debug(f"No credential for gsheet access, so ignoring any gsheet related data access")


		dot_helper = DotHelper(self._CONFIG)
		dot_helper.generate_and_save(self._data)
		self.tear_down()


	def set_up(self):
		self._CONFIG['dirs']['output-dir'] = Path(self._CONFIG['dirs']['output-dir']).resolve()
		self._CONFIG['dirs']['output-dir'].mkdir(parents=True, exist_ok=True)

		if not 'files' in self._CONFIG:
			self._CONFIG['files'] = {}


	def load_theme(self):
		# there should be a theme_key.json in *themes* directory
		self._CONFIG['theme']['theme-dir'] = Path(self._CONFIG['theme']['theme-dir']).resolve()
		self._CONFIG['theme']['theme-path'] = self._CONFIG['theme']['theme-dir'] / f"{self._CONFIG['theme']['theme-name']}.yml"
		try:
			info(f"using theme '{self._CONFIG['theme']['theme-name']}'")
			self._CONFIG['theme']['theme-data'] = yaml.load(open(self._CONFIG['theme']['theme-path'], 'r', encoding='utf-8'), Loader=yaml.FullLoader)

		except Exception as e:
			warn(f"theme {self._CONFIG['theme']['theme-name']} not found or not a theme at path [{self._CONFIG['theme']['theme-path']}]. Using 'task-week-default' theme")
			try:
				self._CONFIG['theme']['theme-name'] = 'task-week-default'
				self._CONFIG['theme']['theme-path'] = self._CONFIG['theme']['theme-dir'] / f"{self._CONFIG['theme']['theme-name']}.yml"
				self._CONFIG['theme']['theme-data'] = yaml.load(open(self._CONFIG['theme']['theme-path'], 'r', encoding='utf-8'), Loader=yaml.FullLoader)

			except Exception as e:
				error(f"theme {self._CONFIG['theme']['theme-name']} not found or not a theme at path [{self._CONFIG['theme']['theme-path']}]. Exiting...")
				raise e
		

	def tear_down(self):
		self.end_time = int(round(time.time() * 1000))
		debug(f"script took {(self.end_time - self.start_time)/1000} seconds")


if __name__ == '__main__':
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--config", required=True, help="configuration yml path")
	ap.add_argument("-y", "--yml", required=True, help="yml file name to generate dot from")
	args = vars(ap.parse_args())

	config = yaml.load(open(args["config"], 'r', encoding='utf-8'), Loader=yaml.FullLoader)

	logger.LOG_LEVEL = config.get('log-level', 0)
	generator = GanttchartFromYml(config=config, yml_name=args["yml"])
	generator.run()
