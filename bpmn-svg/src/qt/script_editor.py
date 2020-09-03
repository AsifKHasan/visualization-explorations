#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from util.logger import *

from qt.qt_utils import *
from qt import *

class ScriptEditor(QObject):

    script_modified = pyqtSignal(bool)
    schema_update_triggered = pyqtSignal(str)

    def __init__(self, ui):
        QObject.__init__(self)
        self.ui = ui
        self.signals_and_slots()
        self.highlight = BpmnHighlighter(self.ui.plainTextEdit_file.document())
        self.current_file_path = None

    def signals_and_slots(self):
        self.ui.button_increase.clicked.connect(self.on_increase)
        self.ui.button_decrease.clicked.connect(self.on_decrease)
        self.ui.check_linewrap.stateChanged.connect(self.on_linewrap)
        self.ui.plainTextEdit_file.modificationChanged.connect(self.on_modified)

    def read_bpmn_file(self, path):
        if path is not None and path != '':
            with open(path, mode='r') as f:
                self.ui.plainTextEdit_file.setPlainText(f.read())
                self.current_file_path = path
                self.schema_update_triggered.emit(self.ui.plainTextEdit_file.toPlainText())

    def save_bpmn_file(self, path):
        if path is not None and path != '':
            with open(path, mode='w') as f:
                f.write(self.ui.plainTextEdit_file.toPlainText())
                self.script_modified.emit(False)
                self.schema_update_triggered.emit(self.ui.plainTextEdit_file.toPlainText())

    def new_bpmn_file(self):
        path, _ = save_file(self.ui, dialog_title='New bpmn script', dialog_location=Path("../data/new-script.bpmn").as_posix(), file_filter='*.bpmn')
        if path is not None and path != '':
            with open(path, mode='w') as f:
                f.write(NEW_BPMN_SCRIPT)
                self.current_file_path = path

            self.read_bpmn_file(self.current_file_path)
            self.script_modified.emit(False)

    def on_open_file(self):
        self.current_file_path, _ = open_file(self.ui, dialog_title='Open bpmn script', dialog_location=Path("../data").as_posix(), file_filter='*.bpmn')
        self.read_bpmn_file(self.current_file_path)
        self.script_modified.emit(False)


    def on_modified(self, modified):
        self.script_modified.emit(modified)

    def on_save_file(self):
        self.save_bpmn_file(self.current_file_path)

    def on_new_file(self):
        self.new_bpmn_file()

    def on_script_generated(self, script):
        self.ui.plainTextEdit_file.setPlainText(script)

    def on_increase(self):
        self.ui.plainTextEdit_file.zoomIn()

    def on_decrease(self):
        self.ui.plainTextEdit_file.zoomOut()

    def on_linewrap(self, state):
        if self.ui.check_linewrap.isChecked():
            self.ui.plainTextEdit_file.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            self.ui.plainTextEdit_file.setLineWrapMode(QPlainTextEdit.NoWrap)
