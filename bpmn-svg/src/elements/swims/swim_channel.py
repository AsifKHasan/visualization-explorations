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

from util.geometry import Point

from util.logger import *
from util.svg_util import *

from elements.flows.flow_object import FlowObject

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

EDGE_TYPE = {
    '-->' : 'Sequence',
    '~~>' : 'Message',
    '...' : 'Association',
    '..>' : 'DirectedAssociation',
    '<.>' : 'BidirectionalAssociation',
}

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
}

def is_in_channel(node_id, channel_list):
    if not channel_list:
        return None

    for channel in channel_list:
        if node_id in channel['channel-nodes']:
            return channel['channel-name']

    return None

class SwimChannel(BpmnElement):
    def __init__(self, bpmn_id, lane_id, pool_id, nodes, edges, channel_dict):
        self.theme = self.current_theme['swims']['SwimChannel']
        self.bpmn_id, self.lane_id, self.pool_id, self.nodes, self.edges, self.channel_dict = bpmn_id, lane_id, pool_id, nodes, edges, channel_dict

    def lay_edges(self):
        # the easyest ones are the edges connecting nodes inside a channel, a channel is by definition straight horizontal stack of nodes, so edges are mostly straight lines except when there is a loop back from a child to a parent or grand-parent
        # get a filtered list of edges containing only those where head and tail both are in this channel
        self.channel_dict['channel-edges'] = []
        local_nodes = self.channel_dict['channel-nodes'].keys()
        for edge in self.edges:
            if edge['head'] in local_nodes and edge['tail'] in local_nodes:
                head_node = self.channel_dict['channel-nodes'][edge['head']]
                tail_node = self.channel_dict['channel-nodes'][edge['tail']]
                edge_type = EDGE_TYPE[edge['type']]
                edge_label = edge.get('label', None)

                # create an appropriate flow object
                flow_object = FlowObject(edge_type)
                flow_svg_element = flow_object.connect_within_channel(head_node, tail_node, edge_label)

                # add to channel svg group
                self.channel_dict['channel-element']['svg'].addElement(flow_svg_element.group)

                # store object for future reference
                edge_object = {'edge': edge, 'type': edge_type, 'svg': flow_svg_element.group, 'width': flow_svg_element.specs['width'], 'height': flow_svg_element.specs['height']}
                self.channel_dict['channel-edges'].append(edge_object)

    def collect_elements(self):
        for node_id in self.channel_dict['channel-nodes']:
            node_data = self.nodes[node_id]
            # we know the node type
            if node_data['type'] in CLASSES:
                # get the svg element
                element_class = getattr(importlib.import_module(CLASSES[node_data['type']]['m']), CLASSES[node_data['type']]['c'])
                element_instance = element_class(self.bpmn_id, self.lane_id, self.pool_id, node_id, node_data)
                svg_element = element_instance.to_svg()
                # print('----------------------------------------------------------------------------------------------------------------')
                # print(self.channel_dict['channel-nodes'][node_id])
                # print('----------------------------------------------------------------------------------------------------------------')
                self.channel_dict['channel-nodes'][node_id]
                self.channel_dict['channel-nodes'][node_id]['type'] = node_data['type']
                self.channel_dict['channel-nodes'][node_id]['svg'] = svg_element.group
                self.channel_dict['channel-nodes'][node_id]['width'] = svg_element.specs['width']
                self.channel_dict['channel-nodes'][node_id]['height'] = svg_element.specs['height']
                self.channel_dict['channel-nodes'][node_id]['snaps'] = svg_element.snaps
                # print('----------------------------------------------------------------------------------------------------------------')
                # print(self.channel_dict['channel-nodes'][node_id])
                # print('----------------------------------------------------------------------------------------------------------------')
            else:
                warn('node type [{0}] is not supported. skipping ..'.format(node_data['type']))

    def assemble_elements(self):
        # wrap it in a svg group
        svg_group = G()

        # get the max height and cumulative width of all elements and adjust height and width accordingly
        group_height = self.get_max_node_height()

        # now we have height and width adjusted, we place the elements with proper displacement
        transformer = TransformBuilder()
        current_x = 0
        for node_id, node_object in self.channel_dict['channel-nodes'].items():
            element_svg = node_object['svg']
            current_y = group_height/2 - node_object['height']/2

            # keep the x, y position and dimension for the node within the group for future reference
            node_object['xy'] = Point(current_x, current_y)

            transformation_xy = '{0},{1}'.format(current_x, current_y)
            transformer.setTranslation(node_object['xy'])
            # debug('........tranforming to {0}'.format(transformation_xy))
            element_svg.set_transform(transformer.getTransform())
            svg_group.addElement(element_svg)
            current_x = current_x + node_object['width'] + self.theme['dx-between-elements']

        group_width = current_x - self.theme['dx-between-elements']

        # the group rect
        channel_rect_svg = Rect(width=group_width, height=group_height)
        channel_rect_svg.set_style(StyleBuilder(self.theme['style']).getStyle())
        svg_group.addElement(channel_rect_svg)

        # store the svg and dimensions for future reference
        self.channel_dict['channel-element'] = {}
        self.channel_dict['channel-element']['svg'] = svg_group
        self.channel_dict['channel-element']['width'] = group_width
        self.channel_dict['channel-element']['height'] = group_height

    def to_svg(self):
        # We go through a collect -> tune -> assemble flow

        # collect the svg elements, but do not assemble now. we need tuning before assembly
        self.collect_elements()

        # collect the svg elements, but do not assemble now. we need tuning before assembly
        self.assemble_elements()

        # lay the edges connecting the nodes
        self.lay_edges()

    def get_max_node_height(self):
        max_element_height = 0
        for node_id, node_object in self.channel_dict['channel-nodes'].items():
            max_element_height = max(node_object['height'], max_element_height)

        return max_element_height

    def x_of_node(self, node_id):
        if node_id in self.channel_dict['channel-nodes']:
            # we actually return the x position after the node
            return self.channel_dict['channel-nodes'][node_id]['xy'].x + self.channel_dict['channel-nodes'][node_id]['width']

        # we could not locate the node in the named channel
        return 0
