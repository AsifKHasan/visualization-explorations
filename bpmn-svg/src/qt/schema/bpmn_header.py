#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

class BpmnHeader(CollapsibleFrame):
    def __init__(self, bpmn_id, bpmn_data, parent=None):
        super().__init__(icon='bpmn', text='BPMN id: {0}'.format(bpmn_id), parent=parent)
        self.bpmn_id, self.bpmn_data = bpmn_id, bpmn_data
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#D8D8D8"; color: "#404040"; font-size: 9pt;')
        self.populate()
        self.signals_and_slots()

    def populate(self):
        # debug('BpmnHeader: {0}'.format(self.bpmn_id))

        content = QWidget()
        self.content_layout = QGridLayout(content)

        # bpmn id
        self.id_label = QLabel("Id:")
        self.id_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.id = QLineEdit()
        self.id.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.id_label, 0, 0)
        self.content_layout.addWidget(self.id, 0, 1)

        # bpmn label
        self.label_label = QLabel("Label:")
        self.label_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label = QLineEdit()
        self.label.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.label_label, 1, 0)
        self.content_layout.addWidget(self.label, 1, 1, 1, 3)

        # hide_labels
        self.hide_labels_label = QLabel("Hide labels:")
        self.hide_labels_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.hide_labels = QCheckBox()
        # self.hide_label.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.hide_labels_label, 2, 0)
        self.content_layout.addWidget(self.hide_labels, 2, 1)

        self.addWidget(content)

        self.id.setText(self.bpmn_id)
        self.label.setText(self.bpmn_data['label'])

        # hide_labels
        if self.bpmn_data['styles'].get('hide_labels', '') == 'true':
            self.hide_labels.setChecked(True)
        else:
            self.hide_labels.setChecked(False)

        for c in range(0, self.content_layout.columnCount()):
            self.content_layout.setColumnStretch(c, 1)

    def signals_and_slots(self):
        self.id.editingFinished.connect(self.on_id_edited)
        self.label.editingFinished.connect(self.on_label_edited)
        self.hide_labels.stateChanged.connect(self.on_hide_labels_changed)

    def on_id_edited(self):
        pass

    def on_label_edited(self):
        self.bpmn_data['label'] = self.label.text()

    def on_hide_labels_changed(self):
        if self.hide_labels.isChecked():
            self.bpmn_data['styles']['hide_labels'] = 'true'
        else:
            self.bpmn_data['styles']['hide_labels'] = 'false'
