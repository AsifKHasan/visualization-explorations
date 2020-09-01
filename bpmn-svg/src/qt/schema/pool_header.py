#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

class PoolHeader(CollapsibleFrame):
    def __init__(self, bpmn_id, lane_id, pool_id, pool_data, parent=None):
        super().__init__(text='Pool id: {0}'.format(pool_id), parent=parent)
        self.bpmn_id, self.lane_id, self.pool_id, self.pool_data = bpmn_id, lane_id, pool_id, pool_data
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040"; font-size: 9pt;')
        self.populate()

    def populate(self):
        debug('PoolHeader: {0}'.format(self.pool_id))

        content = QWidget()
        self.content_layout = QFormLayout(content)

        # Bpmn id
        self.id = QLineEdit()
        self.id.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addRow(QLabel("Id:"), self.id)

        # Bpmn title
        self.title = QLineEdit()
        self.title.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addRow(QLabel("Title:"), self.title)

        # styles
        self.hide_label = QCheckBox()
        self.content_layout.addRow(QLabel("Hide label:"), self.hide_label)

        self.addWidget(content)

        self.id.setText(self.pool_id)
        self.title.setText(self.pool_data['label'])
        if self.pool_data['styles'].get('hide_label', '') == 'true':
            self.hide_label.setChecked(True)
        else:
            self.hide_label.setChecked(False)


class PoolHeader1(CollapsibleBox):
    def __init__(self, bpmn_id, lane_id, pool_id, pool_data, parent=None):
        super().__init__(text='Pool id: {0}'.format(pool_id), parent=parent)
        self.bpmn_id, self.lane_id, self.pool_id, self.pool_data = bpmn_id, lane_id, pool_id, pool_data
        self.content_area.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')
        self.populate()

    def populate(self):
        debug('PoolHeader: {0}'.format(self.pool_id))
        self.content_layout = QFormLayout()

        # Bpmn id
        self.id = QLineEdit()
        self.id.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addRow(QLabel("Id:"), self.id)

        # Bpmn title
        self.title = QLineEdit()
        self.title.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addRow(QLabel("Title:"), self.title)

        # styles
        self.hide_label = QCheckBox()
        self.content_layout.addRow(QLabel("Hide label:"), self.hide_label)

        self.setContentLayout(self.content_layout)

        self.id.setText(self.pool_id)
        self.title.setText(self.pool_data['label'])
        if self.pool_data['styles'].get('hide_label', '') == 'true':
            self.hide_label.setChecked(True)
        else:
            self.hide_label.setChecked(False)
