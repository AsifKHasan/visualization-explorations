#!/usr/bin/env python3
'''
'''
import sys
import json
import importlib
import time
import yaml
import datetime
import argparse
import pprint
from pathlib import Path

from helper.logger import *
from helper.gsheet.gsheet_helper import GsheetHelper


class JsonFromGsheet(object):

	def __init__(self, config_path, gsheet_name, worksheet_name):
		self.start_time = int(round(time.time() * 1000))
		self._config_path = Path(config_path).resolve()
		self._gsheet_name = gsheet_name
		self._worksheet_name = worksheet_name
		self._data = {}


	def run(self):
		self.set_up()

		# process the gsheet
		self._CONFIG['files']['output-json'] = f"{self._CONFIG['dirs']['output-dir']}/{self._worksheet_name}.json"
		self._data = self._gsheethelper.read_gsheet(gsheet_title=gsheet_title, worksheet_title=self._worksheet_name)
		self.save_json()

		self.tear_down()


	def set_up(self):
		# configuration
		self._CONFIG = yaml.load(open(self._config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
		config_dir = self._config_path.parent

		self._CONFIG['dirs']['output-dir'] = config_dir / self._CONFIG['dirs']['output-dir']
		self._CONFIG['files']['google-cred'] = config_dir / self._CONFIG['files']['google-cred']

		# gsheet-helper
		self._gsheethelper = GsheetHelper()
		self._gsheethelper.init(self._CONFIG)


	def save_json(self):
		with open(self._CONFIG['files']['output-json'], "w") as f:
			f.write(json.dumps(self._data, sort_keys=False, indent=4))


	def tear_down(self):
		self.end_time = int(round(time.time() * 1000))
		debug(f"gsheet {self._gsheet_name} worksheet {self._worksheet_name} processed")
		debug(f"script took {(self.end_time - self.start_time)/1000} seconds")


if __name__ == '__main__':
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--config", required=True, help="configuration yml path")
	ap.add_argument("-g", "--gsheet", required=False, help="gsheet name to read from")
	ap.add_argument("-w", "--worksheet", required=False, help="worksheet name to read from")
	args = vars(ap.parse_args())

	generator = JsonFromGsheet(config_path=args["config"], gsheet_name=args["gsheet"], worksheet_name=args["worksheet"])
	generator.run()
