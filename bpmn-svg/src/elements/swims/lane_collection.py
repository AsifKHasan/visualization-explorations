#!/usr/bin/env python3
'''
'''
from pprint import pprint

from pysvg.builders import *
from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *

from util.geometry import Point
from util.logger import *

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

from elements.swims.swim_lane import SwimLane

class LaneCollection(BpmnElement):
    # a lane collection is a vertical stack of lanes
    def __init__(self, bpmn_id, lanes):
        self.theme = self.current_theme['swims']['LaneCollection']
        self.bpmn_id, self.lanes = bpmn_id, lanes

    def lay_edges(self):
        for child_lane_class in self.child_lane_classes:
            child_lane_class.lay_edges()

    def assemble_labels(self):
        group_id = '{0}-lanes-label'.format(self.bpmn_id)
        svg_group = G(id=group_id)

        group_width = 0
        transformer = TransformBuilder()
        for child_lane_class in self.child_lane_classes:
            child_label_element = child_lane_class.assemble_labels()
            if child_label_element is None:
                continue

            # the y position of this lane label in the group will be its corresponding swim-lane's y position
            child_label_xy = Point(0, child_lane_class.svg_element.xy.y)
            transformer.setTranslation(child_label_xy)
            child_label_element.svg.set_transform(transformer.getTransform())
            svg_group.addElement(child_label_element.svg)

            group_width = max(child_label_element.width, group_width)

        group_height = self.svg_element.height

        # wrap it in a svg element
        self.label_element = SvgElement(svg=svg_group, width=group_width, height=group_height)
        # pprint(self.label_element.svg.getXML())
        return self.label_element

    def collect_elements(self):
        info('processing lanes for [{0}]'.format(self.bpmn_id))

        # get the inner lane svg elements in a list
        self.child_lane_classes = []
        for lane_id, lane_data in self.lanes.items():
            child_lane_class = SwimLane(self.bpmn_id, lane_id, lane_data)
            child_lane_class.collect_elements()
            self.child_lane_classes.append(child_lane_class)

        info('processing lanes for [{0}] DONE'.format(self.bpmn_id))

    def assemble_elements(self):
        info('assembling lanes for [{0}] DONE'.format(self.bpmn_id))

        # wrap it in a svg group
        group_id = '{0}-lanes'.format(self.bpmn_id)
        svg_group = G(id=group_id)

        # height of the lane collection is sum of height of all lanes with gaps between lanes
        max_lane_width = 0
        current_x = self.theme['pad-spec']['left']
        current_y = self.theme['pad-spec']['top']
        transformer = TransformBuilder()
        for child_lane_class in self.child_lane_classes:
            swim_lane_element = child_lane_class.assemble_elements()
            swim_lane_element.xy = Point(current_x, current_y)
            transformer.setTranslation(swim_lane_element.xy)
            swim_lane_element.svg.set_transform(transformer.getTransform())
            svg_group.addElement(swim_lane_element.svg)

            max_lane_width = max(max_lane_width, swim_lane_element.width)
            current_y = current_y + swim_lane_element.height + self.theme['dy-between-lanes']

        group_width = self.theme['pad-spec']['left'] + max_lane_width + self.theme['pad-spec']['right']
        group_height = current_y - self.theme['dy-between-lanes'] + self.theme['pad-spec']['bottom']

        # add the ractangle
        lane_collection_rect_svg = Rect(width=group_width, height=group_height)
        lane_collection_rect_svg.set_style(StyleBuilder(self.theme['style']).getStyle())
        svg_group.addElement(lane_collection_rect_svg)

        # wrap it in a svg element
        self.svg_element = SvgElement(svg=svg_group, width=group_width, height=group_height)
        info('assembling lanes for [{0}] DONE'.format(self.bpmn_id))
        return self.svg_element
