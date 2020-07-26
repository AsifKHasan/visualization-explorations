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

def rect_with_text(text, min_width, max_width, specs, debug_enabled=False):
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
    text_rect = Rect(width=width, height=height, rx=rx, ry=ry)
    text_rect.set_style(StyleBuilder(specs['style']).getStyle())

    # render the text
    text_svg = center_text(
                    text=text_rendering_hint[0],
                    shape=text_rect,
                    style=specs['text-style'],
                    vertical_text=vertical_text,
                    pad_spec=specs['pad-spec'])

    return [text_rect, text_svg]

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
        text_lines = textwrap.wrap(text=text, width=text_wrap_at, break_long_words=True)
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
        text_lines = textwrap.wrap(text=text, width=text_wrap_at, break_long_words=True)
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

def center_text(text, shape, style, vertical_text=False, pad_spec=None, text_wrap_at=0, debug=False):
    if pad_spec is None:
        pad_spec = {'left': 10, 'top': 10, 'right': 10, 'bottom': 10}

    if vertical_text:
        style['writing-mode'] = 'vertical-lr'
    else:
        style['writing-mode'] = 'horizontal-tb'

    shape_width = shape.get_width() - pad_spec['left'] - pad_spec['right']
    shape_height = shape.get_height() - pad_spec['top'] - pad_spec['bottom']
    svg = Svg(pad_spec['left'], pad_spec['top'], width=shape_width, height=shape_height)

    t = Text(None)
    t.set_style(StyleBuilder(style).getStyle())

    # if text is a list, do not procees, use the list
    if type(text) is list:
        text_list = text
    else:
        if text_wrap_at > 0:
            text_list = textwrap.wrap(text=text, width=text_wrap_at, break_long_words=True)
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

def text_size_in_pixels(text, font_family, font_size):
    font = ImageFont.truetype(font_family, font_size)
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
