#!/usr/bin/env python3
'''
cd C:\projects\asifhasan@github\bpmn-svg\src
python svg-test.py > ../out/svg-test.svg
'''
import sys, json;

from pysvg.builders import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *

import textwrap

def em_range(n):
    m = int(n/2)
    if (n % 2) == 1:
        return [x for x in range(-m, -m/2+1)]
    else:
        return [x+0.5 for x in range(-m, m)]

def center_text(text, shape, style, vertical_text=False, text_wrap_at=0):
    text_list = ['I am a Global Admin', 'doing my admin job']
    svg = Svg(0, 0, width=shape.get_width(), height=shape.get_height())

    ts1 = Tspan(x="50%", y="50%" , dx="0.5em")
    ts1.appendTextContent(text_list[0])
    ts2 = Tspan(x="50%", y="50%" , dx="-0.5em")
    ts2.appendTextContent(text_list[1])
    t = Text(None, '50%', '50%', style=style)
    t.addElement(ts1)
    t.addElement(ts2)

    if vertical_text:
        style['writing-mode'] = 'vertical-lr'
    else:
        style['writing-mode'] = 'horizontal-tb'

    t.set_style(StyleBuilder(style).getStyle())
    svg.addElement(t)
    return svg

def to_svg():
    rect_width = 50
    rect_height = 100

    rect_style = {'fill': '#E0E0E0', 'stroke-width': 2, 'stroke': '#404040'}
    svg_rect = Rect(width=rect_width, height=rect_height)
    svg_rect.set_style(StyleBuilder(rect_style).getStyle())

    text = 'I am a Global Admin doing my admin job'
    text_style = {'text-anchor': 'middle', 'dominant-baseline': 'middle', 'font-family': 'Calibri', 'font-size': 14, 'fill': '#FF0000', 'stroke': '#000000', 'stroke-width': 0}
    svg_text = center_text(text, svg_rect, text_style, vertical_text=True, text_wrap_at=20)

    # wrap in canvas
    canvas_width = rect_width
    canvas_height = rect_height
    svg = Svg(0, 0, width=canvas_width, height=canvas_height)
    svg.addElement(svg_rect)
    svg.addElement(svg_text)

    return svg.getXML()

if __name__ == "__main__":
    print(to_svg(), sys.stdout)
