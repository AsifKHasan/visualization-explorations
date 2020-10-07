#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

from qt.schema.lane_editor import LaneEditor

class BpmnLanes(CollapsibleFrame):

    bpmn_id_changed = pyqtSignal(str)
    lane_id_changed = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, parent=None):
        super().__init__(icon='lanes', text='BPMN Lanes', parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#D8D8D8"; color: "#404040";')

        self.bpmn_data, self.bpmn_id = bpmn_data, bpmn_id
        self.bpmn_lanes = self.bpmn_data['lanes']

        self.populate()
        self.signals_and_slots()

    def populate(self):
        for lane_id, lane_data in self.bpmn_lanes.items():
            lane_widget = LaneEditor(self.bpmn_data, self.bpmn_id, lane_id, self)
            lane_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(lane_widget)
            self.bpmn_id_changed.connect(lane_widget.on_bpmn_id_changed)
            lane_widget.lane_id_changed.connect(self.on_lane_id_changed)

    def signals_and_slots(self):
        pass

    def on_bpmn_id_changed(self, bpmn_id):
        self.bpmn_id = bpmn_id
        self.bpmn_id_changed.emit(self.bpmn_id)

    def on_lane_id_changed(self, old_lane_id, new_lane_id):
        old_keys = list(self.bpmn_lanes.keys())
        new_keys = [new_node_id if k == old_node_id else k for k in old_keys]

        self.bpmn_lanes = dict(zip(new_keys, self.bpmn_lanes.values()))
        print(list(self.pool_nodes.keys()))

        # populate the nodes
        # self.populate()

        self.lane_id_changed.emit(old_lane_id, new_lane_id)
