#!/usr/bin/env python3
'''
'''
import importlib
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
from util.block_util import *

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

CLASSES = {
    ### activity    ------------------------------------------------------------------------------------------------------------------------------
    # tasks
    'task':                     {'m': 'elements.activities.tasks.activity_task',                                        'c': 'ActivityTask'},
    'businessRuleTask':         {'m': 'elements.activities.tasks.activity_task_business_rule',                          'c': 'ActivityTaskBusinessRule'},
    'manualTask':               {'m': 'elements.activities.tasks.activity_task_manual',                                 'c': 'ActivityTaskManual'},
    'receiveTask':              {'m': 'elements.activities.tasks.activity_task_receive',                                'c': 'ActivityTaskReceive'},
    'scriptTask':               {'m': 'elements.activities.tasks.activity_task_script',                                 'c': 'ActivityTaskScript'},
    'sendTask':                 {'m': 'elements.activities.tasks.activity_task_send',                                   'c': 'ActivityTaskSend'},
    'serviceTask':              {'m': 'elements.activities.tasks.activity_task_service',                                'c': 'ActivityTaskService'},
    'userTask':                 {'m': 'elements.activities.tasks.activity_task_user',                                   'c': 'ActivityTaskUser'},

    # calls
    'call':                     {'m': 'elements.activities.calls.activity_call',                                        'c': 'ActivityCall'},
    'businessRuleCall':         {'m': 'elements.activities.calls.activity_call_business_rule',                          'c': 'ActivityCallBusinessRule'},
    'manualCall':               {'m': 'elements.activities.calls.activity_call_manual',                                 'c': 'ActivityCallManual'},
    'scriptCall':               {'m': 'elements.activities.calls.activity_call_script',                                 'c': 'ActivityCallScript'},
    'userCall':                 {'m': 'elements.activities.calls.activity_call_user',                                   'c': 'ActivityCallUser'},

    # subprocesses
    'process':                  {'m': 'elements.activities.subprocesses.activity_subprocess',                           'c': 'ActivitySubprocess'},
    'adhoc':                    {'m': 'elements.activities.subprocesses.activity_subprocess_adhoc',                     'c': 'ActivityAdhocSubprocess'},
    'transaction':              {'m': 'elements.activities.subprocesses.activity_subprocess_transaction',               'c': 'ActivityTransactionSubprocess'},

    # event subprocesses
    'event':                    {'m': 'elements.activities.subprocesses.activity_subprocess_event',                     'c': 'ActivityEventSubprocess'},
    'eventCompensation':        {'m': 'elements.activities.subprocesses.events.activity_event_compensation',            'c': 'ActivityEventCompensation'},
    'eventConditional':         {'m': 'elements.activities.subprocesses.events.activity_event_conditional',             'c': 'ActivityEventConditional'},
    'eventConditionalNon':      {'m': 'elements.activities.subprocesses.events.activity_event_conditional_non',         'c': 'ActivityEventConditionalNon'},
    'eventError':               {'m': 'elements.activities.subprocesses.events.activity_event_error',                   'c': 'ActivityEventError'},
    'eventEscalation':          {'m': 'elements.activities.subprocesses.events.activity_event_escalation',              'c': 'ActivityEventEscalation'},
    'eventEscalationNon':       {'m': 'elements.activities.subprocesses.events.activity_event_escalation_non',          'c': 'ActivityEventEscalationNon'},
    'eventMessage':             {'m': 'elements.activities.subprocesses.events.activity_event_message',                 'c': 'ActivityEventMessage'},
    'eventMessageNon':          {'m': 'elements.activities.subprocesses.events.activity_event_message_non',             'c': 'ActivityEventMessageNon'},
    'eventMultiple':            {'m': 'elements.activities.subprocesses.events.activity_event_multiple',                'c': 'ActivityEventMultiple'},
    'eventMultipleNon':         {'m': 'elements.activities.subprocesses.events.activity_event_multiple_non',            'c': 'ActivityEventMultipleNon'},
    'eventParallelMultiple':    {'m': 'elements.activities.subprocesses.events.activity_event_parallel_multiple',       'c': 'ActivityEventParallelMultiple'},
    'eventParallelMultipleNon': {'m': 'elements.activities.subprocesses.events.activity_event_parallel_multiple_non',   'c': 'ActivityEventParallelMultipleNon'},
    'eventSignal':              {'m': 'elements.activities.subprocesses.events.activity_event_signal',                  'c': 'ActivityEventSignal'},
    'eventSignalNon':           {'m': 'elements.activities.subprocesses.events.activity_event_signal_non',              'c': 'ActivityEventSignalNon'},
    'eventTimer':               {'m': 'elements.activities.subprocesses.events.activity_event_timer',                   'c': 'ActivityEventTimer'},
    'eventTimerNon':            {'m': 'elements.activities.subprocesses.events.activity_event_timer_non',               'c': 'ActivityEventTimerNon'},

    ### artifact    ------------------------------------------------------------------------------------------------------------------------------
    # artifacts
    'group':                    {'m': 'elements.artifacts.artifact_group',                                              'c': 'ArtifactGroup'},
    'annotation':               {'m': 'elements.artifacts.artifact_text_annotation',                                    'c': 'ArtifactTextAnnotation'},

    ### data        ------------------------------------------------------------------------------------------------------------------------------
    'data':                     {'m': 'elements.datas.data_object',                                                     'c': 'DataObject'},
    'dataCollection':           {'m': 'elements.datas.data_collection',                                                 'c': 'DataCollection'},
    'dataInput':                {'m': 'elements.datas.data_input',                                                      'c': 'DataInput'},
    'dataInputCollection':      {'m': 'elements.datas.data_input_collection',                                           'c': 'DataInputCollection'},
    'dataOutput':               {'m': 'elements.datas.data_output',                                                     'c': 'DataOutput'},
    'dataOutputCollection':     {'m': 'elements.datas.data_output_collection',                                          'c': 'DataOutputCollection'},
    'dataStore':                {'m': 'elements.datas.data_store',                                                      'c': 'DataStore'},

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
    'endCompensation':          {'m': 'elements.events.ends.event_end_compensation',                                    'c': 'EventEndCompensation'},
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

def is_in_channel(node_id, channel):
    if not channel:
        return False

    for object in channel:
        if node_id in object['channel-nodes']:
            return True

    return False

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

    def assemble_channel(self, channel_name, channel_nodes):
        # wrap it in a svg group
        svg_group = G()

        # get the max height and cumulative width of all elements and adjust height and width accordingly
        max_element_height = self.get_max_height(channel_nodes)
        cumulative_width = self.get_cumulative_width(channel_nodes)

        # we have found the bpmn elements, now render them within the group
        # start with the height width hints
        group_width = cumulative_width
        group_height = max_element_height + self.theme['pad-spec']['top'] + self.theme['pad-spec']['bottom']

        # now we have height and width adjusted, we place the elements with proper displacement
        transformer = TransformBuilder()
        current_x = self.theme['pad-spec']['left']
        for node_id, svg_element in channel_nodes.items():
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

    def assemble_elements(self, width_hint):
        # wrap it in a svg group
        group_id = '{0}:{1}:{2}'.format(self.bpmn_id, self.lane_id, self.pool_id)
        svg_group = G(id=group_id)

        # create the channel svg elements
        group_width = 0
        group_height = 0
        transformer = TransformBuilder()
        for channel_list in self.channels:
            for channel in channel_list:
                channel_element = self.assemble_channel(channel['channel-name'], channel['channel-nodes'])
                channel['channel-element'] = channel_element


        # lay the channels, channels are vertically stacked, but only the root channels start at left, branches ar horizontally positioned so that they fall to the right of their parent node's position
        for channel_list in self.channels:
            for channel in channel_list:
                channel_element = channel['channel-element']
                channel_element_svg = channel_element.group

                current_x = 0
                channel_xy = '{0},{1}'.format(current_x, group_height)
                transformer.setTranslation(channel_xy)
                channel_element_svg.set_transform(transformer.getTransform())
                svg_group.addElement(channel_element_svg)

                group_width = max(group_width, channel_element.specs['width'])
                group_height = group_height + channel_element.specs['height']

        # add the ractangle
        block_group_rect_svg = Rect(width=group_width, height=group_height)
        block_group_rect_svg.set_style(StyleBuilder(self.theme['style']).getStyle())
        svg_group.addElement(block_group_rect_svg)

        # wrap it in a svg element
        group_spec = {'width': group_width, 'height': group_height}
        return SvgElement(group_spec, svg_group)

    def collect_elements(self):
        # order and group nodes
        root_channel = group_nodes_inside_a_pool(
                                            bpmn_id=self.bpmn_id,
                                            lane_id=self.lane_id,
                                            pool_id=self.pool_id,
                                            pool_nodes=self.nodes,
                                            pool_edges=self.edges)

        # change the data structure a little bit - make it an array of root channels, where root channels are array of objects ()
        self.channels = []
        channel = None
        for node_id_list in root_channel.as_list():
            if len(node_id_list) > 0:
                if not is_in_channel(node_id_list[0], channel):
                    # if the first node of the list is not in any channel created so far, this is a root channel
                    # create a new channel and append the {first_node: node_id_list} object
                    if channel: self.channels.append(channel)
                    channel = []
                    channel.append({'channel-name': node_id_list[0], 'channel-nodes': {node_id: None for node_id in node_id_list}})
                else:
                    # this must be a sub channel of a previous channel, append in the current channel (the first node becomes the name and will not be in the channel_nodes)
                    channel.append({'channel-name': node_id_list[0], 'channel-nodes': {node_id: None for node_id in node_id_list[1:]}})

        # append the last open channel
        if channel: self.channels.append(channel)

        # pprint(self.channels)

        # now we have the channels defined, get the svg elements
        for channel_list in self.channels:
            for channel in channel_list:
                for node_id in channel['channel-nodes']:
                    node_data = self.nodes[node_id]
                    # we know the node type
                    if node_data['type'] in CLASSES:
                        # get the svg element
                        element_class = getattr(importlib.import_module(CLASSES[node_data['type']]['m']), CLASSES[node_data['type']]['c'])
                        element_instance = element_class(self.bpmn_id, self.lane_id, self.pool_id, node_id, node_data)
                        channel['channel-nodes'][node_id] = element_instance.to_svg()
                    else:
                        warn('node type [{0}] is not supported. skipping ..'.format(node_data['type']))

    def get_max_height(self, channel_nodes):
        max_element_height = 0
        for node_id, svg_element in channel_nodes.items():
            max_element_height = max(svg_element.specs['height'], max_element_height)

        return max_element_height

    def get_cumulative_width(self, channel_nodes):
        cumulative_width = self.theme['pad-spec']['left'] + self.theme['pad-spec']['right']
        element_count = len(channel_nodes.keys())
        for node_id, svg_element in channel_nodes.items():
            cumulative_width = cumulative_width + svg_element.specs['width'] + self.theme['dx-between-elements']

        if element_count > 0:
            cumulative_width = cumulative_width - self.theme['dx-between-elements']

        return cumulative_width
