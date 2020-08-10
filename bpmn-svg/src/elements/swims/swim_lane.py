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

from util.logger import *
from util.svg_util import *

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

from elements.swims.pool_collection import PoolCollection

class SwimLane(BpmnElement):
    # a horizontal lane is a narrow rectangle having a center-aligned text 90 degree anti-clockwise rotated at left and another adjacent rectangle () on its right containing Pool elements stacked vertically
    def __init__(self, bpmn_id, lane_id, lane_data):
        self.theme = self.current_theme['swims']['SwimLane']
        self.bpmn_id, self.lane_id, self.lane_data = bpmn_id, lane_id, lane_data

    def lay_edges(self):
        self.pool_collection_instance.lay_edges()

    def assemble_labels(self):
        group_id = '{0}:{1}-label'.format(self.bpmn_id, self.lane_id)

        # get the lane label, its min_width and max_width is the pool collection's height + all
        label_group, group_width, group_height = text_inside_a_rectangle(
                                                    text=self.lane_data['label'],
                                                    min_width=self.svg_element.height,
                                                    max_width=self.svg_element.height,
                                                    rect_spec=self.theme['rectangle'],
                                                    text_spec=self.theme['text'],
                                                    debug_enabled=False)

        label_group.set_id(id=group_id)

        # now we need to add the pool-collection's label just right to it
        child_label_element = self.pool_collection_instance.assemble_labels()

        transformer = TransformBuilder()
        child_label_xy = Point(group_width, 0)
        transformer.setTranslation(child_label_xy)
        child_label_element.svg.set_transform(transformer.getTransform())
        label_group.addElement(child_label_element.svg)

        group_width = group_width + child_label_element.width

        # wrap it in a svg element
        self.label_element = SvgElement(svg=label_group, width=group_width, height=group_height)
        # pprint(self.label_element.svg.getXML())
        return self.label_element

    def collect_elements(self):
        info('..processing lane [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # get the pool collection
        self.pool_collection_instance = PoolCollection(self.bpmn_id, self.lane_id, self.lane_data['pools'])
        self.pool_collection_instance.collect_elements()

        info('..processing lane [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))

    def assemble_elements(self):
        info('..assembling lane [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        self.svg_element = self.pool_collection_instance.assemble_elements()

        info('..assembling lane [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))
        return self.svg_element
