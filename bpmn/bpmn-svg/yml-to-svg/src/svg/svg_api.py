#!/usr/bin/env python3

import importlib
from pprint import pprint
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
        self._bpmn_object = bpmn_object

        # bpmn to root group
        bpmn_svg = BpmnSvg(config=self._config, theme=self._theme)
        
        bpmn_g = bpmn_svg.to_svg(bpmn_object=bpmn_object)

        canvas_width, canvas_height = dimension_with_margin(width=bpmn_g.width, height=bpmn_g.height, margin=self._theme['bpmn']['margin'])


        # wrap in a SVG drawing
        svg = Svg(0, 0, width=canvas_width, height=canvas_height)
        svg.addElement(bpmn_g.g)

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


    ''' attach label
    '''
    def attach_label(self, attach_to_g):
        # label rect height and width depends on block height and width, label position and label rotation
        pos = self._theme['bpmn']['text']['pos']

        # based on position, groups will be placed
        print(f"label to {pos}")
        if pos == 'in':
            # just embed the text into the attach group
            attach_to_g.g.addElement(text_g.g)
            new_g = attach_to_g

        elif pos == 'north':
            new_g = text_g.group_vertically(svg_group=attach_to_g)

        elif pos == 'south':
            new_g = attach_to_g.group_vertically(svg_group=text_g)

        elif pos == 'west':
            # height is attach object's height, width is text's min-width
            rect_width, rect_height = self._theme['bpmn']['text']['min-width'], self._height

            text_g = a_text(text=self._bpmn_object._label, width=rect_width, height=rect_height, spec=self._theme['bpmn']['text'])

            # y translation of width is necessary
            text_g.translate(0, rect_width)

            new_g = text_g.group_horizontally(svg_group=attach_to_g)

        elif pos == 'east':
            new_g = attach_to_g.group_horizontally(svg_group=text_g)
            
        
        return new_g



    ''' generate the SVG from data
    '''
    def to_svg(self, bpmn_object):
        self._bpmn_object = bpmn_object

        # bpmn to group
        g_bpmn = a_rect(width=self._width, height=self._height, rx=self._theme['bpmn']['rx'], ry=self._theme['bpmn']['ry'], style=self._theme['bpmn']['style'])

        # if there is a label, attach it
        if self._bpmn_object._hide_label == False:
            g_bpmn = self.attach_label(attach_to_g=g_bpmn)


        # return group
        return g_bpmn
