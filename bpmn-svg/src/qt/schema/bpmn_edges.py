#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *

from util.logger import *

class BpmnEdges(QGroupBox):
    def __init__(self, parent=None):
        super(QtWidgets.QGroupBox, self).__init__(parent)
        self.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')
        self.setTitle('Edges between lanes')

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Bpmn id
        self.bpmn_id = QLineEdit()
        self.bpmn_id.setStyleSheet('background-color: "#F8F8F8"')
        self.layout.addWidget(self.bpmn_id)

        self.bpmn_title = QLineEdit()
        self.bpmn_title.setStyleSheet('background-color: "#F8F8F8"')
        self.layout.addWidget(self.bpmn_title)

    def populate(self, bpmn_id, edges):
        self.edges = edges
        self.bpmn_id = bpmn_id
