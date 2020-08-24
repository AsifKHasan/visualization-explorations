#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *

from util.logger import *
from bpmn_parser import *
from bpmn_svg import *

class BpmnEditor(QObject):

    svg_generated = pyqtSignal(str)

    def __init__(self, ui, bpmn_path):
        QObject.__init__(self)
        self.ui = ui
        self.signals_and_slots()
        self.highlight = BpmnHighlighter(self.ui.plainTextEdit_file.document())
        self.current_file_path = bpmn_path
        self.read_bpmn_file(self.current_file_path)

    def signals_and_slots(self):
        self.ui.button_open_file.clicked.connect(self.on_open_file)
        self.ui.button_generate.clicked.connect(self.on_generate)
        self.ui.button_increase.clicked.connect(self.on_increase)
        self.ui.button_decrease.clicked.connect(self.on_decrease)
        self.ui.check_linewrap.stateChanged.connect(self.on_linewrap)

    def read_bpmn_file(self, path):
        if path is not None and path != '':
            with open(path, mode='r') as f:
                self.ui.plainTextEdit_file.setPlainText(f.read())

    def on_open_file(self):
        self.current_file_path, _ = open_file(self.ui, dialog_title='Open bpmn script', dialog_location=Path("../data").as_posix(), file_filter='*.bpmn')
        self.read_bpmn_file(self.current_file_path)

    def on_generate(self):
        bpmn_script_content = self.ui.plainTextEdit_file.toPlainText()
        if bpmn_script_content is not None and bpmn_script_content.strip() != '':
            self.bpmn_json_data = parse_to_json(self.ui.plainTextEdit_file.toPlainText())
            if self.bpmn_json_data is not None:
                self.svg_obj, self.bpmn_id = to_svg(self.bpmn_json_data)
                self.svg_generated.emit(self.svg_obj.getXML())

    def on_increase(self):
        self.ui.plainTextEdit_file.zoomIn()

    def on_decrease(self):
        self.ui.plainTextEdit_file.zoomOut()

    def on_linewrap(self, state):
        if self.ui.check_linewrap.isChecked():
            self.ui.plainTextEdit_file.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            self.ui.plainTextEdit_file.setLineWrapMode(QPlainTextEdit.NoWrap)
