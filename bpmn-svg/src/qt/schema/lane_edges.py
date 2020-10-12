#!/usr/bin/env python3
'''
'''
import copy

from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *
from util.logger import *

from qt.schema.edge_editor import EdgeEditor

class LaneEdges(CollapsibleFrame):

    bpmn_id_change_done = pyqtSignal(str, str)
    lane_id_change_done = pyqtSignal(str, str)
    pool_id_change_done = pyqtSignal(str, str)
    node_id_change_done = pyqtSignal(str, str)

    def __init__(self, bpmn_data, bpmn_id, lane_id, parent=None):
        super().__init__(icon='edges', text='Lane Edges', parent=parent)
        self.set_styles(title_style='background-color: "#D0D0D0"; color: "#404040";', content_style='background-color: "#C8C8C8"; color: "#404040";')

        self.bpmn_data, self.bpmn_id, self.lane_id = bpmn_data, bpmn_id, lane_id
        self.edges = self.bpmn_data['lanes'][self.lane_id]['edges']

        self.init_ui()
        self.signals_and_slots()
        self.populate()

    def signals_and_slots(self):
        self.add_new_edge.clicked.connect(self.on_new_edge)

    def init_ui(self):
        self.warning_widget = None

        # *add* button to add a new edge
        self.add_new_edge = QPushButton()
        pixmap = QPixmap(ACTION_ICONS['new-edge'])
        self.add_new_edge.setIcon(QIcon(pixmap))

        self.add_new_edge.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.add_new_edge.setStyleSheet('font-size: 9px; border: 0px; background-color: #B0B0B0')

        self.add_button(self.add_new_edge, 'new-lane-edge')

    def populate(self, focus_on_edge=None, edges_to_expand=[]):
        # first clear the layout with all edges
        self.clearContent()

        # if we have only one pool, we ctually have no bpmn edges
        if len(self.bpmn_data['lanes'][self.lane_id]['pools']) < 2:
            self.warning_widget = WarningWidget(warning='there are no more than one pool in this lane, so no LANE level edge is possible', parent=self)
            self.warning_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(self.warning_widget)
            return

        # hide warning and allow new-edge
        self.add_new_edge.setEnabled(True)
        if self.warning_widget:
            self.warning_widget.hide()

        self.num_edges = len(self.edges)
        index = 0
        for edge in self.edges:
            edge_widget = EdgeEditor(self.bpmn_data, 'lane', self.bpmn_id, self.lane_id, None, edge, index, self.num_edges)
            edge_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(edge_widget)

            edge_widget.new_edge.connect(self.on_new_edge)
            edge_widget.remove_edge.connect(self.on_remove_edge)
            edge_widget.edge_order_changed.connect(self.on_edge_order_changed)

            self.bpmn_id_change_done.connect(edge_widget.on_bpmn_id_change_done)
            self.lane_id_change_done.connect(edge_widget.on_lane_id_change_done)
            self.pool_id_change_done.connect(edge_widget.on_pool_id_change_done)
            self.node_id_change_done.connect(edge_widget.on_node_id_change_done)

            if index in edges_to_expand:
                edge_widget.expand()

            if focus_on_edge is not None and focus_on_edge == index:
                edge_widget.expand()

            index = index + 1

    def on_bpmn_id_change_done(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
        # print(type(self).__name__, self.lane_id, 'bpmn_id_change_done')
        self.bpmn_id_change_done.emit(old_bpmn_id, new_bpmn_id)

    def on_lane_id_change_done(self, old_lane_id, new_lane_id):
        if self.lane_id == old_lane_id:
            self.lane_id = new_lane_id
            self.edges = self.bpmn_data['lanes'][self.lane_id]['edges']

            print('.' * 12, type(self).__name__, 'lane_id_change_done', old_lane_id, '-->', new_lane_id)
            self.lane_id_change_done.emit(old_lane_id, new_lane_id)

    def on_pool_id_change_done(self, old_pool_id, new_pool_id):
        print('.' * 12, type(self).__name__, 'pool_id_change_done', old_pool_id, '-->', new_pool_id)
        self.pool_id_change_done.emit(old_pool_id, new_pool_id)

    def on_node_id_change_done(self, old_node_id, new_node_id):
        print('.' * 12, type(self).__name__, 'node_id_change_done', old_node_id, '-->', new_node_id)
        self.node_id_change_done.emit(old_node_id, new_node_id)

    def on_new_edge(self, index=0):
        # if there are less than two pools, we can not have Lane level edges
        if len(self.bpmn_data['lanes'][self.lane_id]['pools']) < 2:
            return

        if not index:
            idx = 0
        else:
            idx = index

        # insert a blank edge in bpmn_data
        new_edge_object = copy.deepcopy(NEW_EDGE)
        self.bpmn_data['lanes'][self.lane_id]['edges'].insert(idx, new_edge_object)

        # now populate again
        edges_to_expand = self.edges_expanded()
        self.populate(focus_on_edge=idx, edges_to_expand=edges_to_expand)

    def on_remove_edge(self, index):
        # remove the edge from bpmn_data
        self.bpmn_data['lanes'][self.lane_id]['edges'].pop(index)

        # now populate again
        edges_to_expand = self.edges_expanded()
        self.populate(edges_to_expand=edges_to_expand)

    def on_edge_order_changed(self, index, direction):
        if self.num_edges <= 1:
            pass

        if index == 0 and direction == 'up':
            pass

        if index == self.num_edges - 1 and direction == 'down':
            pass

        # swap edges
        if direction == 'up':
            self.bpmn_data['lanes'][self.lane_id]['edges'][index], self.bpmn_data['lanes'][self.lane_id]['edges'][index - 1] = self.bpmn_data['lanes'][self.lane_id]['edges'][index - 1], self.bpmn_data['lanes'][self.lane_id]['edges'][index]
        elif direction == 'down':
            self.bpmn_data['lanes'][self.lane_id]['edges'][index], self.bpmn_data['lanes'][self.lane_id]['edges'][index + 1] = self.bpmn_data['lanes'][self.lane_id]['edges'][index + 1], self.bpmn_data['lanes'][self.lane_id]['edges'][index]

        edges_to_expand = self.edges_expanded()
        self.populate(edges_to_expand=edges_to_expand)

    def on_remove_lane(self, lane_id):
        print('.' * 12, type(self).__name__, 'remove_lane', lane_id)
        self.bpmn_data['lanes'][self.lane_id]['edges'] = [x for x in self.edges if not associated_with_lane(x, lane_id)]
        self.edges = self.bpmn_data['lanes'][self.lane_id]['edges']
        self.populate()

    def on_remove_pool(self, pool_id):
        print('.' * 12, type(self).__name__, 'remove_pool', pool_id)
        self.bpmn_data['lanes'][self.lane_id]['edges'] = [x for x in self.edges if not associated_with_pool(x, pool_id)]
        self.edges = self.bpmn_data['lanes'][self.lane_id]['edges']
        self.populate()

    def on_remove_node(self, node_id):
        print('.' * 12, type(self).__name__, 'remove_node', node_id)
        self.bpmn_data['lanes'][self.lane_id]['edges'] = [x for x in self.edges if not associated_with_node(x, node_id)]
        self.edges = self.bpmn_data['lanes'][self.lane_id]['edges']
        self.populate()

    def edges_expanded(self):
        return []

def associated_with_lane(edge_data, lane_id):
    lane_of_from_node, _, _, _ = lane_pool_type_of_node(edge_data['from'], self.bpmn_data)
    lane_of_to_node, _, _, _ = lane_pool_type_of_node(edge_data['to'], self.bpmn_data)
    if lane_id == lane_of_from_node or lane_id == lane_of_to_node:
        return True

    return False

def associated_with_pool(edge_data, pool_id):
    _, pool_of_from_node, _, _ = lane_pool_type_of_node(edge_data['from'], self.bpmn_data)
    _, pool_of_to_node, _, _ = lane_pool_type_of_node(edge_data['to'], self.bpmn_data)
    if pool_id == pool_of_from_node or pool_id == pool_of_to_node:
        return True

    return False

def associated_with_node(edge_data, node_id):
    if node_id == edge_data['from'] or node_id == edge_data['to']:
        return True

    return False
