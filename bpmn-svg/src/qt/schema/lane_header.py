#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

class LaneHeader(CollapsibleBox):
    def __init__(self, bpmn_id, lane_id, lane_data, parent=None):
        super().__init__(text='Lane id: {0}'.format(lane_id), parent=parent)
        self.bpmn_id, self.lane_id, self.lane_data = bpmn_id, lane_id, lane_data

        self.content_area.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')

        self.populate()

    def populate(self):
        debug('LaneHeader: {0}'.format(self.lane_id))
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

        self.id.setText(self.lane_id)
        self.title.setText(self.lane_data['label'])
        if self.lane_data['styles'].get('hide_label', '') == 'true':
            self.hide_label.setChecked(True)
        else:
            self.hide_label.setChecked(False)
