#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

from qt.schema.pool_editor import PoolEditor

class LanePools(CollapsibleFrame):

    pool_id_change_requested = pyqtSignal(str, str)
    node_id_change_requested = pyqtSignal(str, str)

    bpmn_id_change_done = pyqtSignal(str, str)
    lane_id_change_done = pyqtSignal(str, str)
    pool_id_change_done = pyqtSignal(str, str)
    node_id_change_done = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, lane_id, parent=None):
        super().__init__(icon='pools', text='Lane Pools', parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040";')

        self.bpmn_data, self.bpmn_id, self.lane_id = bpmn_data, bpmn_id, lane_id
        self.lane_pools = self.bpmn_data['lanes'][self.lane_id]['pools']

        self.populate()

    def populate(self):
        for pool_id, pool_data in self.lane_pools.items():
            pool_widget = PoolEditor(self.bpmn_data, self.bpmn_id, self.lane_id, pool_id, self)
            pool_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(pool_widget)

            self.bpmn_id_change_done.connect(pool_widget.on_bpmn_id_change_done)
            self.lane_id_change_done.connect(pool_widget.on_lane_id_change_done)
            self.pool_id_change_done.connect(pool_widget.on_pool_id_change_done)
            self.node_id_change_done.connect(pool_widget.on_node_id_change_done)

            pool_widget.pool_id_change_requested.connect(self.on_pool_id_change_requested)
            pool_widget.node_id_change_requested.connect(self.on_node_id_change_requested)

    def on_pool_id_change_requested(self, old_pool_id, new_pool_id):
        print('.' * 12, type(self).__name__, 'pool_id_change_requested', old_pool_id, '-->', new_pool_id)
        self.pool_id_change_requested.emit(old_pool_id, new_pool_id)

    def on_node_id_change_requested(self, old_node_id, new_node_id):
        print('.' * 12, type(self).__name__, 'node_id_change_requested', old_node_id, '-->', new_node_id)
        self.node_id_change_requested.emit(old_node_id, new_node_id)

    def on_bpmn_id_change_done(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
        # print(type(self).__name__, self.lane_id, 'bpmn_id_change_done')
        self.bpmn_id_change_done.emit(old_bpmn_id, new_bpmn_id)

    def on_lane_id_change_done(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id
            self.lane_pools = self.bpmn_data['lanes'][self.lane_id]['pools']

            print('.' * 12, type(self).__name__, 'lane_id_change_done', old_lane_id, '-->', new_lane_id)
            self.lane_id_change_done.emit(old_lane_id, new_lane_id)

    def on_pool_id_change_done(self, old_pool_id, new_pool_id):
        old_keys = list(self.lane_pools.keys())
        new_keys = [new_pool_id if k == old_pool_id else k for k in old_keys]

        self.bpmn_data['lanes'][self.lane_id]['pools'] = dict(zip(new_keys, self.lane_pools.values()))
        self.lane_pools = self.bpmn_data['lanes'][self.lane_id]['pools']
        # print(list(self.bpmn_pools.keys()))

        print('.' * 12, type(self).__name__, 'pool_id_change_done', old_pool_id, '-->', new_pool_id)
        self.pool_id_change_done.emit(old_pool_id, new_pool_id)

    def on_node_id_change_done(self, old_node_id, new_node_id):
        print('.' * 12, type(self).__name__, 'node_id_change_done', old_node_id, '-->', new_node_id)
        self.node_id_change_done.emit(old_node_id, new_node_id)
