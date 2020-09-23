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

        self.init_ui()
        self.signals_and_slots()
        self.populate()

    def signals_and_slots(self):
        self.add_new_edge.clicked.connect(self.on_new_edge)

    def init_ui(self):
        self.warning_widget = None

        # *add* button to add a new edge
        self.add_new_edge = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['add'])
        self.add_new_edge.setIcon(QIcon(pixmap))

        self.add_new_edge.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.add_new_edge.setStyleSheet('font-size: 9px;')

        self.add_button(self.add_new_edge, 'new-bpmn-edge')

    def populate(self):
        # if we have only one lane, we ctually have no bpmn edges
        if len(self.bpmn_data['lanes']) < 2:
            self.warning_widget = WarningWidget(warning='there are no more than one lane in this bpmn, so no BPMN level edge is possible', parent=self)
            self.warning_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(self.warning_widget)
            # do not allow new-edge
            self.add_new_edge.setEnabled(False)
            return

        # hide warning and allow new-edge
        self.add_new_edge.setEnabled(True)
        if self.warning_widget:
            self.warning_widget.hide()

        for edge in self.edges:
            edge_widget = EdgeEditor(self.bpmn_data, 'bpmn', self.bpmn_id, None, None, edge)
            edge_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(edge_widget)

    def on_bpmn_id_changed(self, bpmn_id):
        self.bpmn_id = bpmn_id

    def on_new_edge(self):
        pass
