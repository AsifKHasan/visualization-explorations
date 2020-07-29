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

class GatewayEventBased(Gateway):
    # an event-based Gateway is a diamond with
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['gateways']['GatewayEventBased']}

    def get_inside_element(self):
        pad = 3
        outer_radius = min(self.theme['diamond']['diagonal-x'], self.theme['diamond']['diagonal-y']) * 0.27
        inner_radius = outer_radius - pad
        svg_group, width, height = an_equilateral_pentagon_in_two_concentric_circles(
                                    outer_radius=outer_radius,
                                    inner_radius=inner_radius,
                                    outer_style=self.theme['inner-circle-style'],
                                    inner_style=self.theme['inner-circle-style'],
                                    pad=pad,
                                    pentagon_style=self.theme['inner-shape-style'])
        return SvgElement({'width': width, 'height': height}, svg_group)
