#!/usr/bin/env python3

'''
various utilities for SVG code
'''
import re
import random
import string
import textwrap

from pysvg.builders import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *

from helper.logger import *

''' returns a tuple (svg group, group_width, group_height)
'''
def a_circle(radius, spec):
    svg_group = G()

    circle_svg = Circle(cx=radius, cy=radius, r=radius)
    circle_svg.set_style(StyleBuilder(spec.get('style', {})).getStyle())

    # add to group
    svg_group.addElement(circle_svg)
    return svg_group
