#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

from qt.schema.lane_header import LaneHeader
from qt.schema.lane_pools import LanePools
from qt.schema.lane_edges import LaneEdges

class LaneEditor(CollapsibleFrame):

    bpmn_id_changed = pyqtSignal(str)
    lane_id_changed = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, lane_id, parent=None):
        super().__init__(icon='lane', text='LANE id: {0}'.format(lane_id), parent=parent)
        self.set_styles(title_style='background-color: "#D8D8D8"; color: "#404040";', content_style='background-color: "#D0D0D0"; color: "#404040";')

        self.bpmn_data, self.bpmn_id, self.lane_id = bpmn_data, bpmn_id, lane_id
        self.lane_data = self.bpmn_data['lanes'][lane_id]

        self.populate()
        self.signals_and_slots()

    def populate(self):
        # Lane id, title and styles at the top
        self.lane_header_ui = LaneHeader(self.bpmn_data, self.bpmn_id, self.lane_id)
        self.addWidget(self.lane_header_ui)

        # Pool container in the middle
        self.lane_pools_ui = LanePools(self.bpmn_data, self.bpmn_id, self.lane_id)
        self.addWidget(self.lane_pools_ui)

        # Edge container after the pool container
        self.lane_edges_ui = LaneEdges(self.bpmn_data, self.bpmn_id, self.lane_id)
        self.addWidget(self.lane_edges_ui)

    def signals_and_slots(self):
        self.bpmn_id_changed.connect(self.lane_header_ui.on_bpmn_id_changed)
        self.bpmn_id_changed.connect(self.lane_pools_ui.on_bpmn_id_changed)
        self.bpmn_id_changed.connect(self.lane_edges_ui.on_bpmn_id_changed)

        self.lane_header_ui.lane_id_changed.connect(self.on_lane_id_changed)
        self.lane_id_changed.connect(self.lane_header_ui.on_lane_id_changed)
        self.lane_id_changed.connect(self.lane_pools_ui.on_lane_id_changed)
        self.lane_id_changed.connect(self.lane_edges_ui.on_lane_id_changed)

    def on_bpmn_id_changed(self, bpmn_id):
        self.bpmn_id = bpmn_id
        # print(type(self).__name__, self.lane_id, 'bpmn_id_changed')
        self.bpmn_id_changed.emit(self.bpmn_id)

    def on_lane_id_changed(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = lane_id
            self.lane_data = self.bpmn_data['lanes'][self.lane_id]

            print(type(self).__name__, self.lane_id, 'lane_id_changed')
            self.lane_id_changed.emit(old_lane_id, self.lane_id)
