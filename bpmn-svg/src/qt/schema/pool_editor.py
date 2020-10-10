#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

from qt.schema.pool_header import PoolHeader
from qt.schema.pool_nodes import PoolNodes
from qt.schema.pool_edges import PoolEdges

class PoolEditor(CollapsibleFrame):

    pool_id_change_requested = pyqtSignal(str, str)
    node_id_change_requested = pyqtSignal(str, str)

    bpmn_id_change_done = pyqtSignal(str, str)
    lane_id_change_done = pyqtSignal(str, str)
    pool_id_change_done = pyqtSignal(str, str)
    node_id_change_done = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, lane_id, pool_id, parent=None):
        super().__init__(icon='pool', text='POOL id: {0}'.format(pool_id), parent=parent)
        self.set_styles(title_style='background-color: "#C8C8C8"; color: "#404040";', content_style='background-color: "#D0D0D0"; color: "#404040";')

        self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id = bpmn_data, bpmn_id, lane_id, pool_id
        self.pool_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]

        self.populate()
        self.signals_and_slots()

    def populate(self):
        # Pool id, title and styles at the top
        self.pool_header_ui = PoolHeader(self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id)
        self.addWidget(self.pool_header_ui)

        # Node container in the middle
        self.pool_nodes_ui = PoolNodes(self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id)
        self.addWidget(self.pool_nodes_ui)

        # Edge container after the node container
        self.pool_edges_ui = PoolEdges(self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id)
        self.addWidget(self.pool_edges_ui)

    def signals_and_slots(self):
        self.pool_header_ui.pool_id_change_requested.connect(self.on_pool_id_change_requested)
        self.pool_nodes_ui.node_id_change_requested.connect(self.on_node_id_change_requested)

        self.bpmn_id_change_done.connect(self.pool_header_ui.on_bpmn_id_change_done)
        self.bpmn_id_change_done.connect(self.pool_nodes_ui.on_bpmn_id_change_done)
        self.bpmn_id_change_done.connect(self.pool_edges_ui.on_bpmn_id_change_done)

        self.lane_id_change_done.connect(self.pool_header_ui.on_lane_id_change_done)
        self.lane_id_change_done.connect(self.pool_nodes_ui.on_lane_id_change_done)
        self.lane_id_change_done.connect(self.pool_edges_ui.on_lane_id_change_done)

        self.pool_id_change_done.connect(self.pool_header_ui.on_pool_id_change_done)
        self.pool_id_change_done.connect(self.pool_nodes_ui.on_pool_id_change_done)
        self.pool_id_change_done.connect(self.pool_edges_ui.on_pool_id_change_done)

        self.node_id_change_done.connect(self.pool_nodes_ui.on_node_id_change_done)
        self.node_id_change_done.connect(self.pool_edges_ui.on_node_id_change_done)

    def on_pool_id_change_requested(self, old_pool_id, new_pool_id):
        print('.' * 16, type(self).__name__, 'pool_id_change_requested', old_pool_id, '-->', new_pool_id)
        self.pool_id_change_requested.emit(old_pool_id, new_pool_id)

    def on_node_id_change_requested(self, old_node_id, new_node_id):
        print('.' * 16, type(self).__name__, 'node_id_change_requested', old_node_id, '-->', new_node_id)
        self.node_id_change_requested.emit(old_node_id, new_node_id)

    def on_bpmn_id_change_done(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
        # print(type(self).__name__, self.lane_id, self.pool_id, 'bpmn_id_change_done')
        self.bpmn_id_change_done.emit(old_bpmn_id, new_bpmn_id)

    def on_lane_id_change_done(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id
            self.pool_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]

            print('.' * 16, type(self).__name__, 'lane_id_change_done', old_lane_id, '-->', new_lane_id)
            self.lane_id_change_done.emit(old_lane_id, new_lane_id)

    def on_pool_id_change_done(self, old_pool_id, new_pool_id):
        if self.pool_id == old_pool_id:
            self.pool_id = new_pool_id
            self.pool_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]

            print('.' * 16, type(self).__name__, 'pool_id_change_done', old_pool_id, '-->', new_pool_id)
            self.pool_id_change_done.emit(old_pool_id, new_pool_id)

    def on_node_id_change_done(self, old_node_id, new_node_id):
        print('.' * 16, type(self).__name__, 'node_id_change_done', old_node_id, '-->', new_node_id)
        self.node_id_change_done.emit(old_node_id, new_node_id)
