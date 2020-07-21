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

'''
    text        : text that needs to be fitted
    font_family : the font to render the text in
    font_size   : font size of the text
    max_lines   : maximum lines the text can be broken into
    min_width   : returned width can not be less than this
    max_width   : returned width can not be more than this

    returns     (text_lines, width, height)
'''
def break_text_inside_rect(text, font_family, font_size, max_lines, min_width, max_width, pad_spec):
    if pad_spec is None:
        pad_spec = {'left': 10, 'top': 10, 'right': 10, 'bottom': 10}

    # first see the text size in pixel
    text_size = text_size_in_pixels(text, font_family, font_size)

    min_width = min_width - pad_spec['left'] - pad_spec['right']
    max_width = max_width - pad_spec['left'] - pad_spec['right']

    # if the width < min_width, we are fine
    if text_size[0] <= min_width:
        width = min_width + pad_spec['left'] + pad_spec['right']
        height = text_size[1] + pad_spec['top'] + pad_spec['bottom']
        return ([text], width, height)

    # text size exceeds min_width, if it does not exceed min_width by more than 20%, we just adjust width
    if text_size[0] <= min_width * 1.2:
        width = text_size[0] + pad_spec['left'] + pad_spec['right']
        height = text_size[1] + pad_spec['top'] + pad_spec['bottom']
        return ([text], width, height)

    # well, text size exceeds min_width by a wider margin, we have to break the text into multiple lines
    # let us check how many lines we should have if we want to fit it into max_width
    approximate_lines = math.ceil(text_size[0] / max_width)

    # if this exceeds the max_line, we have a problem, the output will look bad and we will need to make it as many line as we need
    if approximate_lines > max_lines:
        text_wrap_at = math.ceil(len(text) / approximate_lines)
        text_lines = textwrap.wrap(text=text, width=text_wrap_at, break_long_words=False)
        width = pad_spec['left'] + pad_spec['right']
        height = pad_spec['top'] + pad_spec['bottom']
        for line in text_lines:
            line_size = text_size_in_pixels(line, font_family, font_size)
            width = max(min_width, width, line_size[0])
            height = height + line_size[1]

        return (text_lines, width, height)

    # now we know that we can be between 2 to max_lines, our target will be to have fewer lines without crossing max_width
    # start iteration
    for break_into in range(2, max_lines + 1):
        # break the text into equal sized parts (for better visuals)
        text_wrap_at = math.ceil(len(text) / break_into)
        text_lines = textwrap.wrap(text=text, width=text_wrap_at, break_long_words=False)
        width = pad_spec['left'] + pad_spec['right']
        height = pad_spec['top'] + pad_spec['bottom']
        for line in text_lines:
            line_size = text_size_in_pixels(line, font_family, font_size)
            width = max(min_width, width, line_size[0])
            height = height + line_size[1]

        # if we have not crossed max_width, we can stick to this
        if width <= max_width:
            return (text_lines, width, height)

    # we are here, which means something went wrong
    return (['SOMETHING WENT WRONG'], min_width, text_size[1])

def center_text(text, shape, style, vertical_text=False, pad_spec=None, text_wrap_at=0):
    if pad_spec is None:
        pad_spec = {'left': 10, 'top': 10, 'right': 10, 'bottom': 10}

    if vertical_text:
        style['writing-mode'] = 'vertical-lr'
        shape_height = shape.get_width() - pad_spec['left'] - pad_spec['right']
        shape_width = shape.get_height() - pad_spec['top'] - pad_spec['bottom']
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
