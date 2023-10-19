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

from qt.schema.pool_editor import PoolEditor

class LanePools(CollapsibleFrame):

    pool_id_change_requested = pyqtSignal(str, str)
    node_id_change_requested = pyqtSignal(str, str)

    pool_removed = pyqtSignal(str)

    node_removed = pyqtSignal(str)
    remove_node = pyqtSignal(str)

    bpmn_id_change_done = pyqtSignal(str, str)
    lane_id_change_done = pyqtSignal(str, str)
    pool_id_change_done = pyqtSignal(str, str)
    node_id_change_done = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, lane_id, parent=None):
        super().__init__(icon='pools', text='Lane Pools', parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040";')

        self.bpmn_data, self.bpmn_id, self.lane_id = bpmn_data, bpmn_id, lane_id
        self.lane_pools = self.bpmn_data['lanes'][self.lane_id]['pools']

        self.init_ui()
        self.signals_and_slots()
        self.populate()

    def init_ui(self):
        self.warning_widget = None

        # *add* button to add a new pool
        self.add_new_pool = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['new-pool'])
        self.add_new_pool.setIcon(QIcon(pixmap))

        self.add_new_pool.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.add_new_pool.setStyleSheet('font-size: 9px; border: 0px; background-color: #B0B0B0')

        self.add_button(self.add_new_pool, 'new-lane-pool')

    def populate(self, focus_on_pool=None, pools_to_expand=[]):
        # first clear the layout with all pools
        self.clearContent()

        self.num_pools = len(self.lane_pools)
        index = 0
        for pool_id, pool_data in self.lane_pools.items():
            pool_widget = PoolEditor(self.bpmn_data, self.bpmn_id, self.lane_id, pool_id, index, self.num_pools, self)
            pool_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(pool_widget)

            pool_widget.new_pool.connect(self.on_new_pool)
            pool_widget.remove_pool.connect(self.on_remove_pool)
            pool_widget.pool_order_changed.connect(self.on_pool_order_changed)

            self.bpmn_id_change_done.connect(pool_widget.on_bpmn_id_change_done)
            self.lane_id_change_done.connect(pool_widget.on_lane_id_change_done)
            self.pool_id_change_done.connect(pool_widget.on_pool_id_change_done)
            self.node_id_change_done.connect(pool_widget.on_node_id_change_done)

            self.remove_node.connect(pool_widget.on_remove_node)

            pool_widget.pool_id_change_requested.connect(self.on_pool_id_change_requested)
            pool_widget.node_id_change_requested.connect(self.on_node_id_change_requested)

            pool_widget.node_removed.connect(self.on_node_removed)

            index = index + 1

            if pool_id in pools_to_expand:
                pool_widget.expand()

            if focus_on_pool and focus_on_pool == pool_id:
                pool_widget.expand()

    def signals_and_slots(self):
        self.add_new_pool.clicked.connect(self.on_new_pool)

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

    def on_node_removed(self, node_id):
        # emit node_removed to parent
        print('.' * 12, type(self).__name__, 'node_removed', node_id)
        self.node_removed.emit(node_id)

    def on_remove_node(self, node_id):
        print('.' * 12, type(self).__name__, 'remove_node', node_id)
        self.remove_node.emit(node_id)

    def on_new_pool(self, index=0):
        old_keys = list(self.lane_pools.keys())

        new_pool_object = copy.deepcopy(NEW_POOL)
        # generate a unique pool key
        new_pool_key = 'new_pool_' + random_string(length=5)

        if index != 0:
            new_dict1 = dict(zip(old_keys[0:index], list(self.lane_pools.values())[0:index]))
        else:
            new_dict1 = {}

        new_dict1[new_pool_key] = new_pool_object
        new_dict2 = dict(zip(old_keys[index:], list(self.lane_pools.values())[index:]))

        self.bpmn_data['lanes'][self.lane_id]['pools'] = {**new_dict1, **new_dict2}
        self.lane_pools = self.bpmn_data['lanes'][self.lane_id]['pools']

        # now populate again
        self.populate(focus_on_pool=new_pool_key)

    def on_remove_pool(self, index):
        pools_to_expand = self.pools_expanded()

        # remove the pool from bpmn_data
        key_to_remove = list(self.lane_pools.keys())[index]
        self.bpmn_data['lanes'][self.lane_id]['pools'].pop(key_to_remove)
        self.lane_pools = self.bpmn_data['lanes'][self.lane_id]['pools']

        # now populate again
        self.populate(pools_to_expand=pools_to_expand)

        # emit pool_removed to parent
        self.pool_removed.emit(key_to_remove)

    def on_pool_order_changed(self, index, direction):
        if self.num_pools <= 1:
            return

        if index == 0 and direction == 'up':
            return

        if index == self.num_pools - 1 and direction == 'down':
            return

        pools_to_expand = self.pools_expanded()

        # swap pools
        keys = list(self.lane_pools.keys())
        vals = list(self.lane_pools.values())
        if direction == 'up':
            keys[index], keys[index - 1] = keys[index - 1], keys[index]
            vals[index], vals[index - 1] = vals[index - 1], vals[index]
        elif direction == 'down':
            keys[index], keys[index + 1] = keys[index + 1], keys[index]
            vals[index], vals[index + 1] = vals[index + 1], vals[index]

        self.bpmn_data['lanes'][self.lane_id]['pools'] = dict(zip(keys, vals))
        self.lane_pools = self.bpmn_data['lanes'][self.lane_id]['pools']

        self.populate(pools_to_expand=pools_to_expand)

    def pools_expanded(self):
        return []
