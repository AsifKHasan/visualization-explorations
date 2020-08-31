#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

from qt.schema.edge_editor import EdgeEditor

class PoolEdges(CollapsibleBox):
    def __init__(self, bpmn_id, lane_id, pool_id, edges, parent=None):
        super().__init__(text='Pool Edges', parent=parent)
        self.bpmn_id, self.lane_id, self.pool_id, self.edges = bpmn_id, lane_id, pool_id, edges

        self.content_area.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')

        self.populate()

    def populate(self):
        debug('PoolEdges: {0}'.format(self.pool_id))
        self.content_layout = QVBoxLayout()

        for edge in self.edges:
            edge_widget = EdgeEditor(self.bpmn_id, self.lane_id, self.pool_id, edge)
            self.content_layout.addWidget(edge_widget)

        self.content_layout.addStretch()
        self.setContentLayout(self.content_layout)
