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
from elements.events.event import Event

class EventStart(Event):
    # a start event is circle with a thin border
    def __init__(self, current_theme, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(current_theme, bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['events']['starts']['EventStart']}

    def get_inside_element(self):
        return None
