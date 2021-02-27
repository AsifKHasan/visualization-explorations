#!/usr/bin/env python3
'''
'''
import sys
import math
from PIL import ImageFont

import random
import textwrap
import string

from util.logger import *
from util.geometry import Point


font_spec = {
    'arial' : {
        'win32' : 'arial',
        'linux' : '/usr/share/fonts/truetype/msttcorefonts/arial.ttf',
        'darwin' : '/Library/Fonts/Arial.ttf'
    },
    'arial-bold' : {
        'win32' : 'arialbd',
        'linux' : 'A/usr/share/fonts/truetype/msttcorefonts/arialbd.ttf',
        'darwin' : '/Library/Fonts/Arial Bold.ttf'
    },
    'calibri' : {
        'win32' : 'calibri',
        'linux' : 'Calibri.ttf',
        'darwin' : '/Library/Fonts/Calibri.ttf'
    },
    'calibri-bold' : {
        'win32' : 'calibrib',
        'linux' : 'Calibri Bold.ttf',
        'darwin' : '/Library/Fonts/Calibri Bold.ttf'
    },
}

#   -----------------------------------------------------------------------------------------------------------------------------------------------------
#   internal utility functions
#   -----------------------------------------------------------------------------------------------------------------------------------------------------
'''
    text        : text that needs to be fitted
    font_family : the font to render the text in
    font_size   : font size of the text
    font_weight : the font weight to render the text in
    stroke_width: the stroke width to render the text in
    max_lines   : maximum lines the text can be broken into
    min_width   : returned width can not be less than this
    max_width   : returned width can not be more than this
    pad_spec    : padding specifications

    returns     (text_lines, width, height)
'''
def break_text_inside_rect(text, font_family, font_size, font_weight, stroke_width, max_lines, min_width, max_width, pad_spec=None, debug_enabled=False):
    if pad_spec is None:
        pad_spec = {'left': 10, 'top': 10, 'right': 10, 'bottom': 10}

    # first see the text size in pixel
    text_size = text_size_in_pixels(text, font_family, font_size, font_weight=font_weight, stroke_width=stroke_width)
    # debug('{0} : ({1}, {2})'.format(text, text_size[0], text_size[1]))

    min_width = min_width - pad_spec['left'] - pad_spec['right']
    max_width = max_width - pad_spec['left'] - pad_spec['right']

    # if the width < min_width, we are fine
    if text_size[0] <= min_width:
        width = min_width + pad_spec['left'] + pad_spec['right']
        height = text_size[1] + pad_spec['top'] + pad_spec['bottom']
        if debug_enabled: debug('text [{0} with font size {1} : ({2})] is below min_width [{3}]. computed width, height is [{4}, {5}]]'.format(text, font_size, text_size[0], min_width, width, height))
        return ([text], width, height)

    # text size exceeds min_width, if it does not exceed min_width by more than 20% and less than mx width, we just adjust width
    if text_size[0] <= min(min_width * 1.2, max_width):
        width = text_size[0] + pad_spec['left'] + pad_spec['right']
        height = text_size[1] + pad_spec['top'] + pad_spec['bottom']
        if debug_enabled: debug('text [{0} with font size {1} : ({2})] is within 20% margin of min_width [{3}]. computed width, height is [{4}, {5}]'.format(text, font_size, text_size[0], min_width, width, height))
        return ([text], width, height)

    # well, text size exceeds min_width by a wider margin, we have to break the text into multiple lines
    # let us check how many lines we should have if we want to fit it into max_width
    approximate_lines = math.ceil(text_size[0] / max_width)
    if debug_enabled: debug('text [{0} ({1})] will break into {2} lines within max width {3}'.format(text, text_size[0], approximate_lines, max_width))

    # if this exceeds the max_line, we have a problem, the output will look bad and we will need to make it as many line as we need
    # we will actually show upto max_lines
    if approximate_lines > max_lines:
        text_wrap_at = math.ceil(len(text) / approximate_lines)
        text_lines = textwrap.wrap(text=text, width=text_wrap_at, break_long_words=False)
        width = 0
        height = pad_spec['top'] + pad_spec['bottom']
        for line in text_lines[:max_lines]:
            line_size = text_size_in_pixels(line, font_family, font_size, font_weight=font_weight, stroke_width=stroke_width)
            width = max(min_width, width, line_size[0])
            height = height + line_size[1] * 1.5

        if debug_enabled: debug('text [{0} ({1})] truncated down into [{2}] lines. computed width, height is [{3}, {4}]'.format(text, text_size[0], len(text_lines[:max_lines]), width, height))

        width = width + pad_spec['left'] + pad_spec['right']
        return (text_lines[:max_lines], width, height)

    # now we know that we can be between 2 to max_lines, our target will be to have fewer lines without crossing max_width
    # start iteration
    for break_into in range(2, max_lines + 1):
        # break the text into equal sized parts (for better visuals)
        text_wrap_at = math.ceil(len(text) / break_into)
        text_lines = textwrap.wrap(text=text, width=text_wrap_at, break_long_words=False)
        width = 0
        height = pad_spec['top'] + pad_spec['bottom']
        for line in text_lines:
            line_size = text_size_in_pixels(line, font_family, font_size, font_weight=font_weight, stroke_width=stroke_width)
            width = max(min_width, width, line_size[0])
            height = height + line_size[1] * 1.5

        # if we have not crossed max_width, we can stick to this
        if width <= max_width:
            if debug_enabled: debug('text [{0} ({1})] broken down into [{2}]. computed width, height is [{3}, {4}]'.format(text, text_size[0], len(text_lines), width, height))

            width = width + pad_spec['left'] + pad_spec['right']
            return (text_lines, width, height)

    # we are here at last iteration, which means something went wrong, we fall back to the last ever try
    if debug_enabled: debug('text [{0} ({1})] broken down into [{2}]. computed width, height is [{3}, {4}]'.format(text, text_size[0], len(text_lines), width, height))

    width = width + pad_spec['left'] + pad_spec['right']
    return (text_lines, width, height)

def text_size_in_pixels(text, font_family, font_size, font_weight='', stroke_width=0):
    adjusted_text = ' ' + text + ' '
    if font_weight != '':
        font_key = font_family + '-' + font_weight
    else:
        font_key = font_family

    try:
        font_path = font_spec[font_key][sys.platform]
        font = ImageFont.truetype(font_path, font_size, layout_engine=ImageFont.LAYOUT_BASIC)
    except:
        font_path = font_spec['arial-bold'][sys.platform]
        font = ImageFont.truetype(font_path, font_size, layout_engine=ImageFont.LAYOUT_BASIC)

    # debug('sizing [{0}] with font {1} size {2}'.format(text, font_path, font_size))
    size = font.getsize(adjusted_text, stroke_width=stroke_width)
    return size

def em_range(n):
    if n == 1:
        return [0]

    m = int(n/2)
    if (n % 2) == 1:
        return [x for x in range(-m, m+1)]
    else:
        return [x+0.5 for x in range(-m, m)]

def points_to_str(points):
    return ' '.join([str(point) for point in points])

def optimize_points(points):
    if len(points) <= 2:
        return points

    if not points[2].on_same_line(points[0], points[1]):
        return [points[0]] + optimize_points(points[1:])
    else:
        return optimize_points([points[0], points[2]] + points[3:])

def points_to_path(points):
    return 'M' + ' L'.join([str(point) for point in points])

def points_to_curved_path(points):
    new_points = optimize_points(points)

    # first we generate a new set of points for every three points so that if the three points make a turn we have actually 5 points
    path = 'M {0}'.format(new_points[0])
    # if we have only two points
    if len(points) == 2:
        path = '{0} L {1}'.format(path, points[1])
        return path

    default_offset = 10
    i = 0
    while i < (len(new_points) - 2):
        p1, p2, p3 = new_points[i], new_points[i+1], new_points[i+2]
        # we know that p1-p2 line is perpendicular to p2-p3 line
        if p1.x == p2.x:
            # line p1-p2 is vertical, so p2-p3 must be horizontal
            if p1.y < p2.y:
                # p1 is above p2
                # we just add a new point p2a just vertically (q_offset) above p2.
                # The default_offset may be greater than the vertical diff betwwen the points p1 and p2, we adjust it
                q_offset = min(abs(p2.y - p1.y)/2, default_offset)
                p2a = Point(p2.x, p2.y - q_offset)

                # The default_offset may be greater than the horizontal diff betwwen the points p2 and p3, we adjust it
                q_offset = min(abs(p3.x - p2.x)/2, default_offset)
                if p2.x < p3.x:
                    # p2 is left to p3
                    # and another new point p2b just horizontally (q_offset) after p2
                    p2b = Point(p2.x + q_offset, p2.y)
                else:
                    # p2 is right to p3
                    # and another new point p2b just horizontally (q_offset) before p2
                    p2b = Point(p2.x - q_offset, p2.y)
            else:
                # p1 is below p2
                # we just add a new point p2a just vertically (q_offset) below p2
                # The default_offset may be greater than the vertical diff betwwen the points p1 and p2, we adjust it
                q_offset = min((p1.y - p2.y)/2, default_offset)
                p2a = Point(p2.x, p2.y + q_offset)

                # The default_offset may be greater than the horizontal diff betwwen the points p2 and p3, we adjust it
                q_offset = min(abs(p3.x - p2.x)/2, default_offset)
                if p2.x < p3.x:
                    # p2 is left to p3
                    # and another new point p2b just horizontally (q_offset) after p2
                    p2b = Point(p2.x + q_offset, p2.y)
                else:
                    # p2 is right to p3
                    # and another new point p2b just horizontally (q_offset) before p2
                    p2b = Point(p2.x - q_offset, p2.y)

        if p1.y == p2.y:
            # line p1-p2 is horizontal, so p2-p3 must be vertical
            if p1.x < p2.x:
                # p1 is left to p2
                # we just add a new point p2a just horizontally (q_offset) before p2
                # The default_offset may be greater than the horizontal diff betwwen the points p1 and p2, we adjust it
                q_offset = min(abs(p2.x - p1.x)/2, default_offset)
                p2a = Point(p2.x - q_offset, p2.y)

                # The default_offset may be greater than the vertical diff betwwen the points p2 and p3, we adjust it
                q_offset = min(abs(p3.y - p2.y)/2, default_offset)
                if p2.y < p3.y:
                    # p2 is above to p3
                    # and another new point p2b just vertically (q_offset) after p2
                    p2b = Point(p2.x, p2.y + q_offset)
                else:
                    # p2 is below p3

                    # and another new point p2b just vertically (q_offset) before p2
                    p2b = Point(p2.x, p2.y - q_offset)
            else:
                # p1 is right to p2
                # we just add a new point p2a just horizontally (q_offset) after p2
                # The default_offset may be greater than the horizontal diff betwwen the points p1 and p2, we adjust it
                q_offset = min(abs(p2.x - p1.x)/2, default_offset)
                p2a = Point(p2.x + q_offset, p2.y)

                # The default_offset may be greater than the vertical diff betwwen the points p2 and p3, we adjust it
                q_offset = min(abs(p3.y - p2.y)/2, default_offset)
                if p2.y < p3.y:
                    # p2 is above p3
                    # and another new point p2b just vertically (q_offset) after p2
                    p2b = Point(p2.x, p2.y + q_offset)
                else:
                    # p2 is below p3
                    # and another new point p2b just vertically (q_offset) before p2
                    p2b = Point(p2.x, p2.y - q_offset)

        # the path is 5 point path with p2 now as the Q point
        # path = '{0} L {1} L {2} Q {3} {4} L {5}'.format(path, p1, p2a, p2, p2b, p3)
        path = '{0} L {1} Q {2} {3}'.format(path, p2a, p2, p2b)

        i = i + 1

    path = '{0} L {1}'.format(path, new_points[-1])

    return path

def id_to_label(id):
    return id.replace('_', ' ').capitalize()

def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def longest_horizontal_line_segment(points):
    if len(points) < 2:
        return None, None

    point_from = points[0]
    point_to = points[1]
    longest_horizontal_length_so_far = abs(point_from.x - point_to.x)
    previous_point = points[1]
    for current_point in points[2:]:
        if current_point.y == previous_point.y:
            if longest_horizontal_length_so_far < abs(current_point.x - previous_point.x):
                longest_horizontal_length_so_far = abs(current_point.x - previous_point.x)
                point_from = previous_point
                point_to = current_point

        previous_point = current_point

    return point_from, point_to

def longest_vertical_line_segment(points):
    if len(points) < 2:
        return None, None

    point_from = points[0]
    point_to = points[1]
    longest_vertical_length_so_far = abs(point_from.y - point_to.y)
    previous_point = points[1]
    for current_point in points[2:]:
        if current_point.x == previous_point.x:
            if longest_vertical_length_so_far < abs(current_point.y - previous_point.y):
                longest_vertical_length_so_far = abs(current_point.y - previous_point.y)
                point_from = previous_point
                point_to = current_point

        previous_point = current_point

    return point_from, point_to

def first_vertical_line_segment_longer_than(points, length):
    if len(points) < 2:
        return None, None

    point_from = points[0]
    point_to = points[1]
    if abs(point_from.y - point_to.y) >= length:
        return point_from, point_to

    previous_point = points[1]
    for current_point in points[2:]:
        if current_point.x == previous_point.x:
            if abs(current_point.y - previous_point.y) >= length:
                point_from = previous_point
                point_to = current_point
                return point_from, point_to

        previous_point = current_point

    return point_from, point_to
