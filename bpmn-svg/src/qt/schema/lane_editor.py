#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

from qt.schema.lane_header import LaneHeader
from qt.schema.lane_pools import LanePools
from qt.schema.lane_edges import LaneEdges

class LaneEditor(CollapsibleFrame):

    lane_id_change_requested = pyqtSignal(str, str)
    pool_id_change_requested = pyqtSignal(str, str)
    node_id_change_requested = pyqtSignal(str, str)

    new_lane = pyqtSignal(int)
    remove_lane = pyqtSignal(int)
    lane_order_changed = pyqtSignal(int, str)

    pool_removed = pyqtSignal(str)
    remove_pool = pyqtSignal(str)

    node_removed = pyqtSignal(str)
    remove_node = pyqtSignal(str)

    bpmn_id_change_done = pyqtSignal(str, str)
    lane_id_change_done = pyqtSignal(str, str)
    pool_id_change_done = pyqtSignal(str, str)
    node_id_change_done = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, lane_id, index, num_lanes, parent=None):
        super().__init__(icon='lane', text='LANE id: {0}'.format(lane_id), parent=parent)
        self.set_styles(title_style='background-color: "#D8D8D8"; color: "#404040";', content_style='background-color: "#D0D0D0"; color: "#404040";')

        self.bpmn_data, self.bpmn_id, self.lane_id, self.index, self.num_lanes = bpmn_data, bpmn_id, lane_id, index, num_lanes
        self.lane_data = self.bpmn_data['lanes'][self.lane_id]

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

        if self.index == self.num_lanes - 1:
            self.arrow_down.hide()

        # *add* button to add a new lane
        self.add_new_lane = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['new-lane'])
        self.add_new_lane.setIcon(QIcon(pixmap))

        self.add_new_lane.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.add_new_lane.setStyleSheet('font-size: 9px; border: 0px; background-color: #C8C8C8')

        self.add_button(self.add_new_lane, 'new-bpmn-lane')

        # *remove* button to remove lane
        self.delete_lane = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['remove-lane'])
        self.delete_lane.setIcon(QIcon(pixmap))

        self.delete_lane.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.delete_lane.setStyleSheet('font-size: 9px; border: 0px; background-color: #C8C8C8')

        self.add_button(self.delete_lane, 'remove-bpmn-lane')

    def populate(self):
        # Lane id, title and styles at the top
        self.lane_header_ui = LaneHeader(self.bpmn_data, self.bpmn_id, self.lane_id)
        self.addWidget(self.lane_header_ui)

        # Pool container in the middle
        self.lane_pools_ui = LanePools(self.bpmn_data, self.bpmn_id, self.lane_id)
        self.addWidget(self.lane_pools_ui)

        # Edge container after the pool container
        self.lane_edges_ui = LaneEdges(self.bpmn_data, self.bpmn_id, self.lane_id)
        self.addWidget(self.lane_edges_ui)

    def signals_and_slots(self):
        self.add_new_lane.clicked.connect(self.on_new_lane)
        self.delete_lane.clicked.connect(self.on_remove_lane)

        self.arrow_down.clicked.connect(self.on_arrow_down)
        self.arrow_up.clicked.connect(self.on_arrow_up)

        self.lane_header_ui.lane_id_change_requested.connect(self.on_lane_id_change_requested)
        self.lane_pools_ui.pool_id_change_requested.connect(self.on_pool_id_change_requested)
        self.lane_pools_ui.node_id_change_requested.connect(self.on_node_id_change_requested)

        self.lane_pools_ui.pool_removed.connect(self.on_pool_removed)
        self.lane_pools_ui.node_removed.connect(self.on_node_removed)

        self.bpmn_id_change_done.connect(self.lane_header_ui.on_bpmn_id_change_done)
        self.bpmn_id_change_done.connect(self.lane_pools_ui.on_bpmn_id_change_done)
        self.bpmn_id_change_done.connect(self.lane_edges_ui.on_bpmn_id_change_done)

        self.lane_id_change_done.connect(self.lane_header_ui.on_lane_id_change_done)
        self.lane_id_change_done.connect(self.lane_pools_ui.on_lane_id_change_done)
        self.lane_id_change_done.connect(self.lane_edges_ui.on_lane_id_change_done)

        self.pool_id_change_done.connect(self.lane_header_ui.on_pool_id_change_done)
        self.pool_id_change_done.connect(self.lane_pools_ui.on_pool_id_change_done)
        self.pool_id_change_done.connect(self.lane_edges_ui.on_pool_id_change_done)

        self.node_id_change_done.connect(self.lane_pools_ui.on_node_id_change_done)
        self.node_id_change_done.connect(self.lane_edges_ui.on_node_id_change_done)

        self.remove_pool.connect(self.lane_pools_ui.on_remove_pool)
        self.remove_pool.connect(self.lane_edges_ui.on_remove_pool)

        self.remove_node.connect(self.lane_pools_ui.on_remove_node)
        self.remove_node.connect(self.lane_edges_ui.on_remove_node)

    def on_lane_id_change_requested(self, old_lane_id, new_lane_id):
        print('.' * 8, type(self).__name__, 'lane_id_change_requested', old_lane_id, '-->', new_lane_id)
        self.lane_id_change_requested.emit(old_lane_id, new_lane_id)

    def on_pool_id_change_requested(self, old_pool_id, new_pool_id):
        print('.' * 8, type(self).__name__, 'pool_id_change_requested', old_pool_id, '-->', new_pool_id)
        self.pool_id_change_requested.emit(old_pool_id, new_pool_id)

    def on_node_id_change_requested(self, old_node_id, new_node_id):
        print('.' * 8, type(self).__name__, 'node_id_change_requested', old_node_id, '-->', new_node_id)
        self.node_id_change_requested.emit(old_node_id, new_node_id)

    def on_bpmn_id_change_done(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
        # print(type(self).__name__, self.lane_id, 'bpmn_id_change_done')
        self.bpmn_id_change_done.emit(old_bpmn_id, new_bpmn_id)

    def on_lane_id_change_done(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id
            self.lane_data = self.bpmn_data['lanes'][self.lane_id]

            print('.' * 8, type(self).__name__, 'lane_id_change_done', old_lane_id, '-->', new_lane_id)
            self.change_title('Lane id: {0}'.format(self.lane_id), icon='lane')
            self.lane_id_change_done.emit(old_lane_id, new_lane_id)

    def on_pool_id_change_done(self, old_pool_id, new_pool_id):
        print('.' * 8, type(self).__name__, 'pool_id_change_done', old_pool_id, '-->', new_pool_id)
        self.pool_id_change_done.emit(old_pool_id, new_pool_id)

    def on_node_id_change_done(self, old_node_id, new_node_id):
        print('.' * 8, type(self).__name__, 'node_id_change_done', old_node_id, '-->', new_node_id)
        self.node_id_change_done.emit(old_node_id, new_node_id)

    def on_lane_removed(self, lane_id):
        # emit node_removed to parent
        print('.' * 8, type(self).__name__, 'lane_removed', lane_id)
        self.lane_removed.emit(node_id)

    def on_pool_removed(self, pool_id):
        # emit node_removed to parent
        print('.' * 8, type(self).__name__, 'pool_removed', pool_id)
        self.pool_removed.emit(node_id)

    def on_node_removed(self, node_id):
        # emit node_removed to parent
        print('.' * 8, type(self).__name__, 'node_removed', node_id)
        self.node_removed.emit(node_id)

    def on_remove_pool(self, pool_id):
        print('.' * 8, type(self).__name__, 'remove_pool', pool_id)
        self.remove_pool.emit(pool_id)

    def on_remove_node(self, node_id):
        print('.' * 8, type(self).__name__, 'remove_node', node_id)
        self.remove_node.emit(node_id)

    def on_arrow_down(self):
        self.lane_order_changed.emit(self.index, 'down')

    def on_arrow_up(self):
        self.lane_order_changed.emit(self.index, 'up')

    def on_new_lane(self):
        self.new_lane.emit(self.index + 1)

    def on_remove_lane(self):
        self.remove_lane.emit(self.index)
