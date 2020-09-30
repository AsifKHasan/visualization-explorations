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

    bpmn_id_changed = pyqtSignal(str)

    def __init__(self, bpmn_data, bpmn_id, lane_id, pool_id, parent=None):
        super().__init__(icon='pool', text='POOL id: {0}'.format(pool_id), parent=parent)
        self.set_styles(title_style='background-color: "#C8C8C8"; color: "#404040";', content_style='background-color: "#D0D0D0"; color: "#404040";')

        self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id = bpmn_data, bpmn_id, lane_id, pool_id
        self.pool_data = self.bpmn_data['lanes'][lane_id]['pools'][pool_id]

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
        self.bpmn_id_changed.connect(self.pool_header_ui.on_bpmn_id_changed)
        self.bpmn_id_changed.connect(self.pool_nodes_ui.on_bpmn_id_changed)
        self.bpmn_id_changed.connect(self.pool_edges_ui.on_bpmn_id_changed)

    def on_bpmn_id_changed(self, bpmn_id):
        self.bpmn_id = bpmn_id
        # print(type(self).__name__, self.lane_id, self.pool_id, 'bpmn_id_changed')
        self.bpmn_id_changed.emit(self.bpmn_id)
