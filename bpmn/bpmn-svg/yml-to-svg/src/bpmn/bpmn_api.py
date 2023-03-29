#!/usr/bin/env python3

import importlib

from bpmn.bpmn_util import *
from helper.util import *
from helper.exception import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   BPMN objects wrappers
#   ----------------------------------------------------------------------------------------------------------------


''' BPMN base object
'''
class BpmnObject(object):
    ''' constructor
    '''
    def __init__(self, config, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config
        self._theme = theme
        self._prepared_data = {}

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

        self._my_type = None
        self._id = None
        self._label = None
        self._hide_label = False


    ''' common processing
    '''
    def parse(self, source_data):
        if self._my_type in source_data:
            self._label = source_data.get(self._my_type, '')

        self._id = f"{self._my_type}__{text_to_identifier(self._label)}"
        self._hide_label = source_data.get('hide-label', False)


''' BPMN root object
'''
class BpmnRoot(BpmnObject):
    ''' constructor
    '''
    def __init__(self, config, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, theme=theme)
        self._my_type = 'bpmn'


    ''' prepare the output data
    '''
    def parse(self, source_data):
        # the 'bpmn' key is a must
        if self._my_type not in source_data:
            raise BpmnDataMissing('BPMN', self._my_type)

        # common processing
        super().parse(source_data=source_data)

        # process 'nodes'
        if 'nodes' in source_data and source_data['nodes']:
            for node in source_data['nodes']:
                # node_object = BpmnLane(config=self._config, theme=self._theme)
                # node_object.parse(source_data=node)
                # self._nodes.append(node_object)
                pass

        else:
            debug(f"no 'node' for [bpmn] : [{self._label}]")

        # process 'edges'
        if 'edges' in source_data and source_data['edges']:
            for edge in source_data['edges']:
                # edge_object = BpmnLane(config=self._config, theme=self._theme)
                # edge_object.parse(source_data=edge)
                # self._edges.append(edge_object)
                pass

        else:
            debug(f"no 'edge' for [bpmn] : [{self._label}]")


        # process 'pools'
        if 'pools' in source_data and source_data['pools']:
            for pool in source_data['pools']:
                pool_object = BpmnPool(config=self._config, theme=self._theme)
                pool_object.parse(source_data=pool)
                self._pools.append(pool_object)

        else:
            debug(f"no 'pool' for [bpmn] : [{self._label}]")



''' BPMN pool object
'''
class BpmnPool(BpmnObject):
    ''' constructor
    '''
    def __init__(self, config, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, theme=theme)
        self._my_type = 'pool'


    ''' prepare the output data
    '''
    def parse(self, source_data):
        # the 'pool' key is a must
        if self._my_type not in source_data:
            raise BpmnDataMissing('BPMN', self._my_type)

        # common processing
        super().parse(source_data=source_data)

        # process 'nodes'
        if 'nodes' in source_data and source_data['nodes']:
            for node in source_data['nodes']:
                # node_object = BpmnLane(config=self._config, theme=self._theme)
                # node_object.parse(source_data=node)
                # self._nodes.append(node_object)
                pass

        else:
            debug(f"no 'node' for [pool] : [{self._label}]")

        # process 'edges'
        if 'edges' in source_data and source_data['edges']:
            for edge in source_data['edges']:
                # edge_object = BpmnLane(config=self._config, theme=self._theme)
                # edge_object.parse(source_data=edge)
                # self._edges.append(edge_object)
                pass

        else:
            debug(f"no 'edge' for [pool] : [{self._label}]")


        # process 'lanes'
        if 'lanes' in source_data and source_data['lanes']:
            for lane in source_data['lanes']:
                lane_object = BpmnLane(config=self._config, theme=self._theme)
                lane_object.parse(source_data=lane)
                self._lanes.append(lane_object)

        else:
            debug(f"no 'lane' for [pool] : [{self._label}]")



''' BPMN lane object
'''
class BpmnLane(BpmnObject):
    ''' constructor
    '''
    def __init__(self, config, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, theme=theme)
        self._my_type = 'lane'


    ''' prepare the output data
    '''
    def parse(self, source_data):
        # the 'lane' key is a must
        if self._my_type not in source_data:
            raise BpmnDataMissing('BPMN', self._my_type)

        # common processing
        super().parse(source_data=source_data)

        # process 'nodes'
        if 'nodes' in source_data and source_data['nodes']:
            for node in source_data['nodes']:
                # node_object = BpmnLane(config=self._config, theme=self._theme)
                # node_object.parse(source_data=node)
                # self._nodes.append(node_object)
                pass

        else:
            debug(f"no 'node' for [lane] : [{self._label}]")

        # process 'edges'
        if 'edges' in source_data and source_data['edges']:
            for edge in source_data['edges']:
                # edge_object = BpmnLane(config=self._config, theme=self._theme)
                # edge_object.parse(source_data=edge)
                # self._edges.append(edge_object)
                pass

        else:
            debug(f"no 'edge' for [lane] : [{self._label}]")

