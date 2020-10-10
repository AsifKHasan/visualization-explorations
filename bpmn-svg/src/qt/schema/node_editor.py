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

    node_id_change_requested = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, lane_id, pool_id, node_id, parent=None):
        self.bpmn_data, self.bpmn_id, self.lane_id, self.pool_id, self.node_id  = bpmn_data, bpmn_id, lane_id, pool_id, node_id

        self.node_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes'][self.node_id]

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

        # node_type
        self.type = QPushButton()
        # self.type.setStyleSheet('border: 1px solid grey; background-color: "#D8D8D8"')
        self.content_layout.addWidget(self.type_label, 0, 2)
        self.content_layout.addWidget(self.type, 0, 3)

        # node label
        self.label_label = QLabel("Label:")
        self.label_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label = QLineEdit()
        self.label.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.label_label, 1, 0)
        self.content_layout.addWidget(self.label, 1, 1, 1, 3)

        # label_pos
        self.label_pos_label = QLabel("Label position:")
        self.label_pos_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_pos = QComboBox()
        self.label_pos.addItems(['', 'top', 'middle', 'bottom', 'none'])
        self.label_pos.setStyleSheet('border: 1px solid grey; background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.label_pos_label, 2, 0)
        self.content_layout.addWidget(self.label_pos, 2, 1)

        # wrap_here
        self.wrap_here_label = QLabel("Wrap here:")
        self.wrap_here_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.wrap_here = QCheckBox()
        # self.wrap_here.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.wrap_here.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.wrap_here_label, 2, 2)
        self.content_layout.addWidget(self.wrap_here, 2, 3)

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
        self.id.setText(self.node_id)

        if self.node_data['type']:
            pixmap = QPixmap(ICONS[self.node_data['type']])
            # pixmap = pixmap.scaledToHeight(24)
            self.type.setIcon(QIcon(pixmap))

        self.label.setText(self.node_data['label'])

        # label_pos
        self.label_pos.setCurrentText(self.node_data['styles'].get('label_pos', ''))

        # wrap_here
        self.wrap_here.setChecked(self.node_data['styles'].get('wrap_here', '') == 'true')

        # move_x
        self.move_x = self.node_data['styles'].get('move_x', 0)

    def signals_and_slots(self):
        self.id.editingFinished.connect(self.on_id_edited)
        self.type.clicked.connect(self.on_selection_dialog)
        self.label.editingFinished.connect(self.on_label_edited)
        self.label_pos.currentTextChanged.connect(self.on_label_pos_changed)
        self.wrap_here.stateChanged.connect(self.on_wrap_here_changed)
        self.move_x.valueChanged.connect(self.on_move_x_changed)

    def on_bpmn_id_change_done(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id

    def on_lane_id_change_done(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id
            self.node_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes'][self.node_id]

            print('.' * 24, type(self).__name__, 'lane_id_change_done', old_lane_id, '-->', new_lane_id)

    def on_pool_id_change_done(self, old_pool_id, new_pool_id):
        if self.pool_id == old_pool_id:
            self.pool_id = new_pool_id
            self.node_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes'][self.node_id]

            print('.' * 24, type(self).__name__, 'pool_id_change_done', old_pool_id, '-->', new_pool_id)

    def on_node_id_change_done(self, old_node_id, new_node_id):
        if self.node_id == old_node_id:
            self.node_id = new_node_id
            self.node_data = self.bpmn_data['lanes'][self.lane_id]['pools'][self.pool_id]['nodes'][self.node_id]

            print('.' * 24, type(self).__name__, 'node_id_change_done', old_node_id, '-->', new_node_id)

    def on_id_edited(self):
        print('.' * 24, type(self).__name__, 'node_id_change_requested', self.node_id, '-->', self.id.text())
        self.node_id_change_requested.emit(self.node_id, self.id.text())

    def on_type_edited(self):
        self.node_data['type'] = self.type.text()

    def on_label_edited(self):
        self.node_data['label'] = self.label.text()

    def on_label_pos_changed(self):
        self.node_data['styles']['label_pos'] = self.label_pos.currentText()

    def on_wrap_here_changed(self):
        if self.wrap_here.isChecked():
            self.node_data['styles']['wrap_here'] = 'true'
        else:
            self.node_data['styles']['wrap_here'] = 'false'

    def on_move_x_changed(self, v):
        # self.move_x = v
        self.node_data['styles']['move_x'] = v

    def on_selection_dialog(self):
        node_type = TypeSelectionDialog.open(self, self.node_data['type'])
        if node_type and node_type != self.node_data['type']:
            # print('Node Type changed {0} --> {1}'.format(self.node_data['type'], node_type))
            self.node_data['type'] = node_type
            pixmap = QPixmap(ICONS[self.node_data['type']])
            # pixmap = pixmap.scaledToHeight(24)
            self.type.setIcon(QIcon(pixmap))
            self.update_title()

    def update_title(self):
        self.change_title(icon=self.node_data['type'], text='NODE id: {0}'.format(self.node_id), err=False)


class TypeSelectionDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setWindowTitle('Type selection')
        self.setMinimumSize(400, 500)
        self.setWindowFlags(QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint)

        self.selected_type = None

        self.init_ui()
        self.signals_and_slots()

    def init_ui(self):
        layout = QVBoxLayout()

        # the node tree
        self.node_tree = QTreeWidget(self)
        self.node_tree.setStyleSheet('background-color: "#F8F8F8"')
        self.node_tree.setHeaderHidden(True)
        layout.addWidget(self.node_tree)

        # the select button
        self.select = QPushButton('Select type')
        # self.select.setStyleSheet('background-color: "#D8D8D8"')
        self.select.setStyleSheet('QPushButton:disabled {background-color:#E8E8E8;}')
        self.select.setEnabled(False)
        layout.addWidget(self.select)

        self.setLayout(layout)

    def init_tree(self):
        # populate the tree
        for group, item in NODE_TYPES.items():
            group_object = QTreeWidgetItem(self.node_tree, 0)
            group_object.setText(0, group)

            # item may be a list or another dict (group)
            if isinstance(item, dict):
                # it is another group
                for subgroup, subitem in item.items():
                    subgroup_object = QTreeWidgetItem(group_object, 0)
                    subgroup_object.setText(0, subgroup)

                    # the subgroup is a list
                    for node_type in subitem:
                        type_item = QTreeWidgetItem(subgroup_object, 1)
                        type_item.setText(0, node_type)
                        pixmap = QPixmap(ICONS[node_type])
                        # pixmap = pixmap.scaledToHeight(24)
                        type_item.setIcon(0, QIcon(pixmap))

                        if self.selected_type and node_type == self.selected_type:
                            self.node_tree.setCurrentItem(type_item)
            else:
                # it is a list of types
                for node_type in item:
                    type_item = QTreeWidgetItem(group_object, 1)
                    type_item.setText(0, node_type)
                    pixmap = QPixmap(ICONS[node_type])
                    # pixmap = pixmap.scaledToHeight(24)
                    type_item.setIcon(0, QIcon(pixmap))

                    if self.selected_type and node_type == self.selected_type:
                        self.node_tree.setCurrentItem(type_item)

    def signals_and_slots(self):
        self.select.clicked.connect(self.on_accept)
        self.node_tree.currentItemChanged.connect(self.on_current_item_change)

    def on_current_item_change(self, current, previous):
        if current.type() == 1:
            # print(current.text(0))
            self.select.setEnabled(True)
        else:
            self.select.setEnabled(False)

    def on_accept(self):
        selected_type_item = self.node_tree.currentItem()
        if selected_type_item:
            self.selected_type = selected_type_item.text(0)
        else:
            self.selected_type = None

        self.accept()

    @staticmethod
    def open(parent, node_type):

        dialog = TypeSelectionDialog(parent)
        dialog.parent, dialog.selected_type = parent, node_type
        dialog.init_tree()

        result = dialog.exec_()

        if result == QDialog.Accepted:
            return dialog.selected_type
        else:
            return None
