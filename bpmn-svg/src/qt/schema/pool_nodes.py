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
    def __init__(self, bpmn_data, bpmn_id, lane_id, pool_id, pool_nodes, parent=None):
        super().__init__(icon='nodes', text='Pool Nodes', parent=parent)
        self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id, self.pool_nodes = bpmn_data, bpmn_id, lane_id, pool_id, pool_nodes
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040";')
        self.populate()

    def populate(self):
        # debug('PoolNodes: {0}'.format(self.pool_id))

        for node_id, node_data in self.pool_nodes.items():
            node_widget = NodeEditor(self.bpmn_id, self.lane_id, self.pool_id, node_id, node_data)
            node_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(node_widget)
