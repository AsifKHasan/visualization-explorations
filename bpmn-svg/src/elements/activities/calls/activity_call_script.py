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
from elements.activities.calls.activity_call import ActivityCall

class ActivityCallScript(ActivityCall):
    # a call activity is a rounded rectangle with thick border a text inside
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['activities']['calls']['ActivityCallScript']}

    def get_top_left_element(self):
        svg_group, group_width, group_height = include_and_scale_svg(spec=self.theme['top-left-inner-shape'])
        return SvgElement(svg=svg_group, width=group_width, height=group_height)
