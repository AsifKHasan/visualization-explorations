#!/usr/bin/env python3

from dot.dot_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Dot objects wrappers
#   ----------------------------------------------------------------------------------------------------------------

''' Dot base object
'''
class DotBase(object):

    ''' constructor
    '''
    def __init__(self, config):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config



''' Dot house object
'''
class DotHouse(DotBase):

    ''' constructor
    '''
    def __init__(self, config):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config)


    ''' generates the Dot code
    '''
    def house_to_dot(self, house_key, house_data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        house_lines = []

        # house attributes
        house_lines.append(f'graph [ compound=true ];')
        house_lines.append(f'label="{house_key}"')
        house_lines.append(f'labelloc="b"')

        # wrap the dot code
        house_lines = indent_and_wrap(house_lines, 'graph', object_name='g')

        return house_lines
