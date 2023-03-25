#!/usr/bin/env python3

'''
various utilities for SVG code
'''
import re
import random
import string
import textwrap

from pysvg.builders import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *

from helper.geometry import *
from helper.logger import *

''' SVG group wrapper
'''
class SvgGroup(object):
    ''' constructor
    '''
    def __init__(self, group, width, height):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self.g, self.width, self.height = group, width, height

    
    ''' add group to the right
    '''
    def group_horizontally(self, group):
        new_group = G()
        new_group.addElement(self.g)

        group_pos_xy = Point(self.width, 0)
        transformer = TransformBuilder()
        transformer.setTranslation(group_pos_xy)
        group.set_transform(transformer.getTransform())
        new_group.addElement(group)

        return new_group


    ''' add group to the bottom
    '''
    def group_vertically(self, group):
        new_group = G()
        new_group.addElement(self.g)

        group_pos_xy = Point(0, self.height)
        transformer = TransformBuilder()
        transformer.setTranslation(group_pos_xy)
        group.set_transform(transformer.getTransform())
        new_group.addElement(group)

        return new_group


''' draws a text inside a rectamgular area
'''
def a_text():


''' draws a rectangle
'''
def a_rect(width, height, rx, ry, style):
    g = G()

    svg = Rect(width=width, height=height, rx=rx, ry=ry)
    svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    g.addElement(svg)

    return g


''' draws a circle
'''
def a_circle(radius, style):
    g = G()
    # print(style)

    svg = Circle(cx=radius, cy=radius, r=radius)
    svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    g.addElement(svg)

    return g


''' return dimension with margins added
'''
def dimension_with_margin(width, height, margin):
    if margin:
        margin_west = int(margin.get('west', 0))
        margin_east = int(margin.get('east', 0))
        margin_north = int(margin.get('north', 0))
        margin_south = int(margin.get('south', 0))

    else:
        return width, height

    new_width, new_height = width + margin_west + margin_east, height + margin_north + margin_south

    return new_width, new_height
    

