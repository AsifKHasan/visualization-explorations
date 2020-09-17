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
    def __init__(self, bpmn_data, bpmn_id, parent=None):
        super().__init__(icon='lanes', text='BPMN Lanes', parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#D8D8D8"; color: "#404040";')

        self.bpmn_data, self.bpmn_id = bpmn_data, bpmn_id
        self.bpmn_lanes = self.bpmn_data['lanes']

        self.populate()

    def populate(self):
        for lane_id, lane_data in self.bpmn_lanes.items():
            lane_widget = LaneEditor(self.bpmn_data, self.bpmn_id, lane_id, self)
            lane_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(lane_widget)

    def on_bpmn_id_changed(self, bpmn_id):
        self.bpmn_id = bpmn_id
