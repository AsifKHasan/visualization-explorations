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
from elements.events.intermediates.event_intermediate import EventIntermediate

class EventIntermediateCatchMultipleNon(EventIntermediate):
    # an intermediate event is two concentric circles
    def __init__(self, current_theme, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(current_theme, bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme.update(self.current_theme['events']['intermediates']['EventIntermediateCatchMultipleNon'])

    def get_inside_element(self):
        svg_group, group_width, group_height = an_equilateral_pentagon_inside_a_circular_shape(radius=self.theme['inner-circle']['radius'], inner_shape_spec=self.theme['inner-shape'])
        return SvgElement(svg=svg_group, width=group_width, height=group_height)
