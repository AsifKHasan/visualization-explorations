#!/usr/bin/env python3
'''
'''
from util.logger import *

'''
    in a pool nodes need to be processed (ordered and grouped)
    1. nodes that are connected with other nodes (in the same pool) should be ordered in a group so that they are in the same channel (a channel is vertical lines for node flow, a lane may have multiple channels if the edges are branched like a tree) and flow from left to right based or edge order (head node at left, tail node at right)
    2. isolated nodes (nodes that do not connect to any other nodes) should be put in a separate group (in which channel they should go is a TODO)
    3. If any node connects to two or more nodes (in the same pool) a new group starts for each branch so that they can be placed into different channels
'''
def order_and_group_nodes(bpmn_id, lane_id, pool_id, nodes, edges):
