#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

class NodeEditor(CollapsibleFrame):
    def __init__(self, bpmn_data, bpmn_id, lane_id, pool_id, node_id, parent=None):
        self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id, self.node_id  = bpmn_data, bpmn_id, lane_id, pool_id, node_id
        self.node_data = self.bpmn_data['lanes'][lane_id]['pools'][pool_id]['nodes'][node_id]

        super().__init__(icon=self.node_data['type'], text='NODE id: {0}'.format(self.node_id), parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#D8D8D8"; color: "#404040"; font-size: 9pt;')

        self.init_ui()
        self.signals_and_slots()

        self.populate()

    def init_ui(self):
        content = QWidget()
        self.content_layout = QGridLayout(content)

        # node id
        self.id_label = QLabel("Id:")
        self.id_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.id = QLineEdit()
        self.id.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.id_label, 0, 0)
        self.content_layout.addWidget(self.id, 0, 1)

        reg_ex = QRegExp("[_a-zA-Z][_0-9a-zA-Z]*")
        input_validator = QtGui.QRegExpValidator(reg_ex, self)
        self.id.setValidator(input_validator)

        # node type
        self.type_label = QLabel("Type:")
        self.type_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.type = QPushButton()
        self.type.setStyleSheet('border: 1px solid grey; background-color: "#D8D8D8"')
        self.content_layout.addWidget(self.type_label, 0, 2)
        self.content_layout.addWidget(self.type, 0, 3)

        # node label
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

        # label_pos
        self.label_pos_label = QLabel("Label position:")
        self.label_pos_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_pos = QComboBox()
        self.label_pos.addItems(['', 'top', 'middle', 'bottom', 'none'])
        self.label_pos.setStyleSheet('border: 1px solid grey; background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.label_pos_label, 2, 2)
        self.content_layout.addWidget(self.label_pos, 2, 3)

        # wrap_here
        self.wrap_here_label = QLabel("Wrap here:")
        self.wrap_here_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.wrap_here = QCheckBox()
        # self.wrap_here.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.wrap_here.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.wrap_here_label, 3, 0)
        self.content_layout.addWidget(self.wrap_here, 3, 1)

        # move_x
        self.move_x_label = QLabel("Horizontally move:")
        self.move_x_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.move_x = QSpinBox()
        self.move_x.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.move_x.setSuffix('px')
        self.move_x.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.move_x_label, 3, 2)
        self.content_layout.addWidget(self.move_x, 3, 3)

        self.addWidget(content)

        for c in range(0, self.content_layout.columnCount()):
            self.content_layout.setColumnStretch(c, 1)

    def populate(self):
        self.id.setText(self.node_id)
        self.type.setText(self.node_data['type'])
        self.label.setText(self.node_data['label'])

        # hide_label
        self.hide_label.setChecked(self.node_data['styles'].get('hide_label', '') == 'true')

        # label_pos
        self.label_pos.setCurrentText(self.node_data['styles'].get('label_pos', ''))

        # wrap_here
        self.wrap_here.setChecked(self.node_data['styles'].get('wrap_here', '') == 'true')

        # move_x
        self.move_x = self.node_data['styles'].get('move_x', 0)

    def signals_and_slots(self):
        pass

    def on_bpmn_id_changed(self, bpmn_id):
        self.bpmn_id = bpmn_id
        # print(type(self).__name__, self.lane_id, self.pool_id, self.node_id, 'bpmn_id_changed')
