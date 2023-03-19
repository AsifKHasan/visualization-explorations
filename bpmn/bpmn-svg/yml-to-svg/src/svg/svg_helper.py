#!/usr/bin/env python3

''' SVG wrapper objects
'''

import time
import yaml
import datetime

from svg.svg_api import GraphObject
from svg.svg_util import *
from helper.logger import *

class DotHelper(object):

    ''' constructor
    '''
    def __init__(self, config):
        self._config = config


    ''' generate and save the SVG
    '''
    def generate_and_save(self, structure):
        # work on the data
        svg_object = GraphObject(config=self._config, data=structure)
        self.svg_lines =  self.svg_lines + svg_object.to_svg()

        # save the markdown document string in a file
        with open(self._config['files']['output-svg'], "w", encoding="utf-8") as f:
            f.write('\n'.join(self.svg_lines))
