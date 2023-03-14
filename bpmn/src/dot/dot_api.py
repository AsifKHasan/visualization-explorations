#!/usr/bin/env python3

import importlib

from dot.dot_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Dot objects wrappers
#   ----------------------------------------------------------------------------------------------------------------

NODE_PROPS = {}
EDGE_PROPS = {}

NODE_DICT = {}


''' parse node properties
'''
def parse_node_props(node_props):
    for k, v in node_props.items():
        prop_dict = props_to_dict(text=v)
        NODE_PROPS[k] = prop_dict


''' parse edge properties
'''
def parse_edge_props(edge_props):
    for k, v in edge_props.items():
        prop_dict = props_to_dict(text=v)
        EDGE_PROPS[k] = prop_dict


''' if the nodes are in different subgraphs
'''
def subgraph_differs(from_node, to_node):
    from_node_object = NODE_DICT[from_node]
    to_node_object = NODE_DICT[to_node]

    if not from_node_object:
        warn(f"node {from_node} missing")
        return True
    
    if not to_node_object:
        warn(f"node {to_node} missing")
        return True
    
    # check pool differs or not
    if from_node_object._parent_pool is None:
        # from node is in the root graph
        if to_node_object._parent_pool is None:
            # to node is in the root graph
            return False
        
        else:
            # to node is not in the root graph
            return True
        
    else:
        # from node is not in the root graph
        if to_node_object._parent_pool is None:
            # to node is in the root graph
            return True
        
        else:
            # to node is not in the root grap
            if from_node_object._parent_pool == to_node_object._parent_pool:

                # pool is same, check lane differs or not
                if from_node_object._parent_lane is None:
                    # from node is in a pool
                    if to_node_object._parent_lane is None:
                        # to node is in the pool
                        return False
                    
                    else:
                        # to node is not in a pool
                        return True
                    
                else:
                    # from node is in a lane
                    if to_node_object._parent_lane is None:
                        # to node is in the pool
                        return True
                    
                    else:
                        # to node is in a lane
                        if from_node_object._parent_lane == to_node_object._parent_lane:
                            # lane is same
                            return False
                        
                        else:
                            # lane is different
                            return True
                
            
            else:
                # pool is different
                return True

    return False


''' Dot base object
'''
class DotObject(object):
    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config
        self._data = data
        self._lines = []
        self._hide_label = self._data.get('hide-label', False)
        self._class = None
        self._label = None


    ''' append single line or list of lines to _lines
    '''
    def append_content(self, content):
        if content is None:
            return

        if isinstance(content, str):
            self._lines.append(content)

        elif isinstance(content, list):
            self._lines = self._lines + content


    ''' process nodes
    '''
    def process_nodes(self, parent_pool=None, parent_lane=None):
        if 'elements' in self._data and self._data['elements']:
            self.append_content(content='')
            self.append_content(content=f"# {self._class} nodes")
            for node in self._data['elements']:
                for k, v in node.items():
                    node_object = NodeObject(config=self._config, data={'type': k, 'value': v}, parent_pool=parent_pool, parent_lane=parent_lane)
                    node_object.parse_node()

                    if not node_object._id in NODE_DICT:
                        debug(f"adding node [{node_object._id}] {node_object._label}")
                        NODE_DICT[node_object._id] = node_object
                        self.append_content(content=node_object.to_dot())
                    else:
                        warn(f"node {node_object._label} is duplicated")


    ''' process edges
    '''
    def process_edges(self):
        if 'edges' in self._data and self._data['edges']:
            self.append_content(content='')
            self.append_content(content=f"# {self._class} edges")
            for edge in self._data['edges']:
                for k, v in edge.items():
                    edge_object = EdgeObject(config=self._config, data={'type': k, 'value': v})
                    self.append_content(content=edge_object.to_dot())


    ''' process label
    '''
    def process_label(self):
        if not self._hide_label:
            self.append_content(content=make_a_property(prop_key='label', prop_value=wrap_text(text=self._label)) + ';')



''' Dot pool object
'''
class PoolObject(DotObject):

    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config, data)

        self._class = 'pool'
        self._theme = self._config['theme']['theme-data'][self._class]

        self._label = self._data.get('pool')
        self._id = f"cluster_{text_to_identifier(text=self._label)}"


    ''' generates the dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # label
        self.process_label()

        # graph properties
        self.append_content(content=f"graph [ {make_property_list(self._theme['graph'])}; ]")

        # elements
        self.process_nodes(parent_pool=self._id)

        # lanes
        if 'lanes' in self._data and self._data['lanes']:
            self.append_content(content='')
            self.append_content(content=f"# lane collection")
            for lane in self._data['lanes']:
                lane_object = LaneObject(config=self._config, data=lane, parent_pool=self._id)
                self.append_content(content=lane_object.to_dot())
                self.append_content(content='')

        # edges
        self.process_edges()

        # wrap as a subgraph
        self._lines = indent_and_wrap(self._lines, wrap_keyword='subgraph ', object_name=self._id)

        return self._lines



''' Dot lane object
'''
class LaneObject(DotObject):

    ''' constructor
    '''
    def __init__(self, config, data, parent_pool):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config, data)

        self._class = 'lane'
        self._theme = self._config['theme']['theme-data'][self._class]

        self._label = self._data.get('lane')
        self._id = f"cluster_{text_to_identifier(text=self._label)}"

        self._parent_pool = parent_pool


    ''' generates the dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # label
        self.process_label()

        # graph properties
        self.append_content(content=f"graph [ {make_property_list(self._theme['graph'])}; ]")

        # elements
        self.process_nodes(parent_pool=self._parent_pool, parent_lane=self._id)
                        

        # edges
        self.process_edges()

        # wrap as a subgraph
        self._lines = indent_and_wrap(self._lines, wrap_keyword='subgraph ', object_name=self._id)

        return self._lines



''' Dot graph object
'''
class GraphObject(DotObject):

    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config, data)

        self._class = 'graph'
        self._theme = self._config['theme']['theme-data'][self._class]

        self._label = self._data.get('bpmn')
        self._id = f"{self._class}_{text_to_identifier(text=self._label)}"




    ''' generates the dot code
    '''
    def to_dot(self):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")

        # parse node and edge properties
        parse_node_props(node_props=self._config['theme']['theme-data']['node']['shapes'])
        parse_edge_props(edge_props=self._config['theme']['theme-data']['edge']['shapes'])

        # label
        self.process_label()

        # graph attributes
        self.append_content(content=make_property_lines(self._theme['attributes']))
        self.append_content(content='')

        # node properties
        self.append_content(content=f"node [ {make_property_list(self._theme['node'])}; ]")

        # edge properties
        self.append_content(content=f"edge [ {make_property_list(self._theme['edge'])}; ]")

        # elements
        self.process_nodes()

        # pools
        if 'pools' in self._data and self._data['pools']:
            self.append_content(content='')
            self.append_content(content=f"# pool collection")
            for pool in self._data['pools']:
                pool_object = PoolObject(config=self._config, data=pool)
                self.append_content(content=pool_object.to_dot())
                self.append_content(content='')

        # edges
        self.process_edges()

        # wrap as a digraph
        self._lines = indent_and_wrap(self._lines, wrap_keyword='digraph ', object_name=self._id)

        return self._lines



''' Dot node object
'''
class NodeObject(DotObject):

    ''' constructor
    '''
    def __init__(self, config, data, parent_pool=None, parent_lane=None):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config, data)

        self._class = 'node'
        self._theme = self._config['theme']['theme-data'][self._class]

        self._type = self._data['type']
        self._value = self._data['value']

        self._prop_dict = {}

        self._wrap_at = self._theme.get('wrap-at', 10)

        self._parent_pool = parent_pool
        self._parent_lane = parent_lane


    ''' parse node
        Pay for the Pizza        [ width='1.5in'; ]
    '''
    def parse_node(self):
        # see if there are properties enclosed inside []
        node_str = self._value
        m = re.search(r"\[(.+)\]", self._value)
        if m:
            prop_str = m.group(1)
            self._prop_dict = props_to_dict(text=prop_str)

            node_str = self._value[:m.start(0)]

        # get the label and id
        self._label = node_str.strip()
        self._id = text_to_identifier(text=self._label)


    ''' generates the dot code
        hungry                              [ shape="circle"; label="Hungry"; ]
    '''
    def to_dot(self):
        # get the shape
        if self._type in NODE_PROPS:
            self._prop_dict = {**NODE_PROPS[self._type], **self._prop_dict}
            # if the property shape is circle, doublecircle or diamond, we need an xlabel
            if 'shape' in self._prop_dict and self._prop_dict['shape'] in ['circle', 'doublecircle', 'diamond']:
                xlabel = True
            else:
                xlabel = False

            self.append_content(content=make_a_node(id=self._id, label=wrap_text(text=self._label, width=self._wrap_at), prop_dict=self._prop_dict, xlabel=xlabel))

        else:
            warn(f"no shape defined for {self._class} type {self._type}")

        return self._lines



''' Dot edge object
'''
class EdgeObject(DotObject):

    ''' constructor
    '''
    def __init__(self, config, data):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config, data)

        self._class = 'edge'
        self._theme = self._config['theme']['theme-data'][self._class]

        self._type = self._data['type']
        self._value = self._data['value']

        self._from_node = None
        self._to_node = None
        self._prop_dict = {}


    ''' parse edge
        Order a Pizza        -> Order Received           [ label='pizza order'; ]
    '''
    def parse_edge(self):
        # see if there are properties enclosed inside []
        edge_str = self._value
        m = re.search(r"\[(.+)\]", self._value)
        if m:
            prop_str = m.group(1)
            # print(prop_str)
            self._prop_dict = props_to_dict(text=prop_str)

            if 'label' in self._prop_dict:
                self._prop_dict['xlabel'] = self._prop_dict.pop('label')

            edge_str = self._value[:m.start(0)]

        if not 'xlabel' in self._prop_dict:
            self._prop_dict['xlabel'] = ''

        # get the from and to nodes
        node_list = edge_str.split('->')
        self._from_node = text_to_identifier(text=node_list[0].strip())
        self._to_node = text_to_identifier(text=node_list[1].strip())

        if subgraph_differs(from_node=self._from_node, to_node=self._to_node):
            self._prop_dict['constraint'] = 'false'


    ''' generates the dot code
    '''
    def to_dot(self):
        # get the shape
        if self._type in EDGE_PROPS:
            self.parse_edge()
            self._prop_dict = {**EDGE_PROPS[self._type], **self._prop_dict}
            self.append_content(content=make_an_edge(from_node=self._from_node, to_node=self._to_node, prop_dict=self._prop_dict))

        else:
            warn(f"no properties defined for {self._class} type {self._type}")

        return self._lines
