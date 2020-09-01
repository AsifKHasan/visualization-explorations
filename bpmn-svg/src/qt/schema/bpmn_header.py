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
        super().__init__(text='BPMN id: {0}'.format(bpmn_id), parent=parent)
        self.bpmn_id, self.bpmn_data = bpmn_id, bpmn_data
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#D8D8D8"; color: "#404040"; font-size: 9pt;')
        self.populate()

    def populate(self):
        debug('BpmnHeader: {0}'.format(self.bpmn_id))

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
        self.hide_labels = QCheckBox()
        self.content_layout.addRow(QLabel("Hide labels:"), self.hide_labels)

        self.addWidget(content)

        self.id.setText(self.bpmn_id)
        self.title.setText(self.bpmn_data['label'])
        if self.bpmn_data['styles'].get('hide_labels', '') == 'true':
            self.hide_labels.setChecked(True)
        else:
            self.hide_labels.setChecked(False)


class BpmnHeader1(CollapsibleBox):
    def __init__(self, bpmn_id, bpmn_data, parent=None):
        super().__init__(text='BPMN id: {0}'.format(bpmn_id), parent=parent)
        self.bpmn_id, self.bpmn_data = bpmn_id, bpmn_data
        self.content_area.setStyleSheet('background-color: "#D0D0D0"; color: "#404040";')
        self.populate()

    def populate(self):
        debug('BpmnHeader: {0}'.format(self.bpmn_id))
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
        self.hide_labels = QCheckBox()
        self.content_layout.addRow(QLabel("Hide labels:"), self.hide_labels)

        self.setContentLayout(self.content_layout)

        self.id.setText(self.bpmn_id)
        self.title.setText(self.bpmn_data['label'])
        if self.bpmn_data['styles'].get('hide_labels', '') == 'true':
            self.hide_labels.setChecked(True)
        else:
            self.hide_labels.setChecked(False)
