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

    bpmn_id_changed = pyqtSignal(str, str)
    lane_id_changed = pyqtSignal(str, str)

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
            self.bpmn_id_changed.connect(pool_widget.update_bpmn_id)
            self.lane_id_changed.connect(pool_widget.update_lane_id)

    def update_bpmn_id(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
        # print(type(self).__name__, self.lane_id, 'bpmn_id_changed')
        self.bpmn_id_changed.emit(old_bpmn_id, new_bpmn_id)

    def update_lane_id(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id
            self.lane_pools = self.bpmn_data['lanes'][self.lane_id]['pools']

            print(type(self).__name__, self.lane_id, 'lane_id_changed')
            self.lane_id_changed.emit(old_lane_id, new_lane_id)
