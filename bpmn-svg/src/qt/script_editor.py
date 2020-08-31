#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt.qt_utils import *

from util.logger import *

class ScriptEditor(QObject):

    script_changed = pyqtSignal(str)

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
        self.ui.plainTextEdit_file.textChanged.connect(self.on_textchange)

    def read_bpmn_file(self, path):
        if path is not None and path != '':
            with open(path, mode='r') as f:
                self.ui.plainTextEdit_file.setPlainText(f.read())
                self.current_file_path = path
                # self.script_changed.emit(self.ui.plainTextEdit_file.toPlainText())

    def on_open_file(self):
        self.current_file_path, _ = open_file(self.ui, dialog_title='Open bpmn script', dialog_location=Path("../data").as_posix(), file_filter='*.bpmn')
        self.read_bpmn_file(self.current_file_path)

    def on_increase(self):
        self.ui.plainTextEdit_file.zoomIn()

    def on_decrease(self):
        self.ui.plainTextEdit_file.zoomOut()

    def on_linewrap(self, state):
        if self.ui.check_linewrap.isChecked():
            self.ui.plainTextEdit_file.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            self.ui.plainTextEdit_file.setLineWrapMode(QPlainTextEdit.NoWrap)

    def on_textchange(self):
        self.script_changed.emit(self.ui.plainTextEdit_file.toPlainText())
