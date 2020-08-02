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
from elements.activities.subprocesses.activity_subprocess_event import ActivityEventSubprocess

class ActivityEventTimerNon(ActivityEventSubprocess):
    # a subprocess activity is a dashed rounded rectangle with text inside, something in top left above the text and a + at the bottom floor of the rectangle below the text
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['activities']['subprocesses']['event-subprocesses']['ActivityEventTimerNon']}

    def get_top_left_element(self):
        inner_svg, inner_width, inner_height = a_clock_inside_a_circular_shape(radius=self.theme['top-left-circle']['radius'], inner_shape_spec=self.theme['top-left-inner-shape'])
        svg_group, svg_width, svg_height = envelop_and_center_in_a_circle(circle_spec=self.theme['top-left-circle'], svg=inner_svg, svg_width=inner_width, svg_height=inner_height)
        return SvgElement({'width': svg_width, 'height': svg_height}, svg_group)
