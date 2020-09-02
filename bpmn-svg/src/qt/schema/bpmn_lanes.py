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
    def __init__(self, bpmn_id, lanes, parent=None):
        super().__init__(icon='lanes', text='BPMN Lanes', parent=parent)
        self.bpmn_id, self.lanes = bpmn_id, lanes
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#D8D8D8"; color: "#404040";')
        self.populate()

    def populate(self):
        debug('BpmnLanes: {0}'.format(self.bpmn_id))

        for lane_id, lane_data in self.lanes.items():
            lane_widget = LaneEditor(self.bpmn_id, lane_id, lane_data)
            # lane_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(lane_widget)


class BpmnLanes1(CollapsibleBox):
    def __init__(self, bpmn_id, lanes, parent=None):
        super().__init__(text='BPMN Lanes', parent=parent)
        self.bpmn_id, self.lanes = bpmn_id, lanes

        self.content_area.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')

        self.populate()

    def populate(self):
        debug('BpmnLanes: {0}'.format(self.bpmn_id))

        self.content_layout = QVBoxLayout()

        for lane_id, lane_data in self.lanes.items():
            lane_widget = LaneEditor(self.bpmn_id, lane_id, lane_data)
            self.content_layout.addWidget(lane_widget)

        self.content_layout.addStretch()
        self.setContentLayout(self.content_layout)
