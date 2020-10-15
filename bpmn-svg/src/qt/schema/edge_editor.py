#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

class EdgeEditor(CollapsibleFrame):

    new_edge = pyqtSignal(int)
    remove_edge = pyqtSignal(int)
    edge_order_changed = pyqtSignal(int, str)

    def __init__(self, bpmn_data, scope, bpmn_id, lane_id, pool_id, edge_data, index, num_edges, parent=None):
        super().__init__(icon=edge_data['type'], text='{0:<30}\n{1:<30}'.format(edge_data['from'], edge_data['to']), parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040"; border: 1px solid #202020;', content_style='background-color: "#C8C8C8"; color: "#404040"; font-size: 9pt;')

        self.bpmn_data, self.scope, self.bpmn_id, self.lane_id, self.pool_id, self.edge_data, self.index, self.num_edges = bpmn_data, scope, bpmn_id, lane_id, pool_id, edge_data, index, num_edges

        self.init_ui()
        self.signals_and_slots()

        self.populate()

    def init_ui(self):
        # 'up' button
        self.arrow_up = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['arrow-up'])
        self.arrow_up.setIcon(QIcon(pixmap))

        self.arrow_up.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.arrow_up.setStyleSheet('font-size: 9px; border: 0px; background-color: none')

        self.add_button(self.arrow_up, 'arrow-up')

        # 'down' button
        self.arrow_down = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['arrow-down'])
        self.arrow_down.setIcon(QIcon(pixmap))

        self.arrow_down.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.arrow_down.setStyleSheet('font-size: 9px; border: 0px; background-color: none')

        self.add_button(self.arrow_down, 'arrow-down')

        if self.index == 0:
            self.arrow_up.hide()

        if self.index == self.num_edges - 1:
            self.arrow_down.hide()

        # *add* button to add a new edge
        self.add_new_edge = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['new-edge'])
        self.add_new_edge.setIcon(QIcon(pixmap))

        self.add_new_edge.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.add_new_edge.setStyleSheet('font-size: 9px; border: 0px; background-color: #C8C8C8')

        self.add_button(self.add_new_edge, 'new-{0}-edge'.format(self.scope))

        # *remove* button to remove edge
        self.delete_edge = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['remove-edge'])
        self.delete_edge.setIcon(QIcon(pixmap))

        self.delete_edge.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.delete_edge.setStyleSheet('font-size: 9px; border: 0px; background-color: #C8C8C8')

        self.add_button(self.delete_edge, 'remove-{0}-edge'.format(self.scope))


        # the content area
        content = QWidget()
        self.content_layout = QGridLayout(content)

        # from node
        self.from_node = EdgeNodeWidget(self.lane_id, self.pool_id, self.edge_data['from'], self.bpmn_data, scope=self.scope, role='from', parent=self)
        self.content_layout.addWidget(self.from_node, 0, 0, 1, 3)

        # edge_type
        self.edge_type = QComboBox()
        self.edge_type.setView(QListView())
        self.edge_type.setStyleSheet('QListView::item{height: 50px} QWidget{background-color: #F8F8F8}')
        for key in EDGE_MAP:
            pixmap = QPixmap(EDGE_MAP[key])
            pixmap = pixmap.scaledToHeight(50)
            self.edge_type.addItem(QIcon(pixmap), None, key)

        self.edge_type.resize(self.edge_type.sizeHint())
        self.edge_type.setIconSize(QSize(75, 25))

        self.content_layout.addWidget(self.edge_type, 0, 3)

        # to node
        self.to_node = EdgeNodeWidget(self.lane_id, self.pool_id, self.edge_data['to'], self.bpmn_data, scope=self.scope, role='to', parent=self)
        self.content_layout.addWidget(self.to_node, 0, 4, 1, 3)

        # label
        self.label = QLineEdit()
        self.label.setStyleSheet('background-color: "#F8F8F8"')
        self.content_layout.addWidget(self.label, 1, 0, 1, 7)

        # Error
        self.error_label = QLabel()
        self.error_label.setStyleSheet('color: "#F80000"')
        self.content_layout.addWidget(self.error_label, 2, 0, 1, 7)

        self.addWidget(content)

        for c in range(0, self.content_layout.columnCount()):
            self.content_layout.setColumnStretch(c, 1)

    def populate(self):
        # we need to let the to-node know about the from-node
        self.to_node.set_other_node_values(self.from_node.values())

        index = self.edge_type.findData(self.edge_data['type'])
        if index != -1:
            self.edge_type.setCurrentIndex(index);

        if self.edge_data['label'] != '':
            self.label.setText(self.edge_data['label'])
        else:
            self.label.setPlaceholderText('label')

        # self.update_error()
        self.update_title()

    def update_error(self):
        self.err = False

        from_node_lane, from_node_pool, from_node_id, from_node_type = self.from_node.values()
        to_node_lane, to_node_pool, to_node_id, to_node_type = self.to_node.values()


        if from_node_id is None or from_node_id in ['', '__UNDEFINED__']:
            self.err = True
            self.err_msg = 'from node is UNDEFINED'

        elif to_node_id is None or to_node_id in ['', '__UNDEFINED__']:
            self.err = True
            self.err_msg = 'to node is UNDEFINED'

        # to and from nade are same
        elif from_node_id == to_node_id:
            self.err = True
            self.err_msg = 'from node and to node are same, it is not allowed'

        # for 'bpmn' scope, the to node must be in a different lane than from node
        elif self.scope == 'bpmn':
            if from_node_lane == to_node_lane:
                self.err = True
                self.err_msg = 'from node and to node are from the same lane, not allowed for BPMN level edges'

        # for 'lane' scope, the to node must be from a different pool but the same lane of from node
        elif self.scope == 'lane':
            if from_node_lane != to_node_lane:
                self.err = True
                self.err_msg = 'from node and to node are from different lanes, not allowed for LANE level edges'
            elif from_node_pool == to_node_pool:
                self.err = True
                self.err_msg = 'from node and to node are from same pool of the specified lane, not allowed for LANE level edges'

        # for 'pool' scope, the to node must be from a same pool of the same lane of from node
        elif self.scope == 'pool':
            if from_node_lane != to_node_lane:
                self.err = True
                self.err_msg = 'from node and to node are from different lanes, not allowed for POOL level edges'
            elif from_node_pool != to_node_pool:
                self.err = True
                self.err_msg = 'from node and to node are from different pools of the specified lane, not allowed for POOL level edges'

        if self.err:
            self.error_label.setText(self.err_msg)
            self.error_label.show()
        else:
            self.error_label.hide()

    def signals_and_slots(self):
        self.add_new_edge.clicked.connect(self.on_new_edge)
        self.delete_edge.clicked.connect(self.on_remove_edge)

        self.arrow_down.clicked.connect(self.on_arrow_down)
        self.arrow_up.clicked.connect(self.on_arrow_up)

        self.from_node.nodeChanged.connect(self.on_from_node_change)
        self.to_node.nodeChanged.connect(self.on_to_node_change)
        self.edge_type.currentIndexChanged.connect(self.on_edge_type_change)
        self.label.textEdited.connect(self.on_edge_label_change)

    def on_bpmn_id_change_done(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
        # print(type(self).__name__, self.lane_id, self.pool_id, 'bpmn_id_change_done')

    def on_lane_id_change_done(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id

        self.from_node.update_lane_id(old_lane_id, new_lane_id)
        self.to_node.update_lane_id(old_lane_id, new_lane_id)

        print('.' * 24, type(self).__name__, 'lane_id_change_done', old_lane_id, '-->', new_lane_id)

    def on_pool_id_change_done(self, old_pool_id, new_pool_id):
        if self.pool_id == old_pool_id:
            self.pool_id = new_pool_id

        self.from_node.update_pool_id(old_pool_id, new_pool_id)
        self.to_node.update_pool_id(old_pool_id, new_pool_id)

        print('.' * 24, type(self).__name__, 'pool_id_change_done', old_pool_id, '-->', new_pool_id)

    def on_node_id_change_done(self, old_node_id, new_node_id):
        from_node_affected = False
        to_node_affected = False

        # TODO: from node, if matches, change id
        if self.from_node.values()[2] == old_node_id:
            from_node_affected = True

        # TODO: to node, if matches, change id
        if self.to_node.values()[2] == old_node_id:
            to_node_affected = True

        if from_node_affected:
            self.from_node.update_node_id(old_node_id, new_node_id)
            self.on_from_node_change()
            print('.' * 24, type(self).__name__, 'node_id_change_done in [from] node', old_node_id, '-->', new_node_id)

        if to_node_affected:
            self.to_node.update_node_id(old_node_id, new_node_id)
            self.on_to_node_change()
            print('.' * 24, type(self).__name__, 'node_id_change_done in [to] node', old_node_id, '-->', new_node_id)

    def on_arrow_down(self):
        self.edge_order_changed.emit(self.index, 'down')

    def on_arrow_up(self):
        self.edge_order_changed.emit(self.index, 'up')

    def on_new_edge(self):
        self.new_edge.emit(self.index + 1)

    def on_remove_edge(self):
        self.remove_edge.emit(self.index)

    def on_from_node_change(self):
        self.edge_data['from'] = self.from_node.values()[2]

        # we need to let the to-node know about the from-node
        self.to_node.set_other_node_values(self.from_node.values())

        self.update_title()

    def on_to_node_change(self):
        self.edge_data['to'] = self.to_node.values()[2]
        self.update_title()

    def on_edge_type_change(self):
        # print(self.edge_type.currentIndex())
        key = self.edge_type.itemData(self.edge_type.currentIndex())
        if key is not None:
            self.edge_data['type'] = key
            self.update_title()

    def on_edge_label_change(self):
        self.edge_data['label'] = self.label.text()

    def update_title(self):
        self.update_error()
        self.change_title(text='{0}\n{1}'.format(self.edge_data['from'], self.edge_data['to']), icon=self.edge_data['type'], err=self.err)

    def associated_with_node(self, node_id):
        if node_id == self.edge_data['from'] or node_id == self.edge_data['to']:
            return True

        return False

class NodeSelectionDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setWindowTitle('Node selection')
        self.setMinimumSize(300, 400)
        self.setWindowFlags(QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint)

        self.selected_lane, self.selected_pool, self.selected_node = None, None, None

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
        self.select = QPushButton('Select node')
        # self.select.setStyleSheet('background-color: "#D8D8D8"')
        self.select.setStyleSheet('QPushButton:disabled {background-color:#E8E8E8;}')
        self.select.setEnabled(False)
        layout.addWidget(self.select)

        self.setLayout(layout)

    def init_tree(self):
        # populate the tree
        for lane_id in self.bpmn_data['lanes']:
            # if scope is 'bpmn' and it is a to node, then we do not allow the lane from from_node
            if self.scope in ['bpmn'] and self.role == 'to' and lane_id == self.other_node_values[0]:
                continue

            # if scope is lane or pool and lane_id is not None, we only show the specific lane
            # print(self.scope, self.lane_id, self.pool_id)
            if self.scope in ['lane', 'pool'] and self.lane_id is not None and lane_id != self.lane_id:
                continue

            lane_item = QTreeWidgetItem(self.node_tree, 0)
            lane_item.setText(0, lane_id)
            for pool_id in self.bpmn_data['lanes'][lane_id]['pools']:
                # if scope is pool and pool_id is not None, we only show the specific pool
                if self.scope in ['pool'] and self.lane_id is not None and self.pool_id is not None and lane_id == self.lane_id and pool_id != self.pool_id:
                    continue

                pool_item = QTreeWidgetItem(lane_item, 1)
                pool_item.setText(0, pool_id)
                for node_id in self.bpmn_data['lanes'][lane_id]['pools'][pool_id]['nodes']:
                    node_item = QTreeWidgetItem(pool_item, 2)
                    node_item.setText(0, node_id)
                    # preselect node if passed (not None)
                    if self.node_id and node_id == self.node_id:
                        self.node_tree.setCurrentItem(node_item)

    def signals_and_slots(self):
        self.select.clicked.connect(self.on_accept)
        self.node_tree.currentItemChanged.connect(self.on_current_item_change)

    def on_current_item_change(self, current, previous):
        if current.type() == 2:
            # print(current.text(0))
            self.select.setEnabled(True)
        else:
            self.select.setEnabled(False)

    def on_accept(self):
        selected_node_item = self.node_tree.currentItem()
        if selected_node_item:
            self.selected_node = selected_node_item.text(0)
            selected_pool_item = selected_node_item.parent()
            self.selected_pool = selected_pool_item.text(0)
            selected_lane_item = selected_pool_item.parent()
            self.selected_lane = selected_lane_item.text(0)
        else:
            self.selected_lane, self.selected_pool, self.selected_node = None, None, None

        self.accept()

    @staticmethod
    def open(parent, lane_id, pool_id, node_id, bpmn_data, scope, role, other_node_values):

        dialog = NodeSelectionDialog(parent)
        dialog.parent, dialog.lane_id, dialog.pool_id, dialog.node_id, dialog.bpmn_data, dialog.scope, dialog.role, dialog.other_node_values = parent, lane_id, pool_id, node_id, bpmn_data, scope, role, other_node_values
        dialog.init_tree()

        result = dialog.exec_()

        if result == QDialog.Accepted:
            return dialog.selected_lane, dialog.selected_pool, dialog.selected_node
        else:
            return None, None, None

class EdgeNodeWidget(QWidget):
    nodeChanged = pyqtSignal()

    def __init__(self, lane_id, pool_id, node_id, bpmn_data, scope='bpmn', role='from', parent=None):
        QFrame.__init__(self, parent=parent)
        self.node_id, self.bpmn_data, self.scope, self.role = node_id, bpmn_data, scope, role
        self.lane_id, self.pool_id, self.node_type, self.other_node_values = lane_id, pool_id, None, None
        self.init_widget()
        self.signals_and_slots()
        self.populate()

    def init_widget(self):
        self.content_layout = QGridLayout(self)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # lane and pool
        self.lane_and_pool = QLineEdit()
        self.lane_and_pool.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lane_and_pool.setStyleSheet('background-color: "#D8D8D8"')
        self.lane_and_pool.setReadOnly(True)
        self.content_layout.addWidget(self.lane_and_pool, 0, 0, 1, 3)

        # node_id
        self.id = QLineEdit()
        self.id.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.id.setStyleSheet('background-color: "#F8F8F8"')
        self.id.setReadOnly(True)
        self.content_layout.addWidget(self.id, 1, 0, 1, 2)

        # node_type
        self.icon = QPushButton()
        self.content_layout.addWidget(self.icon, 1, 2, 1, 1)

        for c in range(0, self.content_layout.columnCount()):
            self.content_layout.setColumnStretch(c, 1)


    def signals_and_slots(self):
        self.icon.clicked.connect(self.on_selection_dialog)

    def populate(self):
        lane_id, pool_id, node_type = lane_pool_type_of_node(self.node_id, self.bpmn_data)
        if self.scope == 'bpmn':
            self.lane_id, self.pool_id, self.node_type = lane_id, pool_id, node_type

        elif self.scope == 'lane':
            self.pool_id, self.node_type = pool_id, node_type

        elif self.scope == 'pool':
            self.node_type = node_type


        if self.lane_id:
            self.lane_and_pool.setText('{0} : {1}'.format(self.lane_id, self.pool_id))

        if self.node_id:
            self.id.setText(self.node_id)

        if self.node_type:
            pixmap = QPixmap(ICONS[self.node_type])
            # pixmap = pixmap.scaledToHeight(24)
            self.icon.setIcon(QIcon(pixmap))

    def update_lane_id(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id
            self.populate()

    def update_pool_id(self, old_pool_id, new_pool_id):
        if self.pool_id == old_pool_id:
            self.pool_id = new_pool_id
            self.populate()

    def update_node_id(self, old_node_id, new_node_id):
        if self.node_id == old_node_id:
            self.node_id = new_node_id
            self.populate()

    def on_selection_dialog(self):
        lane_id, pool_id, node_id = NodeSelectionDialog.open(self, self.lane_id, self.pool_id, self.node_id, self.bpmn_data, self.scope, self.role, self.other_node_values)
        # print(lane_id, pool_id, node_id)
        if node_id and node_id != self.node_id:
            self.lane_id, self.pool_id, self.node_id = lane_id, pool_id, node_id
            self.populate()
            self.nodeChanged.emit()

    def values(self):
        return self.lane_id, self.pool_id, self.node_id, self.node_type

    def set_other_node_values(self, val):
        self.other_node_values = val
