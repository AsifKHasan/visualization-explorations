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
    def __init__(self, bpmn_id, edges, parent=None):
        super().__init__(icon='edges', text='BPMN Edges', parent=parent)
        self.bpmn_id, self.edges = bpmn_id, edges
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#D8D8D8"; color: "#404040";')
        self.populate()

    def populate(self):
        # debug('BpmnEdges: {0}'.format(self.bpmn_id))

        for edge in self.edges:
            edge_widget = EdgeEditor(self.bpmn_id, None, None, edge)
            # edge_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(edge_widget)
