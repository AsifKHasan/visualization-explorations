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

from elements.events.starts.event_start import EventStart

class EventStartSignal(EventStart):
    # a start event is circle. get a list of svg where the first one is the node circle
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(bpmn_id, lane_id, pool_id, node_id, node_data, non_interrupting=False)
        self.theme.update(self.current_theme['events']['starts']['EventStartSignal'])

    def to_svg(self):
        # get what is to be placed inside the outer circle as an element
        inside_svg_element = self.get_inside_element()

        # call the parent for doing the label and circle, just supply the inner svg to be placed inside the circle as an element
        svg_element = super().to_svg(inside_svg_element)
        return svg_element

    def get_inside_element(self):
        return None
