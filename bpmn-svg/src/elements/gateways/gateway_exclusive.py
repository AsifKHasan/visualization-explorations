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

class GatewayExclusive(Gateway):
    # an exclusive Gateway is a diamond with a X inside
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['gateways']['GatewayExclusive']}

    def get_inside_element(self):
        radius = radius_of_the_circle_inside_the_diamond(width=self.theme['diamond']['diagonal-x'], height=self.theme['diamond']['diagonal-y'])
        svg_group, width, height = an_x_inside_a_circular_shape(
                                    radius=radius,
                                    inner_shape_spec=self.theme['inner-shape'])
        return SvgElement({'width': width, 'height': height}, svg_group)
