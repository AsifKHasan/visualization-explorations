#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

class NodeEditor(CollapsibleBox):
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data, parent=None):
        super().__init__(text='NODE id: {0}'.format(node_id), parent=parent)
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.content_area.setStyleSheet('background-color: "#D0D0D0"; color: "#404040"; font-size: 9pt;')
        self.populate()

    def populate(self):
        # debug('NodeEditor: {0}'.format(self.node_id))
        self.content_layout = QFormLayout()

        # Bpmn id
        self.id = QLineEdit()
        self.id.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addRow(QLabel("Id:"), self.id)

        # Bpmn title
        self.title = QLineEdit()
        self.title.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addRow(QLabel("Title:"), self.title)

        self.setContentLayout(self.content_layout)

        self.id.setText(self.node_id)
        self.title.setText(self.node_data['label'])
