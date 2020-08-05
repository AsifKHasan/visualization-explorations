#!/usr/bin/env python3
'''
    spec_def is a dictionary with Element specific inputs
    returns a SvgElement
'''
from pysvg.builders import *
from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *

from util.logger import *
from util.svg_util import *

from elements import *

class BpmnElement():
    current_theme = default_theme

    def to_svg(self, spec_def):
        return None

    def snap_points(self, width, height):
        snaps = {}

        snaps['north'] = Point(width * 0.5, 0)
        snaps['south'] = Point(width * 0.5, height)
        snaps['east'] = Point(width, height * 0.5)
        snaps['west'] = Point(0, height * 0.5)

        return snaps

    def draw_snaps(self, snaps, svg_group):
        for snap in snaps:
            snap_point_group, snap_point_width, snap_point_height = a_snap_point(snaps[snap])
            svg_group.addElement(snap_point_group)
