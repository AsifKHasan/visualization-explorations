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

class PoolEditor(CollapsibleBox):
    def __init__(self, bpmn_id, lane_id, pool_id, pool_data, parent=None):
        super().__init__(text='POOL id: {0}'.format(pool_id), parent=parent)
        self.bpmn_id, self.lane_id, self.pool_id, self.pool_data = bpmn_id, lane_id, pool_id, pool_data

        self.content_area.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')

        self.populate()

    def populate(self):
        debug('PoolEditor: {0}'.format(self.pool_id))
        self.content_layout = QVBoxLayout()

        # Pool id, title and styles at the top
        self.pool_header_ui = PoolHeader(self.bpmn_id, self.lane_id, self.pool_id, self.pool_data)
        self.content_layout.addWidget(self.pool_header_ui)

        # Node container in the middle
        self.pool_nodes_ui = PoolNodes(self.bpmn_id, self.lane_id, self.pool_id, self.pool_data.get('nodes', None))
        self.content_layout.addWidget(self.pool_nodes_ui)

        # Edge container after the node container
        self.pool_edges_ui = PoolEdges(self.bpmn_id, self.lane_id, self.pool_id, self.pool_data.get('edges', None))
        self.content_layout.addWidget(self.pool_edges_ui)

        self.setContentLayout(self.content_layout)
