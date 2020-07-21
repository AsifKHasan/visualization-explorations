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
def break_text_inside_rect(text, font_family, font_size, max_lines, min_width, max_width):
    # first see the text zize in pixel
    text_size = text_size_in_pixels(text, font_family, font_size)

    # if the width < min_width, we are fine
    if text_size[0] <= min_width:
        return ([text], min_width, text_size[1])

    # text size exceeds min_width, if it does not exceed min_width by more than 20%, we just adjust width
    if text_size[0] <= min_width * 1.2:
        return ([text], text_size[0], text_size[1])

    # well, text size exceeds min_width by a wider margin, we have to break the text into multiple lines
    # let us check how many lines we should have if we want to fit it into max_width
    approximate_lines = math.ceil(text_size[0] / max_width)

    # if this exceeds the max_line, we have a problem, the output will look bad and we will need to make it as many line as we need
    if approximate_lines > max_lines:
        text_wrap_at = math.ceil(len(text) / approximate_lines)
        text_lines = textwrap.wrap(text=text, width=text_wrap_at, break_long_words=False)
        height = 0
        width = 0
        for line in text_lines:
            line_size = text_size_in_pixels(line, font_family, font_size)
            width = max(min_width, width, line_size(0))
            height = height + line_size(1)

        return (text_lines, width, height)

    # now we know that we can be between 2 to max_lines, our target will be to have fewer lines without crossing max_width
    # start iteration
    for break_into in range(2, max_lines + 1):
        # break the text into equal sized parts (for better visuals)
        text_wrap_at = math.ceil(len(text) / break_into)
        text_lines = textwrap.wrap(text=text, width=text_wrap_at, break_long_words=False)
        height = 0
        width = 0
        for line in text_lines:
            line_size = text_size_in_pixels(line, font_family, font_size)
            width = max(min_width, width, line_size[0])
            height = height + line_size[1]

        # if we have not crossed max_width, we can stick to this
        if width <= max_width:
            return (text_lines, width, height)

    # we are here, which means something went wrong
    return (['SOMETHING WENT WRONG'], min_width, text_size[1])

def text_size_in_pixels(text, font_family, font_size):
    font = ImageFont.truetype(font_family, 12)
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

def center_text(text, shape, style, vertical_text=False, text_wrap_at=0):
    svg = Svg(0, 0, width=shape.get_width(), height=shape.get_height())

    if vertical_text:
        style['writing-mode'] = 'vertical-lr'
    else:
        style['writing-mode'] = 'horizontal-tb'

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
