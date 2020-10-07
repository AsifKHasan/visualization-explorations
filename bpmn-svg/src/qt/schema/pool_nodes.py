#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

from qt.schema.node_editor import NodeEditor

class PoolNodes(CollapsibleFrame):

    bpmn_id_changed = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, lane_id, pool_id, parent=None):
        super().__init__(icon='nodes', text='Pool Nodes', parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040";')

        self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id = bpmn_data, bpmn_id, lane_id, pool_id
        self.pool_nodes = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes']

        self.signals_and_slots()
        self.populate()

    def populate(self):
        # first clear the layout with all nodes
        self.clearContent()

        for node_id, node_data in self.pool_nodes.items():
            node_widget = NodeEditor(self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id, node_id, self)
            node_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(node_widget)
            node_widget.node_id_changed.connect(self.on_node_id_changed)
            self.bpmn_id_changed.connect(node_widget.update_bpmn_id)

    def signals_and_slots(self):
        pass

    def on_node_id_changed(self, old_node_id, new_node_id):
        old_keys = list(self.pool_nodes.keys())
        new_keys = [new_node_id if k == old_node_id else k for k in old_keys]

        self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes'] = dict(zip(new_keys, self.pool_nodes.values()))
        self.pool_nodes = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes']

        # populate the nodes
        self.populate()

    def update_bpmn_id(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
        # print(type(self).__name__, self.lane_id, self.pool_id, 'bpmn_id_changed')
        self.bpmn_id_changed.emit(old_bpmn_id, new_bpmn_id)

    def update_lane_id(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id
            self.pool_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]

            print(type(self).__name__, self.lane_id, 'lane_id_changed')
