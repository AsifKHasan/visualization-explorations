#!/usr/bin/env python3

''' (GraphViz) dot wrapper objects
'''

import time
import yaml
import datetime

from dot.dot_api import DotHouse
from dot.dot_util import *
from helper.logger import *

class DotHelper(object):

    ''' constructor
    '''
    def __init__(self, config):
        self._config = config
        self.dot_lines = []



    ''' generate and save the dot
    '''
    def generate_and_save(self, structure):

        # work on only the first house
        for key, data in structure.items():
            dot_house = DotHouse(config=self._config, class_type='House', key=key, data=data)
            self.dot_lines =  self.dot_lines + dot_house.house_to_dot()

        # save the markdown document string in a file
        with open(self._config['files']['output-dot'], "w", encoding="utf-8") as f:
            f.write('\n'.join(self.dot_lines))
