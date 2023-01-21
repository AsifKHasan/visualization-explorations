#!/usr/bin/env python3

import os
import sys
import json
import time
import yaml
import datetime
import argparse
from pathlib import Path

from dot.dot_helper import DotHelper
from dot.dot_util import *
from helper.logger import *


class DotFromJson(object):

	def __init__(self, config_path, json_name=None):
		self.start_time = int(round(time.time() * 1000))
		self._config_path = Path(config_path).resolve()
		self._data = {}
		self._json_name = json_name

	def run(self):
		self.set_up()
		self._CONFIG['files']['input-json'] = f"{self._CONFIG['dirs']['output-dir']}/{self._json_name}.json"
		self.load_json()

		# dot-helper
		self._CONFIG['files']['output-dot'] = f"{self._CONFIG['dirs']['output-dir']}/{self._json_name}.gv"
		dot_helper = DotHelper(self._CONFIG)
		dot_helper.generate_and_save(self._data)
		self.tear_down()

	def set_up(self):
		# configuration
		self._CONFIG = yaml.load(open(self._config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
		config_dir = self._config_path.parent

		self._CONFIG['dirs']['output-dir'] = config_dir / self._CONFIG['dirs']['output-dir']
		self._CONFIG['dirs']['output-dir'].mkdir(parents=True, exist_ok=True)

		if not 'files' in self._CONFIG:
			self._CONFIG['files'] = {}

		# there should be a theme_key.json in *themes* directory
		self._CONFIG['theme']['theme-dir'] = Path(self._CONFIG['theme']['theme-dir']).resolve()
		self._CONFIG['theme']['theme-path'] = self._CONFIG['theme']['theme-dir'] / f"{self._CONFIG['theme']['theme-name']}.json"
		try:
			info(f"using theme '{self._CONFIG['theme']['theme-name']}'")
			with open(self._CONFIG['theme']['theme-path'], 'r') as f:
				self._CONFIG['theme']['theme-data'] = json.load(f)

		except Exception as e:
			warn("theme {self._CONFIG['theme']['theme-name']} not found or not a theme at path [{self._CONFIG['theme']['theme-path']}]. Using 'default' theme")
			try:
				self._CONFIG['theme']['theme-name'] = 'default'
				self._CONFIG['theme']['theme-path'] = self._CONFIG['theme']['theme-dir'] / f"{self._CONFIG['theme']['theme-name']}.json"
				with open(self._CONFIG['theme']['theme-path'], 'r') as f:
					self._CONFIG['theme']['theme-data'] = json.load(f)

			except Exception as e:
				error(f"theme {self._CONFIG['theme']['theme-name']} not found or not a theme at path [{self._CONFIG['theme']['theme-path']}]. Exiting...")
				raise e
		

	def load_json(self):
		with open(self._CONFIG['files']['input-json'], "r") as f:
			self._data = json.load(f)

	def tear_down(self):
		self.end_time = int(round(time.time() * 1000))
		debug(f"script took {(self.end_time - self.start_time)/1000} seconds")

if __name__ == '__main__':
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--config", required=True, help="configuration yml path")
	ap.add_argument("-j", "--json", required=True, help="json file name to generate dot from")
	args = vars(ap.parse_args())

	generator = DotFromJson(args["config"], args["json"])
	generator.run()
