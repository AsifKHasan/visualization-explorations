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

class ActivityTaskSend(ActivityTask):
    # a task activity is a rounded rectangle with a text inside
    def __init__(self, current_theme, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(current_theme, bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['activities']['tasks']['ActivityTaskSend']}

    def get_top_left_element(self):
        svg_group, group_width, group_height = an_envelop(width=self.theme['top-left-inner-shape']['width'], height=self.theme['top-left-inner-shape']['height'], spec=self.theme['top-left-inner-shape'])
        return SvgElement(svg=svg_group, width=group_width, height=group_height)
