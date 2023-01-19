#!/usr/bin/env python3

import importlib

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
    def __init__(self, config, key, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config
        self._name = key
        self._key = text_to_identifier(key)
        self._data = data
        self._lines = []


    ''' get the lines from children
    '''
    def append_children(self, class_type, work_data=None):
        child_class = getattr(importlib.import_module('dot.dot_api'), f"Dot{class_type}")

        # if no work_data supplied, use the self._data
        if work_data is None:
            for key, data in self._data.items():
                child_instance = child_class(config=self._config, key=key, data=data)
                self._lines = self._lines + child_instance.to_dot()

        # else assume that the work_data is a list
        else:
            for data in work_data:
                child_instance = child_class(config=self._config, key='', data=data)
                self._lines = self._lines + child_instance.to_dot()


    ''' wrap and close
    '''
    def wrap_and_close(self, as_a):
        if self._name != '-':
            self._lines = indent_and_wrap(self._lines, wrap_keyword=as_a, object_name=self._key)
            self._lines = self._lines + ['']



''' Dot house object
'''
class DotHouse(DotBase):

    ''' constructor
    '''
    def __init__(self, config, key, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, key=key, data=data)


    ''' generates the Dot code
    '''
    def house_to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # house attributes
        if self._name != '-':
            self._lines.append(f"graph [ {make_a_property(prop_key='compound', prop_value='true')}]")
            self._lines.append(make_a_property(prop_key='label', prop_value=self._name))
            self._lines.append(make_a_property(prop_key='labelloc', prop_value='b'))
            self._lines.append('')

        # a house includes areas
        self.append_children(class_type='Area')

        # wrap the dot code
        self.wrap_and_close(as_a='graph')

        return self._lines



''' Dot area object
'''
class DotArea(DotBase):

    ''' constructor
    '''
    def __init__(self, config, key, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, key=key, data=data)


    ''' generates the Dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # area attributes
        if self._name != '-':
            self._lines.append(make_a_property(prop_key='label', prop_value=self._name))
            self._lines.append(make_a_property(prop_key='labelloc', prop_value='b'))
            self._lines.append('')

        # an area includes buildings
        self.append_children(class_type='Building')

        # wrap the dot code
        self.wrap_and_close(as_a='subgraph')

        return self._lines



''' Dot building object
'''
class DotBuilding(DotBase):

    ''' constructor
    '''
    def __init__(self, config, key, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, key=key, data=data)


    ''' generates the Dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # building attributes
        if self._name != '-':
            self._lines.append(make_a_property(prop_key='label', prop_value=self._name))
            self._lines.append(make_a_property(prop_key='labelloc', prop_value='b'))
            self._lines.append('')

        # an building includes floors
        self.append_children(class_type='Floor')

        # wrap the dot code
        self.wrap_and_close(as_a='subgraph')

        return self._lines



''' Dot floor object
'''
class DotFloor(DotBase):

    ''' constructor
    '''
    def __init__(self, config, key, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, key=key, data=data)


    ''' generates the Dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # floor attributes
        if self._name != '-':
            self._lines.append(make_a_property(prop_key='label', prop_value=self._name))
            self._lines.append(make_a_property(prop_key='labelloc', prop_value='b'))
            self._lines.append('')

        # an floor includes rooms
        self.append_children(class_type='Room')

        # wrap the dot code
        self.wrap_and_close(as_a='subgraph')

        return self._lines



''' Dot room object
'''
class DotRoom(DotBase):

    ''' constructor
    '''
    def __init__(self, config, key, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, key=key, data=data)


    ''' generates the Dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # floor attributes
        if self._name != '-':
            self._lines.append(make_a_property(prop_key='label', prop_value=self._name))
            self._lines.append(make_a_property(prop_key='labelloc', prop_value='b'))
            self._lines.append('')

        # a room includes racks
        self.append_children(class_type='Rack')

        # wrap the dot code
        self.wrap_and_close(as_a='subgraph')

        return self._lines



''' Dot rack object
'''
class DotRack(DotBase):

    ''' constructor
    '''
    def __init__(self, config, key, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, key=key, data=data)


    ''' generates the Dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # rack attributes
        if self._name != '-':
            self._lines.append(make_a_property(prop_key='label', prop_value=self._name))
            self._lines.append(make_a_property(prop_key='labelloc', prop_value='b'))
            self._lines.append('')

        # a rack includes equipments
        self.append_children(class_type='Equipment')

        # wrap the dot code
        self.wrap_and_close(as_a='subgraph')

        return self._lines



''' Dot equipment object
'''
class DotEquipment(DotBase):

    ''' constructor
    '''
    def __init__(self, config, key, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, key=key, data=data)


    ''' generates the Dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # equipment node
        node_str = make_a_node(node_key=self._key, label=f'{self._data["name"]}\\n{self._data["make"]}\\n{self._data["model"]}')
        self._lines.append(node_str)
        self._lines.append('')

        # an equipment includes ports
        self.append_children(class_type='Port', work_data=self._data['ports'])

        return self._lines



''' Dot port object
'''
class DotPort(DotBase):

    ''' constructor
    '''
    def __init__(self, config, key, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, key=key, data=data)


    ''' generates the Dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # port attributes
        self._lines.append(f'# port : [{self._data["port"]}]')
        self._lines.append(f'# link : [{self._data["link"]}]')
        self._lines.append('')

        return self._lines
