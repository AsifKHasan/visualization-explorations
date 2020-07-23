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
    def __init__(self):
        self.theme = self.current_theme['PoolGroup']

    def to_svg(self, bpmn_id, lane_id, pools):
        # a pool group is a vertical stack of pools
        info('..processing pools for [{0}:{1}] ...'.format(bpmn_id, lane_id))

        # We go through a collect -> tune -> assemble flow

        # collect the svg elements, but do not assemble now. we need tuning before assembly
        svg_elements = self.collect_elements(bpmn_id, lane_id, pools)

        # tune the svg elements as needed
        svg_elements = self.tune_elements(bpmn_id, lane_id, pools, svg_elements)

        # finally assemble the svg elements into a final one
        final_svg_element = self.assemble_elements(bpmn_id, lane_id, svg_elements)

        info('..processing pools for [{0}:{1}] DONE ...'.format(bpmn_id, lane_id))
        return final_svg_element

    def tune_elements(self, bpmn_id, lane_id, pools, svg_elements):
        return svg_elements

    def collect_elements(self, bpmn_id, lane_id, pools):
        # get the inner pool svg elements in a list
        svg_elements = []
        for pool_id, pool_data in pools.items():
            svg_element = SwimPool().to_svg(bpmn_id, lane_id, pool_id, pool_data)
            svg_elements.append(svg_element)

        return svg_elements

    def assemble_elements(self, bpmn_id, lane_id, svg_elements):
        # wrap it in a svg group
        group_id = '{0}:{1}-pools'.format(bpmn_id, lane_id)
        svg_group = G(id=group_id)

        # height of the pool group is sum of height of all pools with gaps between pools
        group_height = 0
        group_width = 0
        pool_count = 0
        for pool_svg_element in svg_elements:
            # if this is not the first pool add gap to height
            if pool_count > 0:
                group_height = group_height + self.theme['gap-between-pools']

            # this specific pool should be vertically moved to the current height
            transformer = TransformBuilder()
            transformer.setTranslation("{0},{1}".format(0, group_height))
            swim_pool_svg = pool_svg_element.group
            swim_pool_svg.set_transform(transformer.getTransform())

            # adjust height
            group_height = group_height + pool_svg_element.specs['height']
            group_width = max(group_width, pool_svg_element.specs['width'])

            svg_group.addElement(swim_pool_svg)

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}
        return SvgElement(group_specs, svg_group)
