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

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

from elements.swims.swim_lane import SwimLane

class LaneGroup(BpmnElement):
    def __init__(self):
        self.theme = self.current_theme['LaneGroup']

    def to_svg(self, bpmn_id, lanes):
        info('processing lanes for [{0}] ...'.format(bpmn_id))

        # a lane group is a vertical stack of lanes
        lane_svg_element_list = self.lane_svg_elements(bpmn_id, lanes)

        # assemble the lane svg's into a final one
        svg_element = self.assemble_element(bpmn_id, lane_svg_element_list)

        info('processing lanes for [{0}] DONE ...'.format(bpmn_id))
        return svg_element

    def lane_svg_elements(self, bpmn_id, lanes):
        # get the inner lane svg elements in a list
        lane_svg_element_list = []
        for lane_id, lane_data in lanes.items():
            swim_lane_svg_element = SwimLane().to_svg(bpmn_id, lane_id, lane_data)
            lane_svg_element_list.append(swim_lane_svg_element)

        return lane_svg_element_list

    def assemble_element(self, bpmn_id, lane_svg_element_list):
        # wrap it in a svg group
        group_id = '{0}-lanes'.format(bpmn_id)
        svg_group = G(id=group_id)

        # height of the lane group is sum of height of all lanes with gaps between lanes
        group_height = 0
        group_width = 0
        lane_count = 0
        for lane_svg_element in lane_svg_element_list:
            # if this is not the first lane add gap to height
            if lane_count > 0:
                group_height = group_height + self.theme['gap-between-lanes']

            # this specific lane should be vertically moved to the current height
            transformer = TransformBuilder()
            transformer.setTranslation("{0},{1}".format(0, group_height))
            swim_lane_svg = lane_svg_element.group
            swim_lane_svg.set_transform(transformer.getTransform())

            # adjust height
            group_height = group_height + lane_svg_element.specs['height']
            group_width = max(group_width, lane_svg_element.specs['width'])

            svg_group.addElement(swim_lane_svg)

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}
        return SvgElement(group_specs, svg_group)
