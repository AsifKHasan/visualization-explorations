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

from elements.activities.subprocesses.activity_subprocess import ActivitySubprocess
from elements.svg_element import SvgElement

class ActivityAdhocSubprocess(ActivitySubprocess):
    # a subprocess activity is a rounded rectangle with text inside and a + and a ~ side by side at the bottom floor of the rectangle below the text
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['activities']['subprocesses']['ActivityAdhocSubprocess']}

    def get_bottom_center_element(self):
        rect_svg_group, rect_svg_width, rect_svg_height = a_cross_in_a_rectangle(
                                                    width=self.theme['bottom-center-rectangle']['width'],
                                                    height=self.theme['bottom-center-rectangle']['height'],
                                                    rect_spec=self.theme['bottom-center-rectangle'],
                                                    cross_spec=self.theme['bottom-center-inner-shape'])
        rect_svg_element = SvgElement({'width': rect_svg_width, 'height': rect_svg_height}, rect_svg_group)

        tilde_svg_group, tilde_svg_width, tilde_svg_height = a_tilde_in_a_rectangular_shape(
                                                    width=self.theme['bottom-center-rectangle']['width'],
                                                    height=self.theme['bottom-center-rectangle']['height'],
                                                    rect_spec=self.theme['bottom-center-rectangle'],
                                                    tilde_spec=self.theme['bottom-center-inner-shape'])
        tilde_svg_element = SvgElement({'width': tilde_svg_width, 'height': tilde_svg_height}, tilde_svg_group)

        combined_svg_group, combined_svg_width, combined_svg_height = align_and_combine_horizontally([rect_svg_element, tilde_svg_element])

        return SvgElement({'width': combined_svg_width, 'height': combined_svg_height}, combined_svg_group)
