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

class GatewayEventBasedParallelStart(Gateway):
    # an event-based parallel start Gateway is a diamond with cross inside a circle
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['gateways']['GatewayEventBasedParallelStart']}

    def get_inside_element(self):
        radius = radius_of_the_circle_inside_the_diamond(self.theme['diamond']['diagonal-x'], self.theme['diamond']['diagonal-y']) - 4
        svg_group, width, height = a_cross_in_a_circle(
                                    radius=radius,
                                    circle_style=self.theme['inner-circle-style'],
                                    cross_style=self.theme['inner-shape-style'])
        return SvgElement({'width': width, 'height': height}, svg_group)
