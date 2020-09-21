#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

class EdgeEditor(CollapsibleFrame):
    def __init__(self, bpmn_data, scope, bpmn_id, lane_id, pool_id, edge_data, parent=None):
        super().__init__(icon=edge_data['type'], text='{0}\n{1}'.format(edge_data['from'], edge_data['to']), parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040"; font-size: 9pt;')

        self.bpmn_data, self.scope, self.bpmn_id, self.lane_id, self.pool_id, self.edge_data = bpmn_data, scope, bpmn_id, lane_id, pool_id, edge_data

        self.init_ui()
        self.signals_and_slots()

        self.populate()

    def init_ui(self):
        content = QWidget()
        self.content_layout = QGridLayout(content)

        # from node
        self.from_node = EdgeNodeWidget(self.edge_data['from'], self.bpmn_data, scope=self.scope, role='from', parent=self)
        self.content_layout.addWidget(self.from_node, 0, 0, 1, 3)

        # edge_type
        self.edge_type = QComboBox()
        self.edge_type.setView(QListView())
        self.edge_type.setStyleSheet('QListView::item{height: 50px} QWidget{background-color: #F8F8F8}')
        for key in EDGE_MAP:
            pixmap = QPixmap(EDGE_MAP[key])
            pixmap = pixmap.scaledToHeight(50)
            self.edge_type.addItem(QIcon(pixmap), None, key)

        self.edge_type.resize(self.edge_type.sizeHint())
        self.edge_type.setIconSize(QSize(75, 25))

        self.content_layout.addWidget(self.edge_type, 0, 3)

        # to node
        self.to_node = EdgeNodeWidget(self.edge_data['to'], self.bpmn_data, scope=self.scope, role='to', parent=self)
        self.content_layout.addWidget(self.to_node, 0, 4, 1, 3)

        # label
        self.label = QLineEdit()
        self.label.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.label, 1, 0, 1, 7)

        # Error
        self.error_label = QLabel()
        self.error_label.setStyleSheet('color: "#F80000"')
        self.content_layout.addWidget(self.error_label, 2, 0, 1, 7)

        self.addWidget(content)

        for c in range(0, self.content_layout.columnCount()):
            self.content_layout.setColumnStretch(c, 1)

    def populate(self):
        # we need to let the to-node know about the from-node
        self.to_node.set_other_node_values(self.from_node.values())

        index = self.edge_type.findData(self.edge_data['type'])
        if index != -1:
            self.edge_type.setCurrentIndex(index);

        if self.edge_data['label'] != '':
            self.label.setText(self.edge_data['label'])
        else:
            self.label.setPlaceholderText('label')

        self.update_error()
        self.update_title()

    def update_error(self):
        self.err = False
        # for 'bpmn' scope, the to node must be in a different lane than from node
        if self.scope == 'bpmn':
            from_node_lane, _, _, _ = self.from_node.values()
            to_node_lane, _, _, _ = self.to_node.values()
            if from_node_lane == to_node_lane:
                self.err = True
                self.err_msg = 'from node and to node are from the same lane, not allowed for BPMN level edges'

        if self.err:
            self.error_label.setText(self.err_msg)
            self.error_label.show()
        else:
            self.error_label.hide()

    def signals_and_slots(self):
        self.from_node.nodeChanged.connect(self.on_from_node_change)
        self.to_node.nodeChanged.connect(self.on_to_node_change)
        self.edge_type.currentIndexChanged.connect(self.on_edge_type_change)
        self.label.textEdited.connect(self.on_edge_label_change)

    def on_from_node_change(self):
        self.edge_data['from'] = self.from_node.values()[2]

        # we need to let the to-node know about the from-node
        self.to_node.set_other_node_values(self.from_node.values())

        self.update_title()

    def on_to_node_change(self):
        self.edge_data['to'] = self.from_node.values()[2]
        self.update_title()

    def on_edge_type_change(self):
        # print(self.edge_type.currentIndex())
        key = self.edge_type.itemData(self.edge_type.currentIndex())
        if key is not None:
            self.edge_data['type'] = key
            self.update_title()

    def on_edge_label_change(self):
        self.edge_data['label'] = self.label.text()

    def update_title(self):
        self.update_error()
        self.change_title(text='{0}\n{1}'.format(self.edge_data['from'], self.edge_data['to']), icon=self.edge_data['type'], err=self.err)
