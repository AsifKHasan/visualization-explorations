#!/usr/bin/env python3
'''
'''
from pysvg.builders import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *

import math
from PIL import ImageFont

import textwrap

from util.logger import *
from util.geometry import Point
from util.helpers import *

# returns a tuple (svg group, group_width, group_height)
def circle(radius, style):
    svg_group = G()

    circle_svg = Circle(cx=radius, cy=radius, r=radius)
    circle_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(circle_svg)
    return svg_group, radius * 2, radius * 2

# returns a tuple (svg group, group_width, group_height)
def rectangle(width, height, rx, ry, style):
    svg_group = G()

    rect_svg = Rect(width=width, height=height, rx=rx, ry=ry)
    rect_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(rect_svg)
    return svg_group, width, height

# returns a tuple (svg group, group_width, group_height)
def diamond(diagonal_x, diagonal_y, style):
    svg_group = G()

    points = [Point(0, diagonal_y/2), Point(diagonal_x/2, 0), Point(diagonal_x, diagonal_y/2), Point(diagonal_x/2, diagonal_y), Point(0, diagonal_y/2)]
    diamond_svg = Polyline(points=points_to_str(points))
    diamond_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(diamond_svg)
    return svg_group, diagonal_x, diagonal_y

# returns a tuple (svg group, group_width, group_height)
def circle_with_circle_inside(outer_radius, inner_radius, outer_style, inner_style):
    svg_group = G()

    # outer circle
    outer_circle_svg = Circle(cx=outer_radius, cy=outer_radius, r=outer_radius)
    outer_circle_svg.set_style(StyleBuilder(outer_style).getStyle())

    # inner circle
    inner_circle_svg = Circle(cx=outer_radius, cy=outer_radius, r=inner_radius)
    inner_circle_svg.set_style(StyleBuilder(inner_style).getStyle())

    # add to group
    svg_group.addElement(outer_circle_svg)
    svg_group.addElement(inner_circle_svg)

    return svg_group, outer_radius * 2, outer_radius * 2

# returns a tuple (svg group, group_width, group_height)
def rectangle_with_cross_inside(width, height, rx, ry, style, x_style):
    svg_group, group_width, group_height = rectangle(width, height, rx, ry, style)

    # make the X inside the diamond
    line1_svg = Line(x1=width * 0.2, y1=height * 0.5, x2=width * 0.8, y2=height * 0.5)
    line1_svg.set_style(StyleBuilder(x_style).getStyle())

    line2_svg = Line(x1=width * 0.5, y1=height * 0.2, x2=width * 0.5, y2=height * 0.8)
    line2_svg.set_style(StyleBuilder(x_style).getStyle())

    # add to group
    svg_group.addElement(line1_svg)
    svg_group.addElement(line2_svg)

    return svg_group, group_width, group_height

# returns a tuple (svg group, group_width, group_height)
def diaomond_with_x_inside(diagonal_x, diagonal_y, style, x_style):
    svg_group, group_width, group_height = diamond(diagonal_x, diagonal_y, style)

    # make the X inside the diamond
    line1_svg = Line(x1=diagonal_x * 0.33, y1=diagonal_y * 0.33, x2=diagonal_x * 0.67, y2=diagonal_y * 0.67)
    line1_svg.set_style(StyleBuilder(x_style).getStyle())

    line2_svg = Line(x1=diagonal_x * 0.67, y1=diagonal_y * 0.33, x2=diagonal_x * 0.33, y2=diagonal_y * 0.67)
    line2_svg.set_style(StyleBuilder(x_style).getStyle())

    # add to group
    svg_group.addElement(line1_svg)
    svg_group.addElement(line2_svg)

    return svg_group, group_width, group_height

# returns a tuple (svg group, group_width, group_height)
def diaomond_with_cross_inside(diagonal_x, diagonal_y, style, x_style):
    svg_group, group_width, group_height = diamond(diagonal_x, diagonal_y, style)

    # make the X inside the diamond
    line1_svg = Line(x1=diagonal_x * 0.5, y1=diagonal_y * 0.2, x2=diagonal_x * 0.5, y2=diagonal_y * 0.8)
    line1_svg.set_style(StyleBuilder(x_style).getStyle())

    line2_svg = Line(x1=diagonal_x * 0.2, y1=diagonal_y * 0.5, x2=diagonal_x * 0.8, y2=diagonal_y * 0.5)
    line2_svg.set_style(StyleBuilder(x_style).getStyle())

    # add to group
    svg_group.addElement(line1_svg)
    svg_group.addElement(line2_svg)

    return svg_group, group_width, group_height

# returns a tuple (svg group, group_width, group_height)
def diaomond_with_circle_inside(diagonal_x, diagonal_y, style, x_style):
    svg_group, group_width, group_height = diamond(diagonal_x, diagonal_y, style)

    # make the circle inside the diamond
    circle_svg = Circle(cx=diagonal_x * 0.5, cy=diagonal_y * 0.5, r=min(diagonal_x, diagonal_y) * 0.25)
    circle_svg.set_style(StyleBuilder(x_style).getStyle())

    # add to group
    svg_group.addElement(circle_svg)

    return svg_group, group_width, group_height

# returns a tuple (svg group, group_width, group_height)
def rectangle_with_text_inside(text, min_width, max_width, specs, debug_enabled=False):

    # to get the width, height we need to calculate the text rendering function
    vertical_text = specs['vertical-text']
    text_rendering_hint = break_text_inside_rect(
                                text=text,
                                font_family=specs['text-style']['font-family'],
                                font_size=specs['text-style']['font-size'],
                                max_lines=specs['max-lines'],
                                min_width=min_width,
                                max_width=max_width,
                                pad_spec=specs['pad-spec'],
                                debug_enabled=debug_enabled)

    if vertical_text:
        width = text_rendering_hint[2]
        height = text_rendering_hint[1]
    else:
        width = text_rendering_hint[1]
        height = text_rendering_hint[2]

    rx = specs['rx'] if 'rx' in specs else 0
    ry = specs['ry'] if 'ry' in specs else 0

    # create the rectangle
    svg_group, group_width, group_height = rectangle(width=width, height=height, rx=rx, ry=ry, style=specs['style'])

    # render the text
    text_svg = center_text_inside_rect(
                    text=text_rendering_hint[0],
                    width=group_width,
                    height=group_height,
                    style=specs['text-style'],
                    vertical_text=vertical_text,
                    pad_spec=specs['pad-spec'])

    # add the svg's into group
    svg_group.addElement(text_svg)

    return svg_group, group_width, group_height

# returns a tuple (svg group, group_width, group_height)
def align_and_combine_horizontally(svg_elements):
    svg_group = G()

    # we are aligning horizontally, so we need the height of the element which is maximum
    group_height = 0
    for svg_element in svg_elements:
        group_height = max(group_height, svg_element.specs['height'])

    # now we place the elements in the group side by side with height adjustment
    group_width = 0
    for svg_element in svg_elements:
        element_svg = svg_element.group
        height_to_adjust = (group_height - svg_element.specs['height']) / 2
        # now do the transformation
        element_svg_xy = '{0},{1}'.format(group_width, height_to_adjust)
        transformer = TransformBuilder()
        transformer.setTranslation(element_svg_xy)
        element_svg.set_transform(transformer.getTransform())
        svg_group.addElement(element_svg)

        group_width = group_width + svg_element.specs['width']

    return svg_group, group_width, group_height

def center_text_inside_rect(text, width, height, style, vertical_text=False, pad_spec=None, text_wrap_at=0, debug=False):
    if pad_spec is None:
        pad_spec = {'left': 10, 'top': 10, 'right': 10, 'bottom': 10}

    if vertical_text:
        style['writing-mode'] = 'vertical-lr'
    else:
        style['writing-mode'] = 'horizontal-tb'

    shape_width = width - pad_spec['left'] - pad_spec['right']
    shape_height = height - pad_spec['top'] - pad_spec['bottom']
    svg = Svg(pad_spec['left'], pad_spec['top'], width=shape_width, height=shape_height)

    t = Text(None)
    t.set_style(StyleBuilder(style).getStyle())

    # if text is a list, do not procees, use the list
    if type(text) is list:
        text_list = text
    else:
        if text_wrap_at > 0:
            text_list = textwrap.wrap(text=text, width=text_wrap_at, break_long_words=False)
        else:
            text_list = [text]

    ems = em_range(len(text_list))
    if vertical_text:
        ems.reverse()

    count = 0
    for text_line in text_list:
        em_text = '{0}em'.format(ems[count])
        if vertical_text:
            ts = Tspan(x="50%", y="50%", dx=em_text)
        else:
            ts = Tspan(x="50%", y="50%", dy=em_text)

        ts.appendTextContent(text_line)
        t.addElement(ts)
        count = count + 1

    svg.addElement(t)

    return svg
