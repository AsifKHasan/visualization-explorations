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

from elements.swims.swim_pool import SwimPool

class PoolGroup(BpmnElement):
    # a pool group is a vertical stack of pools
    def __init__(self, bpmn_id, lane_id, pools):
        self.theme = self.current_theme['PoolGroup']
        self.bpmn_id, self.lane_id, self.pools = bpmn_id, lane_id, pools

    def get_max_width_of_elements_of_children(self):
        pool_text_element_max_width = 0
        pool_block_group_max_width = 0
        for child_element_class in self.child_element_classes:
            child_pool_text_element_max_width, child_block_group_max_width = child_element_class.get_max_width_of_elements_of_children()

            pool_text_element_max_width = max(pool_text_element_max_width, child_pool_text_element_max_width)
            pool_block_group_max_width = max(pool_block_group_max_width, child_block_group_max_width)

        return pool_text_element_max_width, pool_block_group_max_width

    def tune_elements(self, tune_spec):
        info('..tuning pools for [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # tune the children
        for child_element_class in self.child_element_classes:
            child_element_class.tune_elements(tune_spec)

        info('..tuning pools for [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))

    def collect_elements(self):
        info('..processing pools for [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # get the inner pool svg elements in a list
        self.child_element_classes = []
        for pool_id, pool_data in self.pools.items():
            child_element_class = SwimPool(self.bpmn_id, self.lane_id, pool_id, pool_data)
            child_element_class.collect_elements()
            self.child_element_classes.append(child_element_class)

        info('..processing pools for [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))

    def assemble_elements(self):
        info('..assembling pools for [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # wrap it in a svg group
        group_id = '{0}:{1}-pools'.format(self.bpmn_id, self.lane_id)
        svg_group = G(id=group_id)

        # height of the pool group is sum of height of all pools with gaps between pools
        group_height = 0
        group_width = 0
        counter = 0
        for child_element_class in self.child_element_classes:
            swim_pool_svg_element = child_element_class.assemble_elements()
            # if this is not the first pool add gap to height
            if counter > 0:
                group_height = group_height + self.theme['gap-between-pools']

            counter = counter + 1

            # this specific pool should be vertically moved to the current height
            transformer = TransformBuilder()
            transformer.setTranslation("{0},{1}".format(0, group_height))
            swim_pool_svg = swim_pool_svg_element.group
            swim_pool_svg.set_transform(transformer.getTransform())

            # adjust height
            group_height = group_height + swim_pool_svg_element.specs['height']
            group_width = max(group_width, swim_pool_svg_element.specs['width'])

            svg_group.addElement(swim_pool_svg)

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}

        info('..assembling pools for [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))
        return SvgElement(group_specs, svg_group)

    def get_height(self):
        height = 0
        for child_element_class in self.child_element_classes:
            height = height + child_element_class.get_height()

        if len(self.child_element_classes) > 0:
            height = height + self.theme['gap-between-pools'] * (len(self.child_element_classes) - 1)

        return height
