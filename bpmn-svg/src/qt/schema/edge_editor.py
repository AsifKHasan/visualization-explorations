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

    new_edge = pyqtSignal(int)
    remove_edge = pyqtSignal(int)
    order_changed = pyqtSignal(int, str)

    def __init__(self, bpmn_data, scope, bpmn_id, lane_id, pool_id, edge_data, index, num_edges, parent=None):
        super().__init__(icon=edge_data['type'], text='{0:<30}\n{1:<30}'.format(edge_data['from'], edge_data['to']), parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040"; border: 1px solid #202020;', content_style='background-color: "#C8C8C8"; color: "#404040"; font-size: 9pt;')

        self.bpmn_data, self.scope, self.bpmn_id, self.lane_id, self.pool_id, self.edge_data, self.index, self.num_edges = bpmn_data, scope, bpmn_id, lane_id, pool_id, edge_data, index, num_edges

        self.init_ui()
        self.signals_and_slots()

        self.populate()

    def init_ui(self):
        # 'up' button
        self.arrow_up = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['arrow-up'])
        self.arrow_up.setIcon(QIcon(pixmap))

        self.arrow_up.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.arrow_up.setStyleSheet('font-size: 9px; border: 0px; background-color: none')

        self.add_button(self.arrow_up, 'arrow-up')

        # 'down' button
        self.arrow_down = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['arrow-down'])
        self.arrow_down.setIcon(QIcon(pixmap))

        self.arrow_down.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.arrow_down.setStyleSheet('font-size: 9px; border: 0px; background-color: none')

        self.add_button(self.arrow_down, 'arrow-down')

        if self.index == 0:
            self.arrow_up.hide()

        if self.index == self.num_edges - 1:
            self.arrow_down.hide()

        # *add* button to add a new edge
        self.add_new_edge = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['new-edge'])
        self.add_new_edge.setIcon(QIcon(pixmap))

        self.add_new_edge.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.add_new_edge.setStyleSheet('font-size: 9px; border: 0px; background-color: #C8C8C8')

        self.add_button(self.add_new_edge, 'new-{0}-edge'.format(self.scope))

        # *remove* button to remove edge
        self.delete_edge = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['remove-edge'])
        self.delete_edge.setIcon(QIcon(pixmap))

        self.delete_edge.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.delete_edge.setStyleSheet('font-size: 9px; border: 0px; background-color: #C8C8C8')

        self.add_button(self.delete_edge, 'remove-{0}-edge'.format(self.scope))


        # the content area
        content = QWidget()
        self.content_layout = QGridLayout(content)

        # from node
        self.from_node = EdgeNodeWidget(self.lane_id, self.pool_id, self.edge_data['from'], self.bpmn_data, scope=self.scope, role='from', parent=self)
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
        self.to_node = EdgeNodeWidget(self.lane_id, self.pool_id, self.edge_data['to'], self.bpmn_data, scope=self.scope, role='to', parent=self)
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

        # self.update_error()
        self.update_title()

    def update_error(self):
        self.err = False

        from_node_lane, from_node_pool, from_node_id, from_node_type = self.from_node.values()
        to_node_lane, to_node_pool, to_node_id, to_node_type = self.to_node.values()


        if from_node_id is None or from_node_id in ['', '__UNDEFINED__']:
            self.err = True
            self.err_msg = 'from node is UNDEFINED'

        elif to_node_id is None or to_node_id in ['', '__UNDEFINED__']:
            self.err = True
            self.err_msg = 'to node is UNDEFINED'

        # for 'bpmn' scope, the to node must be in a different lane than from node
        elif self.scope == 'bpmn':
            if from_node_lane == to_node_lane:
                self.err = True
                self.err_msg = 'from node and to node are from the same lane, not allowed for BPMN level edges'

        # for 'lane' scope, the to node must be from a different pool but the same lane of from node
        elif self.scope == 'lane':
            if from_node_lane != to_node_lane:
                self.err = True
                self.err_msg = 'from node and to node are from different lanes, not allowed for LANE level edges'
            elif from_node_pool == to_node_pool:
                self.err = True
                self.err_msg = 'from node and to node are from same pool of the specified lane, not allowed for LANE level edges'

        # for 'pool' scope, the to node must be from a same pool of the same lane of from node
        elif self.scope == 'pool':
            if from_node_lane != to_node_lane:
                self.err = True
                self.err_msg = 'from node and to node are from different lanes, not allowed for POOL level edges'
            elif from_node_pool != to_node_pool:
                self.err = True
                self.err_msg = 'from node and to node are from different pools of the specified lane, not allowed for POOL level edges'


        if self.err:
            self.error_label.setText(self.err_msg)
            self.error_label.show()
        else:
            self.error_label.hide()

    def signals_and_slots(self):
        self.add_new_edge.clicked.connect(self.on_new_edge)
        self.delete_edge.clicked.connect(self.on_remove_edge)

        self.arrow_down.clicked.connect(self.on_arrow_down)
        self.arrow_up.clicked.connect(self.on_arrow_up)

        self.from_node.nodeChanged.connect(self.on_from_node_change)
        self.to_node.nodeChanged.connect(self.on_to_node_change)
        self.edge_type.currentIndexChanged.connect(self.on_edge_type_change)
        self.label.textEdited.connect(self.on_edge_label_change)

    def update_bpmn_id(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
        print(type(self).__name__, self.lane_id, self.pool_id, 'bpmn_id_changed')

    def update_lane_id(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id
            self.from_node.update_lane_id(old_lane_id, new_lane_id)
            self.to_node.update_lane_id(old_lane_id, new_lane_id)
            print(type(self).__name__, self.lane_id, self.pool_id, 'lane_id_changed')

    def update_pool_id(self, old_pool_id, new_pool_id):
        if self.pool_id == old_pool_id:
            self.pool_id = new_pool_id
            self.from_node.update_pool_id(old_pool_id, new_pool_id)
            self.to_node.update_pool_id(old_pool_id, new_pool_id)
            print(type(self).__name__, self.lane_id, self.pool_id, 'pool_id_changed')


    def on_arrow_down(self):
        self.order_changed.emit(self.index, 'down')

    def on_arrow_up(self):
        self.order_changed.emit(self.index, 'up')

    def on_new_edge(self):
        self.new_edge.emit(self.index + 1)

    def on_remove_edge(self):
        self.remove_edge.emit(self.index)

    def on_from_node_change(self):
        self.edge_data['from'] = self.from_node.values()[2]

        # we need to let the to-node know about the from-node
        self.to_node.set_other_node_values(self.from_node.values())

        self.update_title()

    def on_to_node_change(self):
        self.edge_data['to'] = self.to_node.values()[2]
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
