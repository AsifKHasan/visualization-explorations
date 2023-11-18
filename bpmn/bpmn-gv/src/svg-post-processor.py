#!/usr/bin/env python3

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *
from pysvg.parser import parse

SVG_IN_PATH = '../out/ruling-application-process.svg'
SVG_OUT_PATH = '../out/ruling-application-process.svg'

def update_view_box(svg_root):
    w = svg_root.get_width()
    h = svg_root.get_height()
    vp = svg_root.get_viewBox()
    print(vp)
    print(w)
    print(h)
    


if __name__ == '__main__':
    svg_root = parse(inFileName=SVG_IN_PATH)
    update_view_box(svg_root=svg_root)