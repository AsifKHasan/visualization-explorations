#!/usr/bin/env python3

import importlib

from bpmn.bpmn_api import *
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
    def __init__(self, config, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config
        self._theme = theme


    ''' generate the SVG from data
    '''
    def to_svg(self, bpmn_object):

        # bpmn to root group
        bpmn_svg = BpmnSvg(config=self._config, theme=self._theme)
        
        g_bpmn = bpmn_svg.to_svg(bpmn_object=bpmn_object)

        canvas_width, canvas_height = dimension_with_margin(width=bpmn_svg._width, height=bpmn_svg._height, margin=self._theme['bpmn']['margin'])


        # wrap in a SVG drawing
        svg = Svg(0, 0, width=canvas_width, height=canvas_height)
        svg.addElement(g_bpmn)

        # finally save the svg
        svg.save(self._config['files']['output-svg'], encoding="UTF-8")



''' BPMN SVG object
'''
class BpmnSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, config, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, theme=theme)

        self._width = self._theme['bpmn']['min-width']
        self._height = self._theme['bpmn']['min-height']


    ''' generate the SVG from data
    '''
    def to_svg(self, bpmn_object):

        # bpmn to group
        g_bpmn = a_rect(width=self._width, height=self._height, rx=self._theme['bpmn']['rx'], ry=self._theme['bpmn']['ry'], style=self._theme['bpmn']['style'])

        # return group
        return g_bpmn
