#!/usr/bin/env python3

import importlib
from pprint import pprint

from bpmn.bpmn_util import *
from helper.util import *
from helper.exception import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   BPMN objects wrappers
#   ----------------------------------------------------------------------------------------------------------------

ALL_NODES = {}


''' BPMN base object
'''
class BpmnObject(object):
    ''' constructor
    '''
    def __init__(self, my_type, location={}):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._prepared_data = {}

        self._location = location

        # BpmnObject may have nodes
        self._nodes = []

        # BpmnObject may have edges
        self._edges = []

        # BpmnObject may have pools
        self._pools = []

        # BpmnObject may have lanes
        self._lanes = []

        # BpmnObject may have bands
        self._bands = []

        self._my_type = my_type
        self._id = None
        self._label = None
        self._hide_label = False


    ''' common processing - labels, nodes, edges, bands
    '''
    def parse_common(self, source_data):
        if self._my_type in source_data:
            self._label = source_data.get(self._my_type, '')

        self._id = f"{self._my_type}__{text_to_identifier(self._label)}"
        self._hide_label = source_data.get('hide-label', False)
        # print(f"[{self._my_type}] : [{self._id}] : [{self._label}] : {self._location}")



    ''' parse nodes, edges, bands
    '''
    def parse_bands(self, source_data, location):
        global ALL_NODES

        # process 'nodes'
        if 'nodes' in source_data and source_data['nodes']:
            for node in source_data['nodes']:
                node_object = BpmnNode(location=location)
                node_object.parse(source_data=node)
                self._nodes.append(node_object)
                ALL_NODES[node_object._id] = node_object

        else:
            debug(f"no 'node' for [{self._my_type}] : [{self._label}]")

        # process 'edges'
        if 'edges' in source_data and source_data['edges']:
            for edge in source_data['edges']:
                edge_object = BpmnEdge(location=location)
                edge_object.parse(source_data=edge)
                self._edges.append(edge_object)

        else:
            debug(f"no 'edge' for [{self._my_type}] : [{self._label}]")

        # from edges create bands only if the tail and head nodes are in the same group
        node_list = [ node._label for node in self._nodes ]
        edge_list = [ (edge._tail_node, edge._head_node) for edge in self._edges if edge._tail_node in node_list and edge._head_node in node_list]
        band_list = edges_to_bands(edge_list=edge_list, node_list=node_list)
        # pprint(band_list)



''' BPMN root object
'''
class BpmnRoot(BpmnObject):
    ''' constructor
    '''
    def __init__(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(my_type='bpmn', location={})


    ''' prepare the output data
    '''
    def parse(self, source_data):
        global ALL_NODES
        # the 'bpmn' key is a must
        if self._my_type not in source_data:
            raise BpmnDataMissing('BPMN', self._my_type)

        # common processing
        super().parse_common(source_data=source_data)

        # nodes, edges, bands
        super().parse_bands(source_data=source_data, location={})

        # process 'pools'
        if 'pools' in source_data and source_data['pools']:
            for pool in source_data['pools']:
                pool_object = BpmnPool()
                pool_object.parse(source_data=pool)
                self._pools.append(pool_object)

        else:
            debug(f"no 'pool' for [bpmn] : [{self._label}]")



''' BPMN pool object
'''
class BpmnPool(BpmnObject):
    ''' constructor
    '''
    def __init__(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(my_type='pool')


    ''' prepare the output data
    '''
    def parse(self, source_data):
        # the 'pool' key is a must
        if self._my_type not in source_data:
            raise BpmnDataMissing('BPMN', self._my_type)

        # common processing
        super().parse_common(source_data=source_data)

        # location for children
        location = {'pool': self._id}

        # nodes, edges, bands
        super().parse_bands(source_data=source_data, location=location)

        # process 'lanes'
        if 'lanes' in source_data and source_data['lanes']:
            for lane in source_data['lanes']:
                lane_object = BpmnLane(location=location)
                lane_object.parse(source_data=lane)
                self._lanes.append(lane_object)

        else:
            debug(f"no 'lane' for [pool] : [{self._label}]")



''' BPMN lane object
'''
class BpmnLane(BpmnObject):
    ''' constructor
    '''
    def __init__(self, location):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(my_type='lane', location=location)


    ''' prepare the output data
    '''
    def parse(self, source_data):
        # the 'lane' key is a must
        if self._my_type not in source_data:
            raise BpmnDataMissing('BPMN', self._my_type)

        # common processing
        super().parse_common(source_data=source_data)

        # location for children
        location = {**self._location, **{'lane': self._id}}

        # nodes, edges, bands
        super().parse_bands(source_data=source_data, location=location)



''' BPMN band object
'''
class BpmnBand(BpmnObject):
    ''' constructor
    '''
    def __init__(self, parent_id, serial, location):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(my_type='band', location=location)

        self._id = f"{self._my_type}__{parent_id}__{serial}"
        self._hide_label = True



''' BPMN node object
'''
class BpmnNode(object):
    ''' constructor
    '''
    def __init__(self, location):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._location = location


    ''' prepare the output data
    '''
    def parse(self, source_data):
        k, v = list(source_data.items())[0]
        self._ntype = k

        # value is a label + optional properties enclosed in []
        self._label, self._props = parse_node_from_text(text=v)
        self._id = f"node__{self._ntype}__{text_to_identifier(self._label)}"
        # print(f"[node] : [{self._ntype}] : [{self._id}] : [{self._label}] : {self._location}")


''' BPMN edge object
'''
class BpmnEdge(object):
    ''' constructor
    '''
    def __init__(self, location):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._location = location


    ''' prepare the output data
    '''
    def parse(self, source_data):
        k, v = list(source_data.items())[0]
        self._etype = k

        # value is a node -> node + optional properties enclosed in []
        self._tail_node, self._head_node, self._props = parse_edge_from_text(text=v)
        self._id = f"edge__{self._etype}__{text_to_identifier(self._tail_node)}__{text_to_identifier(self._head_node)}"
        # print(f"[edge] : [{self._etype}] : [{self._tail_node}] -> [{self._head_node}] : {self._location}")
