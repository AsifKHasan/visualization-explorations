#!/usr/bin/env python3
'''
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

from elements.svg_element import SvgElement
from elements.events.ends.event_end import EventEnd

class EventEndCompensation(EventEnd):
    # a multiple end is an end event with filled pentagon inside
    def __init__(self, current_theme, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(current_theme, bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme.update(self.current_theme['events']['ends']['EventEndCompensation'])

    def get_inside_element(self):
        svg_group, group_width, group_height = a_triangular_rewind_inside_a_circular_shape(radius=self.theme['circle']['radius'], inner_shape_spec=self.theme['inner-shape'])
        return SvgElement(svg=svg_group, width=group_width, height=group_height)
