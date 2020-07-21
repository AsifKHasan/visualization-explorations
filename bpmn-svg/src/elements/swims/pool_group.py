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

    def to_svg(self, pool_group_id, pools):
        svg_group = G(id='pools')

        # height of the pool group is sum of height of all pools with gaps between pools
        group_height = 0
        group_width = 0
        for pool_id, pool_data in pools.items():
            # if this is not the first pool add gap to height
            if group_height > 0:
                group_height = group_height + self.theme['gap-between-pools']

            # this specific pool should be vertically moved to the current height
            transformer = TransformBuilder()
            transformer.setTranslation("{0},{1}".format(0, group_height))

            swim_pool = SwimPool().to_svg(pool_id, pool_data)
            swim_pool_svg = swim_pool.group

            group_height = group_height + swim_pool.specs['height']
            if swim_pool.specs['width'] > group_width:
                group_width = swim_pool.specs['width']

            # move this specific pool
            swim_pool_svg.set_transform(transformer.getTransform())

            svg_group.addElement(swim_pool_svg)

        group_specs = {'width': group_width, 'height': group_height}

        return SvgElement(group_specs, svg_group)
