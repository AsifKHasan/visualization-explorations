#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

class LaneHeader(CollapsibleFrame):
    def __init__(self, bpmn_id, lane_id, lane_data, parent=None):
        super().__init__(icon='lane', text='Lane id: {0}'.format(lane_id), parent=parent)
        self.bpmn_id, self.lane_id, self.lane_data = bpmn_id, lane_id, lane_data
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040"; font-size: 9pt;')
        self.populate()
        self.signals_and_slots()

    def populate(self):
        # debug('LaneHeader: {0}'.format(self.lane_id))

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

        self.id.setText(self.lane_id)
        self.title.setText(self.lane_data['label'])
        if self.lane_data['styles'].get('hide_label', '') == 'true':
            self.hide_label.setChecked(True)
        else:
            self.hide_label.setChecked(False)

    def signals_and_slots(self):
        self.id.editingFinished.connect(self.on_id_edited)
        self.title.editingFinished.connect(self.on_title_edited)
        self.hide_label.stateChanged.connect(self.on_hide_label_changed)

    def on_id_edited(self):
        pass

    def on_title_edited(self):
        self.bpmn_data['label'] = self.title.text()

    def on_hide_label_changed(self):
        if self.hide_label.isChecked():
            self.bpmn_data['styles']['hide_label'] = 'true'
        else:
            self.bpmn_data['styles']['hide_label'] = 'false'
