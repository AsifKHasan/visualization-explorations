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

from elements.activities.activity import Activity
from elements.svg_element import SvgElement

class ActivitySubprocess(Activity):
    # a subprocess activity is a rounded rectangle with text inside, something in top left above the text and a + at the bottom floor of the rectangle below the text
    def __init__(self, current_theme, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(current_theme, bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['activities']['subprocesses']['ActivitySubprocess']}

    def get_bottom_center_element(self):
        svg_group, group_width, group_height = a_cross_in_a_rectangle(
                                                    width=self.theme['bottom-center-rectangle']['width'],
                                                    height=self.theme['bottom-center-rectangle']['height'],
                                                    rect_spec=self.theme['bottom-center-rectangle'],
                                                    cross_spec=self.theme['bottom-center-inner-shape'])

        return SvgElement(svg=svg_group, width=group_width, height=group_height)
