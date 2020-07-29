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
        pass

    def assemble_elements(self):
        info('......assembling node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # wrap it in a svg group
        svg_group = G(id=self.group_id)

        # get the elements
        label_svg_element = self.node_elements[0]
        label_svg = label_svg_element.group

        rect_svg_element = self.node_elements[1]
        wave_svg_element = self.node_elements[2]

        combined_svg, combined_svg_width, combined_svg_height = align_and_combine_horizontally([rect_svg_element, wave_svg_element])

        # the rect is inside the label, we keep a gap betwwen the bottom edge of the label and the botto edge of the rect
        gap_between_label_and_rect_bootom_edges = 5
        combined_svg_xy = '{0},{1}'.format((label_svg_element.specs['width'] - combined_svg_width)/2, label_svg_element.specs['height'] - combined_svg_height - gap_between_label_and_rect_bootom_edges)
        transformer = TransformBuilder()
        transformer.setTranslation(combined_svg_xy)
        combined_svg.set_transform(transformer.getTransform())

        # the wave is inside teh label, we keep a gap betwwen the bottom edge of the label and the bottom edge of the rect

        # place the elements
        svg_group.addElement(label_svg)
        svg_group.addElement(combined_svg)

        group_width = label_svg_element.specs['width']
        group_height = label_svg_element.specs['height']

        info('......assembling node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        return SvgElement({'width': group_width, 'height': group_height}, svg_group)
