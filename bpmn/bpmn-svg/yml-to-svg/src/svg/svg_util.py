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

from helper.util import *
from helper.geometry import *
from helper.logger import *

ROTATION_MATRIX = {
    "left":         {'angle': -90, 'translation': (0, 1)},
    "right":        {'angle':  90, 'translation': (1, 0)},
    "none":         {'angle':   0, 'translation': (0, 0)}
}


''' SVG group wrapper
'''
class SvgGroup(object):
    ''' constructor
    '''
    def __init__(self, g, width, height):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self.g, self.width, self.height = g, width, height

    
    ''' translate
    '''
    def translate(self, x, y):
        xy = Point(x, y)
        transformer = TransformBuilder()
        transformer.setTranslation(xy)
        self.g.set_transform(transformer.getTransform() + str(self.g.get_transform() or ''))



    ''' rotate
    '''
    def rotate(self, angle):
        transformer = TransformBuilder()
        transformer.setRotation(angle)
        self.g.set_transform(transformer.getTransform() + str(self.g.get_transform() or ''))


    ''' add group to the right
    '''
    def group_horizontally(self, svg_group):
        if not isinstance(svg_group, SvgGroup):
            raise TypeError

        new_group = G()
        new_group.addElement(self.g)

        svg_group.translate(x=self.width, y=0)

        new_group.addElement(svg_group.g)

        width = self.width + svg_group.width
        height = max(self.height, svg_group.height)

        return SvgGroup(g=new_group, width=width, height=height)


    ''' add group to the bottom
    '''
    def group_vertically(self, svg_group):
        if not isinstance(svg_group, SvgGroup):
            raise TypeError

        new_group = G()
        new_group.addElement(self.g)

        svg_group.translate(x=0, y=self.height)

        new_group.addElement(svg_group.g)

        width = max(self.width, svg_group.width)
        height = self.height + svg_group.height

        return SvgGroup(g=new_group, width=width, height=height)



''' group a list of groups together specified by position
'''
def group_together(svg_groups, position):
    # we need at least two groups
    if len(svg_groups) < 2:
        return None
    
    if position == 'north':
        return svg_groups[1].group_vertically(svg_group=svg_groups[0])

    elif position == 'south':
        return svg_groups[0].group_vertically(svg_group=svg_groups[1])

    elif position == 'west':
        return svg_groups[1].group_horizontally(svg_group=svg_groups[0])

    elif position == 'east':
        return svg_groups[0].group_horizontally(svg_group=svg_groups[1])
    



''' draws a text inside a rectangular area
'''
def a_text(text, width, height, spec):
    # whether wrapping is required
    text_pixels = text_size_in_pixels(text=text, font_family=spec['label-style']['font-family'], font_size=int(spec['label-style']['font-size']), font_weight=spec['label-style']['font-weight'], stroke_width=int(spec['label-style']['stroke-width']))
    margin_west = int(spec['margin']['west'])
    margin_east = int(spec['margin']['east'])
    margin_north = int(spec['margin']['north'])
    margin_south = int(spec['margin']['south'])

    max_text_width = width - margin_west - margin_east
    max_text_height = height - margin_north - margin_south

    if text_pixels[0] > max_text_width:
        # wrap if specified
        wrap = int(spec['text-wrap'])
        if wrap > 0:
            text_lines = textwrap.wrap(text=text, width=wrap, break_long_words=True)
        else:
            text_lines = [text]

    else:
        # no need to wrap
        text_lines = [text]


    # create the rect
    svg_group = a_rect(width=width, height=height, rx=spec['rx'], ry=spec['ry'], style=spec['shape-style'])

    # calculate a proper dy from font-size
    font_size = int(spec['label-style']['font-size'])
    dy = font_size * 1.1
    the_range = balanced_range(len(text_lines))

    # horizontal alignments
    halign = spec['halign']
    if halign == 'center':
        x = width / 2

    elif halign == 'west':
        x = margin_west
        spec['label-style']['text-anchor'] = 'start'

    elif halign == 'east':
        x = width - margin_east
        spec['label-style']['text-anchor'] = 'end'
    
    # vertical alignment
    valign = spec['valign']
    if valign == 'middle':
        y = height / 2

    elif valign == 'north':
        y = margin_north + (dy * len(the_range)/2)

    elif valign == 'south':
        y = height - margin_south - (dy * len(the_range)/2)



    # create the texts
    i = 0
    for t in text_lines:
        svg_t = Text(content=t, x=x, y=y, dy=dy * the_range[i])
        svg_t.set_style(StyleBuilder(spec['label-style']).getStyle())
        svg_group.g.addElement(svg_t)
        i = i + 1


    # TODO: rotate
    new_width, new_height = width, height
    rotation = spec['rotation']
    svg_group.rotate(angle=ROTATION_MATRIX[rotation]['angle'])
    if rotation in ['left', 'right']:
        new_width, new_height = height, width


    return SvgGroup(g=svg_group.g, width=new_width, height=new_height)



''' draws a rectangle
'''
def a_rect(width, height, rx, ry, style):
    g = G()

    svg = Rect(width=width, height=height, rx=rx, ry=ry)
    svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    g.addElement(svg)

    return SvgGroup(g=g, width=width, height=height)


''' draws a circle
'''
def a_circle(radius, style):
    g = G()

    svg = Circle(cx=radius, cy=radius, r=radius)
    svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    g.addElement(svg)

    return SvgGroup(g=g, width=radius*2, height=radius*2)


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
    

