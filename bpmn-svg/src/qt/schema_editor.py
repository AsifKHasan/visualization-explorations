#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from util.logger import *

from bpmn_parser import *
from bpmn_svg import *

from qt.qt_utils import *

from qt.schema.bpmn_header import BpmnHeader
from qt.schema.bpmn_lanes import BpmnLanes
from qt.schema.bpmn_edges import BpmnEdges

from qt.schema.lane_editor import LaneEditor
from qt.schema.edge_editor import EdgeEditor

class SchemaEditor(QVBoxLayout):

    svg_generated = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QVBoxLayout, self).__init__(parent)
        self.parent = parent
        self.bpmn_json_data = {}

        self.signals_and_slots()

    def signals_and_slots(self):
        pass

    def populate(self):

        self.bpmn_id = list(self.bpmn_json_data.keys())[0]

        self.bpmn_lanes_ui, self.bpmn_lanes_ui, self.bpmn_edges_ui, self.vertical_spacer = None, None, None, None

        # Bpmn id, title and styles at the top
        self.bpmn_header_ui = BpmnHeader(self.bpmn_id, self.bpmn_json_data[self.bpmn_id])
        self.addWidget(self.bpmn_header_ui)

        # Lane container in the middle
        self.bpmn_lanes_ui = BpmnLanes(self.bpmn_id, self.bpmn_json_data[self.bpmn_id].get('lanes', None))
        self.addWidget(self.bpmn_lanes_ui)

        # Edge container after the lane container
        self.bpmn_edges_ui = BpmnEdges(self.bpmn_id, self.bpmn_json_data[self.bpmn_id].get('edges', None))
        self.addWidget(self.bpmn_edges_ui)

        # vertical spacer at the bottom
        self.vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addItem(self.vertical_spacer)

        self.addStretch()

    def on_script_changed(self, script):
        if script is not None and script.strip() != '':
            self.bpmn_json_data = parse_to_json(script)
            self.populate()

    def on_generate(self):
        if self.bpmn_json_data is not None:
            self.svg_obj, self.bpmn_id = to_svg(self.bpmn_json_data)
            self.svg_generated.emit(self.svg_obj.getXML())
