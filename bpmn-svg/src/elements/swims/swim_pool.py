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
from util.svg_util import *

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

from elements.swims.channel_collection import ChannelCollection

class SwimPool(BpmnElement):
    # a horizontal pool is a narrow rectangle having a center-aligned text 90 degree anti-clockwise rotated at left and another adjacent rectangle () on its right containing nodes and edges
    def __init__(self, bpmn_id, lane_id, pool_id, pool_data):
        self.theme = self.current_theme['swims']['SwimPool']
        self.bpmn_id, self.lane_id, self.pool_id, self.pool_data = bpmn_id, lane_id, pool_id, pool_data

    def lay_edges(self):
        self.channel_collection_instance.lay_edges()

    def assemble_labels(self):
        group_id = '{0}:{1}:{2}-label'.format(self.bpmn_id, self.lane_id, self.pool_id)

        # get the lane label, its min_width and max_width is the channel collection's height
        label_group, group_width, group_height = text_inside_a_rectangle(
                                                    text=self.pool_data['label'],
                                                    min_width=self.svg_element.height,
                                                    max_width=self.svg_element.height,
                                                    rect_spec=self.theme['rectangle'],
                                                    text_spec=self.theme['text'],
                                                    debug_enabled=False)

        # label_group.set_id(id=group_id)

        self.label_element = SvgElement(svg=label_group, width=group_width, height=group_height)
        # pprint(self.label_element.svg.getXML())
        return self.label_element

    def collect_elements(self):
        info('....processing pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        # get the channel collection
        self.channel_collection_instance = ChannelCollection(self.bpmn_id, self.lane_id, self.pool_id, self.pool_data['nodes'], self.pool_data['edges'])
        self.channel_collection_instance.collect_elements()

        info('....processing pool [{0}:{1}:{2}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id))

    def assemble_elements(self):
        info('....assembling pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        self.svg_element = self.channel_collection_instance.assemble_elements()

        info('....assembling pool [{0}:{1}:{2}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id))
        return self.svg_element
