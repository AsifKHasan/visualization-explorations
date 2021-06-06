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

from elements.gateways.gateway import Gateway
from elements.svg_element import SvgElement

class GatewayEventBasedStart(Gateway):
    # an event-based start Gateway is a diamond with
    def __init__(self, current_theme, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(current_theme, bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['gateways']['GatewayEventBasedStart']}

    def get_inside_element(self):
        radius = min(self.theme['diamond']['diagonal-x'], self.theme['diamond']['diagonal-y']) * 0.27
        svg_group, group_width, group_height = an_equilateral_pentagon_in_a_circle(
                                    radius=radius,
                                    circle_spec=self.theme['inner-circle'],
                                    pentagon_spec=self.theme['inner-shape'])
        return SvgElement(svg=svg_group, width=group_width, height=group_height)
