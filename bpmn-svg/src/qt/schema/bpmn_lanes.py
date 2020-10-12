#!/usr/bin/env python3
'''
'''
import copy

from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *
from util.helper_util import *

from qt.schema.lane_editor import LaneEditor

class BpmnLanes(CollapsibleFrame):

    lane_id_change_requested = pyqtSignal(str, str)
    pool_id_change_requested = pyqtSignal(str, str)
    node_id_change_requested = pyqtSignal(str, str)

    lane_removed = pyqtSignal(str)
    remove_lane = pyqtSignal(str)

    pool_removed = pyqtSignal(str)
    remove_pool = pyqtSignal(str)

    node_removed = pyqtSignal(str)
    remove_node = pyqtSignal(str)

    bpmn_id_change_done = pyqtSignal(str, str)
    lane_id_change_done = pyqtSignal(str, str)
    pool_id_change_done = pyqtSignal(str, str)
    node_id_change_done = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, parent=None):
        super().__init__(icon='lanes', text='BPMN Lanes', parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#D8D8D8"; color: "#404040";')

        self.bpmn_data, self.bpmn_id = bpmn_data, bpmn_id
        self.bpmn_lanes = self.bpmn_data['lanes']

        self.populate()
        self.signals_and_slots()

    def populate(self):
        for lane_id, lane_data in self.bpmn_lanes.items():
            lane_widget = LaneEditor(self.bpmn_data, self.bpmn_id, lane_id, self)
            lane_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(lane_widget)

            self.bpmn_id_change_done.connect(lane_widget.on_bpmn_id_change_done)
            self.lane_id_change_done.connect(lane_widget.on_lane_id_change_done)
            self.pool_id_change_done.connect(lane_widget.on_pool_id_change_done)
            self.node_id_change_done.connect(lane_widget.on_node_id_change_done)

            self.remove_lane.connect(lane_widget.on_remove_lane)
            self.remove_pool.connect(lane_widget.on_remove_pool)
            self.remove_node.connect(lane_widget.on_remove_node)

            lane_widget.lane_id_change_requested.connect(self.on_lane_id_change_requested)
            lane_widget.pool_id_change_requested.connect(self.on_pool_id_change_requested)
            lane_widget.node_id_change_requested.connect(self.on_node_id_change_requested)

            lane_widget.lane_removed.connect(self.on_lane_removed)
            lane_widget.pool_removed.connect(self.on_pool_removed)
            lane_widget.node_removed.connect(self.on_node_removed)

    def signals_and_slots(self):
        pass

    def on_lane_id_change_requested(self, old_lane_id, new_lane_id):
        print('.' * 4, type(self).__name__, 'lane_id_change_requested', old_lane_id, '-->', new_lane_id)
        self.lane_id_change_requested.emit(old_lane_id, new_lane_id)

    def on_pool_id_change_requested(self, old_pool_id, new_pool_id):
        print('.' * 4, type(self).__name__, 'pool_id_change_requested', old_pool_id, '-->', new_pool_id)
        self.pool_id_change_requested.emit(old_pool_id, new_pool_id)

    def on_node_id_change_requested(self, old_node_id, new_node_id):
        print('.' * 4, type(self).__name__, 'node_id_change_requested', old_node_id, '-->', new_node_id)
        self.node_id_change_requested.emit(old_node_id, new_node_id)

    def on_bpmn_id_change_done(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
        self.bpmn_id_change_done.emit(old_bpmn_id, new_bpmn_id)

    def on_lane_id_change_done(self, old_lane_id, new_lane_id):
        old_keys = list(self.bpmn_lanes.keys())
        new_keys = [new_lane_id if k == old_lane_id else k for k in old_keys]

        self.bpmn_data['lanes'] = dict(zip(new_keys, self.bpmn_lanes.values()))
        self.bpmn_lanes = self.bpmn_data['lanes']
        # print(list(self.bpmn_lanes.keys()))

        print('.' * 4, type(self).__name__, 'lane_id_change_done', old_lane_id, '-->', new_lane_id)
        self.lane_id_change_done.emit(old_lane_id, new_lane_id)

    def on_pool_id_change_done(self, old_pool_id, new_pool_id):
        print('.' * 4, type(self).__name__, 'pool_id_change_done', old_pool_id, '-->', new_pool_id)
        self.pool_id_change_done.emit(old_pool_id, new_pool_id)

    def on_node_id_change_done(self, old_node_id, new_node_id):
        print('.' * 4, type(self).__name__, 'node_id_change_done', old_node_id, '-->', new_node_id)
        self.node_id_change_done.emit(old_node_id, new_node_id)

    def on_lane_removed(self, lane_id):
        print('.' * 4, type(self).__name__, 'lane_removed', lane_id)
        self.lane_removed.emit(lane_id)

    def on_remove_lane(self, lane_id):
        print('.' * 4, type(self).__name__, 'remove_lane', lane_id)
        self.remove_lane.emit(lane_id)

    def on_pool_removed(self, pool_id):
        print('.' * 4, type(self).__name__, 'pool_removed', pool_id)
        self.pool_removed.emit(pool_id)

    def on_remove_pool(self, pool_id):
        print('.' * 4, type(self).__name__, 'remove_pool', pool_id)
        self.remove_pool.emit(pool_id)

    def on_node_removed(self, node_id):
        print('.' * 4, type(self).__name__, 'node_removed', node_id)
        self.node_removed.emit(node_id)

    def on_remove_node(self, node_id):
        print('.' * 4, type(self).__name__, 'remove_node', node_id)
        self.remove_node.emit(node_id)
