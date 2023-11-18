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

from helper.geometry import Point

SVG_IN_PATH = '../out/ruling-application-process.svg'
SVG_OUT_PATH = '../out/ruling-application-process-new.svg'

def update_svg_root(svg_root):

    # view box
    vp_str = svg_root.get_viewBox()
    vp_strs = vp_str.split(' ')
    # add 100 to width
    new_vp_width = float(vp_strs[2]) + 100
    new_vp_str = f"{vp_strs[0]} {vp_strs[1]} {new_vp_width:.2f} {vp_strs[3]}"

    # svg width
    w_str = svg_root.get_width()
    w = w_str[0:-2]
    new_w = float(w) + 100

    print(new_vp_str)
    print(new_w)

    svg_root.set_viewBox(new_vp_str)
    svg_root.set_width(f"{new_w}pt")

    return svg_root
    


if __name__ == '__main__':
    svg_root = parse(inFileName=SVG_IN_PATH)
    new_svg_root = update_svg_root(svg_root=svg_root)
    new_svg_root.save(filename=SVG_OUT_PATH, encoding="UTF-8")
    