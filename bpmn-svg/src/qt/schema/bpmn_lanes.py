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

        self.init_ui()
        self.populate()
        self.signals_and_slots()

    def init_ui(self):
        self.warning_widget = None

        # *add* button to add a new lane
        self.add_new_lane = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['new-lane'])
        self.add_new_lane.setIcon(QIcon(pixmap))

        self.add_new_lane.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.add_new_lane.setStyleSheet('font-size: 9px; border: 0px; background-color: #B0B0B0')

        self.add_button(self.add_new_lane, 'new-bpmn-lane')

    def populate(self, focus_on_lane=None, lanes_to_expand=[]):
        # first clear the layout with all lanes
        self.clearContent()

        self.num_lanes = len(self.bpmn_lanes)
        index = 0
        for lane_id, lane_data in self.bpmn_lanes.items():
            lane_widget = LaneEditor(self.bpmn_data, self.bpmn_id, lane_id, index, self.num_lanes, self)
            lane_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(lane_widget)

            lane_widget.new_lane.connect(self.on_new_lane)
            lane_widget.remove_lane.connect(self.on_remove_lane)
            lane_widget.lane_order_changed.connect(self.on_lane_order_changed)

            self.bpmn_id_change_done.connect(lane_widget.on_bpmn_id_change_done)
            self.lane_id_change_done.connect(lane_widget.on_lane_id_change_done)
            self.pool_id_change_done.connect(lane_widget.on_pool_id_change_done)
            self.node_id_change_done.connect(lane_widget.on_node_id_change_done)

            self.remove_pool.connect(lane_widget.on_remove_pool)
            self.remove_node.connect(lane_widget.on_remove_node)

            lane_widget.lane_id_change_requested.connect(self.on_lane_id_change_requested)
            lane_widget.pool_id_change_requested.connect(self.on_pool_id_change_requested)
            lane_widget.node_id_change_requested.connect(self.on_node_id_change_requested)

            lane_widget.pool_removed.connect(self.on_pool_removed)
            lane_widget.node_removed.connect(self.on_node_removed)

            index = index + 1

            if lane_id in lanes_to_expand:
                lane_widget.expand()

            if focus_on_lane and focus_on_lane == lane_id:
                lane_widget.expand()

    def signals_and_slots(self):
        self.add_new_lane.clicked.connect(self.on_new_lane)

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

    def on_new_lane(self, index=0):
        old_keys = list(self.bpmn_lanes.keys())

        new_lane_object = copy.deepcopy(NEW_LANE)
        # generate a unique lane key
        new_lane_key = 'new_lane_' + random_string(length=5)

        if index != 0:
            new_dict1 = dict(zip(old_keys[0:index], list(self.bpmn_lanes.values())[0:index]))
        else:
            new_dict1 = {}

        new_dict1[new_lane_key] = new_lane_object
        new_dict2 = dict(zip(old_keys[index:], list(self.bpmn_lanes.values())[index:]))

        self.bpmn_data['lanes'] = {**new_dict1, **new_dict2}
        self.bpmn_lanes = self.bpmn_data['lanes']

        # now populate again
        self.populate(focus_on_lane=new_lane_key)

    def on_remove_lane(self, index):
        lanes_to_expand = self.lanes_expanded()

        # remove the lane from bpmn_data
        key_to_remove = list(self.bpmn_lanes.keys())[index]
        self.bpmn_data['lanes'].pop(key_to_remove)
        self.lane_lanes = self.bpmn_data['lanes']

        # now populate again
        self.populate(lanes_to_expand=lanes_to_expand)

        # emit lane_removed to parent
        self.lane_removed.emit(key_to_remove)

    def on_lane_order_changed(self, index, direction):
        if self.num_lanes <= 1:
            return

        if index == 0 and direction == 'up':
            return

        if index == self.num_lanes - 1 and direction == 'down':
            return

        lanes_to_expand = self.lanes_expanded()

        # swap lanes
        keys = list(self.bpmn_lanes.keys())
        vals = list(self.bpmn_lanes.values())
        if direction == 'up':
            keys[index], keys[index - 1] = keys[index - 1], keys[index]
            vals[index], vals[index - 1] = vals[index - 1], vals[index]
        elif direction == 'down':
            keys[index], keys[index + 1] = keys[index + 1], keys[index]
            vals[index], vals[index + 1] = vals[index + 1], vals[index]

        self.bpmn_data['lanes'] = dict(zip(keys, vals))
        self.bpmn_lanes = self.bpmn_data['lanes']

        self.populate(lanes_to_expand=lanes_to_expand)

    def lanes_expanded(self):
        return []
