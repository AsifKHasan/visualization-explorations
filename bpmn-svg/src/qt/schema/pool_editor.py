#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

from qt.schema.pool_header import PoolHeader
from qt.schema.pool_nodes import PoolNodes
from qt.schema.pool_edges import PoolEdges

class PoolEditor(CollapsibleFrame):

    pool_id_change_requested = pyqtSignal(str, str)
    node_id_change_requested = pyqtSignal(str, str)

    new_pool = pyqtSignal(int)
    remove_pool = pyqtSignal(int)
    pool_order_changed = pyqtSignal(int, str)

    node_removed = pyqtSignal(str)
    remove_node = pyqtSignal(str)

    bpmn_id_change_done = pyqtSignal(str, str)
    lane_id_change_done = pyqtSignal(str, str)
    pool_id_change_done = pyqtSignal(str, str)
    node_id_change_done = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, lane_id, pool_id, index, num_pools, parent=None):
        super().__init__(icon='pool', text='POOL id: {0}'.format(pool_id), parent=parent)
        self.set_styles(title_style='background-color: "#C8C8C8"; color: "#404040";', content_style='background-color: "#D0D0D0"; color: "#404040";')

        self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id, self.index, self.num_pools = bpmn_data, bpmn_id, lane_id, pool_id, index, num_pools
        self.pool_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]

        self.init_ui()
        self.populate()
        self.signals_and_slots()

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

        if self.index == self.num_pools - 1:
            self.arrow_down.hide()

        # *add* button to add a new pool
        self.add_new_pool = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['new-pool'])
        self.add_new_pool.setIcon(QIcon(pixmap))

        self.add_new_pool.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.add_new_pool.setStyleSheet('font-size: 9px; border: 0px; background-color: #C8C8C8')

        self.add_button(self.add_new_pool, 'new-lane-pool')

        # *remove* button to remove pool
        self.delete_pool = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['remove-pool'])
        self.delete_pool.setIcon(QIcon(pixmap))

        self.delete_pool.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.delete_pool.setStyleSheet('font-size: 9px; border: 0px; background-color: #C8C8C8')

        self.add_button(self.delete_pool, 'remove-lane-pool')

    def populate(self):
        # Pool id, title and styles at the top
        self.pool_header_ui = PoolHeader(self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id)
        self.addWidget(self.pool_header_ui)

        # Node container in the middle
        self.pool_nodes_ui = PoolNodes(self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id)
        self.addWidget(self.pool_nodes_ui)

        # Edge container after the node container
        self.pool_edges_ui = PoolEdges(self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id)
        self.addWidget(self.pool_edges_ui)

    def signals_and_slots(self):
        self.add_new_pool.clicked.connect(self.on_new_pool)
        self.delete_pool.clicked.connect(self.on_remove_pool)

        self.arrow_down.clicked.connect(self.on_arrow_down)
        self.arrow_up.clicked.connect(self.on_arrow_up)

        self.pool_header_ui.pool_id_change_requested.connect(self.on_pool_id_change_requested)
        self.pool_nodes_ui.node_id_change_requested.connect(self.on_node_id_change_requested)
        self.pool_nodes_ui.node_removed.connect(self.on_node_removed)

        self.bpmn_id_change_done.connect(self.pool_header_ui.on_bpmn_id_change_done)
        self.bpmn_id_change_done.connect(self.pool_nodes_ui.on_bpmn_id_change_done)
        self.bpmn_id_change_done.connect(self.pool_edges_ui.on_bpmn_id_change_done)

        self.lane_id_change_done.connect(self.pool_header_ui.on_lane_id_change_done)
        self.lane_id_change_done.connect(self.pool_nodes_ui.on_lane_id_change_done)
        self.lane_id_change_done.connect(self.pool_edges_ui.on_lane_id_change_done)

        self.pool_id_change_done.connect(self.pool_header_ui.on_pool_id_change_done)
        self.pool_id_change_done.connect(self.pool_nodes_ui.on_pool_id_change_done)
        self.pool_id_change_done.connect(self.pool_edges_ui.on_pool_id_change_done)

        self.node_id_change_done.connect(self.pool_nodes_ui.on_node_id_change_done)
        self.node_id_change_done.connect(self.pool_edges_ui.on_node_id_change_done)

        self.remove_node.connect(self.pool_edges_ui.on_remove_node)

    def on_pool_id_change_requested(self, old_pool_id, new_pool_id):
        print('.' * 16, type(self).__name__, 'pool_id_change_requested', old_pool_id, '-->', new_pool_id)
        self.pool_id_change_requested.emit(old_pool_id, new_pool_id)

    def on_node_id_change_requested(self, old_node_id, new_node_id):
        print('.' * 16, type(self).__name__, 'node_id_change_requested', old_node_id, '-->', new_node_id)
        self.node_id_change_requested.emit(old_node_id, new_node_id)

    def on_bpmn_id_change_done(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
        # print(type(self).__name__, self.lane_id, self.pool_id, 'bpmn_id_change_done')
        self.bpmn_id_change_done.emit(old_bpmn_id, new_bpmn_id)

    def on_lane_id_change_done(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id
            self.pool_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]

            print('.' * 16, type(self).__name__, 'lane_id_change_done', old_lane_id, '-->', new_lane_id)
            self.lane_id_change_done.emit(old_lane_id, new_lane_id)

    def on_pool_id_change_done(self, old_pool_id, new_pool_id):
        if self.pool_id == old_pool_id:
            self.pool_id = new_pool_id
            self.pool_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]

            print('.' * 16, type(self).__name__, 'pool_id_change_done', old_pool_id, '-->', new_pool_id)
            self.pool_id_change_done.emit(old_pool_id, new_pool_id)

    def on_node_id_change_done(self, old_node_id, new_node_id):
        print('.' * 16, type(self).__name__, 'node_id_change_done', old_node_id, '-->', new_node_id)
        self.node_id_change_done.emit(old_node_id, new_node_id)

    def on_node_removed(self, node_id):
        # emit node_removed to parent
        print('.' * 16, type(self).__name__, 'node_removed', node_id)
        self.node_removed.emit(node_id)

    def on_remove_node(self, node_id):
        print('.' * 16, type(self).__name__, 'remove_node', node_id)
        self.remove_node.emit(node_id)

    def on_arrow_down(self):
        self.pool_order_changed.emit(self.index, 'down')

    def on_arrow_up(self):
        self.pool_order_changed.emit(self.index, 'up')

    def on_new_pool(self):
        self.new_pool.emit(self.index + 1)

    def on_remove_pool(self):
        self.remove_pool.emit(self.index)
