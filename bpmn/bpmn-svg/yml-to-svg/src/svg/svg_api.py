#!/usr/bin/env python3

import importlib

from svg.svg_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Dot objects wrappers
#   ----------------------------------------------------------------------------------------------------------------


''' SVG base object
'''
class SvgObject(object):
    ''' constructor
    '''
    def __init__(self, config):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config
        self._bpmn_g = None

        self._canvas_width = 100
        self._canvas_height = 100



    ''' create the BPMN root group
    '''
    def create_root_group(self):
        self._bpmn_g = a_circle(radius=10, spec={})



    ''' generate the SVG from data
    '''
    def to_svg(self, bpmn_data):

        # bpmn to root group
        self.create_root_group()


        # wrap in a SVG drawing
        svg = Svg(0, 0, width=self._canvas_width, height=self._canvas_height)
        svg.addElement(self._bpmn_g)

        # finally save the svg
        svg.save(self._config['files']['output-svg'], encoding="UTF-8")




