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
from elements.activities.tasks.activity_task import ActivityTask

class ActivityTaskUser(ActivityTask):
    # a task activity is a rounded rectangle with a text inside
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['activities']['tasks']['ActivityTaskUser']}

    def get_top_left_element(self):
        svg_group, width, height = include_and_scale_svg(spec=self.theme['top-left-inner-shape'])
        return SvgElement({'width': width, 'height': height}, svg_group)
