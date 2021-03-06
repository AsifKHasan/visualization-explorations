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

from elements.flows.flow_object import EdgeObject
from elements.flows.channel_flow import ChannelFlow

from elements.bpmn_element import BpmnElement, NodeObject, EDGE_TYPE
from elements.svg_element import SvgElement

CLASSES = {
    ### activity    ------------------------------------------------------------------------------------------------------------------------------
    # tasks
    'task':                     {'m': 'elements.activities.tasks.activity_task',                                        'c': 'ActivityTask',                                'g': 'activity'},
    'businessRuleTask':         {'m': 'elements.activities.tasks.activity_task_business_rule',                          'c': 'ActivityTaskBusinessRule',                    'g': 'activity'},
    'manualTask':               {'m': 'elements.activities.tasks.activity_task_manual',                                 'c': 'ActivityTaskManual',                          'g': 'activity'},
    'receiveTask':              {'m': 'elements.activities.tasks.activity_task_receive',                                'c': 'ActivityTaskReceive',                         'g': 'activity'},
    'scriptTask':               {'m': 'elements.activities.tasks.activity_task_script',                                 'c': 'ActivityTaskScript',                          'g': 'activity'},
    'sendTask':                 {'m': 'elements.activities.tasks.activity_task_send',                                   'c': 'ActivityTaskSend',                            'g': 'activity'},
    'serviceTask':              {'m': 'elements.activities.tasks.activity_task_service',                                'c': 'ActivityTaskService',                         'g': 'activity'},
    'userTask':                 {'m': 'elements.activities.tasks.activity_task_user',                                   'c': 'ActivityTaskUser',                            'g': 'activity'},

    # calls
    'call':                     {'m': 'elements.activities.calls.activity_call',                                        'c': 'ActivityCall',                                'g': 'activity'},
    'businessRuleCall':         {'m': 'elements.activities.calls.activity_call_business_rule',                          'c': 'ActivityCallBusinessRule',                    'g': 'activity'},
    'manualCall':               {'m': 'elements.activities.calls.activity_call_manual',                                 'c': 'ActivityCallManual',                          'g': 'activity'},
    'scriptCall':               {'m': 'elements.activities.calls.activity_call_script',                                 'c': 'ActivityCallScript',                          'g': 'activity'},
    'userCall':                 {'m': 'elements.activities.calls.activity_call_user',                                   'c': 'ActivityCallUser',                            'g': 'activity'},

    # subprocesses
    'process':                  {'m': 'elements.activities.subprocesses.activity_subprocess',                           'c': 'ActivitySubprocess',                          'g': 'activity'},
    'adhoc':                    {'m': 'elements.activities.subprocesses.activity_subprocess_adhoc',                     'c': 'ActivityAdhocSubprocess',                     'g': 'activity'},
    'transaction':              {'m': 'elements.activities.subprocesses.activity_subprocess_transaction',               'c': 'ActivityTransactionSubprocess',               'g': 'activity'},

    # event subprocesses
    'event':                    {'m': 'elements.activities.subprocesses.activity_subprocess_event',                     'c': 'ActivityEventSubprocess',                     'g': 'activity'},
    'eventCompensation':        {'m': 'elements.activities.subprocesses.events.activity_event_compensation',            'c': 'ActivityEventCompensation',                   'g': 'activity'},
    'eventConditional':         {'m': 'elements.activities.subprocesses.events.activity_event_conditional',             'c': 'ActivityEventConditional',                    'g': 'activity'},
    'eventConditionalNon':      {'m': 'elements.activities.subprocesses.events.activity_event_conditional_non',         'c': 'ActivityEventConditionalNon',                 'g': 'activity'},
    'eventError':               {'m': 'elements.activities.subprocesses.events.activity_event_error',                   'c': 'ActivityEventError',                          'g': 'activity'},
    'eventEscalation':          {'m': 'elements.activities.subprocesses.events.activity_event_escalation',              'c': 'ActivityEventEscalation',                     'g': 'activity'},
    'eventEscalationNon':       {'m': 'elements.activities.subprocesses.events.activity_event_escalation_non',          'c': 'ActivityEventEscalationNon',                  'g': 'activity'},
    'eventMessage':             {'m': 'elements.activities.subprocesses.events.activity_event_message',                 'c': 'ActivityEventMessage',                        'g': 'activity'},
    'eventMessageNon':          {'m': 'elements.activities.subprocesses.events.activity_event_message_non',             'c': 'ActivityEventMessageNon',                     'g': 'activity'},
    'eventMultiple':            {'m': 'elements.activities.subprocesses.events.activity_event_multiple',                'c': 'ActivityEventMultiple',                       'g': 'activity'},
    'eventMultipleNon':         {'m': 'elements.activities.subprocesses.events.activity_event_multiple_non',            'c': 'ActivityEventMultipleNon',                    'g': 'activity'},
    'eventParallelMultiple':    {'m': 'elements.activities.subprocesses.events.activity_event_parallel_multiple',       'c': 'ActivityEventParallelMultiple',               'g': 'activity'},
    'eventParallelMultipleNon': {'m': 'elements.activities.subprocesses.events.activity_event_parallel_multiple_non',   'c': 'ActivityEventParallelMultipleNon',            'g': 'activity'},
    'eventSignal':              {'m': 'elements.activities.subprocesses.events.activity_event_signal',                  'c': 'ActivityEventSignal',                         'g': 'activity'},
    'eventSignalNon':           {'m': 'elements.activities.subprocesses.events.activity_event_signal_non',              'c': 'ActivityEventSignalNon',                      'g': 'activity'},
    'eventTimer':               {'m': 'elements.activities.subprocesses.events.activity_event_timer',                   'c': 'ActivityEventTimer',                          'g': 'activity'},
    'eventTimerNon':            {'m': 'elements.activities.subprocesses.events.activity_event_timer_non',               'c': 'ActivityEventTimerNon',                       'g': 'activity'},

    ### artifact    ------------------------------------------------------------------------------------------------------------------------------
    # artifacts
    'group':                    {'m': 'elements.artifacts.artifact_group',                                              'c': 'ArtifactGroup',                               'g': 'artifact'},
    'annotation':               {'m': 'elements.artifacts.artifact_text_annotation',                                    'c': 'ArtifactTextAnnotation',                      'g': 'artifact'},

    ### data        ------------------------------------------------------------------------------------------------------------------------------
    'data':                     {'m': 'elements.datas.data_object',                                                     'c': 'DataObject',                                  'g': 'data'},
    'dataCollection':           {'m': 'elements.datas.data_collection',                                                 'c': 'DataCollection',                              'g': 'data'},
    'dataInput':                {'m': 'elements.datas.data_input',                                                      'c': 'DataInput',                                   'g': 'data'},
    'dataInputCollection':      {'m': 'elements.datas.data_input_collection',                                           'c': 'DataInputCollection',                         'g': 'data'},
    'dataOutput':               {'m': 'elements.datas.data_output',                                                     'c': 'DataOutput',                                  'g': 'data'},
    'dataOutputCollection':     {'m': 'elements.datas.data_output_collection',                                          'c': 'DataOutputCollection',                        'g': 'data'},
    'dataStore':                {'m': 'elements.datas.data_store',                                                      'c': 'DataStore',                                   'g': 'data'},

    ### event      ------------------------------------------------------------------------------------------------------------------------------
    #   start events
    'start':                    {'m': 'elements.events.starts.event_start',                                             'c': 'EventStart',                                  'g': 'event'},
    'startCompensation':        {'m': 'elements.events.starts.event_start_compensation',                                'c': 'EventStartCompensation',                      'g': 'event'},
    'startConditional':         {'m': 'elements.events.starts.event_start_conditional',                                 'c': 'EventStartConditional',                       'g': 'event'},
    'startConditionalNon':      {'m': 'elements.events.starts.event_start_conditional_non',                             'c': 'EventStartConditionalNon',                    'g': 'event'},
    'startError':               {'m': 'elements.events.starts.event_start_error',                                       'c': 'EventStartError',                             'g': 'event'},
    'startEscalation':          {'m': 'elements.events.starts.event_start_escalation',                                  'c': 'EventStartEscalation',                        'g': 'event'},
    'startEscalationNon':       {'m': 'elements.events.starts.event_start_escalation_non',                              'c': 'EventStartEscalationNon',                     'g': 'event'},
    'startMessage':             {'m': 'elements.events.starts.event_start_message',                                     'c': 'EventStartMessage',                           'g': 'event'},
    'startMessageNon':          {'m': 'elements.events.starts.event_start_message_non',                                 'c': 'EventStartMessageNon',                        'g': 'event'},
    'startMultiple':            {'m': 'elements.events.starts.event_start_multiple',                                    'c': 'EventStartMultiple',                          'g': 'event'},
    'startMultipleNon':         {'m': 'elements.events.starts.event_start_multiple_non',                                'c': 'EventStartMultipleNon',                       'g': 'event'},
    'startParallelMultiple':    {'m': 'elements.events.starts.event_start_parallel_multiple',                           'c': 'EventStartParallelMultiple',                  'g': 'event'},
    'startParallelMultipleNon': {'m': 'elements.events.starts.event_start_parallel_multiple_non',                       'c': 'EventStartParallelMultipleNon',               'g': 'event'},
    'startSignal':              {'m': 'elements.events.starts.event_start_signal',                                      'c': 'EventStartSignal',                            'g': 'event'},
    'startSignalNon':           {'m': 'elements.events.starts.event_start_signal_non',                                  'c': 'EventStartSignalNon',                         'g': 'event'},
    'startTimer':               {'m': 'elements.events.starts.event_start_timer',                                       'c': 'EventStartTimer',                             'g': 'event'},
    'startTimerNon':            {'m': 'elements.events.starts.event_start_timer_non',                                   'c': 'EventStartTimerNon',                          'g': 'event'},

    #   end events
    'end':                      {'m': 'elements.events.ends.event_end',                                                 'c': 'EventEnd',                                    'g': 'event'},
    'endCancel':                {'m': 'elements.events.ends.event_end_cancel',                                          'c': 'EventEndCancel',                              'g': 'event'},
    'endCompensation':          {'m': 'elements.events.ends.event_end_compensation',                                    'c': 'EventEndCompensation',                        'g': 'event'},
    'endError':                 {'m': 'elements.events.ends.event_end_error',                                           'c': 'EventEndError',                               'g': 'event'},
    'endEscalation':            {'m': 'elements.events.ends.event_end_escalation',                                      'c': 'EventEndEscalation',                          'g': 'event'},
    'endMessage':               {'m': 'elements.events.ends.event_end_message',                                         'c': 'EventEndMessage',                             'g': 'event'},
    'endMultiple':              {'m': 'elements.events.ends.event_end_multiple',                                        'c': 'EventEndMultiple',                            'g': 'event'},
    'endSignal':                {'m': 'elements.events.ends.event_end_signal',                                          'c': 'EventEndSignal',                              'g': 'event'},
    'endTerminate':             {'m': 'elements.events.ends.event_end_terminate',                                       'c': 'EventEndTerminate',                           'g': 'event'},

    #   intermediate events
    'intermediate':             {'m': 'elements.events.intermediates.event_intermediate',                               'c': 'EventIntermediate',                           'g': 'event'},
    'catchCancel':              {'m': 'elements.events.intermediates.event_intermediate_catch_cancel',                  'c': 'EventIntermediateCatchCancel',                'g': 'event'},
    'catchCompensation':        {'m': 'elements.events.intermediates.event_intermediate_catch_compensation',            'c': 'EventIntermediateCatchCompensation',          'g': 'event'},
    'throwCompensation':        {'m': 'elements.events.intermediates.event_intermediate_throw_compensation',            'c': 'EventIntermediateThrowCompensation',          'g': 'event'},
    'catchError':               {'m': 'elements.events.intermediates.event_intermediate_catch_error',                   'c': 'EventIntermediateCatchError',                 'g': 'event'},
    'catchEscalation':          {'m': 'elements.events.intermediates.event_intermediate_catch_escalation',              'c': 'EventIntermediateCatchEscalation',            'g': 'event'},
    'catchEscalationNon':       {'m': 'elements.events.intermediates.event_intermediate_catch_escalation_non',          'c': 'EventIntermediateCatchEscalationNon',         'g': 'event'},
    'throwEscalation':          {'m': 'elements.events.intermediates.event_intermediate_throw_escalation',              'c': 'EventIntermediateThrowEscalation',            'g': 'event'},
    'catchLink':                {'m': 'elements.events.intermediates.event_intermediate_catch_link',                    'c': 'EventIntermediateCatchLink',                  'g': 'event'},
    'throwLink':                {'m': 'elements.events.intermediates.event_intermediate_throw_link',                    'c': 'EventIntermediateThrowLink',                  'g': 'event'},
    'catchMessage':             {'m': 'elements.events.intermediates.event_intermediate_catch_message',                 'c': 'EventIntermediateCatchMessage',               'g': 'event'},
    'catchMessageNon':          {'m': 'elements.events.intermediates.event_intermediate_catch_message_non',             'c': 'EventIntermediateCatchMessageNon',            'g': 'event'},
    'throwMessage':             {'m': 'elements.events.intermediates.event_intermediate_throw_message',                 'c': 'EventIntermediateThrowMessage',               'g': 'event'},
    'catchMultiple':            {'m': 'elements.events.intermediates.event_intermediate_catch_multiple',                'c': 'EventIntermediateCatchMultiple',              'g': 'event'},
    'catchMultipleNon':         {'m': 'elements.events.intermediates.event_intermediate_catch_multiple_non',            'c': 'EventIntermediateCatchMultipleNon',           'g': 'event'},
    'throwMultiple':            {'m': 'elements.events.intermediates.event_intermediate_throw_multiple',                'c': 'EventIntermediateThrowMultiple',              'g': 'event'},
    'catchParallelMultiple':    {'m': 'elements.events.intermediates.event_intermediate_catch_parallel_multiple',       'c': 'EventIntermediateCatchParallelMultiple',      'g': 'event'},
    'catchParallelMultipleNon': {'m': 'elements.events.intermediates.event_intermediate_catch_parallel_multiple_non',   'c': 'EventIntermediateCatchParallelMultipleNon',   'g': 'event'},
    'catchSignal':              {'m': 'elements.events.intermediates.event_intermediate_catch_signal',                  'c': 'EventIntermediateCatchSignal',                'g': 'event'},
    'catchSignalNon':           {'m': 'elements.events.intermediates.event_intermediate_catch_signal_non',              'c': 'EventIntermediateCatchSignalNon',             'g': 'event'},
    'throwSignal':              {'m': 'elements.events.intermediates.event_intermediate_throw_signal',                  'c': 'EventIntermediateThrowSignal',                'g': 'event'},
    'conditional':              {'m': 'elements.events.intermediates.event_intermediate_conditional',                   'c': 'EventIntermediateConditional',                'g': 'event'},
    'conditionalNon':           {'m': 'elements.events.intermediates.event_intermediate_conditional_non',               'c': 'EventIntermediateConditionalNon',             'g': 'event'},
    'timer':                    {'m': 'elements.events.intermediates.event_intermediate_timer',                         'c': 'EventIntermediateTimer',                      'g': 'event'},
    'timerNon':                 {'m': 'elements.events.intermediates.event_intermediate_timer_non',                     'c': 'EventIntermediateTimerNon',                   'g': 'event'},

    # gateways
    'inclusive':                {'m': 'elements.gateways.gateway_inclusive',                                            'c': 'GatewayInclusive',                            'g': 'gateway'},
    'exclusive':                {'m': 'elements.gateways.gateway_exclusive',                                            'c': 'GatewayExclusive',                            'g': 'gateway'},
    'parallel':                 {'m': 'elements.gateways.gateway_parallel',                                             'c': 'GatewayParallel',                             'g': 'gateway'},
    'complex':                  {'m': 'elements.gateways.gateway_complex',                                              'c': 'GatewayComplex',                              'g': 'gateway'},
    'eventBased':               {'m': 'elements.gateways.gateway_event_based',                                          'c': 'GatewayEventBased',                           'g': 'gateway'},
    'eventBasedStart':          {'m': 'elements.gateways.gateway_event_based_start',                                    'c': 'GatewayEventBasedStart',                      'g': 'gateway'},
    'eventBasedParallelStart':  {'m': 'elements.gateways.gateway_event_based_parallel_start',                           'c': 'GatewayEventBasedParallelStart',              'g': 'gateway'},
}

'''
    a channel is a horizontally laid group of nodes (bpmn elements)
'''
class SwimChannel(BpmnElement):
    def __init__(self, bpmn_id, lane_id, pool_id, nodes, edges, channel_object):
        self.bpmn_id, self.lane_id, self.pool_id, self.nodes, self.edges, self.channel_object = bpmn_id, lane_id, pool_id, nodes, edges, channel_object
        self.theme = self.current_theme['swims']['SwimChannel']
        self.channel_object.theme = self.theme

    def lay_edges(self):
        # get a filtered list of edges containing only those where from-node and to-node both are in this channel
        self.channel_object.edges = []
        local_nodes = self.channel_object.nodes.keys()
        for edge in self.edges:
            if edge['from'] in local_nodes and edge['to'] in local_nodes:
                from_node = self.channel_object.nodes[edge['from']]
                to_node = self.channel_object.nodes[edge['to']]
                edge_type = EDGE_TYPE[edge['type']]
                edge_label = edge.get('label', None)

                # create an appropriate flow object, use ChannelFlow which manages flows inside a SwimChannel
                flow_object = ChannelFlow(edge_type, self.channel_object)
                flow_svg_element = flow_object.create_flow(from_node, to_node, edge_label)

                # add to channel svg group
                if flow_svg_element is not None and flow_svg_element.svg is not None:
                    self.channel_object.element.svg.addElement(flow_svg_element.svg)

                    # store object for future reference
                    self.channel_object.edges.append(EdgeObject(edge=edge, type=edge_type, element=flow_svg_element))

    def collect_elements(self):
        for node_id in self.channel_object.nodes:
            node_data = self.nodes[node_id]
            # we know the node type
            if node_data['type'] in CLASSES:
                # get the svg element
                element_class = getattr(importlib.import_module(CLASSES[node_data['type']]['m']), CLASSES[node_data['type']]['c'])
                element_instance = element_class(self.bpmn_id, self.lane_id, self.pool_id, node_id, node_data)
                svg_element = element_instance.to_svg()
                self.channel_object.nodes[node_id] = NodeObject(id=node_id, category=CLASSES[node_data['type']]['g'], type=node_data['type'], styles=node_data['styles'], element=svg_element, instance=element_instance)
            else:
                warn('node type [{0}] is not supported. skipping ..'.format(node_data['type']))

    def assemble_elements(self):
        # a channel is a rectangular area with padding for edge routes and nodes inside between the paddings
        # the edges are inside another rectangle, all inner references are from the outer (rectangle) group

        # wrap it in a svg group
        svg_group = G()

        # get the max height and cumulative width of all elements and adjust height and width accordingly
        outer_rect_height = self.theme['channel-outer-rect']['pad-spec']['top'] + self.channel_object.max_node_height() + self.theme['channel-outer-rect']['pad-spec']['bottom']
        inner_rect_height = outer_rect_height - self.theme['channel-outer-rect']['pad-spec']['top'] - self.theme['channel-outer-rect']['pad-spec']['bottom']

        # now we have height and width adjusted, we place the elements with proper displacement
        transformer = TransformBuilder()
        current_x = self.theme['channel-outer-rect']['pad-spec']['left']
        for node_id, node_object in self.channel_object.nodes.items():
            node_svg_element = node_object.element
            current_y = inner_rect_height/2 - node_svg_element.height/2 + self.theme['channel-outer-rect']['pad-spec']['top']

            # the node may have a *move_x* style to indicate whether and how much it should move to east (+ve) or west (-ve)
            if 'move_x' in node_object.styles:
                move_x = float(node_object.styles['move_x'])
            else:
                move_x = 0

            current_x = current_x + move_x

            # keep the x, y position and dimension for the node within the group for future reference
            node_svg_element.xy = Point(current_x, current_y)
            transformer.setTranslation(node_svg_element.xy)
            node_svg_element.svg.set_transform(transformer.getTransform())
            svg_group.addElement(node_svg_element.svg)

            # curent_x to be repositioned for next node
            current_x = current_x + node_svg_element.width + self.theme['channel-inner-rect']['dx-between-elements']

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

        # wrap it in a svg element
        self.svg_element = SvgElement(svg=svg_group, width=outer_rect_width, height=outer_rect_height)

        # store the svg and dimensions for future reference
        self.channel_object.element = self.svg_element

    def to_svg(self):
        self.collect_elements()
        self.assemble_elements()

        return self.svg_element


''' ----------------------------------------------------------------------------------------------------------------------------------
    collection of nodes
'''
class ChannelObject:
    def __init__(self, name, number, is_root, parent_channel, nodes):
        self.name = name
        self.number = number
        self.is_root = is_root
        self.parent_channel = parent_channel
        self.nodes = nodes

        self.instance = None
        self.element = None


    '''
        the string representation of the Channel
    '''
    def __repr__(self):
        s = 'number: {0}, root: {1}, name: {2}, parent: [{3}], nodes: {4}'.format(self.number, self.is_root, self.name, self.parent_channel, [*self.nodes])
        return s


    '''
        height of the node which has the maximum height among all nodes in the channel
    '''
    def max_node_height(self):
        max_height = 0
        for _, node_object in self.nodes.items():
            max_height = max(node_object.element.height, max_height)

        return max_height

    '''
        given a node od, returns the x position of the node in the channel
    '''
    def x_of_node(self, node_id):
        if node_id in self.nodes:
            return self.nodes[node_id].element.xy.x

        # we could not locate the node in the named channel
        return 0


    '''
        given a node, returns the ordinal position of the node in the channel
    '''
    def node_ordinal(self, node):
        ordinal = 0
        for node_id in [*self.nodes]:
            if node_id == node.id:
                return ordinal
            else:
                ordinal = ordinal + 1

        return -1


    '''
        (path from the snap point to the exact point of the node) or (path to the snap point from the exact point of the node) in channel coordinates
    '''
    def to_snap_point(self, node, side, position, role, approach_snap_point_from, peer, edge_type):
        points_in_node_coordinate = node.instance.to_snap_point(side, position, role, approach_snap_point_from, peer, edge_type)
        points_in_channel_coordinate = [node.element.xy + p for p in points_in_node_coordinate]
        return points_in_channel_coordinate


    '''
        the path connects node to the boundary of the channel in channel coordinate.
        the path may cross inner node-boundary depending on the value of boundary (if not None), but does not cross the channel boundary
        boundary - [north|south|east|west]
    '''
    def inside_the_channel(self, boundary, node, side, position, role, approach_snap_point_from, peer, edge_type):
        forbidden_combinations = [('north', 'south'), ('south', 'north'), ('east', 'west'), ('west', 'east')]

        points_in_node_coordinate = node.instance.to_snap_point(side, position, role, approach_snap_point_from, peer, edge_type)
        points_in_channel_coordinate = [node.element.xy + p for p in points_in_node_coordinate]

        # if boundary is None, we return this
        if boundary is None:
            return points_in_channel_coordinate

        if (boundary, side) in forbidden_combinations:
            warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed'.format(side, node.id, edgeover, boundary))
            return points_in_channel_coordinate

        if role == 'to':
            point_to_extend = points_in_channel_coordinate[0]
        else:
            point_to_extend = points_in_channel_coordinate[-1]

        if boundary == 'south':
            the_point = Point(point_to_extend.x, self.element.height - self.theme['channel-outer-rect']['pad-spec']['bottom']/2)

        elif boundary == 'north':
            the_point = Point(point_to_extend.x, self.theme['channel-outer-rect']['pad-spec']['top']/2)

        elif boundary == 'east':
            # allow only for east-most node
            if self.node_ordinal(node) == len(self.nodes) - 1:
                the_point = Point(self.element.width - self.theme['channel-outer-rect']['pad-spec']['right']/2, point_to_extend.y)
            else:
                warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed as it is not the {3}-most node'.format(side, node.id, edgeover, boundary))
                return points_in_channel_coordinate

        elif boundary == 'west':
            # allow only for west-most node
            if self.node_ordinal(node) == 0:
                the_point = Point(self.theme['channel-outer-rect']['pad-spec']['left']/2, point_to_extend.y)
            else:
                warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed as it is not the {3}-most node'.format(side, node.id, edgeover, boundary))
                return points_in_channel_coordinate

        if role == 'to':
            return [the_point] + points_in_channel_coordinate
        else:
            return points_in_channel_coordinate + [the_point]


    '''
        the path connects node to the boundary point outside the channel in channel coordinate.
        the path is for getting outside of the channel from a node or getting into a node from outside the channel
        boundary is the side through which the path should get out of the channel or get into the channel [north|south|east|west]
    '''
    def outside_the_channel(self, boundary, node, side, position, role, approach_snap_point_from, peer, edge_type, margin_spec):
        forbidden_combinations = [('north', 'south'), ('south', 'north'), ('east', 'west'), ('west', 'east')]

        points_in_node_coordinate = node.instance.to_snap_point(side, position, role, approach_snap_point_from, peer, edge_type)
        points_in_channel_coordinate = [node.element.xy + p for p in points_in_node_coordinate]

        # if boundary is None, we return this
        if boundary is None:
            return points_in_channel_coordinate

        if (boundary, side) in forbidden_combinations:
            warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed'.format(side, node.id, edgeover, boundary))
            return points_in_channel_coordinate

        if role == 'to':
            point_to_extend = points_in_channel_coordinate[0]
        else:
            point_to_extend = points_in_channel_coordinate[-1]

        if boundary == 'south':
            the_point = Point(point_to_extend.x, self.element.height + margin_spec['bottom'])

        elif boundary == 'north':
            the_point = Point(point_to_extend.x, -margin_spec['top'])

        elif boundary == 'east':
            # allow only for east-most node
            if self.node_ordinal(node) == len(self.nodes) - 1:
                the_point = Point(self.element.width + margin_spec['right'], point_to_extend.y)
            else:
                warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed as it is not the {3}-most node'.format(side, node.id, edgeover, boundary))
                return points_in_channel_coordinate

        elif boundary == 'west':
            # allow only for west-most node
            if self.node_ordinal(node) == 0:
                the_point = Point(-margin_spec['left'], point_to_extend.y)
            else:
                warn('path from [{0}] of the node [{1}] to [{2}] of [{3}] boundary is not allowed as it is not the {3}-most node'.format(side, node.id, edgeover, boundary))
                return points_in_channel_coordinate

        if role == 'to':
            return [the_point] + points_in_channel_coordinate
        else:
            return points_in_channel_coordinate + [the_point]


    '''
        given a vertical line segment, finds out whether any portion of the channel falls on the line segment
    '''
    def is_vertically_between(self, x, north_y, south_y, padding):
        result = False

        # we make sure we consider that the channel area includes edge routing area outside the outer-rect of the channel
        # west-most point of channel is
        channel_west_x = self.westmost_x() - 0
        channel_east_x = self.element.xy.x + self.element.width + 0

        if channel_west_x < x < channel_east_x:
            # the vertical line between Point(x, north_y) and Point(x, south_y) will fall inside the channel, unless it is vertically not between  Point(x, north_y) and Point(x, south_y)
            channel_north_y = self.element.xy.y - 0
            channel_south_y = self.element.xy.y + self.element.height + 0
            if (north_y < channel_north_y < south_y) or (north_y < channel_south_y < south_y):
                # channel falls in the path, testing with both north_y or south_y is required to eliminate the channels in between partially
                # debug('channel [{0}:{1}] N=[{2}] S=[{3}] W=[{4}] E=[{5}] is vertically between x: {6} and y: [{6} {8}]'.format(self.number, self.name, channel_north_y, channel_south_y, channel_west_x, channel_east_x, x, north_y, south_y))
                result = True

        return result


    '''
        given a horizontal line segment, finds out whether any portion of the channel falls on the line segment
    '''
    def is_horizontally_between(self, y, west_x, east_x, padding):
        result = False

        # we make sure we consider that the channel area includes edge routing area outside the outer-rect of the channel
        channel_west_x = self.westmost_x() - 0
        channel_east_x = self.element.xy.x + self.element.width + 0
        if (west_x < channel_east_x < east_x) or (west_x < channel_east_x < east_x):
            # the channel is horizontally between the west_x and east_x, now we need to make sure the point y is within the channel
            channel_north_y = self.element.xy.y - 0
            channel_south_y = self.element.xy.y + self.element.height + 0
            if channel_north_y < y < channel_south_y:
                # debug('channel [{0}:{1}] N=[{2}] S=[{3}] W=[{4}] E=[{5}] is horizontally between y: {6} and x: [{7} {8}]'.format(self.number, self.name, channel_north_y, channel_south_y, channel_west_x, channel_east_x, y, west_x, east_x))
                result = True

        return result

    '''
        we want a path to bypass the channel through the routing area
    '''
    def bypass_vertically(self, coming_from, going_to, margin_spec):
        # the coming_from point is north of going_to, so we have to reach a point south of the channel either through east or west or directly dpending on which direction we are going_to
        if coming_from.north_of(going_to):
            # if the coming_from point is already below the channel, we have no point
            # warn('I {0} am going to south to {1} bypassing channel {2}'.format(coming_from, going_to, self.name))
            if coming_from.y >= self.element.xy.y + self.element.height + margin_spec['bottom']:
                # warn('I {0} am going to {1} and I am already below the channel {2}'.format(coming_from, going_to, self.name))
                return []

            # if the coming_from point's x position is outside the channel, we can directly go south
            elif (self.element.xy.x - margin_spec['left']) >= coming_from.x or coming_from.x >= (self.element.xy.x + self.element.width + margin_spec['right']):
                # warn('I {0} am going to south to {1} going straight through {2}'.format(coming_from, going_to, self.name))
                return [Point(coming_from.x, self.element.xy.y + self.element.height + margin_spec['bottom'])]

            # if the coming_from point is properly above the channel, we make a path
            else:
                # to the channel north vertically below coming_from
                p1 = Point(coming_from.x, self.element.xy.y - margin_spec['top'])
                if going_to.east_of(coming_from):
                    # warn('I {0} am going to south to {1} bypassing channel {2} from east'.format(coming_from, going_to, self.name))
                    # to the channel north-east
                    p2 = Point(self.element.xy.x + self.element.width + margin_spec['right'], p1.y)
                    # debug('southward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))
                else:
                    # warn('I {0} am going to south to {1} bypassing channel {2} from west'.format(coming_from, going_to, self.name))
                    # to the channel north-west
                    p2 = Point(self.element.xy.x - margin_spec['left'], p1.y)
                    # debug('northward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))

                # to the channel south vertically below p2
                p3 = Point(p2.x, self.element.xy.y + self.element.height + margin_spec['bottom'])

        # the coming_from point is south of going_to, so we have to reach a point north of the channel either through east or west dpending on which direction we are going_to
        else:
            # if the coming_from point is already above the channel, we have no point
            # warn('I {0} am going to north to {1} bypassing channel {2}'.format(coming_from, going_to, self.name))
            if coming_from.y <= self.element.xy.y - margin_spec['top']:
                return []

            # if the coming_from point's x position is outside the channel, we can directly go north
            elif (self.element.xy.x - margin_spec['left']) >= coming_from.x or coming_from.x >= (self.element.xy.x + self.element.width + margin_spec['right']):
                return [Point(coming_from.x, self.element.xy.y - margin_spec['top'])]

            # if the coming_from point is properly below the channel, we make a path
            else:
                # to the channel south vertically above coming_from
                p1 = Point(coming_from.x, self.element.xy.y + self.element.height + margin_spec['bottom'])
                if going_to.east_of(coming_from):
                    # to the channel south-east
                    p2 = Point(self.element.xy.x + self.element.width + margin_spec['right'], p1.y)
                    # debug('southward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))
                else:
                    # to the channel south-west
                    p2 = Point(self.element.xy.x - margin_spec['left'] , p1.y)
                    # debug('northward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))

                # to the channel north vertically above p2
                p3 = Point(p2.x, self.element.xy.y - margin_spec['top'])

        return [p1, p2, p3]

    '''
        a channel's westmost x position may not always be the xy.x of the channel - when the westmost node has a move_x displacement, the westmost point will also be displaced
        returns position in pool coordinate
    '''
    def westmost_x(self):
        # get the first node
        first_node = self.nodes[[*self.nodes][0]]
        return self.element.xy.x + first_node.element.xy.x - self.theme['channel-outer-rect']['pad-spec']['left']

    def east_of(self, channel):
        if self.element.xy.x + self.element.width >= channel.element.xy.x + channel.element.width:
            return True
        else:
            return False


    def west_of(self, channel):
        if self.element.xy.x <= channel.element.xy.x:
            return True
        else:
            return False


    def north_of(self, channel):
        if self.element.xy.y <= channel.element.xy.y:
            return True
        else:
            return False


    def south_of(self, channel):
        if self.element.xy.y + self.element.height >= channel.element.xy.y + channel.element.height:
            return True
        else:
            return False
