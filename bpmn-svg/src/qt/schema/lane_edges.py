#!/usr/bin/env python3
'''
'''
import copy

from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

from qt.schema.edge_editor import EdgeEditor

class LaneEdges(CollapsibleFrame):
    def __init__(self, bpmn_data, bpmn_id, lane_id, parent=None):
        super().__init__(icon='edges', text='Lane Edges', parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040";')

        self.bpmn_data, self.bpmn_id, self.lane_id = bpmn_data, bpmn_id, lane_id
        self.edges = self.bpmn_data['lanes'][lane_id]['edges']

        self.init_ui()
        self.signals_and_slots()
        self.populate()

    def signals_and_slots(self):
        self.add_new_edge.clicked.connect(self.on_new_edge)

    def init_ui(self):
        self.warning_widget = None

        # *add* button to add a new edge
        self.add_new_edge = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['new-edge'])
        self.add_new_edge.setIcon(QIcon(pixmap))

        self.add_new_edge.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.add_new_edge.setStyleSheet('font-size: 9px; border: 0px; background-color: #B0B0B0')

        self.add_button(self.add_new_edge, 'new-lane-edge')

    def populate(self):
        # first clear the layout with all edges
        self.clearContent()

        # if we have only one pool, we ctually have no bpmn edges
        if len(self.bpmn_data['lanes'][self.lane_id]['pools']) < 2:
            self.warning_widget = WarningWidget(warning='there are no more than one pool in this lane, so no LANE level edge is possible', parent=self)
            self.warning_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(self.warning_widget)
            # do not allow new-edge
            self.add_new_edge.setEnabled(False)
            return

        # hide warning and allow new-edge
        self.add_new_edge.setEnabled(True)
        if self.warning_widget:
            self.warning_widget.hide()

        self.num_edges = len(self.edges)
        index = 0
        for edge in self.edges:
            edge_widget = EdgeEditor(self.bpmn_data, 'lane', self.bpmn_id, self.lane_id, None, edge, index, self.num_edges)
            edge_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(edge_widget)
            edge_widget.new_edge.connect(self.on_new_edge)
            edge_widget.remove_edge.connect(self.on_remove_edge)
            edge_widget.order_changed.connect(self.on_order_changed)
            index = index + 1

    def on_bpmn_id_changed(self, bpmn_id):
        self.bpmn_id = bpmn_id

    def on_lane_id_changed(self, lane_id):
        self.lane_id = lane_id

    def on_new_edge(self, index=0):
        # insert a blank edge in bpmn_data
        new_edge_object = copy.deepcopy(NEW_EDGE)
        self.bpmn_data['lanes'][self.lane_id]['edges'].insert(index, new_edge_object)

        # now populate again
        self.populate()

    def on_remove_edge(self, index):
        # remove the edge from bpmn_data
        self.bpmn_data['lanes'][self.lane_id]['edges'].pop(index)

        # now populate again
        self.populate()

    def on_order_changed(self, index, direction):
        if self.num_edges <= 1:
            pass

        if index == 0 and direction == 'up':
            pass

        if index == self.num_edges - 1 and direction == 'down':
            pass

        # swap edges
        if direction == 'up':
            self.bpmn_data['lanes'][self.lane_id]['edges'][index], self.bpmn_data['lanes'][self.lane_id]['edges'][index - 1] = self.bpmn_data['lanes'][self.lane_id]['edges'][index - 1], self.bpmn_data['lanes'][self.lane_id]['edges'][index]
            self.populate()
        elif direction == 'down':
            self.bpmn_data['lanes'][self.lane_id]['edges'][index], self.bpmn_data['lanes'][self.lane_id]['edges'][index + 1] = self.bpmn_data['lanes'][self.lane_id]['edges'][index + 1], self.bpmn_data['lanes'][self.lane_id]['edges'][index]
            self.populate()
