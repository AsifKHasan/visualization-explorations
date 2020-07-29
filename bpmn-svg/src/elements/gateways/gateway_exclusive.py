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
        svg_group, width, height = an_x(
                                    width=self.theme['diamond']['diagonal-x'],
                                    height=self.theme['diamond']['diagonal-y'],
                                    style=self.theme['inner-shape-style'])
        return SvgElement({'width': width, 'height': height}, svg_group)
