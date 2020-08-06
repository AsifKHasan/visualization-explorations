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
        svg_group, group_width, group_height = a_cross_in_a_circle(
                                    radius=radius,
                                    circle_spec=self.theme['inner-circle'],
                                    cross_spec=self.theme['inner-shape'])
        return SvgElement(svg=svg_group, width=group_width, height=group_height)
