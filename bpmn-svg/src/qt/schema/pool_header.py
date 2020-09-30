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
    def __init__(self, bpmn_data, bpmn_id, lane_id, pool_id, parent=None):
        super().__init__(icon='pool', text='Pool id: {0}'.format(pool_id), parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040"; font-size: 9pt;')

        self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id = bpmn_data, bpmn_id, lane_id, pool_id
        self.pool_data = self.bpmn_data['lanes'][lane_id]['pools'][pool_id]

        self.init_ui()
        self.signals_and_slots()

        self.populate()

    def init_ui(self):
        content = QWidget()
        self.content_layout = QGridLayout(content)

        # pool id
        self.id_label = QLabel("Id:")
        self.id_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.id = QLineEdit()
        self.id.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.id_label, 0, 0)
        self.content_layout.addWidget(self.id, 0, 1)

        reg_ex = QRegExp("[_a-zA-Z][_0-9a-zA-Z]*")
        input_validator = QtGui.QRegExpValidator(reg_ex, self)
        self.id.setValidator(input_validator)

        # pool label
        self.label_label = QLabel("Label:")
        self.label_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label = QLineEdit()
        self.label.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.label_label, 1, 0)
        self.content_layout.addWidget(self.label, 1, 1, 1, 3)

        # hide_label
        self.hide_label_label = QLabel("Hide labels:")
        self.hide_label_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.hide_label = QCheckBox()
        # self.hide_label.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.hide_label_label, 2, 0)
        self.content_layout.addWidget(self.hide_label, 2, 1)

        # move_x
        self.move_x_label = QLabel("Horizontally move:")
        self.move_x_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.move_x = QSpinBox()
        self.move_x.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.move_x.setSuffix('px')
        self.move_x.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.move_x_label, 3, 0)
        self.content_layout.addWidget(self.move_x, 3, 1)

        self.addWidget(content)

        for c in range(0, self.content_layout.columnCount()):
            self.content_layout.setColumnStretch(c, 1)

    def populate(self):
        self.id.setText(self.pool_id)
        self.label.setText(self.pool_data['label'])

        # hide_label
        self.hide_label.setChecked(self.pool_data['styles'].get('hide_label', '') == 'true')

        # move_x
        self.move_x = self.pool_data['styles'].get('move_x', 0)

    def signals_and_slots(self):
        self.id.editingFinished.connect(self.on_id_edited)
        self.label.editingFinished.connect(self.on_label_edited)
        self.hide_label.stateChanged.connect(self.on_hide_label_changed)

    def on_id_edited(self):
        pass

    def on_label_edited(self):
        self.pool_data['label'] = self.label.text()

    def on_hide_label_changed(self):
        if self.hide_label.isChecked():
            self.pool_data['styles']['hide_label'] = 'true'
        else:
            self.pool_data['styles']['hide_label'] = 'false'

    def on_bpmn_id_changed(self, bpmn_id):
        self.bpmn_id = bpmn_id
        # print(type(self).__name__, self.lane_id, self.pool_id, 'bpmn_id_changed')
