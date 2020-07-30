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

# --------------------------------------------------------------------------------------
# basic shapes ---------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

# returns a tuple (svg group, group_width, group_height)
def a_circle(radius, style):
    svg_group = G()

    circle_svg = Circle(cx=radius, cy=radius, r=radius)
    circle_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(circle_svg)
    return svg_group, radius * 2, radius * 2

# returns a tuple (svg group, group_width, group_height)
def a_rectangle(width, height, rx, ry, style):
    svg_group = G()

    rect_svg = Rect(width=width, height=height, rx=rx, ry=ry)
    rect_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(rect_svg)
    return svg_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_diamond(diagonal_x, diagonal_y, style):
    svg_group = G()

    points = [Point(0, diagonal_y/2), Point(diagonal_x/2, 0), Point(diagonal_x, diagonal_y/2), Point(diagonal_x/2, diagonal_y), Point(0, diagonal_y/2)]
    diamond_svg = Polygon(points=points_to_str(points))
    diamond_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(diamond_svg)
    return svg_group, diagonal_x, diagonal_y

# returns a tuple (svg group, group_width, group_height)
def two_concentric_circles(outer_radius, inner_radius, outer_style, inner_style):
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
def an_x(width, height, style):
    svg_group = G()

    # make the X inside the group
    line1_svg = Line(x1=width * 0.33, y1=height * 0.33, x2=width * 0.67, y2=height * 0.67)
    line1_svg.set_style(StyleBuilder(style).getStyle())

    line2_svg = Line(x1=width * 0.67, y1=height * 0.33, x2=width * 0.33, y2=height * 0.67)
    line2_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(line1_svg)
    svg_group.addElement(line2_svg)

    return svg_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_cross(width, height, x_bar_height, y_bar_width, style):
    svg_group = G()

    # make the X inside the group
    cross_points = [Point(0, (height + x_bar_height)/2),
                    Point(0, (height - x_bar_height)/2),
                    Point((width - y_bar_width)/2, (height - x_bar_height)/2),
                    Point((width - y_bar_width)/2, 0),
                    Point((width + y_bar_width)/2, 0),
                    Point((width + y_bar_width)/2, (height - x_bar_height)/2),
                    Point(width, (height - x_bar_height)/2),
                    Point(width, (height + x_bar_height)/2),
                    Point((width + y_bar_width)/2, (height + x_bar_height)/2),
                    Point((width + y_bar_width)/2, height),
                    Point((width - y_bar_width)/2, height),
                    Point((width - y_bar_width)/2, (height + x_bar_height)/2)]

    cross_svg = Polygon(points=points_to_str(cross_points))
    cross_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(cross_svg)

    return svg_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_star(width, height, style):
    svg_group = G()

    # make the + inside the group
    line1_svg = Line(x1=width * 0.5, y1=height * 0.2, x2=width * 0.5, y2=height * 0.8)
    line1_svg.set_style(StyleBuilder(style).getStyle())

    line2_svg = Line(x1=width * 0.2, y1=height * 0.5, x2=width * 0.8, y2=height * 0.5)
    line2_svg.set_style(StyleBuilder(style).getStyle())

    # make the X inside the group
    line3_svg = Line(x1=width * 0.33, y1=height * 0.33, x2=width * 0.67, y2=height * 0.67)
    line3_svg.set_style(StyleBuilder(style).getStyle())

    line4_svg = Line(x1=width * 0.67, y1=height * 0.33, x2=width * 0.33, y2=height * 0.67)
    line4_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(line1_svg)
    svg_group.addElement(line2_svg)
    svg_group.addElement(line3_svg)
    svg_group.addElement(line4_svg)

    return svg_group, width, height


# --------------------------------------------------------------------------------------
# shapes inside a circular shape ---------------------------------------------------------------
# --------------------------------------------------------------------------------------

# returns a tuple (svg group, group_width, group_height)
def an_envelop_inside_a_circular_shape(radius, style):
    svg_group = G()

    pad_x = radius * 0.5
    pad_y = radius * 0.6

    width = (radius - pad_x) * 2
    height = (radius - pad_y) * 2

    envelop_group, envelop_width, envelop_height = a_rectangle(width, height, 0, 0, style)

    # two lines from center to top left and top right to give it an envelop look
    center_point = Point(width/2, height/2)
    top_left_point = Point(0, 0)
    top_right_point = Point(width, 0)
    points = [top_left_point, center_point, top_right_point, top_left_point]

    # the lines' color is shapes stroke
    line_style = StyleBuilder(style).getStyle()
    line1_svg = Line(x1=0, y1=0, x2=width/2, y2=height/2, style=style)
    line2_svg = Line(x1=width/2, y1=height/2, x2=width, y2=0, style=style)
    line1_svg.set_style(line_style)
    line2_svg.set_style(line_style)
    envelop_group.addElement(line1_svg)
    envelop_group.addElement(line2_svg)

    envelop_group_xy = '{0},{1}'.format(pad_x, pad_y)
    transformer = TransformBuilder()
    transformer.setTranslation(envelop_group_xy)
    envelop_group.set_transform(transformer.getTransform())

    # add to group
    svg_group.addElement(envelop_group)
    return svg_group, radius * 2, radius * 2

# returns a tuple (svg group, group_width, group_height)
def an_equilateral_pentagon_inside_a_circular_shape(radius, style):
    svg_group = G()

    pad = radius * 0.5
    center_to_vertex = radius - pad
    center_point = Point(radius, radius)
    point_a = center_point.to_point(-90 - (72 * 0), center_to_vertex)
    point_b = center_point.to_point(-90 - (72 * 1), center_to_vertex)
    point_c = center_point.to_point(-90 - (72 * 2), center_to_vertex)
    point_d = center_point.to_point(-90 - (72 * 3), center_to_vertex)
    point_e = center_point.to_point(-90 - (72 * 4), center_to_vertex)
    points = [point_a, point_b, point_c, point_d, point_e, point_a]
    pentagon_svg = Polygon(points=points_to_str(points))
    pentagon_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(pentagon_svg)
    return svg_group, radius * 2, radius * 2

# returns a tuple (svg group, group_width, group_height)
def an_equilateral_triangle_inside_a_circular_shape(radius, style):
    # in a trangle ABC, A is alwys the top vertex
    svg_group = G()

    pad = radius * 0.5
    center_to_vertex = radius - pad
    center_point = Point(radius, radius)
    point_a = center_point.to_point(-90, center_to_vertex)
    point_b = center_point.to_point(-210, center_to_vertex)
    point_c = center_point.to_point(-330, center_to_vertex)
    points = [point_a, point_b, point_c, point_a]
    triangle_svg = Polygon(points=points_to_str(points))
    triangle_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(triangle_svg)
    return svg_group, radius * 2, radius * 2

# returns a tuple (svg group, group_width, group_height)
def a_cross_inside_a_circular_shape(radius, style):
    svg_group = G()

    pad = radius * 0.5
    width = radius * 2 - pad * 2
    height = radius * 2 - pad * 2
    x_bar_height = radius * 0.2
    y_bar_width = radius * 0.2
    cross_group_svg, _, _ = a_cross(width=width, height=height, x_bar_height=x_bar_height, y_bar_width=y_bar_width, style=style)

    cross_group_xy = '{0},{1}'.format(pad, pad)
    transformer = TransformBuilder()
    transformer.setTranslation(cross_group_xy)
    cross_group_svg.set_transform(transformer.getTransform())

    # add to group
    svg_group.addElement(cross_group_svg)
    return svg_group, radius * 2, radius * 2

# returns a tuple (svg group, group_width, group_height)
def something_missing_inside_a_circular_shape(radius, style):
    svg_group = G()
    width = radius * 2
    height = radius * 2
    style = {'fill': '#FFFFFF', 'stroke-width': 2, 'stroke': '#FF8080'}
    missing_svg, _, _ = an_x(width=width, height=height, style=style)
    missing_svg.set_style(StyleBuilder(style).getStyle())

    # add to group
    svg_group.addElement(missing_svg)
    return svg_group, radius * 2, radius * 2


# --------------------------------------------------------------------------------------
# shapes inside a rectangle ---------------------------------------------------------------
# --------------------------------------------------------------------------------------

# returns a tuple (svg group, group_width, group_height)
def a_cross_in_a_rectangle(width, height, rx, ry, rect_style, cross_style):
    svg_group = G()

    rect_group, rect_group_width, rect_group_height = a_rectangle(width, height, rx, ry, rect_style)
    x_bar_height = height * 0.2
    y_bar_width = width * 0.2
    cross_group, cross_group_width, cross_group_height = a_cross(width=width, height=height, x_bar_height=x_bar_height, y_bar_width=y_bar_width, style=cross_style)

    # add to group
    svg_group.addElement(rect_group)
    svg_group.addElement(cross_group)

    return svg_group, rect_group_width, rect_group_height

# returns a tuple (svg group, group_width, group_height)
def text_inside_a_rectangle(text, min_width, max_width, rect_specs, text_specs, debug_enabled=False):

    # to get the width, height we need to calculate the text rendering function
    vertical_text = text_specs['vertical-text']
    text_rendering_hint = break_text_inside_rect(
                                text=text,
                                font_family=text_specs['style']['font-family'],
                                font_size=text_specs['style']['font-size'],
                                max_lines=text_specs['max-lines'],
                                min_width=min_width,
                                max_width=max_width,
                                pad_spec=rect_specs['pad-spec'],
                                debug_enabled=debug_enabled)

    if vertical_text:
        width = text_rendering_hint[2]
        height = text_rendering_hint[1]
    else:
        width = text_rendering_hint[1]
        height = text_rendering_hint[2]

    rx = rect_specs['rx'] if 'rx' in rect_specs else 0
    ry = rect_specs['ry'] if 'ry' in rect_specs else 0

    # create the rectangle
    svg_group, group_width, group_height = a_rectangle(width=width, height=height, rx=rx, ry=ry, style=rect_specs['style'])

    # render the text
    text_svg = center_text_inside_rect(
                    text=text_rendering_hint[0],
                    width=group_width,
                    height=group_height,
                    style=text_specs['style'],
                    vertical_text=vertical_text,
                    pad_spec=rect_specs['pad-spec'])

    # add the svg's into group
    svg_group.addElement(text_svg)

    return svg_group, group_width, group_height


# --------------------------------------------------------------------------------------
# shapes inside a circle ---------------------------------------------------------------
# --------------------------------------------------------------------------------------

# returns a tuple (svg group, group_width, group_height)
def a_cross_in_a_circle(radius, circle_style, cross_style):
    svg_group = G()

    circle_group, circle_group_width, circle_group_height = a_circle(radius, circle_style)

    pad = radius * 0.4
    width = radius * 2 - pad * 2
    height = radius * 2 - pad * 2
    x_bar_height = radius * 0.3
    y_bar_width = radius * 0.3
    cross_group, cross_group_width, cross_group_height = a_cross(width=width, height=height, x_bar_height=x_bar_height, y_bar_width=y_bar_width, style=cross_style)

    cross_group_xy = '{0},{1}'.format(pad, pad)
    transformer = TransformBuilder()
    transformer.setTranslation(cross_group_xy)
    cross_group.set_transform(transformer.getTransform())

    # add to group
    svg_group.addElement(circle_group)
    svg_group.addElement(cross_group)

    return svg_group, circle_group_width, circle_group_height

# returns a tuple (svg group, group_width, group_height)
def an_equilateral_pentagon_in_a_circle(radius, circle_style, pentagon_style):
    svg_group = G()

    circle_group, circle_group_width, circle_group_height = a_circle(radius, circle_style)
    pentagon_group, pentagon_group_width, pentagon_group_height = an_equilateral_pentagon_inside_a_circular_shape(radius, pentagon_style)

    # add to group
    svg_group.addElement(circle_group)
    svg_group.addElement(pentagon_group)

    return svg_group, circle_group_width, circle_group_height

# returns a tuple (svg group, group_width, group_height)
def an_equilateral_pentagon_in_two_concentric_circles(outer_radius, inner_radius, outer_style, inner_style, pad, pentagon_style):
    svg_group = G()

    circle_group, circle_group_width, circle_group_height = two_concentric_circles(outer_radius=outer_radius, inner_radius=inner_radius, outer_style=outer_style, inner_style=inner_style)
    pentagon_group, pentagon_group_width, pentagon_group_height = an_equilateral_pentagon_inside_a_circular_shape(outer_radius, pentagon_style)

    # add to group
    svg_group.addElement(circle_group)
    svg_group.addElement(pentagon_group)

    return svg_group, circle_group_width, circle_group_height


# --------------------------------------------------------------------------------------
# mesecllaneous utilities
# --------------------------------------------------------------------------------------

# returns a tuple (svg group, group_width, group_height)
def envelop_and_center_in_a_rectangle(svg, svg_width, svg_height, rect_specs):
    rx = rect_specs['rx'] if 'rx' in rect_specs else 0
    ry = rect_specs['ry'] if 'ry' in rect_specs else 0
    rectangle_width = svg_width + rect_specs['pad-spec']['left'] + rect_specs['pad-spec']['right']
    rectangle_height = svg_height + rect_specs['pad-spec']['top'] + rect_specs['pad-spec']['bottom']
    rectangle_group, rectangle_width, rectangle_height = a_rectangle(rectangle_width, rectangle_height, rx, ry, rect_specs['style'])

    svg_xy = '{0},{1}'.format(rect_specs['pad-spec']['left'], rect_specs['pad-spec']['top'])
    transformer = TransformBuilder()
    transformer.setTranslation(svg_xy)
    svg.set_transform(transformer.getTransform())

    # add the svg into group
    rectangle_group.addElement(svg)

    return rectangle_group, rectangle_width, rectangle_height

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

def radius_of_the_circle_inside_the_diamond(width, height):
    theta = math.atan(max((width, height))/min(width, height))
    return math.sin(theta) * min(width, height)/2
