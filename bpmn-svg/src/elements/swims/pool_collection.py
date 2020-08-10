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

from elements.swims.swim_pool import SwimPool

class PoolCollection(BpmnElement):
    # a pool collection is a vertical stack of pools
    def __init__(self, bpmn_id, lane_id, pools):
        self.theme = self.current_theme['swims']['PoolCollection']
        self.bpmn_id, self.lane_id, self.pools = bpmn_id, lane_id, pools

    def lay_edges(self):
        for child_pool_class in self.child_pool_classes:
            child_pool_class.lay_edges()

    def assemble_labels(self):
        group_id = '{0}:{1}-pools-labels'.format(self.bpmn_id, self.lane_id)
        svg_group = G(id=group_id)

        group_width = 0
        transformer = TransformBuilder()
        for child_pool_class in self.child_pool_classes:
            child_label_element = child_pool_class.assemble_labels()

            # the y position of this pool label in the group will be its corresponding swim-pool's y position
            child_label_xy = Point(0, child_pool_class.svg_element.xy.y)
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
        info('..processing pools for [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # get the inner pool svg elements in a list
        self.child_pool_classes = []
        for pool_id, pool_data in self.pools.items():
            child_pool_class = SwimPool(self.bpmn_id, self.lane_id, pool_id, pool_data)
            child_pool_class.collect_elements()
            self.child_pool_classes.append(child_pool_class)

        info('..processing pools for [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))

    def assemble_elements(self):
        info('..assembling pools for [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # wrap it in a svg group
        group_id = '{0}:{1}-pools'.format(self.bpmn_id, self.lane_id)
        svg_group = G(id=group_id)

        # height of the pool collection is sum of height of all pools with gaps between pools
        max_pool_width = 0
        current_x = self.theme['pad-spec']['left']
        current_y = self.theme['pad-spec']['top']
        transformer = TransformBuilder()
        for child_pool_class in self.child_pool_classes:
            swim_pool_element = child_pool_class.assemble_elements()
            swim_pool_element.xy = Point(current_x, current_y)
            transformer.setTranslation(swim_pool_element.xy)
            swim_pool_element.svg.set_transform(transformer.getTransform())
            svg_group.addElement(swim_pool_element.svg)

            max_pool_width = max(max_pool_width, swim_pool_element.width)
            current_y = current_y + swim_pool_element.height + self.theme['dy-between-pools']

        group_width = self.theme['pad-spec']['left'] + max_pool_width + self.theme['pad-spec']['right']
        group_height = current_y - self.theme['dy-between-pools'] + self.theme['pad-spec']['bottom']

        # add the ractangle
        pool_collection_rect_svg = Rect(width=group_width, height=group_height)
        pool_collection_rect_svg.set_style(StyleBuilder(self.theme['style']).getStyle())
        svg_group.addElement(pool_collection_rect_svg)

        # wrap it in a svg element
        self.svg_element = SvgElement(svg=svg_group, width=group_width, height=group_height)
        info('..assembling pools for [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))
        return self.svg_element
