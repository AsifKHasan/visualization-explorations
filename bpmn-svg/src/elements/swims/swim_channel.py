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
    'task':                     {'m': 'elements.activities.tasks.activity_task',                                        'c': 'ActivityTask',                                'g': 'Activity'},
    'businessRuleTask':         {'m': 'elements.activities.tasks.activity_task_business_rule',                          'c': 'ActivityTaskBusinessRule',                    'g': 'Activity'},
    'manualTask':               {'m': 'elements.activities.tasks.activity_task_manual',                                 'c': 'ActivityTaskManual',                          'g': 'Activity'},
    'receiveTask':              {'m': 'elements.activities.tasks.activity_task_receive',                                'c': 'ActivityTaskReceive',                         'g': 'Activity'},
    'scriptTask':               {'m': 'elements.activities.tasks.activity_task_script',                                 'c': 'ActivityTaskScript',                          'g': 'Activity'},
    'sendTask':                 {'m': 'elements.activities.tasks.activity_task_send',                                   'c': 'ActivityTaskSend',                            'g': 'Activity'},
    'serviceTask':              {'m': 'elements.activities.tasks.activity_task_service',                                'c': 'ActivityTaskService',                         'g': 'Activity'},
    'userTask':                 {'m': 'elements.activities.tasks.activity_task_user',                                   'c': 'ActivityTaskUser',                            'g': 'Activity'},

    # calls
    'call':                     {'m': 'elements.activities.calls.activity_call',                                        'c': 'ActivityCall',                                'g': 'Activity'},
    'businessRuleCall':         {'m': 'elements.activities.calls.activity_call_business_rule',                          'c': 'ActivityCallBusinessRule',                    'g': 'Activity'},
    'manualCall':               {'m': 'elements.activities.calls.activity_call_manual',                                 'c': 'ActivityCallManual',                          'g': 'Activity'},
    'scriptCall':               {'m': 'elements.activities.calls.activity_call_script',                                 'c': 'ActivityCallScript',                          'g': 'Activity'},
    'userCall':                 {'m': 'elements.activities.calls.activity_call_user',                                   'c': 'ActivityCallUser',                            'g': 'Activity'},

    # subprocesses
    'process':                  {'m': 'elements.activities.subprocesses.activity_subprocess',                           'c': 'ActivitySubprocess',                          'g': 'Activity'},
    'adhoc':                    {'m': 'elements.activities.subprocesses.activity_subprocess_adhoc',                     'c': 'ActivityAdhocSubprocess',                     'g': 'Activity'},
    'transaction':              {'m': 'elements.activities.subprocesses.activity_subprocess_transaction',               'c': 'ActivityTransactionSubprocess',               'g': 'Activity'},

    # event subprocesses
    'event':                    {'m': 'elements.activities.subprocesses.activity_subprocess_event',                     'c': 'ActivityEventSubprocess',                     'g': 'Activity'},
    'eventCompensation':        {'m': 'elements.activities.subprocesses.events.activity_event_compensation',            'c': 'ActivityEventCompensation',                   'g': 'Activity'},
    'eventConditional':         {'m': 'elements.activities.subprocesses.events.activity_event_conditional',             'c': 'ActivityEventConditional',                    'g': 'Activity'},
    'eventConditionalNon':      {'m': 'elements.activities.subprocesses.events.activity_event_conditional_non',         'c': 'ActivityEventConditionalNon',                 'g': 'Activity'},
    'eventError':               {'m': 'elements.activities.subprocesses.events.activity_event_error',                   'c': 'ActivityEventError',                          'g': 'Activity'},
    'eventEscalation':          {'m': 'elements.activities.subprocesses.events.activity_event_escalation',              'c': 'ActivityEventEscalation',                     'g': 'Activity'},
    'eventEscalationNon':       {'m': 'elements.activities.subprocesses.events.activity_event_escalation_non',          'c': 'ActivityEventEscalationNon',                  'g': 'Activity'},
    'eventMessage':             {'m': 'elements.activities.subprocesses.events.activity_event_message',                 'c': 'ActivityEventMessage',                        'g': 'Activity'},
    'eventMessageNon':          {'m': 'elements.activities.subprocesses.events.activity_event_message_non',             'c': 'ActivityEventMessageNon',                     'g': 'Activity'},
    'eventMultiple':            {'m': 'elements.activities.subprocesses.events.activity_event_multiple',                'c': 'ActivityEventMultiple',                       'g': 'Activity'},
    'eventMultipleNon':         {'m': 'elements.activities.subprocesses.events.activity_event_multiple_non',            'c': 'ActivityEventMultipleNon',                    'g': 'Activity'},
    'eventParallelMultiple':    {'m': 'elements.activities.subprocesses.events.activity_event_parallel_multiple',       'c': 'ActivityEventParallelMultiple',               'g': 'Activity'},
    'eventParallelMultipleNon': {'m': 'elements.activities.subprocesses.events.activity_event_parallel_multiple_non',   'c': 'ActivityEventParallelMultipleNon',            'g': 'Activity'},
    'eventSignal':              {'m': 'elements.activities.subprocesses.events.activity_event_signal',                  'c': 'ActivityEventSignal',                         'g': 'Activity'},
    'eventSignalNon':           {'m': 'elements.activities.subprocesses.events.activity_event_signal_non',              'c': 'ActivityEventSignalNon',                      'g': 'Activity'},
    'eventTimer':               {'m': 'elements.activities.subprocesses.events.activity_event_timer',                   'c': 'ActivityEventTimer',                          'g': 'Activity'},
    'eventTimerNon':            {'m': 'elements.activities.subprocesses.events.activity_event_timer_non',               'c': 'ActivityEventTimerNon',                       'g': 'Activity'},

    ### artifact    ------------------------------------------------------------------------------------------------------------------------------
    # artifacts
    'group':                    {'m': 'elements.artifacts.artifact_group',                                              'c': 'ArtifactGroup',                               'g': 'Artifact'},
    'annotation':               {'m': 'elements.artifacts.artifact_text_annotation',                                    'c': 'ArtifactTextAnnotation',                      'g': 'Artifact'},

    ### data        ------------------------------------------------------------------------------------------------------------------------------
    'data':                     {'m': 'elements.datas.data_object',                                                     'c': 'DataObject',                                  'g': 'Data'},
    'dataCollection':           {'m': 'elements.datas.data_collection',                                                 'c': 'DataCollection',                              'g': 'Data'},
    'dataInput':                {'m': 'elements.datas.data_input',                                                      'c': 'DataInput',                                   'g': 'Data'},
    'dataInputCollection':      {'m': 'elements.datas.data_input_collection',                                           'c': 'DataInputCollection',                         'g': 'Data'},
    'dataOutput':               {'m': 'elements.datas.data_output',                                                     'c': 'DataOutput',                                  'g': 'Data'},
    'dataOutputCollection':     {'m': 'elements.datas.data_output_collection',                                          'c': 'DataOutputCollection',                        'g': 'Data'},
    'dataStore':                {'m': 'elements.datas.data_store',                                                      'c': 'DataStore',                                   'g': 'Data'},

    ### event      ------------------------------------------------------------------------------------------------------------------------------
    #   start events
    'start':                    {'m': 'elements.events.starts.event_start',                                             'c': 'EventStart',                                  'g': 'Event'},
    'startCompensation':        {'m': 'elements.events.starts.event_start_compensation',                                'c': 'EventStartCompensation',                      'g': 'Event'},
    'startConditional':         {'m': 'elements.events.starts.event_start_conditional',                                 'c': 'EventStartConditional',                       'g': 'Event'},
    'startConditionalNon':      {'m': 'elements.events.starts.event_start_conditional_non',                             'c': 'EventStartConditionalNon',                    'g': 'Event'},
    'startError':               {'m': 'elements.events.starts.event_start_error',                                       'c': 'EventStartError',                             'g': 'Event'},
    'startEscalation':          {'m': 'elements.events.starts.event_start_escalation',                                  'c': 'EventStartEscalation',                        'g': 'Event'},
    'startEscalationNon':       {'m': 'elements.events.starts.event_start_escalation_non',                              'c': 'EventStartEscalationNon',                     'g': 'Event'},
    'startMessage':             {'m': 'elements.events.starts.event_start_message',                                     'c': 'EventStartMessage',                           'g': 'Event'},
    'startMessageNon':          {'m': 'elements.events.starts.event_start_message_non',                                 'c': 'EventStartMessageNon',                        'g': 'Event'},
    'startMultiple':            {'m': 'elements.events.starts.event_start_multiple',                                    'c': 'EventStartMultiple',                          'g': 'Event'},
    'startMultipleNon':         {'m': 'elements.events.starts.event_start_multiple_non',                                'c': 'EventStartMultipleNon',                       'g': 'Event'},
    'startParallelMultiple':    {'m': 'elements.events.starts.event_start_parallel_multiple',                           'c': 'EventStartParallelMultiple',                  'g': 'Event'},
    'startParallelMultipleNon': {'m': 'elements.events.starts.event_start_parallel_multiple_non',                       'c': 'EventStartParallelMultipleNon',               'g': 'Event'},
    'startSignal':              {'m': 'elements.events.starts.event_start_signal',                                      'c': 'EventStartSignal',                            'g': 'Event'},
    'startSignalNon':           {'m': 'elements.events.starts.event_start_signal_non',                                  'c': 'EventStartSignalNon',                         'g': 'Event'},
    'startTimer':               {'m': 'elements.events.starts.event_start_timer',                                       'c': 'EventStartTimer',                             'g': 'Event'},
    'startTimerNon':            {'m': 'elements.events.starts.event_start_timer_non',                                   'c': 'EventStartTimerNon',                          'g': 'Event'},

    #   end events
    'end':                      {'m': 'elements.events.ends.event_end',                                                 'c': 'EventEnd',                                    'g': 'Event'},
    'endCancel':                {'m': 'elements.events.ends.event_end_cancel',                                          'c': 'EventEndCancel',                              'g': 'Event'},
    'endCompensation':          {'m': 'elements.events.ends.event_end_compensation',                                    'c': 'EventEndCompensation',                        'g': 'Event'},
    'endError':                 {'m': 'elements.events.ends.event_end_error',                                           'c': 'EventEndError',                               'g': 'Event'},
    'endEscalation':            {'m': 'elements.events.ends.event_end_escalation',                                      'c': 'EventEndEscalation',                          'g': 'Event'},
    'endMessage':               {'m': 'elements.events.ends.event_end_message',                                         'c': 'EventEndMessage',                             'g': 'Event'},
    'endMultiple':              {'m': 'elements.events.ends.event_end_multiple',                                        'c': 'EventEndMultiple',                            'g': 'Event'},
    'endSignal':                {'m': 'elements.events.ends.event_end_signal',                                          'c': 'EventEndSignal',                              'g': 'Event'},
    'endTerminate':             {'m': 'elements.events.ends.event_end_terminate',                                       'c': 'EventEndTerminate',                           'g': 'Event'},

    #   intermediate events
    'intermediate':             {'m': 'elements.events.intermediates.event_intermediate',                               'c': 'EventIntermediate',                           'g': 'Event'},
    'catchCancel':              {'m': 'elements.events.intermediates.event_intermediate_catch_cancel',                  'c': 'EventIntermediateCatchCancel',                'g': 'Event'},
    'catchCompensation':        {'m': 'elements.events.intermediates.event_intermediate_catch_compensation',            'c': 'EventIntermediateCatchCompensation',          'g': 'Event'},
    'throwCompensation':        {'m': 'elements.events.intermediates.event_intermediate_throw_compensation',            'c': 'EventIntermediateThrowCompensation',          'g': 'Event'},
    'catchError':               {'m': 'elements.events.intermediates.event_intermediate_catch_error',                   'c': 'EventIntermediateCatchError',                 'g': 'Event'},
    'catchEscalation':          {'m': 'elements.events.intermediates.event_intermediate_catch_escalation',              'c': 'EventIntermediateCatchEscalation',            'g': 'Event'},
    'catchEscalationNon':       {'m': 'elements.events.intermediates.event_intermediate_catch_escalation_non',          'c': 'EventIntermediateCatchEscalationNon',         'g': 'Event'},
    'throwEscalation':          {'m': 'elements.events.intermediates.event_intermediate_throw_escalation',              'c': 'EventIntermediateThrowEscalation',            'g': 'Event'},
    'catchLink':                {'m': 'elements.events.intermediates.event_intermediate_catch_link',                    'c': 'EventIntermediateCatchLink',                  'g': 'Event'},
    'throwLink':                {'m': 'elements.events.intermediates.event_intermediate_throw_link',                    'c': 'EventIntermediateThrowLink',                  'g': 'Event'},
    'catchMessage':             {'m': 'elements.events.intermediates.event_intermediate_catch_message',                 'c': 'EventIntermediateCatchMessage',               'g': 'Event'},
    'catchMessageNon':          {'m': 'elements.events.intermediates.event_intermediate_catch_message_non',             'c': 'EventIntermediateCatchMessageNon',            'g': 'Event'},
    'throwMessage':             {'m': 'elements.events.intermediates.event_intermediate_throw_message',                 'c': 'EventIntermediateThrowMessage',               'g': 'Event'},
    'catchMultiple':            {'m': 'elements.events.intermediates.event_intermediate_catch_multiple',                'c': 'EventIntermediateCatchMultiple',              'g': 'Event'},
    'catchMultipleNon':         {'m': 'elements.events.intermediates.event_intermediate_catch_multiple_non',            'c': 'EventIntermediateCatchMultipleNon',           'g': 'Event'},
    'throwMultiple':            {'m': 'elements.events.intermediates.event_intermediate_throw_multiple',                'c': 'EventIntermediateThrowMultiple',              'g': 'Event'},
    'catchParallelMultiple':    {'m': 'elements.events.intermediates.event_intermediate_catch_parallel_multiple',       'c': 'EventIntermediateCatchParallelMultiple',      'g': 'Event'},
    'catchParallelMultipleNon': {'m': 'elements.events.intermediates.event_intermediate_catch_parallel_multiple_non',   'c': 'EventIntermediateCatchParallelMultipleNon',   'g': 'Event'},
    'catchSignal':              {'m': 'elements.events.intermediates.event_intermediate_catch_signal',                  'c': 'EventIntermediateCatchSignal',                'g': 'Event'},
    'catchSignalNon':           {'m': 'elements.events.intermediates.event_intermediate_catch_signal_non',              'c': 'EventIntermediateCatchSignalNon',             'g': 'Event'},
    'throwSignal':              {'m': 'elements.events.intermediates.event_intermediate_throw_signal',                  'c': 'EventIntermediateThrowSignal',                'g': 'Event'},
    'conditional':              {'m': 'elements.events.intermediates.event_intermediate_conditional',                   'c': 'EventIntermediateConditional',                'g': 'Event'},
    'conditionalNon':           {'m': 'elements.events.intermediates.event_intermediate_conditional_non',               'c': 'EventIntermediateConditionalNon',             'g': 'Event'},
    'timer':                    {'m': 'elements.events.intermediates.event_intermediate_timer',                         'c': 'EventIntermediateTimer',                      'g': 'Event'},
    'timerNon':                 {'m': 'elements.events.intermediates.event_intermediate_timer_non',                     'c': 'EventIntermediateTimerNon',                   'g': 'Event'},

    # gateways
    'inclusive':                {'m': 'elements.gateways.gateway_inclusive',                                            'c': 'GatewayInclusive',                            'g': 'Gateway'},
    'exclusive':                {'m': 'elements.gateways.gateway_exclusive',                                            'c': 'GatewayExclusive',                            'g': 'Gateway'},
    'parallel':                 {'m': 'elements.gateways.gateway_parallel',                                             'c': 'GatewayParallel',                             'g': 'Gateway'},
    'complex':                  {'m': 'elements.gateways.gateway_complex',                                              'c': 'GatewayComplex',                              'g': 'Gateway'},
    'eventBased':               {'m': 'elements.gateways.gateway_event_based',                                          'c': 'GatewayEventBased',                           'g': 'Gateway'},
    'eventBasedStart':          {'m': 'elements.gateways.gateway_event_based_start',                                    'c': 'GatewayEventBasedStart',                      'g': 'Gateway'},
    'eventBasedParallelStart':  {'m': 'elements.gateways.gateway_event_based_parallel_start',                           'c': 'GatewayEventBasedParallelStart',              'g': 'Gateway'},
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
        # get a filtered list of edges containing only those where from-node and to-node both are in this channel
        self.channel_dict['channel-edges'] = []
        local_nodes = self.channel_dict['channel-nodes'].keys()
        for edge in self.edges:
            if edge['from'] in local_nodes and edge['to'] in local_nodes:
                from_node = self.channel_dict['channel-nodes'][edge['from']]
                to_node = self.channel_dict['channel-nodes'][edge['to']]
                edge_type = EDGE_TYPE[edge['type']]
                edge_label = edge.get('label', None)

                # create an appropriate flow object
                flow_object = FlowObject(edge_type)
                flow_svg_element = flow_object.connect_within_channel(from_node, to_node, edge_label)

                # add to channel svg group
                if flow_svg_element is not None and flow_svg_element.svg is not None:
                    self.channel_dict['channel-element']['svg'].addElement(flow_svg_element.svg)

                    # store object for future reference
                    edge_object = {'edge': edge, 'type': edge_type, 'svg': flow_svg_element.svg, 'width': flow_svg_element.width, 'height': flow_svg_element.height}
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
                self.channel_dict['channel-nodes'][node_id]['category'] = CLASSES[node_data['type']]['g']
                self.channel_dict['channel-nodes'][node_id]['type'] = node_data['type']
                self.channel_dict['channel-nodes'][node_id]['svg'] = svg_element.svg
                self.channel_dict['channel-nodes'][node_id]['width'] = svg_element.width
                self.channel_dict['channel-nodes'][node_id]['height'] = svg_element.height
                self.channel_dict['channel-nodes'][node_id]['snap-points'] = svg_element.snap_points
                self.channel_dict['channel-nodes'][node_id]['label-pos'] = svg_element.label_pos
                # print('----------------------------------------------------------------------------------------------------------------')
                # print(self.channel_dict['channel-nodes'][node_id])
                # print('----------------------------------------------------------------------------------------------------------------')
            else:
                warn('node type [{0}] is not supported. skipping ..'.format(node_data['type']))

    def assemble_elements(self):
        # a channel is a rectangular area with padding for edge routes and nodes inside between the paddings
        # the edges are inside another rectangle, all inner references are from the outer (rectangle) group

        # wrap it in a svg group
        svg_group = G()

        # get the max height and cumulative width of all elements and adjust height and width accordingly
        outer_rect_height = self.get_max_node_height() + self.theme['channel-outer-rect']['pad-spec']['top'] + self.theme['channel-outer-rect']['pad-spec']['bottom']
        inner_rect_height = outer_rect_height - self.theme['channel-outer-rect']['pad-spec']['top'] - self.theme['channel-outer-rect']['pad-spec']['bottom']

        # now we have height and width adjusted, we place the elements with proper displacement
        transformer = TransformBuilder()
        current_x = self.theme['channel-outer-rect']['pad-spec']['left']
        for node_id, node_object in self.channel_dict['channel-nodes'].items():
            element_svg = node_object['svg']
            current_y = inner_rect_height/2 - node_object['height']/2 + self.theme['channel-outer-rect']['pad-spec']['top']

            # keep the x, y position and dimension for the node within the group for future reference
            node_object['xy'] = Point(current_x, current_y)
            transformer.setTranslation(node_object['xy'])
            element_svg.set_transform(transformer.getTransform())
            svg_group.addElement(element_svg)
            current_x = current_x + node_object['width'] + self.theme['channel-inner-rect']['dx-between-elements']

        outer_rect_width = current_x - self.theme['channel-inner-rect']['dx-between-elements'] + self.theme['channel-outer-rect']['pad-spec']['right']

        # channel outer rect
        channel_outer_rect_svg = Rect(width=outer_rect_width, height=outer_rect_height)
        channel_outer_rect_svg.set_style(StyleBuilder(self.theme['channel-outer-rect']['style']).getStyle())
        svg_group.addElement(channel_outer_rect_svg)

        # channel inner rect
        inner_rect_x = self.theme['channel-outer-rect']['pad-spec']['left']
        inner_rect_y = self.theme['channel-outer-rect']['pad-spec']['top']
        inner_rect_width = outer_rect_width - self.theme['channel-outer-rect']['pad-spec']['left'] - self.theme['channel-outer-rect']['pad-spec']['right']
        channel_inner_rect_svg = Rect(x=inner_rect_x, y=inner_rect_y, width=inner_rect_width, height=inner_rect_height)
        channel_inner_rect_svg.set_style(StyleBuilder(self.theme['channel-inner-rect']['style']).getStyle())
        svg_group.addElement(channel_inner_rect_svg)

        # store the svg and dimensions for future reference
        self.channel_dict['channel-element'] = {}
        self.channel_dict['channel-element']['svg'] = svg_group
        self.channel_dict['channel-element']['width'] = outer_rect_width
        self.channel_dict['channel-element']['height'] = outer_rect_height

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
