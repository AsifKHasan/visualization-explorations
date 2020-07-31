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
    ### activity    ------------------------------------------------------------------------------------------------------------------------------
    # activities
    'task':         {'m': 'elements.activities.tasks.activity_task',                            'c': 'ActivityTask'},
    'call':         {'m': 'elements.activities.calls.activity_call',                            'c': 'ActivityCall'},
    'process':      {'m': 'elements.activities.subprocesses.activity_subprocess',               'c': 'ActivitySubprocess'},
    'transaction':  {'m': 'elements.activities.subprocesses.activity_subprocess_transaction',   'c': 'ActivityTransactionSubprocess'},
    'event':        {'m': 'elements.activities.subprocesses.activity_subprocess_event',         'c': 'ActivityEventSubprocess'},
    'adhoc':        {'m': 'elements.activities.subprocesses.activity_subprocess_adhoc',         'c': 'ActivityAdhocSubprocess'},

    ### artifact    ------------------------------------------------------------------------------------------------------------------------------
    # artifacts
    'group':        {'m': 'elements.artifacts.artifact_group',              'c': 'ArtifactGroup'},
    'annotation':   {'m': 'elements.artifacts.artifact_text_annotation',    'c': 'ArtifactTextAnnotation'},

    ### data        ------------------------------------------------------------------------------------------------------------------------------
    'data':         {'m': 'elements.activities.data_object',                'c': 'DataObject'},

    ### event      ------------------------------------------------------------------------------------------------------------------------------
    #   start events
    'start':                    {'m': 'elements.events.starts.event_start',                                             'c': 'EventStart'},
    'startCompensation':        {'m': 'elements.events.starts.event_start_compensation',                                'c': 'EventStartCompensation'},
    'startConditional':         {'m': 'elements.events.starts.event_start_conditional',                                 'c': 'EventStartConditional'},
    'startConditionalNon':      {'m': 'elements.events.starts.event_start_conditional_non',                             'c': 'EventStartConditionalNon'},
    'startError':               {'m': 'elements.events.starts.event_start_error',                                       'c': 'EventStartError'},
    'startEscalation':          {'m': 'elements.events.starts.event_start_escalation',                                  'c': 'EventStartEscalation'},
    'startEscalationNon':       {'m': 'elements.events.starts.event_start_escalation_non',                              'c': 'EventStartEscalationNon'},
    'startMessage':             {'m': 'elements.events.starts.event_start_message',                                     'c': 'EventStartMessage'},
    'startMessageNon':          {'m': 'elements.events.starts.event_start_message_non',                                 'c': 'EventStartMessageNon'},
    'startMultiple':            {'m': 'elements.events.starts.event_start_multiple',                                    'c': 'EventStartMultiple'},
    'startMultipleNon':         {'m': 'elements.events.starts.event_start_multiple_non',                                'c': 'EventStartMultipleNon'},
    'startParallelMultiple':    {'m': 'elements.events.starts.event_start_parallel_multiple',                           'c': 'EventStartParallelMultiple'},
    'startParallelMultipleNon': {'m': 'elements.events.starts.event_start_parallel_multiple_non',                       'c': 'EventStartParallelMultipleNon'},
    'startSignal':              {'m': 'elements.events.starts.event_start_signal',                                      'c': 'EventStartSignal'},
    'startSignalNon':           {'m': 'elements.events.starts.event_start_signal_non',                                  'c': 'EventStartSignalNon'},
    'startTimer':               {'m': 'elements.events.starts.event_start_timer',                                       'c': 'EventStartTimer'},
    'startTimerNon':            {'m': 'elements.events.starts.event_start_timer_non',                                   'c': 'EventStartTimerNon'},

    #   end events
    'end':                      {'m': 'elements.events.ends.event_end',                                                 'c': 'EventEnd'},
    'endCancel':                {'m': 'elements.events.ends.event_end_cancel',                                          'c': 'EventEndCancel'},
    'endCompensate':            {'m': 'elements.events.ends.event_end_compensate',                                      'c': 'EventEndCompensate'},
    'endError':                 {'m': 'elements.events.ends.event_end_error',                                           'c': 'EventEndError'},
    'endEscalation':            {'m': 'elements.events.ends.event_end_escalation',                                      'c': 'EventEndEscalation'},
    'endMessage':               {'m': 'elements.events.ends.event_end_message',                                         'c': 'EventEndMessage'},
    'endMultiple':              {'m': 'elements.events.ends.event_end_multiple',                                        'c': 'EventEndMultiple'},
    'endSignal':                {'m': 'elements.events.ends.event_end_signal',                                          'c': 'EventEndSignal'},
    'endTerminate':             {'m': 'elements.events.ends.event_end_terminate',                                       'c': 'EventEndTerminate'},

    #   intermediate events
    'intermediate':             {'m': 'elements.events.intermediates.event_intermediate',                               'c': 'EventIntermediate'},
    'catchCancel':              {'m': 'elements.events.intermediates.event_intermediate_catch_cancel',                  'c': 'EventIntermediateCatchCancel'},
    'catchCompensation':        {'m': 'elements.events.intermediates.event_intermediate_catch_compensation',            'c': 'EventIntermediateCatchCompensation'},
    'throwCompensation':        {'m': 'elements.events.intermediates.event_intermediate_throw_compensation',            'c': 'EventIntermediateThrowCompensation'},
    'catchError':               {'m': 'elements.events.intermediates.event_intermediate_catch_error',                   'c': 'EventIntermediateCatchError'},
    'catchEscalation':          {'m': 'elements.events.intermediates.event_intermediate_catch_escalation',              'c': 'EventIntermediateCatchEscalation'},
    'catchEscalationNon':       {'m': 'elements.events.intermediates.event_intermediate_catch_escalation_non',          'c': 'EventIntermediateCatchEscalationNon'},
    'throwEscalation':          {'m': 'elements.events.intermediates.event_intermediate_throw_escalation',              'c': 'EventIntermediateThrowEscalation'},
    'catchLink':                {'m': 'elements.events.intermediates.event_intermediate_catch_link',                    'c': 'EventIntermediateCatchLink'},
    'throwLink':                {'m': 'elements.events.intermediates.event_intermediate_throw_link',                    'c': 'EventIntermediateThrowLink'},
    'catchMessage':             {'m': 'elements.events.intermediates.event_intermediate_catch_message',                 'c': 'EventIntermediateCatchMessage'},
    'catchMessageNon':          {'m': 'elements.events.intermediates.event_intermediate_catch_message_non',             'c': 'EventIntermediateCatchMessageNon'},
    'throwMessage':             {'m': 'elements.events.intermediates.event_intermediate_throw_message',                 'c': 'EventIntermediateThrowMessage'},
    'catchMultiple':            {'m': 'elements.events.intermediates.event_intermediate_catch_multiple',                'c': 'EventIntermediateCatchMultiple'},
    'catchMultipleNon':         {'m': 'elements.events.intermediates.event_intermediate_catch_multiple_non',            'c': 'EventIntermediateCatchMultipleNon'},
    'throwMultiple':            {'m': 'elements.events.intermediates.event_intermediate_throw_multiple',                'c': 'EventIntermediateThrowMultiple'},
    'catchParallelMultiple':    {'m': 'elements.events.intermediates.event_intermediate_catch_parallel_multiple',       'c': 'EventIntermediateCatchParallelMultiple'},
    'catchParallelMultipleNon': {'m': 'elements.events.intermediates.event_intermediate_catch_parallel_multiple_non',   'c': 'EventIntermediateCatchParallelMultipleNon'},
    'catchSignal':              {'m': 'elements.events.intermediates.event_intermediate_catch_signal',                  'c': 'EventIntermediateCatchSignal'},
    'catchSignalNon':           {'m': 'elements.events.intermediates.event_intermediate_catch_signal_non',              'c': 'EventIntermediateCatchSignalNon'},
    'throwSignal':              {'m': 'elements.events.intermediates.event_intermediate_throw_signal',                  'c': 'EventIntermediateThrowSignal'},
    'conditional':              {'m': 'elements.events.intermediates.event_intermediate_conditional',                   'c': 'EventIntermediateConditional'},
    'conditionalNon':           {'m': 'elements.events.intermediates.event_intermediate_conditional_non',               'c': 'EventIntermediateConditionalNon'},
    'timer':                    {'m': 'elements.events.intermediates.event_intermediate_timer',                         'c': 'EventIntermediateTimer'},
    'timerNon':                 {'m': 'elements.events.intermediates.event_intermediate_timer_non',                     'c': 'EventIntermediateTimerNon'},

    # gateways
    'inclusive':                {'m': 'elements.gateways.gateway_inclusive',                    'c': 'GatewayInclusive'},
    'exclusive':                {'m': 'elements.gateways.gateway_exclusive',                    'c': 'GatewayExclusive'},
    'parallel':                 {'m': 'elements.gateways.gateway_parallel',                     'c': 'GatewayParallel'},
    'complex':                  {'m': 'elements.gateways.gateway_complex',                      'c': 'GatewayComplex'},
    'eventBased':               {'m': 'elements.gateways.gateway_event_based',                  'c': 'GatewayEventBased'},
    'eventBasedStart':          {'m': 'elements.gateways.gateway_event_based_start',            'c': 'GatewayEventBasedStart'},
    'eventBasedParallelStart':  {'m': 'elements.gateways.gateway_event_based_parallel_start',   'c': 'GatewayEventBasedParallelStart'},

    # flows
    'sequence':     {'m': 'elements.flows.flow_sequence',                   'c': 'FlowSequence'},
    'message':      {'m': 'elements.flows.flow_message',                    'c': 'FlowMessage'},
    'association':  {'m': 'elements.flows.flow_association',                'c': 'FlowAssociation'},
    'dataflow':     {'m': 'elements.flows.flow_data_association',           'c': 'FlowDataAssociation'},
}

class BlockGroup(BpmnElement):
    def __init__(self, bpmn_id, lane_id, pool_id, nodes, edges):
        self.theme = self.current_theme['swims']['BlockGroup']
        self.bpmn_id, self.lane_id, self.pool_id, self.nodes, self.edges = bpmn_id, lane_id, pool_id, nodes, edges

    def to_svg(self, width_hint):
        # We go through a collect -> tune -> assemble flow

        # collect the svg elements, but do not assemble now. we need tuning before assembly
        self.collect_elements()

        # tune the svg elements as needed
        self.tune_elements()

        # finally assemble the svg elements into a final one
        final_svg_element = self.assemble_elements(width_hint)
        return final_svg_element

    def tune_elements(self):
        pass

    def assemble_elements(self, width_hint):
        # wrap it in a svg group
        group_id = '{0}:{1}:{2}'.format(self.bpmn_id, self.lane_id, self.pool_id)
        svg_group = G(id=group_id)

        # get the max height and cumulative width of all elements and adjustheight and width accordingly
        max_element_height = self.get_max_height(self.svg_elements)
        cumulative_width = self.get_cumulative_width(self.svg_elements)

        # we have found the bpmn elements, now render them within the block
        # TODO: vertically stack elements when cumulative width is > max-width

        # start with the height width hints
        group_width = max(width_hint, cumulative_width)
        group_height = max_element_height + self.theme['pad-spec']['top'] + self.theme['pad-spec']['bottom']

        # add theractangle
        block_group_rect_svg = Rect(width=group_width, height=group_height)
        block_group_rect_svg.set_style(StyleBuilder(self.theme['style']).getStyle())
        svg_group.addElement(block_group_rect_svg)

        # now we have height and width adjusted, we place the elements with proper displacement
        transformer = TransformBuilder()
        current_x = self.theme['pad-spec']['left']
        for svg_element in self.svg_elements:
            element_svg = svg_element.group
            current_y = group_height/2 - svg_element.specs['height']/2
            transformation_xy = '{0},{1}'.format(current_x, current_y)
            transformer.setTranslation(transformation_xy)
            # debug('........tranforming to {0}'.format(transformation_xy))
            element_svg.set_transform(transformer.getTransform())
            svg_group.addElement(element_svg)
            current_x = current_x + svg_element.specs['width'] + self.theme['dx-between-elements']

        # wrap it in a svg element
        group_spec = {'width': group_width, 'height': group_height}
        return SvgElement(group_spec, svg_group)

    def collect_elements(self):
        # iterate the nodes and get the node svg's
        self.svg_elements = []
        for node_id, node_data in self.nodes.items():
            # we know the node type
            if node_data['type'] in CLASSES:
                # get the svg element
                element_class = getattr(importlib.import_module(CLASSES[node_data['type']]['m']), CLASSES[node_data['type']]['c'])
                element_instance = element_class(self.bpmn_id, self.lane_id, self.pool_id, node_id, node_data)
                self.svg_elements.append(element_instance.to_svg())
            else:
                warn('node type [{0}] is not supported. skipping ..'.format(node_data['type']))

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
