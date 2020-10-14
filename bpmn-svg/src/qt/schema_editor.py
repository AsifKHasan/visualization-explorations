#!/usr/bin/env python3
'''
'''
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from util.logger import *

from bpmn_parser import *
from bpmn_script import *
from bpmn_svg import *

from qt.qt_utils import *

from qt.schema.bpmn_header import BpmnHeader
from qt.schema.bpmn_lanes import BpmnLanes
from qt.schema.bpmn_edges import BpmnEdges

from qt.schema.lane_editor import LaneEditor
from qt.schema.edge_editor import EdgeEditor

class SchemaEditor(QVBoxLayout):

    script_generated = pyqtSignal(str)
    svg_generated = pyqtSignal(str, str)

    bpmn_id_change_done = pyqtSignal(str, str)
    lane_id_change_done = pyqtSignal(str, str)
    pool_id_change_done = pyqtSignal(str, str)
    node_id_change_done = pyqtSignal(str, str)

    remove_lane = pyqtSignal(str)
    remove_pool = pyqtSignal(str)
    remove_node = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QVBoxLayout, self).__init__(parent)
        self.parent = parent
        self.bpmn_json_data = {}
        # self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

    def signals_and_slots(self):
        self.bpmn_header_ui.bpmn_id_change_requested.connect(self.on_bpmn_id_change_requested)
        self.bpmn_lanes_ui.lane_id_change_requested.connect(self.on_lane_id_change_requested)
        self.bpmn_lanes_ui.pool_id_change_requested.connect(self.on_pool_id_change_requested)
        self.bpmn_lanes_ui.node_id_change_requested.connect(self.on_node_id_change_requested)

        self.bpmn_lanes_ui.lane_removed.connect(self.on_lane_removed)
        self.bpmn_lanes_ui.pool_removed.connect(self.on_pool_removed)
        self.bpmn_lanes_ui.node_removed.connect(self.on_node_removed)

        self.bpmn_id_change_done.connect(self.bpmn_header_ui.on_bpmn_id_change_done)
        self.bpmn_id_change_done.connect(self.bpmn_lanes_ui.on_bpmn_id_change_done)
        self.bpmn_id_change_done.connect(self.bpmn_edges_ui.on_bpmn_id_change_done)

        self.lane_id_change_done.connect(self.bpmn_header_ui.on_lane_id_change_done)
        self.lane_id_change_done.connect(self.bpmn_lanes_ui.on_lane_id_change_done)
        self.lane_id_change_done.connect(self.bpmn_edges_ui.on_lane_id_change_done)

        self.pool_id_change_done.connect(self.bpmn_header_ui.on_pool_id_change_done)
        self.pool_id_change_done.connect(self.bpmn_lanes_ui.on_pool_id_change_done)
        self.pool_id_change_done.connect(self.bpmn_edges_ui.on_pool_id_change_done)

        self.node_id_change_done.connect(self.bpmn_lanes_ui.on_node_id_change_done)
        self.node_id_change_done.connect(self.bpmn_edges_ui.on_node_id_change_done)

        self.remove_lane.connect(self.bpmn_edges_ui.on_remove_lane)

        self.remove_pool.connect(self.bpmn_lanes_ui.on_remove_pool)
        self.remove_pool.connect(self.bpmn_edges_ui.on_remove_pool)

        self.remove_node.connect(self.bpmn_lanes_ui.on_remove_node)
        self.remove_node.connect(self.bpmn_edges_ui.on_remove_node)

    def populate(self):

        self.bpmn_id = list(self.bpmn_json_data.keys())[0]
        self.bpmn_data = self.bpmn_json_data[self.bpmn_id]

        for i in reversed(range(self.count())):
            widgetToRemove = self.itemAt(i).widget()
            # remove it from the layout list
            self.removeWidget(widgetToRemove)
            # remove it from the gui
            if widgetToRemove: widgetToRemove.setParent(None)
            # self.itemAt(i).widget().setParent(None)

        self.bpmn_header_ui, self.bpmn_lanes_ui, self.bpmn_edges_ui, self.vertical_spacer = None, None, None, None

        # Bpmn id, title and styles at the top
        self.bpmn_header_ui = BpmnHeader(self.bpmn_data, self.bpmn_id)
        self.addWidget(self.bpmn_header_ui)

        # Lane container in the middle
        self.bpmn_lanes_ui = BpmnLanes(self.bpmn_data, self.bpmn_id)
        self.addWidget(self.bpmn_lanes_ui)

        # Edge container after the lane container
        self.bpmn_edges_ui = BpmnEdges(self.bpmn_data, self.bpmn_id)
        self.addWidget(self.bpmn_edges_ui)

        # vertical spacer at the bottom
        self.vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addItem(self.vertical_spacer)

        # self.addStretch()
        self.signals_and_slots()

    def on_bpmn_id_change_requested(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_json_data[new_bpmn_id] = self.bpmn_json_data.pop(old_bpmn_id)
        self.bpmn_id = list(self.bpmn_json_data.keys())[0]
        self.bpmn_data = self.bpmn_json_data[self.bpmn_id]
        self.bpmn_id_change_done.emit(old_bpmn_id, new_bpmn_id)

    def on_lane_id_change_requested(self, old_lane_id, new_lane_id):
        print(type(self).__name__, 'lane_id_change_requested', old_lane_id, '-->', new_lane_id)
        print(type(self).__name__, 'lane_id_change_done', old_lane_id, '-->', new_lane_id)
        self.lane_id_change_done.emit(old_lane_id, new_lane_id)

    def on_pool_id_change_requested(self, old_pool_id, new_pool_id):
        print(type(self).__name__, 'pool_id_change_requested', old_pool_id, '-->', new_pool_id)
        print(type(self).__name__, 'pool_id_change_done', old_pool_id, '-->', new_pool_id)
        self.pool_id_change_done.emit(old_pool_id, new_pool_id)

    def on_node_id_change_requested(self, old_node_id, new_node_id):
        print(type(self).__name__, 'node_id_change_requested', old_node_id, '-->', new_node_id)
        print(type(self).__name__, 'node_id_change_done', old_node_id, '-->', new_node_id)
        self.node_id_change_done.emit(old_node_id, new_node_id)

    def on_lane_removed(self, lane_id):
        print(type(self).__name__, 'lane_removed', lane_id)
        print(type(self).__name__, 'remove_lane', lane_id)
        self.remove_lane.emit(lane_id)

    def on_pool_removed(self, pool_id):
        print(type(self).__name__, 'pool_removed', pool_id)
        print(type(self).__name__, 'remove_pool', pool_id)
        self.remove_pool.emit(pool_id)

    def on_node_removed(self, node_id):
        print(type(self).__name__, 'node_removed', node_id)
        print(type(self).__name__, 'remove_node', node_id)
        self.remove_node.emit(node_id)

    def on_schema_update_triggered(self, script):
        if script is not None and script.strip() != '':
            self.bpmn_json_data = parse_to_json(script)
            self.populate()

    def on_generate_script(self):
        if self.bpmn_json_data is not None:
            script = repr_bpmn(self.bpmn_id, self.bpmn_json_data[self.bpmn_id])
            self.script_generated.emit(script)

    def on_generate_svg(self):
        if self.bpmn_json_data is not None:
            self.svg_obj, self.bpmn_id = to_svg(self.bpmn_json_data)
            self.svg_generated.emit(self.bpmn_id, self.svg_obj.getXML())
