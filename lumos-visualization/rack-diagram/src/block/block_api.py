#!/usr/bin/env python3

import importlib

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
        self._type = self._data['type']
        self._make = self._data['make']
        self._model = self._data['model']
        self._template = self._data['template']

        self._svg_attrs = self._config['svg-attrs'][self._type][self._make][self._model][self._template]

        self._SVG = None


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
        svg_template_path = f"{self._config['dirs']['svg-template-dir']}/{self._type}/{self._make}/{self._model}/{self._template}.svg"
        self._SVG = open_svg_from_file(template_path=svg_template_path)

        # iterate children
        for equipment in self._data['equipments']:
            # get the u position
            u_pos_list = equipment['position'].split('-')
            u_start, u_end = int(u_pos_list[0]), int(u_pos_list[-1])
            for u in range(u_start, u_end+1):
                u_str = '{:0>2}'.format(u)
                equipment_type = equipment['type']
                equipment_make = equipment['make']
                equipment_mpdel = equipment['model']
                equipment_template = equipment['template']
                message = f"position [{u_str}] occuied by equipment [{equipment_type}][{equipment_make}][{equipment_mpdel}][{equipment_template}]"
                debug(message)

        my_group = get_child_by_id(parent=self._SVG, id='g-u-40', element_type=G)
        print(my_group.getXML())

        return self._SVG
