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
    def __init__(self, bpmn_data, bpmn_id, lane_id, lane_data, parent=None):
        super().__init__(icon='lane', text='LANE id: {0}'.format(lane_id), parent=parent)
        self.bpmn_data, self.bpmn_id, self.lane_id, self.lane_data = bpmn_data, bpmn_id, lane_id, lane_data
        self.set_styles(title_style='background-color: "#D8D8D8"; color: "#404040";', content_style='background-color: "#D0D0D0"; color: "#404040";')
        self.populate()

    def populate(self):
        # debug('LaneEditor: {0}'.format(self.lane_id))

        # Lane id, title and styles at the top
        self.lane_header_ui = LaneHeader(self.bpmn_data, self.bpmn_id, self.lane_id, self.lane_data)
        self.addWidget(self.lane_header_ui)

        # Pool container in the middle
        self.lane_pools_ui = LanePools(self.bpmn_data, self.bpmn_id, self.lane_id, self.lane_data.get('pools', None))
        self.addWidget(self.lane_pools_ui)

        # Edge container after the pool container
        self.lane_edges_ui = LaneEdges(self.bpmn_data, self.bpmn_id, self.lane_id, self.lane_data.get('edges', None))
        self.addWidget(self.lane_edges_ui)
