#!/usr/bin/env python3
'''
'''
import importlib

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

CLASSES = {
    # activities
    'task':         {'module': 'elements.blocks.activities.activity_task',              'class': 'ActivityTask'},
    'subprocess':   {'module': 'elements.blocks.activities.activity_subprocess',        'class': 'ActivitySubprocess'},
    'call':         {'module': 'elements.blocks.activities.activity_call',              'class': 'ActivityCall'},

    # artifacts
    'group':        {'module': 'elements.blocks.artifacts.artifact_group',              'class': 'ArtifactGroup'},
    'annotation':   {'module': 'elements.blocks.artifacts.artifact_text_annotation',    'class': 'ArtifactTextAnnotation'},

    # datas
    'data':         {'module': 'elements.blocks.activities.data_object',                'class': 'DataObject'},

    # events
    'start':        {'module': 'elements.blocks.events.event_start',                    'class': 'EventStart'},
    'end':          {'module': 'elements.blocks.events.event_end',                      'class': 'EventEnd'},
    'intermediate': {'module': 'elements.blocks.events.event_intermediate',             'class': 'EventIntermediate'},

    # gateways
    'exclusive':    {'module': 'elements.blocks.gateways.gateway_exclusive',            'class': 'GatewayExclusive'},

    # flows
    'sequence':     {'module': 'elements.blocks.flows.flow_sequence',                   'class': 'FlowSequence'},
    'message':      {'module': 'elements.blocks.flows.flow_message',                    'class': 'FlowMessage'},
    'association':  {'module': 'elements.blocks.flows.flow_association',                'class': 'FlowAssociation'},
    'dataflow':     {'module': 'elements.blocks.flows.flow_data_association',           'class': 'FlowDataAssociation'},
}

class BlockGroup(BpmnElement):
    def __init__(self):
        self.theme = self.current_theme['BlockGroup']

    def to_svg(self, bpmn_id, lane_id, pool_id, nodes, edges, width_hint):
        # We go through a collect -> tune -> assemble flow

        # collect the svg elements, but do not assemble now. we need tuning before assembly
        svg_elements = self.collect_elements(bpmn_id, lane_id, pool_id, nodes)

        # tune the svg elements as needed
        svg_elements = self.tune_elements(bpmn_id, lane_id, pool_id, nodes, svg_elements)

        # finally assemble the svg elements into a final one
        final_svg_element = self.assemble_elements(bpmn_id, lane_id, pool_id, nodes, width_hint, svg_elements)
        return final_svg_element

    def tune_elements(self, bpmn_id, lane_id, pool_id, nodes, svg_elements):
        return svg_elements

    def assemble_elements(self, bpmn_id, lane_id, pool_id, nodes, width_hint, svg_elements):
        # wrap it in a svg group
        group_id = '{0}:{1}:{2}-blocks'.format(bpmn_id, lane_id, pool_id)
        svg_group = G(id=group_id)

        # get the max height and cumulative width of all elements and adjust block height and width accordingly
        max_element_height = self.get_max_height(svg_elements)
        cumulative_width = self.get_cumulative_width(svg_elements)

        # we have found the bpmn elements, now render them within the block
        # TODO: vertically stack elements when cumulative width is > max-width

        # start with the height width hints
        group_width = max(width_hint, cumulative_width)
        group_height = max_element_height + self.theme['pad-spec']['top'] + self.theme['pad-spec']['bottom']

        # now we have height and width adjusted, we place the elements with proper displacement
        transformer = TransformBuilder()
        current_x = self.theme['pad-spec']['left']
        for svg_element in svg_elements:
            element_svg = svg_element.group
            current_y = group_height/2 - svg_element.specs['height']/2
            transformation_xy = '{0},{1}'.format(current_x, current_y)
            transformer.setTranslation(transformation_xy)
            # debug('........tranforming to {0}'.format(transformation_xy))
            element_svg.set_transform(transformer.getTransform())
            svg_group.addElement(element_svg)
            current_x = current_x + svg_element.specs['width'] + self.theme['dx-between-elements']

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}
        return SvgElement(group_specs, svg_group)

    def collect_elements(self, bpmn_id, lane_id, pool_id, nodes):
        # iterate the nodes and get the node svg's
        svg_elements = []
        for node_id, node_data in nodes.items():
            # we know the node type
            if node_data['type'] in CLASSES:
                # get the svg element
                element_class = getattr(importlib.import_module(CLASSES[node_data['type']]['module']), CLASSES[node_data['type']]['class'])
                element_instance = element_class()
                svg_elements.append(element_instance.to_svg(node_id, node_data))
            else:
                warn('node type [{0}] is not supported. skipping ..'.format(node_data['type']))

        return svg_elements

    def get_max_height(self, svg_elements):
        max_element_height = 0
        for svg_element in svg_elements:
            max_element_height = max(svg_element.specs['height'], max_element_height)

        return max_element_height

    def get_cumulative_width(self, svg_elements):
        cumulative_width = self.theme['pad-spec']['left'] + self.theme['pad-spec']['right']
        element_count = len(svg_elements)
        for svg_element in svg_elements:
            cumulative_width = cumulative_width + svg_element.specs['width'] + self.theme['dx-between-elements']

        if element_count > 0:
            cumulative_width = cumulative_width - self.theme['dx-between-elements']

        return cumulative_width
