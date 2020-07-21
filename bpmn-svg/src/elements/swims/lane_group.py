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

    def to_svg(self, lane_group_id, lanes):
        svg_group = G(id='lanes')

        # height of the lane group is sum of height of all lanes with gaps between lanes
        group_height = 0
        group_width = 0
        for lane_id, lane_data in lanes.items():
            # if this is not the first lane add gap to height
            if group_height > 0:
                group_height = group_height + self.theme['gap-between-lanes']

            # this specific lane should be vertically moved to the current height
            transformer = TransformBuilder()
            transformer.setTranslation("{0},{1}".format(0, group_height))

            swim_lane = SwimLane().to_svg(lane_id, lane_data)
            group_height = group_height + swim_lane.specs['height']
            if swim_lane.specs['width'] > group_width:
                group_width = swim_lane.specs['width']

            # move this specific lane
            swim_lane_svg = swim_lane.group
            swim_lane_svg.set_transform(transformer.getTransform())

            svg_group.addElement(swim_lane_svg)

        group_specs = {'width': group_width, 'height': group_height}

        return SvgElement(group_specs, svg_group)
