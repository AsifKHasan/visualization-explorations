#!/usr/bin/env python3
'''
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

    def to_svg(self):
        return None

    def label_position(self):
        pass

    def switch_label_position(self):
        pass

    def draw_snaps(self, snaps, svg_group):
        for side in snaps:
            for position in snaps[side]:
                snap_point_group, snap_point_width, snap_point_height = a_snap_point(snaps[side][position]['point'])
                svg_group.addElement(snap_point_group)
