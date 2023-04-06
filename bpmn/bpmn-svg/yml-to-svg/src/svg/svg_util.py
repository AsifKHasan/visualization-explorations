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
    def __init__(self, g, width, height, x=0, y=0, angle=0):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self.g, self.g_width, self.g_height, self.g_x, self.g_y, self.g_angle = g, width, height, x, y, 0

    
    ''' translate
    '''
    def translate(self, x, y):
        self.g_x, self.g_y = x, y
        xy = Point(self.g_x, self.g_y)
        transformer = TransformBuilder()
        transformer.setTranslation(xy)
        self.g.set_transform(transformer.getTransform() + str(self.g.get_transform() or ''))



    ''' rotate
    '''
    def rotate(self, angle):
        self.g_angle = angle
        transformer = TransformBuilder()
        transformer.setRotation(self.g_angle)
        self.g.set_transform(transformer.getTransform() + str(self.g.get_transform() or ''))



    ''' add groups to the right
    '''
    def group_horizontally(self, gid, svg_groups):
        if not isinstance(svg_groups, list):
            raise TypeError

        new_group = G(id=gid)
        new_group.addElement(self.g)

        translate_to_x = self.g_width
        new_width = self.g_width
        new_height = self.g_height

        # place groups one by one
        for svg_group in svg_groups:
            # horizontally translate this group
            svg_group.translate(x=translate_to_x, y=0)

            # add this group
            new_group.addElement(svg_group.g)

            # new height and width to be recalculated
            new_width = new_width + svg_group.g_width
            new_height = max(new_height, svg_group.g_height)

            # move the translation position for the next group
            translate_to_x = translate_to_x + svg_group.g_width

        return SvgGroup(g=new_group, width=new_width, height=new_height)


    ''' add groups to the bottom
    '''
    def group_vertically(self, gid, svg_groups):
        if not isinstance(svg_groups, list):
            raise TypeError

        new_group = G(id=gid)
        new_group.addElement(self.g)

        translate_to_y = self.g_height
        new_width = self.g_width
        new_height = self.g_height

        # place groups one by one
        for svg_group in svg_groups:
            # horizontally translate this group
            svg_group.translate(x=0, y=translate_to_y)

            # add this group
            new_group.addElement(svg_group.g)

            # new height and width to be recalculated
            new_width = max(new_width, svg_group.g_width)
            new_height = new_height + svg_group.g_height

            # move the translation position for the next group
            translate_to_y = translate_to_y + svg_group.g_height

        return SvgGroup(g=new_group, width=new_width, height=new_height)



    ''' embed group inside the group
    '''
    def embed(self, svg_group):
        if not isinstance(svg_group, SvgGroup):
            raise TypeError

        translate_to_x = (self.g_width - svg_group.g_width) / 2
        translate_to_y = (self.g_height - svg_group.g_height) / 2

        svg_group.translate(x=translate_to_x, y=translate_to_y)

        self.g.addElement(svg_group.g)

        return self


    
    ''' embed groups vertically inside the group
    '''
    def embed_vertically(self, svg_groups, margin={}):
        if not isinstance(svg_groups, list):
            raise TypeError

        translate_to_x = int(margin.get('west', 0))
        translate_to_y = int(margin.get('north', 0))

        # place groups one by one
        for svg_group in svg_groups:
            svg_group.translate(x=translate_to_x, y=translate_to_y)

            # add this group
            self.g.addElement(svg_group.g)
    
            # move the translation position for the next group
            translate_to_y  = translate_to_y + svg_group.g_height

        return self



    ''' add groups vertically inside the group and extend the group
    '''
    def extend_vertically(self, svg_groups):
        if not isinstance(svg_groups, list):
            raise TypeError

        translate_to_x = 0
        translate_to_y = self.g_height

        # place groups one by one
        for svg_group in svg_groups:
            svg_group.translate(x=translate_to_x, y=translate_to_y)

            # add this group
            self.g.addElement(svg_group.g)
    
            # move the translation position for the next group
            translate_to_y  = translate_to_y + svg_group.g_height

            self.g_width = max(self.g_width, svg_group.g_width)
            self.g_height = self.g_height + svg_group.g_height

        return self



''' group a list of groups together specified by position
'''
def group_together(gid, svg_groups, position):
    # we need at least two groups
    if len(svg_groups) < 2:
        return None
    
    if position == 'north':
        return svg_groups[1].group_vertically(gid=gid, svg_groups=[svg_groups[0]])

    elif position == 'south':
        return svg_groups[0].group_vertically(gid=gid, svg_groups=[svg_groups[1]])

    elif position == 'west':
        return svg_groups[1].group_horizontally(gid=gid, svg_groups=[svg_groups[0]])

    elif position == 'east':
        return svg_groups[0].group_horizontally(gid=gid, svg_groups=[svg_groups[1]])

    elif position == 'in':
        return svg_groups[0].embed(svg_group=svg_groups[1])


    



''' draws a text inside a rectangular area
'''
def a_text(gid, text, width, height, spec):
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
    svg_group = a_rect(gid=gid, width=width, height=height, rx=spec['rx'], ry=spec['ry'], style=spec['shape-style'])

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
def a_rect(gid, width, height, rx, ry, style):
    g = G(id=gid)

    svg = Rect(width=width, height=height, rx=rx, ry=ry)
    svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    g.addElement(svg)

    return SvgGroup(g=g, width=width, height=height)


''' draws a circle
'''
def a_circle(gid, radius, style):
    g = G(id=gid)

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
    

''' return dimension without margins
'''
def dimension_without_margin(width, height, margin):
    if margin:
        margin_west = int(margin.get('west', 0))
        margin_east = int(margin.get('east', 0))
        margin_north = int(margin.get('north', 0))
        margin_south = int(margin.get('south', 0))

    else:
        return width, height

    new_width, new_height = width - margin_west - margin_east, height - margin_north - margin_south

    return new_width, new_height
    

