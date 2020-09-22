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

class BpmnEdges(CollapsibleFrame):
    def __init__(self, bpmn_data, bpmn_id, parent=None):
        super().__init__(icon='edges', text='BPMN Edges', parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#D8D8D8"; color: "#404040";')

        self.bpmn_data, self.bpmn_id = bpmn_data, bpmn_id
        self.edges = self.bpmn_data['edges']

        self.warning_widget = None

        self.populate()

    def populate(self):
        # if we have only one lane, we ctually have no bpmn edges
        if len(self.bpmn_data['lanes']) < 2:
            self.warning_widget = WarningWidget(warning='there are no more than one lane in this bpmn, so no BPMN level edge is possible', parent=self)
            self.warning_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(self.warning_widget)
            return

        # hide warning
        if self.warning_widget:
            self.warning_widget.hide()
            
        for edge in self.edges:
            edge_widget = EdgeEditor(self.bpmn_data, 'bpmn', self.bpmn_id, None, None, edge)
            edge_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(edge_widget)

    def on_bpmn_id_changed(self, bpmn_id):
        self.bpmn_id = bpmn_id
