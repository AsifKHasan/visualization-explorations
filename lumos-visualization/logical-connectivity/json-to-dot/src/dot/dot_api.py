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

        # a house includes areas
        for area_key, area_data in house_data.items():
            dot_area = DotArea(config=self._config)
            house_lines =  house_lines + dot_area.area_to_dot(area_key=area_key, area_data=area_data)

        # wrap the dot code
        house_lines = indent_and_wrap(house_lines, 'graph', object_name='g')

        return house_lines



''' Dot area object
'''
class DotArea(DotBase):

    ''' constructor
    '''
    def __init__(self, config):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config)


    ''' generates the Dot code
    '''
    def area_to_dot(self, area_key, area_data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        area_lines = []

        # an area includes buildings
        building_lines = []
        for building_key, building_data in area_data.items():
            dot_building = DotBuilding(config=self._config)
            building_lines = building_lines + dot_building.building_to_dot(building_key=building_key, building_data=building_data)

        # omit this if the key is '-'
        if area_key != '-':
            # area attributes
            area_lines.append(f'label="{area_key}"')
            area_lines.append(f'labelloc="t"')
            area_lines.append('')

            # append the building lines
            area_lines = area_lines + building_lines

            # wrap the dot code
            area_lines = indent_and_wrap(area_lines, 'subgraph', object_name=area_key)
            area_lines = [''] + area_lines

        else:
            area_lines = building_lines

        return area_lines



''' Dot building object
'''
class DotBuilding(DotBase):

    ''' constructor
    '''
    def __init__(self, config):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config)


    ''' generates the Dot code
    '''
    def building_to_dot(self, building_key, building_data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        building_lines = []

        # an building includes floors
        floor_lines = []
        for floor_key, floor_data in building_data.items():
            dot_floor = DotFloor(config=self._config)
            floor_lines = floor_lines + dot_floor.floor_to_dot(floor_key=floor_key, floor_data=floor_data)

        # omit this if the key is '-'
        if building_key != '-':
            # building attributes
            building_lines.append(f'label="{building_key}"')
            building_lines.append(f'labelloc="t"')
            building_lines.append('')

            # append the floor lines
            building_lines = building_lines + floor_lines

            # wrap the dot code
            building_lines = indent_and_wrap(building_lines, 'subgraph', object_name=building_key)
            building_lines = [''] + building_lines

        else:
            building_lines = floor_lines

        return building_lines



''' Dot floor object
'''
class DotFloor(DotBase):

    ''' constructor
    '''
    def __init__(self, config):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config)


    ''' generates the Dot code
    '''
    def floor_to_dot(self, floor_key, floor_data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        floor_lines = []

        # an floor includes rooms
        room_lines = []
        for room_key, room_data in floor_data.items():
            dot_room = DotRoom(config=self._config)
            room_lines = room_lines + dot_room.room_to_dot(room_key=room_key, room_data=room_data)

        # omit this if the key is '-'
        if floor_key != '-':
            # floor attributes
            floor_lines.append(f'label="{floor_key}"')
            floor_lines.append(f'labelloc="t"')
            floor_lines.append('')

            # append the room lines
            floor_lines = floor_lines + room_lines

            # wrap the dot code
            floor_lines = indent_and_wrap(floor_lines, 'subgraph', object_name=floor_key)
            floor_lines = [''] + floor_lines

        else:
            floor_lines = room_lines

        return floor_lines



''' Dot room object
'''
class DotRoom(DotBase):

    ''' constructor
    '''
    def __init__(self, config):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config)


    ''' generates the Dot code
    '''
    def room_to_dot(self, room_key, room_data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        room_lines = []

        # a room includes racks
        rack_lines = []
        for rack_key, rack_data in room_data.items():
            dot_rack = DotRack(config=self._config)
            rack_lines = rack_lines +  dot_rack.rack_to_dot(rack_key=rack_key, rack_data=rack_data)

        # omit this if the key is '-'
        if room_key != '-':
            # floor attributes
            room_lines.append(f'label="{room_key}"')
            room_lines.append(f'labelloc="t"')
            room_lines.append('')

            # append the rack lines
            room_lines = room_lines + rack_lines

            # wrap the dot code
            room_lines = indent_and_wrap(room_lines, 'subgraph', object_name=room_key)
            room_lines = [''] + room_lines

        else:
            room_lines = rack_lines

        return room_lines



''' Dot rack object
'''
class DotRack(DotBase):

    ''' constructor
    '''
    def __init__(self, config):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config)


    ''' generates the Dot code
    '''
    def rack_to_dot(self, rack_key, rack_data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        rack_lines = []

        # an rack includes equipments
        equipment_lines = []
        for equipment_key, equipment_data in rack_data.items():
            dot_equipment = DotEquipment(config=self._config)
            equipment_lines = equipment_lines + dot_equipment.equipment_to_dot(equipment_key=equipment_key, equipment_data=equipment_data)

        # omit this if the key is '-'
        if rack_key != '-':
            # rack attributes
            rack_lines.append(f'label="{rack_key}"')
            rack_lines.append(f'labelloc="t"')
            rack_lines.append('')

            # append the rack lines
            rack_lines = rack_lines + equipment_lines

            # wrap the dot code
            rack_lines = indent_and_wrap(rack_lines, 'subgraph', object_name=rack_key)
            rack_lines = [''] + rack_lines

        else:
            rack_lines = equipment_lines

        return rack_lines



''' Dot equipment object
'''
class DotEquipment(DotBase):

    ''' constructor
    '''
    def __init__(self, config):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config)


    ''' generates the Dot code
    '''
    def equipment_to_dot(self, equipment_key, equipment_data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        equipment_lines = []

        # equipment node
        equipment_lines.append(f'"{equipment_data["name"]}\\n{equipment_data["make"]}\\n{equipment_data["model"]}" []')
        equipment_lines.append('')

        # an equipment includes ports
        for port_data in equipment_data['ports']:
            dot_port = DotPort(config=self._config)
            equipment_lines =  equipment_lines + dot_port.port_to_dot(port_data=port_data)

        return equipment_lines



''' Dot port object
'''
class DotPort(DotBase):

    ''' constructor
    '''
    def __init__(self, config):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config)


    ''' generates the Dot code
    '''
    def port_to_dot(self, port_data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        port_lines = []

        # port attributes
        port_lines.append(f'# port : [{port_data["port"]}]')
        port_lines.append(f'# link : [{port_data["link"]}]')
        port_lines.append('')

        return port_lines
