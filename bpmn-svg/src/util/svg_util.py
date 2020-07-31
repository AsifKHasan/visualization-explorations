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
def a_circle(radius, spec):
    svg_group = G()

    circle_svg = Circle(cx=radius, cy=radius, r=radius)
    circle_svg.set_style(StyleBuilder(spec['style']).getStyle())

    # add to group
    svg_group.addElement(circle_svg)
    return svg_group, radius * 2, radius * 2

# returns a tuple (svg group, group_width, group_height)
def a_rectangle(width, height, spec):
    svg_group = G()

    rx = spec['rx'] if 'rx' in spec else 0
    ry = spec['ry'] if 'ry' in spec else 0

    rect_svg = Rect(width=width, height=height, rx=rx, ry=ry)
    rect_svg.set_style(StyleBuilder(spec['style']).getStyle())

    # add to group
    svg_group.addElement(rect_svg)
    return svg_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_diamond(diagonal_x, diagonal_y, spec):
    svg_group = G()

    points = [Point(0, diagonal_y/2), Point(diagonal_x/2, 0), Point(diagonal_x, diagonal_y/2), Point(diagonal_x/2, diagonal_y), Point(0, diagonal_y/2)]
    diamond_svg = Polygon(points=points_to_str(points))
    diamond_svg.set_style(StyleBuilder(spec['style']).getStyle())

    # add to group
    svg_group.addElement(diamond_svg)
    return svg_group, diagonal_x, diagonal_y

# returns a tuple (svg group, group_width, group_height)
def two_concentric_circles(outer_radius, inner_radius, outer_circle_spec, inner_circle_spec):
    # outer circle
    outer_circle_group, _, _ = a_circle(radius=outer_radius, spec=outer_circle_spec)
    inner_circle_group, _, _ = a_circle_inside_a_circular_shape(outer_radius=outer_radius, inner_radius=inner_radius, inner_shape_spec=inner_circle_spec)

    outer_circle_group.addElement(inner_circle_group)

    return outer_circle_group, outer_radius * 2, outer_radius * 2

# returns a tuple (svg group, group_width, group_height)
def an_x(width, height, x, spec):
    svg_group = G()

    theta = math.atan(height/(width - x))
    top_cross_point = Point(width/2, math.tan(theta) * (width/2 - x))
    bottom_croos_point = Point(width/2, math.tan(theta) * width/2)

    left_cross_point = Point(math.tan(math.pi/2 - theta) * height/2, height/2)
    right_cross_point = Point(width - math.tan(math.pi/2 - theta) * height/2, height/2)

    # make the X inside the group
    x_points = [Point(0, 0),
                 Point(x, 0),
                 top_cross_point,
                 Point(width - x, 0),
                 Point(width, 0),
                 right_cross_point,
                 Point(width, height),
                 Point(width - x, height),
                 bottom_croos_point,
                 Point(x, height),
                 Point(0, height),
                 left_cross_point]

    x_svg = Polygon(points=points_to_str(x_points))
    x_svg.set_style(StyleBuilder(spec['style']).getStyle())

    # add to group
    svg_group.addElement(x_svg)

    return svg_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_cross(width, height, x_bar_height, y_bar_width, spec):
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
    cross_svg.set_style(StyleBuilder(spec['style']).getStyle())

    # add to group
    svg_group.addElement(cross_svg)

    return svg_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_star(width, height, spec):
    svg_group = G()

    # make the + inside the group
    line1_svg = Line(x1=width * 0.5, y1=height * 0.2, x2=width * 0.5, y2=height * 0.8)
    line1_svg.set_style(StyleBuilder(spec['style']).getStyle())

    line2_svg = Line(x1=width * 0.2, y1=height * 0.5, x2=width * 0.8, y2=height * 0.5)
    line2_svg.set_style(StyleBuilder(spec['style']).getStyle())

    # make the X inside the group
    line3_svg = Line(x1=width * 0.33, y1=height * 0.33, x2=width * 0.67, y2=height * 0.67)
    line3_svg.set_style(StyleBuilder(spec['style']).getStyle())

    line4_svg = Line(x1=width * 0.67, y1=height * 0.33, x2=width * 0.33, y2=height * 0.67)
    line4_svg.set_style(StyleBuilder(spec['style']).getStyle())

    # add to group
    svg_group.addElement(line1_svg)
    svg_group.addElement(line2_svg)
    svg_group.addElement(line3_svg)
    svg_group.addElement(line4_svg)

    return svg_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_clock(radius, spec):
    clock_group_svg, _, _ = a_circle(radius, spec)

    hour_mark_length = radius * 0.3
    minute_hand_length = radius * 0.6
    hour_hand_length = radius * 0.4

    minute_hand_svg = Line(x1=radius, y1=radius, x2=radius, y2=(radius - minute_hand_length))
    minute_hand_svg.set_style(StyleBuilder(spec['style']).getStyle())
    hour_hand_svg = Line(x1=radius, y1=radius, x2=radius + hour_hand_length, y2=radius)
    hour_hand_svg.set_style(StyleBuilder(spec['style']).getStyle())

    clock_group_svg.addElement(minute_hand_svg)
    clock_group_svg.addElement(hour_hand_svg)

    # the hour marks
    center_point = Point(radius, radius)
    for hour in range(0, 12):
        point_on_circle = center_point.to_point(30 * hour, radius)
        point_inside = center_point.to_point(30 * hour, radius - hour_mark_length)
        hour_mark_svg = Line(x1=point_on_circle.x, y1=point_on_circle.y, x2=point_inside.x, y2=point_inside.y)
        hour_mark_svg.set_style(StyleBuilder(spec['style']).getStyle())
        clock_group_svg.addElement(hour_mark_svg)

    # add to group
    return clock_group_svg, radius * 2, radius * 2

# returns a tuple (svg group, group_width, group_height)
def a_page(width, height, spec):
    rect_svg_group, _, _ = a_rectangle(width=width, height=height, spec=spec)

    left_edge = width * 0.1
    right_edge = width * 0.1
    num_lines = 4
    y_gap_between_lines = height / (num_lines + 1)
    for line in range (1, num_lines + 1):
        y_len = line * y_gap_between_lines
        left_point = Point(left_edge, y_len)
        right_point = Point(width - right_edge, y_len)
        line_svg = Line(x1=left_point.x, y1=left_point.y, x2=right_point.x, y2=right_point.y)
        line_svg.set_style(StyleBuilder(spec['style']).getStyle())
        rect_svg_group.addElement(line_svg)

    return rect_svg_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_triangular_rewind(width, height, spec):
    svg_group = G()

    left_arrow_point_left = Point(0, height/2)
    left_arrow_point_top = Point(width/2, 0)
    left_arrow_point_bottom = Point(width/2, height)

    right_arrow_point_left = Point(width/2, height/2)
    right_arrow_point_top = Point(width, 0)
    right_arrow_point_bottom = Point(width, height)

    left_arrow_points = [left_arrow_point_left, left_arrow_point_top, left_arrow_point_bottom]
    right_arrow_points = [right_arrow_point_left, right_arrow_point_top, right_arrow_point_bottom]

    left_arrow_svg = Polygon(points=points_to_str(left_arrow_points))
    left_arrow_svg.set_style(StyleBuilder(spec['style']).getStyle())

    right_arrow_svg = Polygon(points=points_to_str(right_arrow_points))
    right_arrow_svg.set_style(StyleBuilder(spec['style']).getStyle())

    svg_group.addElement(left_arrow_svg)
    svg_group.addElement(right_arrow_svg)

    return svg_group, width, height

# returns a tuple (svg group, group_width, group_height)
def an_upword_arrowhead(width, height, spec):
    mid_point = Point(width/2, height/2)
    top_point = Point(width/2, 0)
    left_point = Point(0, height)
    right_point = Point(width, height)

    arrowhead_points = [mid_point, left_point, top_point, right_point]

    arrowhead_svg = Polygon(points=points_to_str(arrowhead_points))
    arrowhead_svg.set_style(StyleBuilder(spec['style']).getStyle())

    return arrowhead_svg, width, height

# returns a tuple (svg group, group_width, group_height)
def a_right_arrow(width, height, spec):
    arrow_height = height/3

    top_left = Point(0, (height - arrow_height)/2)
    mid_top = Point(width/2, (height - arrow_height)/2)
    top = Point(width/2, 0)
    right = Point(width, height/2)
    bottom = Point(width/2, height)
    mid_bottom = Point(width/2, (height + arrow_height)/2)
    bottom_left = Point(0, (height + arrow_height)/2)

    arrow_points = [top_left, mid_top, top, right, bottom, mid_bottom, bottom_left]

    arrow_svg = Polygon(points=points_to_str(arrow_points))
    arrow_svg.set_style(StyleBuilder(spec['style']).getStyle())

    return arrow_svg, width, height

# returns a tuple (svg group, group_width, group_height)
def a_lightning(width, height, spec):
    diagonal = math.sqrt(width * width + height * height)
    len_mb_mt = (diagonal/2) * 0.3
    len_mt_tl = (diagonal/2) * 0.4
    angle_bl_tr = math.atan(height/width)
    angle_mt_tl = math.pi/2

    bottom_left = Point(0, height)
    mid_top = bottom_left.to_point(-math.degrees(angle_bl_tr), diagonal/2 + len_mb_mt/2)
    mid_bottom = bottom_left.to_point(-math.degrees(angle_bl_tr), diagonal/2 - len_mb_mt/2)
    top_left = mid_top.to_point(-math.degrees(angle_mt_tl + angle_bl_tr), len_mt_tl)

    top_right = Point(width, 0)
    bottom_right = mid_bottom.to_point(math.degrees(angle_mt_tl - angle_bl_tr), len_mt_tl)

    lightning_points = [bottom_left, top_left, mid_top, top_right, bottom_right, mid_bottom]
    # lightning_points = [bottom_left, top_left, mid_top]

    lightning_svg = Polygon(points=points_to_str(lightning_points))
    lightning_svg.set_style(StyleBuilder(spec['style']).getStyle())

    return lightning_svg, width, height

# --------------------------------------------------------------------------------------
# shapes inside a circular shape ---------------------------------------------------------------
# --------------------------------------------------------------------------------------

# returns a tuple (svg group, group_width, group_height)
def a_circle_inside_a_circular_shape(outer_radius, inner_radius, inner_shape_spec):
    pad = outer_radius - inner_radius

    circle_group, width, height = a_circle(inner_radius, spec=inner_shape_spec)

    circle_group_xy = '{0},{1}'.format(pad, pad)
    transformer = TransformBuilder()
    transformer.setTranslation(circle_group_xy)
    circle_group.set_transform(transformer.getTransform())

    return circle_group, width, height

# returns a tuple (svg group, group_width, group_height)
def an_envelop_inside_a_circular_shape(radius, inner_shape_spec):
    pad_x = radius * 0.5
    pad_y = radius * 0.6

    width = (radius - pad_x) * 2
    height = (radius - pad_y) * 2

    envelop_group, envelop_width, envelop_height = a_rectangle(width, height, spec=inner_shape_spec)

    # two lines from center to top left and top right to give it an envelop look
    center_point = Point(width/2, height/2)
    top_left_point = Point(0, 0)
    top_right_point = Point(width, 0)
    points = [top_left_point, center_point, top_right_point, top_left_point]

    # the lines' color is shapes stroke
    line_style = StyleBuilder(inner_shape_spec['style']).getStyle()
    line1_svg = Line(x1=0, y1=0, x2=width/2, y2=height/2, style=inner_shape_spec['style'])
    line2_svg = Line(x1=width/2, y1=height/2, x2=width, y2=0, style=inner_shape_spec['style'])
    line1_svg.set_style(line_style)
    line2_svg.set_style(line_style)
    envelop_group.addElement(line1_svg)
    envelop_group.addElement(line2_svg)

    return envelop_group, width, height

# returns a tuple (svg group, group_width, group_height)
def an_equilateral_pentagon_inside_a_circular_shape(radius, inner_shape_spec):
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
    pentagon_svg.set_style(StyleBuilder(inner_shape_spec['style']).getStyle())

    # add to group
    svg_group.addElement(pentagon_svg)
    return svg_group, radius * 2, radius * 2

# returns a tuple (svg group, group_width, group_height)
def an_equilateral_triangle_inside_a_circular_shape(radius, inner_shape_spec):
    # in a trangle ABC, A is alwys the top vertex
    svg_group = G()

    pad = radius * 0.4
    center_to_vertex = radius - pad
    center_point = Point(radius, radius)
    point_a = center_point.to_point(-90, center_to_vertex)
    point_b = center_point.to_point(-210, center_to_vertex)
    point_c = center_point.to_point(-330, center_to_vertex)
    points = [point_a, point_b, point_c, point_a]
    triangle_svg = Polygon(points=points_to_str(points))
    triangle_svg.set_style(StyleBuilder(inner_shape_spec['style']).getStyle())

    # add to group
    svg_group.addElement(triangle_svg)
    return svg_group, radius * 2, radius * 2

# returns a tuple (svg group, group_width, group_height)
def a_cross_inside_a_circular_shape(radius, inner_shape_spec):
    pad = radius * 0.5
    width = radius * 2 - pad * 2
    height = radius * 2 - pad * 2
    x_bar_height = radius * 0.2
    y_bar_width = radius * 0.2
    cross_group, _, _ = a_cross(width=width, height=height, x_bar_height=x_bar_height, y_bar_width=y_bar_width, spec=inner_shape_spec)

    return cross_group, width, height

# returns a tuple (svg group, group_width, group_height)
def an_x_inside_a_circular_shape(radius, inner_shape_spec):
    pad = radius * 0.5
    width = radius * 2 - pad * 2
    height = radius * 2 - pad * 2
    x = width * 0.3
    x_group, _, _ = an_x(width=width, height=height, x=x, spec=inner_shape_spec)

    return x_group, width, height

# returns a tuple (svg group, group_width, group_height)
def something_missing_inside_a_circular_shape(radius, inner_shape_spec):
    pad = radius * 0.5
    width = radius * 2 - pad * 2
    height = radius * 2 - pad * 2
    x = width * 0.2
    inner_shape_spec = {'style': {'fill': '#FFFFFF', 'stroke-width': 1, 'stroke': '#FF8080'}}
    missing_group, _, _ = an_x(width=width, height=height, x=x, spec=inner_shape_spec)

    return missing_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_clock_inside_a_circular_shape(radius, inner_shape_spec):
    pad = radius * 0.2

    clock_group, width, height = a_clock(radius - pad, spec=inner_shape_spec)

    return clock_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_page_inside_a_circular_shape(radius, inner_shape_spec):
    pad_x = radius * 0.5
    pad_y = radius * 0.4
    width = (radius - pad_x) * 2
    height = (radius - pad_y) * 2

    page_group, _, _ = a_page(width=width, height=height, spec=inner_shape_spec)

    return page_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_triangular_rewind_inside_a_circular_shape(radius, inner_shape_spec):
    width = radius * 1.1
    height = radius * 1.0

    triangular_rewind_group, _, _ = a_triangular_rewind(width=width, height=height, spec=inner_shape_spec)

    return triangular_rewind_group, width, height

# returns a tuple (svg group, group_width, group_height)
def an_upword_arrowhead_inside_a_circular_shape(radius, inner_shape_spec):
    width = radius * 1.3
    height = radius * 1.3

    arrowhead_group, _, _ = an_upword_arrowhead(width=width, height=height, spec=inner_shape_spec)

    return arrowhead_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_right_arrow_inside_a_circular_shape(radius, inner_shape_spec):
    width = radius * 1.2
    height = radius * 1.0

    arrow_group, _, _ = a_right_arrow(width=width, height=height, spec=inner_shape_spec)

    return arrow_group, width, height

# returns a tuple (svg group, group_width, group_height)
def a_lightning_inside_a_circular_shape(radius, inner_shape_spec):
    width = radius * 1.0
    height = radius * 1.2

    lightning_group, _, _ = a_lightning(width=width, height=height, spec=inner_shape_spec)

    return lightning_group, width, height

# --------------------------------------------------------------------------------------
# shapes inside a rectangle ---------------------------------------------------------------
# --------------------------------------------------------------------------------------

# returns a tuple (svg group, group_width, group_height)
def a_cross_in_a_rectangle(width, height, rx, ry, rect_spec, cross_spec):
    rect_group, rect_group_width, rect_group_height = a_rectangle(width, height, rect_spec)
    x_bar_height = height * 0.2
    y_bar_width = width * 0.2
    cross_group, cross_group_width, cross_group_height = a_cross(width=width, height=height, x_bar_height=x_bar_height, y_bar_width=y_bar_width, spec=cross_spec)

    rect_group.addElement(cross_group)

    return rect_group, rect_group_width, rect_group_height

# returns a tuple (svg group, group_width, group_height)
def text_inside_a_rectangle(text, min_width, max_width, rect_spec, text_spec, debug_enabled=False):

    # to get the width, height we need to calculate the text rendering function
    vertical_text = text_spec['vertical-text']
    text_rendering_hint = break_text_inside_rect(
                                text=text,
                                font_family=text_spec['style']['font-family'],
                                font_size=text_spec['style']['font-size'],
                                max_lines=text_spec['max-lines'],
                                min_width=min_width,
                                max_width=max_width,
                                pad_spec=rect_spec['pad-spec'],
                                debug_enabled=debug_enabled)

    if vertical_text:
        width = text_rendering_hint[2]
        height = text_rendering_hint[1]
    else:
        width = text_rendering_hint[1]
        height = text_rendering_hint[2]

    # create the rectangle
    svg_group, group_width, group_height = a_rectangle(width=width, height=height, spec=rect_spec)

    # render the text
    text_svg = center_text_inside_rect(
                    text=text_rendering_hint[0],
                    width=group_width,
                    height=group_height,
                    style=text_spec['style'],
                    vertical_text=vertical_text,
                    pad_spec=rect_spec['pad-spec'])

    # add the svg's into group
    svg_group.addElement(text_svg)

    return svg_group, group_width, group_height


# --------------------------------------------------------------------------------------
# shapes inside a circle ---------------------------------------------------------------
# --------------------------------------------------------------------------------------

# returns a tuple (svg group, group_width, group_height)
def a_cross_in_a_circle(radius, circle_spec, cross_spec):
    circle_group, circle_group_width, circle_group_height = a_circle(radius, circle_spec)

    pad = radius * 0.4
    width = radius * 2 - pad * 2
    height = radius * 2 - pad * 2
    x_bar_height = radius * 0.3
    y_bar_width = radius * 0.3
    cross_group, cross_group_width, cross_group_height = a_cross(width=width, height=height, x_bar_height=x_bar_height, y_bar_width=y_bar_width, spec=cross_spec)

    cross_group_xy = '{0},{1}'.format(pad, pad)
    transformer = TransformBuilder()
    transformer.setTranslation(cross_group_xy)
    cross_group.set_transform(transformer.getTransform())

    circle_group.addElement(cross_group)

    return circle_group, circle_group_width, circle_group_height

# returns a tuple (svg group, group_width, group_height)
def an_equilateral_pentagon_in_a_circle(radius, circle_spec, pentagon_spec):
    circle_group, circle_group_width, circle_group_height = a_circle(radius, circle_spec)
    pentagon_group, pentagon_group_width, pentagon_group_height = an_equilateral_pentagon_inside_a_circular_shape(radius, pentagon_spec)

    circle_group.addElement(pentagon_group)

    return circle_group, circle_group_width, circle_group_height

# returns a tuple (svg group, group_width, group_height)
def an_equilateral_pentagon_in_two_concentric_circles(outer_radius, inner_radius, outer_circle_spec, inner_circle_spec, pad, pentagon_spec):
    svg_group = G()

    circle_group, circle_group_width, circle_group_height = two_concentric_circles(outer_radius=outer_radius, inner_radius=inner_radius, outer_circle_spec=outer_circle_spec, inner_circle_spec=inner_circle_spec)
    pentagon_group, pentagon_group_width, pentagon_group_height = an_equilateral_pentagon_inside_a_circular_shape(outer_radius, pentagon_spec)

    # add to group
    svg_group.addElement(circle_group)
    svg_group.addElement(pentagon_group)

    return svg_group, circle_group_width, circle_group_height


# --------------------------------------------------------------------------------------
# mesecllaneous utilities
# --------------------------------------------------------------------------------------

# returns a tuple (svg group, group_width, group_height)
def envelop_and_center_in_a_rectangle(svg, svg_width, svg_height, rect_spec):
    rectangle_width = svg_width + rect_spec['pad-spec']['left'] + rect_spec['pad-spec']['right']
    rectangle_height = svg_height + rect_spec['pad-spec']['top'] + rect_spec['pad-spec']['bottom']
    rectangle_group, rectangle_width, rectangle_height = a_rectangle(rectangle_width, rectangle_height, rect_spec)

    svg_xy = '{0},{1}'.format(rect_spec['pad-spec']['left'], rect_spec['pad-spec']['top'])
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
