#!/usr/bin/env python3

import importlib
from os import path

from pysvg.parser import *

from svg.svg_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Block object wrapper
#   ----------------------------------------------------------------------------------------------------------------

''' Base object
'''
class BlockBase(object):
    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config
        self._data = data
        self._SVG = None


    ''' get and open the template from data
    '''
    def open_template(self):
        # which svg template to load?
        svg_template_path = f"{self._config['dirs']['svg-template-dir']}/{self._data['type']}/{self._data['make']}/{self._data['model']}/{self._data['template']}.svg"
        if not path.exists(svg_template_path):
            error("no svg template [{svg_template_path}]")
            return

        # open as an SVG object
        self._SVG = parse(svg_template_path)



''' Rack object
'''
class Rack(BlockBase):

    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, data=data)


    ''' generates the SVG object
    '''
    def to_svg(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self.open_template()

        # TODO: do somnething arbitrary


        return self._SVG



