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

HALIGN_TO_SVG = {
    "center":       "50%",
    "west":         "10%",
    "east":         "90%",
}

VALIGN_TO_SVG = {
    "middle":       "50%",
    "north":        "10%",
    "south":        "90%",
}


ROTATION_TO_ANGLE = {
    "left":         -90,
    "right":        90,
    "flip":         180
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


''' draws a text inside a rectangular area
'''
def a_text(text, width, height, spec):
    # whether wrapping is required
    text_pixels = text_size_in_pixels(text=text, font_family=spec['label-style']['font-family'], font_size=int(spec['label-style']['font-size']), font_weight=spec['label-style']['font-weight'], stroke_width=int(spec['label-style']['stroke-width']))

    if text_pixels[0] > width:
        # wrap if specified
        wrap = int(spec['text-wrap'])
        if wrap > 0:
            text_lines = textwrap.wrap(text=text, width=wrap, break_long_words=False)
        else:
            text_lines = [text]

    else:
        # no need to wrap
        text_lines = [text]


    # create the rect
    svg_group = a_rect(width=width, height=height, rx=spec['rx'], ry=spec['ry'], style=spec['shape-style'])

    # TODO: allow for margins

    # alignments
    x = width / 2
    y = height / 2

    # HACK: calculate a proper dy from font-size
    font_size = int(spec['label-style']['font-size'])
    dy = font_size * 1.1
    the_range = balanced_range(len(text_lines))


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
    if rotation != 'none':
        svg_group.rotate(angle=ROTATION_TO_ANGLE[rotation])

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
    

