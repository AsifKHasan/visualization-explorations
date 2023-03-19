#!/usr/bin/env python3

''' Block helper object
'''

import importlib

from block.block_util import *
from helper.logger import *

class BlockHelper(object):

    ''' constructor
    '''
    def __init__(self, config):
        self._config = config


    ''' generate and save the SVG
    '''
    def generate_and_save(self, structure):
        # get the BlockBase based on type
        block_class = getattr(importlib.import_module('block.block_api'), pascal_case(text=structure['type']))
        block_instance = block_class(config=self._config, data=structure)

        # get the SVG object from the RackObject
        svg = block_instance.to_svg()

        # save the SVG in a file
        svg.save(self._config['files']['output-svg'], encoding="UTF-8")
