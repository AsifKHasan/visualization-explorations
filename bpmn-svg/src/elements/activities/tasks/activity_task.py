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
from elements.activities.activity import Activity

class ActivityTask(Activity):
    # a task activity is a rounded rectangle with a text inside
    def __init__(self, current_theme, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(current_theme, bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['activities']['tasks']['ActivityTask']}

    def get_top_left_element(self):
        return None

    def get_bottom_center_element(self):
        return None
