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
    # a lane group is a vertical stack of lanes
    def __init__(self, bpmn_id, lanes):
        self.theme = self.current_theme['LaneGroup']
        self.bpmn_id, self.lanes = bpmn_id, lanes

    def to_svg(self):
        # We go through a collect -> tune -> assemble flow

        # collect the svg elements, but do not assemble now. we need tuning before assembly
        self.collect_elements()

        # tune the svg elements as needed
        self.tune_elements()

        # finally assemble the svg elements into a final one
        final_svg_element = self.assemble_elements()
        return final_svg_element

    def tune_elements(self):
        info('tuning lanes for [{0}]'.format(self.bpmn_id))
        info('tuning lanes for [{0}] DONE'.format(self.bpmn_id))

    def collect_elements(self):
        info('processing lanes for [{0}]'.format(self.bpmn_id))

        # get the inner lane svg elements in a list
        self.child_element_classes = []
        for lane_id, lane_data in self.lanes.items():
            child_element_class = SwimLane(self.bpmn_id, lane_id, lane_data)
            child_element_class.collect_elements()
            self.child_element_classes.append(child_element_class)

        info('processing lanes for [{0}] DONE'.format(self.bpmn_id))

    def assemble_elements(self):
        info('assembling lanes for [{0}] DONE'.format(self.bpmn_id))

        # wrap it in a svg group
        group_id = '{0}-lanes'.format(self.bpmn_id)
        svg_group = G(id=group_id)

        # height of the lane group is sum of height of all lanes with gaps between lanes
        group_height = 0
        group_width = 0
        counter = 0
        for child_element_class in self.child_element_classes:
            swim_lane_svg_element = child_element_class.assemble_elements()
            # if this is not the first lane add gap to height
            if counter > 0:
                group_height = group_height + self.theme['gap-between-lanes']

            counter = counter + 1

            # this specific lane should be vertically moved to the current height
            transformer = TransformBuilder()
            transformer.setTranslation("{0},{1}".format(0, group_height))
            swim_lane_svg = swim_lane_svg_element.group
            swim_lane_svg.set_transform(transformer.getTransform())

            # adjust height
            group_height = group_height + swim_lane_svg_element.specs['height']
            group_width = max(group_width, swim_lane_svg_element.specs['width'])

            svg_group.addElement(swim_lane_svg)

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}

        info('assembling lanes for [{0}] DONE'.format(self.bpmn_id))
        return SvgElement(group_specs, svg_group)
