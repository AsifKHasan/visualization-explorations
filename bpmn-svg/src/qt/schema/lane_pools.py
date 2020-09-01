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
    def __init__(self, bpmn_id, lane_id, lane_pools, parent=None):
        super().__init__(text='Lane Pools', parent=parent)
        self.bpmn_id, self.lane_id, self.lane_pools = bpmn_id, lane_id, lane_pools
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040";')
        self.populate()

    def populate(self):
        debug('LanePools: {0}'.format(self.lane_id))

        for pool_id, pool_data in self.lane_pools.items():
            pool_widget = PoolEditor(self.bpmn_id, self.lane_id, pool_id, pool_data)
            self.addWidget(pool_widget)


class LanePools1(CollapsibleBox):
    def __init__(self, bpmn_id, lane_id, lane_pools, parent=None):
        super().__init__(text='Lane Pools', parent=parent)
        self.bpmn_id, self.lane_id, self.lane_pools = bpmn_id, lane_id, lane_pools

        self.content_area.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')

        self.populate()

    def populate(self):
        debug('LanePools: {0}'.format(self.lane_id))
        self.content_layout = QVBoxLayout()

        for pool_id, pool_data in self.lane_pools.items():
            pool_widget = PoolEditor(self.bpmn_id, self.lane_id, pool_id, pool_data)
            self.content_layout.addWidget(pool_widget)

        self.content_layout.addStretch()
        self.setContentLayout(self.content_layout)
