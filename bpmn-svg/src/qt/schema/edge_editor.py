#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

class EdgeEditor(CollapsibleFrame):
    def __init__(self, bpmn_id, lane_id, pool_id, edge_data, parent=None):
        super().__init__(icon='edge', text='EDGE: {0} {1} {2}'.format(edge_data['from'], edge_data['type'], edge_data['to']), parent=parent)
        self.bpmn_id, self.lane_id, self.pool_id, self.edge_data = bpmn_id, lane_id, pool_id, edge_data
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040"; font-size: 9pt;')
        self.populate()
        self.signals_and_slots()

    def populate(self):
        # debug('EdgeEditor: {0} {1} {2}'.format(self.edge_data['from'], self.edge_data['type'], self.edge_data['to']))

        content = QWidget()
        self.content_layout = QGridLayout(content)

        # from node
        self.from_node = QLineEdit()
        self.from_node.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.from_node, 0, 0, 1, 2)

        # edge_type
        self.edge_type = QLineEdit()
        self.edge_type.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.edge_type, 0, 2)

        # to node
        self.to_node = QLineEdit()
        self.to_node.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.to_node, 0, 3, 1, 2)

        # label
        self.label_label = QLabel("Label:")
        self.label_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label = QLineEdit()
        self.label.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.label_label, 1, 0)
        self.content_layout.addWidget(self.label, 1, 1, 1, 4)

        self.addWidget(content)

        self.from_node.setText(self.edge_data['from'])
        self.edge_type.setText(self.edge_data['type'])
        self.to_node.setText(self.edge_data['to'])
        self.label.setText(self.edge_data['label'])

        for c in range(0, self.content_layout.columnCount()):
            self.content_layout.setColumnStretch(c, 1)

    def signals_and_slots(self):
        pass
