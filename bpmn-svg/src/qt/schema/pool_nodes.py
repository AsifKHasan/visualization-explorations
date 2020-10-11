#!/usr/bin/env python3
'''
'''
import copy

from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

from qt.schema.node_editor import NodeEditor

class PoolNodes(CollapsibleFrame):

    node_id_change_requested = pyqtSignal(str, str)

    bpmn_id_change_done = pyqtSignal(str, str)
    node_id_change_done = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, lane_id, pool_id, parent=None):
        super().__init__(icon='nodes', text='Pool Nodes', parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040";')

        self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id = bpmn_data, bpmn_id, lane_id, pool_id
        self.pool_nodes = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes']

        self.init_ui()
        self.signals_and_slots()
        self.populate()

    def init_ui(self):
        self.warning_widget = None

        # *add* button to add a new node
        self.add_new_node = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['new-node'])
        self.add_new_node.setIcon(QIcon(pixmap))

        self.add_new_node.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.add_new_node.setStyleSheet('font-size: 9px; border: 0px; background-color: #B0B0B0')

        self.add_button(self.add_new_node, 'new-pool-node')

    def populate(self, focus_on_node=None, nodes_to_expand=[]):
        # first clear the layout with all nodes
        self.clearContent()

        self.num_nodes = len(self.pool_nodes)
        index = 0
        for node_id, node_data in self.pool_nodes.items():
            node_widget = NodeEditor(self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id, node_id, index, self.num_nodes, self)
            node_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(node_widget)

            node_widget.new_node.connect(self.on_new_node)
            node_widget.remove_node.connect(self.on_remove_node)
            node_widget.node_order_changed.connect(self.on_node_order_changed)

            node_widget.node_id_change_requested.connect(self.on_node_id_change_requested)
            self.bpmn_id_change_done.connect(node_widget.on_bpmn_id_change_done)
            self.node_id_change_done.connect(node_widget.on_node_id_change_done)
            index = index + 1

            if node_id in nodes_to_expand:
                node_widget.expand()

            if focus_on_node and focus_on_node == node_id:
                node_widget.expand()


    def signals_and_slots(self):
        self.add_new_node.clicked.connect(self.on_new_node)

    def on_node_id_change_requested(self, old_node_id, new_node_id):
        print('.' * 20, type(self).__name__, 'node_id_change_requested', old_node_id, '-->', new_node_id)
        self.node_id_change_requested.emit(old_node_id, new_node_id)

    def on_bpmn_id_change_done(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
        # print(type(self).__name__, self.lane_id, self.pool_id, 'bpmn_id_change_done')
        self.bpmn_id_change_done.emit(old_bpmn_id, new_bpmn_id)

    def on_lane_id_change_done(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id
            self.pool_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]

            print('.' * 20, type(self).__name__, 'lane_id_change_done', old_lane_id, '-->', new_lane_id)

    def on_pool_id_change_done(self, old_pool_id, new_pool_id):
        if self.pool_id == old_pool_id:
            self.pool_id = new_pool_id
            self.pool_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]

            print('.' * 20, type(self).__name__, 'pool_id_change_done', old_pool_id, '-->', new_pool_id)

    def on_node_id_change_done(self, old_node_id, new_node_id):
        old_keys = list(self.pool_nodes.keys())
        new_keys = [new_node_id if k == old_node_id else k for k in old_keys]

        self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes'] = dict(zip(new_keys, self.pool_nodes.values()))
        self.pool_nodes = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes']

        # populate the nodes
        self.populate(focus_on_node=new_node_id)

    def on_new_node(self, index=0):
        old_keys = list(self.pool_nodes.keys())

        new_node_object = copy.deepcopy(NEW_NODE)
        # TODO: generate a unique node key
        new_node_key = 'new_node'
        # new_keys = old_keys[0:index-1] + new_node_key + old_keys[index:]

        if index != 0:
            new_dict1 = dict(zip(old_keys[0:index], list(self.pool_nodes.values())[0:index]))
        else:
            new_dict1 = {}

        new_dict1[new_node_key] = new_node_object
        new_dict2 = dict(zip(old_keys[index:], list(self.pool_nodes.values())[index:]))

        # print(index)
        # print(new_dict1.keys())
        # print(new_dict2.keys())

        self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes'] = {**new_dict1, **new_dict2}
        self.pool_nodes = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes']

        # now populate again
        self.populate(focus_on_node=new_node_key)

    def on_remove_node(self, index):
        nodes_to_expand = self.nodes_expanded()

        # remove the node from bpmn_data
        key_to_remove = list(self.pool_nodes.keys())[index]
        self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes'].pop(key_to_remove)
        self.pool_nodes = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes']

        # now populate again
        self.populate(nodes_to_expand=nodes_to_expand)

    def on_node_order_changed(self, index, direction):
        if self.num_nodes <= 1:
            return

        if index == 0 and direction == 'up':
            return

        if index == self.num_nodes - 1 and direction == 'down':
            return

        nodes_to_expand = self.nodes_expanded()

        # swap nodes
        keys = list(self.pool_nodes.keys())
        vals = list(self.pool_nodes.values())
        if direction == 'up':
            keys[index], keys[index - 1] = keys[index - 1], keys[index]
            vals[index], vals[index - 1] = vals[index - 1], vals[index]
        elif direction == 'down':
            keys[index], keys[index + 1] = keys[index + 1], keys[index]
            vals[index], vals[index + 1] = vals[index + 1], vals[index]

        self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes'] = dict(zip(keys, vals))
        self.pool_nodes = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes']

        self.populate(nodes_to_expand=nodes_to_expand)

    def nodes_expanded(self):
        return []
