#!/usr/bin/env python3
'''
'''
import sys
import math
from PIL import ImageFont

import textwrap

from util.logger import *
from util.geometry import Point


font_spec = {
    'arial' : {
        'win32' : 'arial',
        'linux' : 'Arial.ttf',
        'darwin' : '/Library/Fonts/Arial.ttf'
    }
}

#   -----------------------------------------------------------------------------------------------------------------------------------------------------
#   internal utility functions
#   -----------------------------------------------------------------------------------------------------------------------------------------------------
'''
    text        : text that needs to be fitted
    font_family : the font to render the text in
    font_size   : font size of the text
    max_lines   : maximum lines the text can be broken into
    min_width   : returned width can not be less than this
    max_width   : returned width can not be more than this
    pad_spec    : padding specifications

    returns     (text_lines, width, height)
'''
def break_text_inside_rect(text, font_family, font_size, max_lines, min_width, max_width, pad_spec=None, debug_enabled=False):
    if pad_spec is None:
        pad_spec = {'left': 10, 'top': 10, 'right': 10, 'bottom': 10}

    # first see the text size in pixel
    text_size = text_size_in_pixels(text, font_family, font_size)
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
            line_size = text_size_in_pixels(line, font_family, font_size)
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
            line_size = text_size_in_pixels(line, font_family, font_size)
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

def text_size_in_pixels(text, font_family, font_size):
    try:
        font_path = font_spec[font_family][sys.platform]
        font = ImageFont.truetype(font_path, font_size)
    except:
        font_path = font_spec['arial'][sys.platform]
        font = ImageFont.truetype(font_path, font_size)

    size = font.getsize(text)
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

def points_to_path(points):
    return 'M' + ' L'.join([str(point) for point in points])

def points_to_curved_path(points):
    # first we generate a new set of points for every three points so that if the three points make a turn we have actually 5 points
    q_offset = 10
    path = 'M {0}'.format(points[0])
    i = 0
    while i < (len(points) - 2):
        p1, p2, p3 = points[i], points[i+1], points[i+2]
        # see if they make an angle (we assume that any two consecutive points either make a vertical or a horizontal line)
        if p1.x == p2.x == p3.x or p1.y == p2.y == p3.y:
            # the three points do not make any corner
            path = '{0} L {1}'.format(path, p2)
            # i = i + 1
        else:
            # now we know that p1-p2 line is perpendicular to p2-p3 line
            if p1.x == p2.x:
                # line p1-p2 is vertical, so p2-p3 must be horizontal
                if p1.y < p2.y:
                    # p1 is above p2
                    # we just add a new point p2a just vertically (q_offset) above p2
                    p2a = Point(p2.x, p2.y - q_offset)
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
                    p2a = Point(p2.x, p2.y + q_offset)
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
                    p2a = Point(p2.x - q_offset, p2.y)
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
                    p2a = Point(p2.x + q_offset, p2.y)
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

    path = '{0} L {1} L {2}'.format(path, points[-2], points[-1])

    return path
