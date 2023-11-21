#!/usr/bin/env python3

''' (GraphViz) dot wrapper objects
'''

import time
import yaml
import datetime

from dot.dot_api import GraphObject
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
        # work on the data
        dot_object = GraphObject(config=self._config, data=structure)
        self.dot_lines =  self.dot_lines + dot_object.to_dot()

        # save the dot document lines in a file
        with open(self._config['files']['output-dot'], "w", encoding="utf-8") as f:
            f.write('\n'.join(self.dot_lines))
