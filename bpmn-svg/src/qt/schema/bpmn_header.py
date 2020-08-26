#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *

from util.logger import *

class BpmnHeader(QGroupBox):
    def __init__(self, parent=None):
        super(QtWidgets.QGroupBox, self).__init__(parent)
        self.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')
        self.setTitle('Properties')

        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Bpmn id
        self.id = QLineEdit()
        self.id.setStyleSheet('background-color: "#F8F8F8"')
        self.layout.addRow(QLabel("Id:"), self.id)

        # Bpmn title
        self.title = QLineEdit()
        self.title.setStyleSheet('background-color: "#F8F8F8"')
        self.layout.addRow(QLabel("Title:"), self.title)

        # styles
        self.hide_labels = QCheckBox()
        # self.hide_labels.setStyleSheet('background-color: "#F8F8F8"')
        self.layout.addRow(QLabel("Hide labels:"), self.hide_labels)

    def populate(self, bpmn_id, schema):
        self.schema = schema
        self.bpmn_id = bpmn_id
        self.id.setText(self.bpmn_id)
        self.title.setText(self.schema['label'])
        if self.schema['styles'].get('hide_labels', '') == 'true':
            self.hide_labels.setChecked(True)
        else:
            self.hide_labels.setChecked(False)
