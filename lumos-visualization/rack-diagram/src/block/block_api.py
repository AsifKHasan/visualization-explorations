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
        self._h = self._svg_attrs['h']
        self._w = self._svg_attrs['w']

        self._SVG = None


    ''' generates the SVG object
    '''
    def to_svg(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        svg_template_path = f"{self._config['dirs']['svg-template-dir']}/{self._type}/{self._make}/{self._model}/{self._template}.svg"
        self._SVG = open_svg_from_file(template_path=svg_template_path)



''' Rack object
'''
class Rack(BlockBase):

    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, data=data)


    ''' given a u position return the G object for the u position
    '''
    def group_from_u(self, u):
        id = '{}-{:0>2}'.format(self._svg_attrs['u-group-prefix'], u)
        group = get_child_by_id(parent=self._SVG, id=id, element_type=G)

        return group


    ''' given a starting u and ending u returns
        starting u, width, height (covering the u positions)
    '''
    def rack_area_from_u_position(self, u_position):
        u_pos_list = str(u_position).split('-')
        u1, u2 = int(u_pos_list[0]), int(u_pos_list[-1])
        u_top, u_bottom = max(u1, u2), min(u1, u2)

        # the rack area is top u's top left to bottom u's bottom right 

        top_u_group = self.group_from_u(u=u_top)
        bottom_u_group = self.group_from_u(u=u_bottom)

        # TODO: top u's (left_x, top_y) is group's translate's (x, y)
        left_x = 0
        top_y = 0

        # TODO: bottom u's (right_x, bottom_y) is group's translate's (x, y) if it is there + inner rect's (x, y)
        right_x = 0
        bottom_y = 0

        u_w = right_x - left_x
        u_h = bottom_y - top_y

        u_w, u_h = 0, 0

        # HACK: for now just get width of the rects and add the height of the rects
        for u in range(u_top, u_bottom-1, -1):
            # get the u's group and its inner rect
            u_group = self.group_from_u(u=u)
            rect_id = '{}-{:0>2}'.format(self._svg_attrs['u-rect-prefix'], u)
            u_rect = get_child_by_id(u_group, id=rect_id, element_type=Rect)
            u_h = u_h + float(u_rect.get_height())
            u_w = float(u_rect.get_width())

        return u_top, u_w, u_h


    ''' generates the SVG object
    '''
    def to_svg(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().to_svg()

        # iterate children
        for equipment_data in self._data['equipments']:
            if equipment_data['hide']:
                continue
            
            # get the equipment svg
            equipment = Equipment(config=self._config, data=equipment_data)
            equipment_svg = equipment.to_svg()

            # get the height and width of the area to be covered by the equipment
            u_start, equipment_w, equipment_h = self.rack_area_from_u_position(u_position=equipment_data['position'])

            # get the G where the equipment is to be embedded
            group = self.group_from_u(u=u_start)

            # calculate the scaling factor for the G so that the equipment's real sizes are scaled to the rack's actual area
            x_scale = (equipment_w/equipment._w)
            y_scale = (equipment_h/equipment._h)

            # embed and scale, scaling to be done at parent group, not the equipment svg node
            scale_group(group=group, x_scale=x_scale, y_scale=y_scale)
            equipment_svg.set_viewBox(None)
            group.addElement(equipment_svg)

            message = f"equipment [{equipment._type}][{equipment._make}][{equipment._model}][{equipment._template}] covers position {equipment_data['position']} scaled at ({x_scale},{y_scale})"
            debug(message)
        

        return self._SVG



''' Equipment object
'''
class Equipment(BlockBase):

    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, data=data)


    ''' generates the SVG object
    '''
    def to_svg(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().to_svg()

        return self._SVG
