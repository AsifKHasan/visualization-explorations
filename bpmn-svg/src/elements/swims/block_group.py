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

def is_in_channel(node_id, channel_list):
    if not channel_list:
        return None

    for channel in channel_list:
        if node_id in channel['channel-nodes']:
            return channel['channel-name']

    return None

class BlockGroup(BpmnElement):
    def __init__(self, bpmn_id, lane_id, pool_id, nodes, edges):
        self.theme = self.current_theme['swims']['BlockGroup']
        self.bpmn_id, self.lane_id, self.pool_id, self.nodes, self.edges = bpmn_id, lane_id, pool_id, nodes, edges

    def connect_nodes_inside_channel(self, channel, head, tail, type, label):
        # TODO: it is a quick hack connecting head's right snap-point with tail's left snap-point
        head_x = head['x'] + head['width']
        head_y = head['y'] + head['height']/2
        tail_x = tail['x']
        tail_y = tail['y'] + tail['height']/2

        edge_group_svg, edge_group_width, edge_group_height = a_labeled_line(point_from=Point(head_x, head_y), point_to=Point(tail_x, tail_y), label=label, spec=None)

        # add to channel svg group
        channel['channel-element']['svg'].addElement(edge_group_svg)

    def lay_edges_within_the_channel(self, channel):
        # get a filtered list of edges containing only those where head and tail both are in this channel
        local_edges = []
        local_nodes = channel['channel-nodes'].keys()
        for edge in self.edges:
            if edge['head'] in local_nodes and edge['tail'] in local_nodes:
                self.connect_nodes_inside_channel(channel=channel, head=channel['channel-nodes'][edge['head']], tail=channel['channel-nodes'][edge['tail']], type=edge['type'], label=edge.get('label', None))

    def lay_edges(self):
        # the easyest ones are the edges connecting nodes inside a channel, a channel is by definition straight horizontal stack of nodes, so edges are mostly straight lines except when there is a loop back from a child to a parent or grand-parent
        for channel_list in self.channels:
            for channel in channel_list:
                self.lay_edges_within_the_channel(channel)

    def assemble_elements(self):
        # channels are vertically stacked
        # root channels start at x=0
        # channels that are branch of some parent channel start horizontally after the node to which the first node is the tail
        # TODO: how to horizontally shift channels based on tail relation ship with heads from other lane/pool
        # TODO: how and where to place the island channel?

        # wrap it in a svg group
        group_id = '{0}:{1}:{2}'.format(self.bpmn_id, self.lane_id, self.pool_id)
        svg_group = G(id=group_id)


        # pprint(self.channels)

        # lay the channels, channels are vertically stacked, but only the root channels start at left, branches ar horizontally positioned so that they fall to the right of their parent node's position
        group_width = 0

        current_y = self.theme['pad-spec']['top']
        transformer = TransformBuilder()
        for channel_list in self.channels:
            for channel in channel_list:
                # if it is a root channel it, starts at left (0) x position
                if channel['root-channel'] == True:
                    current_x = self.theme['pad-spec']['left']
                else:
                    # we find the parent node from which this channel is branched and position accordingly
                    x_pos = self.x_of_node_in_channel(channel_name=channel['parent-channel'], node_id=channel['channel-name'])
                    if x_pos != 0:
                        current_x = self.theme['pad-spec']['left'] + x_pos + self.theme['dx-between-elements']
                    else:
                        current_x = self.theme['pad-spec']['left']

                channel_element = channel['channel-element']
                channel_element_svg = channel_element['svg']
                channel_element['x'] = current_x
                channel_element['y'] = current_y

                channel_xy = '{0},{1}'.format(current_x, current_y)
                transformer.setTranslation(channel_xy)
                channel_element_svg.set_transform(transformer.getTransform())
                svg_group.addElement(channel_element_svg)

                group_width = max(group_width, channel_element['x'] + channel_element['width'] + self.theme['pad-spec']['right'])
                current_y = current_y + channel_element['height'] + self.theme['dy-between-channels']

        group_height = current_y - self.theme['dy-between-channels'] + self.theme['pad-spec']['bottom']

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

        # pprint(root_channel)
        # pprint(root_channel.as_list())

        # change the data structure a little bit - make it an array of root channels, where root channels are array of objects ()
        self.channels = []
        channel = None
        for node_id_list in root_channel.as_list():
            if len(node_id_list) > 0:
                parent_channel_name = is_in_channel(node_id_list[0], channel)
                if not parent_channel_name:
                    # if the first node of the list is not in any channel created so far, this is a root channel
                    # create a new channel and append the {first_node: node_id_list} object
                    if channel: self.channels.append(channel)
                    channel = []
                    channel.append({'channel-name': node_id_list[0], 'root-channel': True, 'channel-nodes': {node_id: {} for node_id in node_id_list}})
                else:
                    # this must be a sub channel of a previous channel, append in the current channel (the first node becomes the name and will not be in the channel_nodes)
                    channel.append({'channel-name': node_id_list[0], 'root-channel': False, 'parent-channel': parent_channel_name, 'channel-nodes': {node_id: {} for node_id in node_id_list[1:]}})

        # append the last open channel
        if channel: self.channels.append(channel)

        # we need a special channel for islands
        if len(root_channel.islands):
            channel = []
            channel.append({'channel-name': '-', 'root-channel': False, 'parent-channel': None, 'channel-nodes': {node_id: {} for node_id in root_channel.islands}})
            self.channels.append(channel)

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
                        svg_element = element_instance.to_svg()
                        channel['channel-nodes'][node_id]['type'] = node_data['type']
                        channel['channel-nodes'][node_id]['svg'] = svg_element.group
                        channel['channel-nodes'][node_id]['width'] = svg_element.specs['width']
                        channel['channel-nodes'][node_id]['height'] = svg_element.specs['height']
                    else:
                        warn('node type [{0}] is not supported. skipping ..'.format(node_data['type']))

    def build_channels(self):
        # create the channel svg elements
        for channel_list in self.channels:
            for channel in channel_list:
                channel_element = assemble_channel(channel['channel-name'], channel['channel-nodes'], self.theme)
                # store the svg and dimensions for future reference
                channel['channel-element'] = {}
                channel['channel-element']['svg'] = channel_element.group
                channel['channel-element']['width'] = channel_element.specs['width']
                channel['channel-element']['height'] = channel_element.specs['height']

    def to_svg(self):
        # We go through a collect -> tune -> assemble flow

        # collect the svg elements, but do not assemble now. we need tuning before assembly
        self.collect_elements()

        # collect the svg elements, but do not assemble now. we need tuning before assembly
        self.build_channels()

        # lay the edges connecting the nodes
        self.lay_edges()

        # finally assemble the svg elements into a final one
        final_svg_element = self.assemble_elements()
        return final_svg_element

    def x_of_node_in_channel(self, channel_name, node_id):
        for channel_list in self.channels:
            for channel in channel_list:
                if channel['channel-name'] == channel_name:
                    # get the node
                    if node_id in channel['channel-nodes']:
                        # we actually return the x position after the node
                        return channel['channel-nodes'][node_id]['x'] + channel['channel-nodes'][node_id]['width']

        # we could not locate the node in the named channel
        return 0
