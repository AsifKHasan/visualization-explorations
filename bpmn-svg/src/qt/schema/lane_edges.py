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

class LaneEdges(CollapsibleFrame):
    def __init__(self, bpmn_data, bpmn_id, lane_id, edges, parent=None):
        super().__init__(icon='edges', text='Lane Edges', parent=parent)
        self.bpmn_data, self.bpmn_id, self.lane_id, self.edges = bpmn_data, bpmn_id, lane_id, edges
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040";')
        self.populate()

    def populate(self):
        # debug('LaneEdges: {0}'.format(self.lane_id))

        for edge in self.edges:
            edge_widget = EdgeEditor(self.bpmn_data, 'lane', self.bpmn_id, self.lane_id, None, edge)
            # edge_widget = EdgeEditor(self.bpmn_id, self.lane_id, None, edge)
            edge_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(edge_widget)
