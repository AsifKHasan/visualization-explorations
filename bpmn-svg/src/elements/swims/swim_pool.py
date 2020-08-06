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
from util.svg_util import *

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

from elements.swims.channel_collection import ChannelCollection

class SwimPool(BpmnElement):
    # a horizontal pool is a narrow rectangle having a center-aligned text 90 degree anti-clockwise rotated at left and another adjacent rectangle () on its right containing nodes and edges
    def __init__(self, bpmn_id, lane_id, pool_id, pool_data):
        self.theme = self.current_theme['swims']['SwimPool']
        self.bpmn_id, self.lane_id, self.pool_id, self.pool_data = bpmn_id, lane_id, pool_id, pool_data

    def tune_elements(self, tune_spec):
        info('....tuning pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        # label_svg_element width may need some tuning
        label_element_target_width = tune_spec['pool-text-element-target-width']
        self.tune_label_element(label_element_target_width)

        # channel_collection_svg_element width may need some tuning
        channel_collection_target_width = tune_spec['pool-block-group-target-width']
        self.tune_channel_collection_element(channel_collection_target_width)

        info('....tuning pool [{0}:{1}:{2}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id))

    def collect_elements(self):
        info('....processing pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        # get the inner svg elements in a list
        self.node_elements = []

        # get the channel collection
        channel_collection = ChannelCollection(self.bpmn_id, self.lane_id, self.pool_id, self.pool_data['nodes'], self.pool_data['edges'])
        channel_collection_svg_element = channel_collection.to_svg()
        self.node_elements.append(channel_collection_svg_element)

        # get the lane label, its min_width and max_width is the channel collection's height
        label_group, group_width, group_height = text_inside_a_rectangle(
                                                    text=self.pool_data['label'],
                                                    min_width=channel_collection_svg_element.height,
                                                    max_width=channel_collection_svg_element.height,
                                                    rect_spec=self.theme['rectangle'],
                                                    text_spec=self.theme['text'],
                                                    debug_enabled=False)

        self.node_elements.append(SvgElement(svg=label_group, width=group_width, height=group_height))

        info('....processing pool [{0}:{1}:{2}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id))

    def assemble_elements(self):
        info('....assembling pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))

        # wrap it in a svg group
        group_id = '{0}:{1}:{2}'.format(self.bpmn_id, self.lane_id, self.pool_id)
        svg_group = G(id=group_id)

        channel_collection_svg_element = self.node_elements[0]
        channel_collection_svg = channel_collection_svg_element.svg
        label_svg_element = self.node_elements[1]
        label_svg = label_svg_element.svg

        # a pool's width is pool text width + channel collection width + some padding
        group_height = channel_collection_svg_element.height + self.theme['pool-rect']['pad-spec']['top'] + self.theme['pool-rect']['pad-spec']['bottom']
        group_width = label_svg_element.width + channel_collection_svg_element.width + self.theme['pool-rect']['pad-spec']['left'] + self.theme['pool-rect']['pad-spec']['right'] + self.theme['gap-between-text-and-block-group']

        # add the pool outline
        outline_svg, group_width, group_height = a_rectangle(width=group_width, height=group_height, spec=self.theme['pool-rect'])

        # add the label svg
        label_svg_xy = '{0},{1}'.format(self.theme['pool-rect']['pad-spec']['left'], self.theme['pool-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(label_svg_xy)
        label_svg.set_transform(transformer.getTransform())

        # add the channel collection svg
        channel_collection_svg_xy = '{0},{1}'.format(self.theme['pool-rect']['pad-spec']['left'] + label_svg_element.width + self.theme['gap-between-text-and-block-group'], self.theme['pool-rect']['pad-spec']['top'])
        transformer = TransformBuilder()
        transformer.setTranslation(channel_collection_svg_xy)
        channel_collection_svg.set_transform(transformer.getTransform())

        svg_group.addElement(outline_svg)
        svg_group.addElement(label_svg)
        svg_group.addElement(channel_collection_svg)

        # wrap it in a svg element
        info('....assembling pool [{0}:{1}:{2}]'.format(self.bpmn_id, self.lane_id, self.pool_id))
        return SvgElement(svg=svg_group, width=group_width, height=group_height)

    def tune_label_element(self, label_element_target_width):
        label_svg_element = self.node_elements[1]

        # this is a group with a rect and an svg, we just add the differential in width to both elements
        group = label_svg_element.svg
        # we know that the rect is the first child and svg is the second child
        rect = group.getElementAt(0)
        svg = group.getElementAt(1)

        if label_element_target_width > rect.get_width():
            width_to_increase = label_element_target_width - rect.get_width()
            rect.set_width(rect.get_width() + width_to_increase)
            svg.set_width(svg.get_width() + width_to_increase)
            label_svg_element.width = label_svg_element.width + width_to_increase

    def tune_channel_collection_element(self, channel_collection_target_width):
        channel_collection_svg_element = self.node_elements[0]

        # this is a group with a rect and one or more element groups, we just add the differential in width to the rect
        group = channel_collection_svg_element.svg
        width_to_increase = channel_collection_target_width - channel_collection_svg_element.width
        if width_to_increase > 0:
            # we know that the rect is the first child
            rect = group.getElementAt(0)
            # TODO
            # rect.set_width(rect.get_width() + width_to_increase)
            channel_collection_svg_element.width = channel_collection_target_width

    def get_height(self):
        channel_collection_svg_element = self.node_elements[0]
        return channel_collection_svg_element.height + self.theme['pool-rect']['pad-spec']['top'] + self.theme['pool-rect']['pad-spec']['bottom']

    def get_max_width_of_elements_of_children(self):
        label_svg_element = self.node_elements[1]
        channel_collection_svg_element = self.node_elements[0]
        return label_svg_element.width, channel_collection_svg_element.width
