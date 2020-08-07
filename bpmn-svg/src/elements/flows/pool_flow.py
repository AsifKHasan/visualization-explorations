#!/usr/bin/env python3
'''
TODO: Udemy
https://www.udemy.com/course/mega-course-vmware-vsphere-67-bootcamp-100-hands-on-labs/
'''
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

from elements.svg_element import SvgElement
from elements.flows.flow_object import FlowObject

'''
    Class to handle a flows/edges between channels of a pool where from-node is in one channel and to-node is in another channel within the same ChabnnelCollection  (pool).

    Criteria - from-node and to-node must be in same ChannelCollection, but not in same Channel. The possible scenarios are

    #1  *from-node* channel is just above the *to-node* channel and *to-node* is the first node of its Channel
        a) from-node's snap-position is on
            1   EAST-TOP for Activity
            2   EAST-MIDDLE for Gateway/Event/Data
        b) to-node's snap-position is on
            1   WEST-TOP for Activity
            2   NORTH-MIDDLE for Gateway/Event/Data (swicth label to bottom if necessary)

    #2  *from-node* channel is just above the *to-node* channel and *to-node* is not the first node of its Channel
        a) from-node's snap-position is on
            1   EAST-TOP for Activity
            2   EAST-MIDDLE for Gateway/Event/Data
        b) to-node's snap-position is on
            1   WEST-TOP for Activity
            2   NORTH-MIDDLE for Gateway/Event/Data (swicth label to bottom if necessary)

    #2  *from-node* channel is two or more Channels above the *to-node* channel (there are channels in between) and *to-node* IS the first node of its Channel

    #3  *from-node* channel is two or more Channels above the *to-node* channel (there are channels in between) and *to-node* IS NOT the first node of its Channel

'''
class PoolFlow(FlowObject):

    def __init__(self, edge_type, channel_collection):
        super().__init__(edge_type)
        self.channel_collection = channel_collection

    def create_flow(self, from_node, to_node, label):
        # decide which edge rule we should apply
