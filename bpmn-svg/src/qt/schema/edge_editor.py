#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

class EdgeEditor(CollapsibleBox):
    def __init__(self, bpmn_id, lane_id, pool_id, edge_data, parent=None):
        super().__init__(text='EDGE: {0} {1} {2}'.format(edge_data['from'], edge_data['type'], edge_data['to']), parent=parent)
        self.bpmn_id, self.lane_id, self.pool_id, self.edge_data = bpmn_id, lane_id, pool_id, edge_data

        self.content_area.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')

        self.populate()

    def populate(self):
        debug('EdgeEditor: {0} {1} {2}'.format(self.edge_data['from'], self.edge_data['type'], self.edge_data['to']))
        self.content_layout = QGridLayout()

        # from node
        self.from_node = QLineEdit()
        self.from_node.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.from_node)

        # edge_type
        self.edge_type = QLineEdit()
        self.edge_type.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.edge_type)

        # to node
        self.to_node = QLineEdit()
        self.to_node.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.to_node)

        # to node
        self.label = QLineEdit()
        self.label.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.label)

        self.setContentLayout(self.content_layout)

        self.from_node.setText(self.edge_data['from'])
        self.edge_type.setText(self.edge_data['type'])
        self.to_node.setText(self.edge_data['to'])
        self.label.setText(self.edge_data['label'])

class EdgeEditor1(QFrame):
    def __init__(self, bpmn_id, lane_id, pool_id, edge_data, parent=None):
        super().__init__(parent)
        self.bpmn_id, self.lane_id, self.pool_id, self.edge_data = bpmn_id, lane_id, pool_id, edge_data

        self.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')

        self.populate()

    def title(self):
        return 'EDGE: {0} {1} {2}'.format(self.edge_data['from'], self.edge_data['type'], self.edge_data['to'])

    def populate(self):
        debug('EdgeEditor: {0} {1} {2}'.format(self.edge_data['from'], self.edge_data['type'], self.edge_data['to']))

        self.content_layout = QGridLayout()

        # from node
        self.from_node = QLineEdit()
        self.from_node.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.from_node)

        # edge_type
        self.edge_type = QLineEdit()
        self.edge_type.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.edge_type)

        # to node
        self.to_node = QLineEdit()
        self.to_node.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.to_node)

        # to node
        self.label = QLineEdit()
        self.label.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.label)

        self.setLayout(self.content_layout)

        self.from_node.setText(self.edge_data['from'])
        self.edge_type.setText(self.edge_data['type'])
        self.to_node.setText(self.edge_data['to'])
        self.label.setText(self.edge_data['label'])
