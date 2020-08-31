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

class PoolNodes(CollapsibleBox):
    def __init__(self, bpmn_id, lane_id, pool_id, pool_nodes, parent=None):
        super().__init__(text='Pool Nodes', parent=parent)
        self.bpmn_id, self.lane_id, self.pool_id, self.pool_nodes = bpmn_id, lane_id, pool_id, pool_nodes

        self.content_area.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')

        self.populate()

    def populate(self):
        debug('PoolNodes: {0}'.format(self.pool_id))
        self.content_layout = QVBoxLayout()

        for node_id, node_data in self.pool_nodes.items():
            node_widget = NodeEditor(self.bpmn_id, self.lane_id, self.pool_id, node_id, node_data)
            self.content_layout.addWidget(node_widget)

        self.content_layout.addStretch()
        self.setContentLayout(self.content_layout)
