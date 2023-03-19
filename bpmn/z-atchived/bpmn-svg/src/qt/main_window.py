#!/usr/bin/env python3
'''
'''
import sys

from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QKeySequence

from util.logger import *

from qt.qt_utils import *
from qt.log_stream import LogStream

from qt.script_editor import ScriptEditor
from qt.schema_editor import SchemaEditor
from qt.svg_viewer import SvgViewer

class MainWindow(QMainWindow):
    def __init__(self, screen, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.settings = QtCore.QSettings('spectrum', 'bpmn-svg')

        # the custom output stream
        # sys.stdout = LogStream(log_generated=self.on_log_generated)
        # sys.stderr = LogStream(log_generated=self.on_log_generated)

        self.screen = screen
        self.ui = uic.loadUi("./bpmn-svg.ui", self)

        self.restore_settings()
        self.signals_and_slots()

        # get previously loaded bpmn path from settings
        bpmn_path = self.settings.value('bpmn-path')
        self.script_editor.read_bpmn_file(bpmn_path)

        self.ui.show()

    def __del__(self):
        # restore sys.stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def restore_settings(self):
        self.ui.centralwidget.setContentsMargins(0, 0, 0, 0)
        # self.ui.splitter_vertical.setContentsMargins(0, 0, 0, 0)

        vertical_splitter_size = self.settings.value('vertical-splitter', [], int)
        if vertical_splitter_size:
            self.ui.splitter_vertical.setSizes(vertical_splitter_size)

        horizontal_splitter_size = self.settings.value('horizontal-splitter', [], int)
        if horizontal_splitter_size:
            self.ui.splitter_horizontal.setSizes(horizontal_splitter_size)

        zoom_factor = float(self.settings.value('zoom-factor', 1.0, float))
        if zoom_factor is None or zoom_factor == 0:
            zoom_factor = 1.0

        self.script_editor = ScriptEditor(self.ui)
        self.svg_viewer = SvgViewer(self.ui, zoom_factor)

        # bpmn schema editor
        self.schema_editor = SchemaEditor(self.scrollAreaWidgetContents)

        main_window_size = self.settings.value('main-window-size')
        if main_window_size:
            self.resize(main_window_size)

        main_window_geometry = self.settings.value('main-window-geometry')
        if main_window_geometry:
            self.setGeometry(main_window_geometry)

    def closeEvent(self, event):
        # settings = QtCore.QSettings('spectrum', 'bpmn-svg')
        self.settings.setValue('zoom-factor', self.svg_viewer.zoom_factor)
        self.settings.setValue('bpmn-path', self.script_editor.current_file_path)
        self.settings.setValue('vertical-splitter', self.ui.splitter_vertical.sizes())
        self.settings.setValue('horizontal-splitter', self.ui.splitter_horizontal.sizes())
        self.settings.setValue('main-window-size', self.size())
        self.settings.setValue('main-window-geometry', self.geometry())

    def signals_and_slots(self):
        self.ui.button_open_file.clicked.connect(self.script_editor.on_open_file)
        self.ui.button_save_file.clicked.connect(self.script_editor.on_save_file)
        self.ui.button_new_file.clicked.connect(self.script_editor.on_new_file)

        self.ui.button_generate_script.clicked.connect(self.schema_editor.on_generate_script)
        self.ui.button_generate_svg.clicked.connect(self.schema_editor.on_generate_svg)

        self.script_editor.script_modified.connect(self.on_script_modified)
        self.script_editor.schema_update_triggered.connect(self.schema_editor.on_schema_update_triggered)

        self.schema_editor.script_generated.connect(self.script_editor.on_script_generated)
        self.schema_editor.svg_generated.connect(self.svg_viewer.on_svg_generated)

        self.shortcut_horizontal_splitter_left = QShortcut(QKeySequence('Ctrl+<'), self)
        self.shortcut_horizontal_splitter_right = QShortcut(QKeySequence('Ctrl+>'), self)
        self.shortcut_vertical_splitter_up = QShortcut(QKeySequence('Alt+<'), self)
        self.shortcut_vertical_splitter_down = QShortcut(QKeySequence('Alt+>'), self)

        self.shortcut_horizontal_splitter_left.activated.connect(self.on_horizontal_splitter_left)
        self.shortcut_horizontal_splitter_right.activated.connect(self.on_horizontal_splitter_right)
        self.shortcut_vertical_splitter_up.activated.connect(self.on_vertical_splitter_up)
        self.shortcut_vertical_splitter_down.activated.connect(self.on_vertical_splitter_down)

        # bpmn_id_changed from bpmn_header
        self.schema_editor.bpmn_id_change_done.connect(self.on_bpmn_id_change_done)

    def on_horizontal_splitter_left(self):
        sizes = self.ui.splitter_horizontal.sizes()
        step = 100
        if sizes[0] < step:
            step = sizes[0]

        self.ui.splitter_horizontal.setSizes([sizes[0] - step,  sizes[1] + step])

    def on_horizontal_splitter_right(self):
        sizes = self.ui.splitter_horizontal.sizes()
        step = 100
        if sizes[1] < step:
            step = sizes[1]

        self.ui.splitter_horizontal.setSizes([sizes[0] + step,  sizes[1] - step])

    def on_vertical_splitter_up(self):
        sizes = self.ui.splitter_vertical.sizes()
        step = 50
        if sizes[0] < step:
            step = sizes[0]

        self.ui.splitter_vertical.setSizes([sizes[0] - step,  sizes[1] + step])

    def on_vertical_splitter_down(self):
        sizes = self.ui.splitter_vertical.sizes()
        step = 50
        if sizes[1] < step:
            step = sizes[1]

        self.ui.splitter_vertical.setSizes([sizes[0] + step,  sizes[1] - step])

    def on_log_generated(self, text):
        self.ui.plainTextEdit_log.insertPlainText(text)

    def on_script_modified(self, modified):
        if modified:
            self.ui.button_save_file.setEnabled(True)
        else:
            self.ui.button_save_file.setEnabled(False)
            # a new script was loaded/created, clear the svg
            self.svg_viewer.clear_svg()

    def on_bpmn_id_change_done(self, old_bpmn_id, new_bpmn_id):
        self.svg_viewer.on_bpmn_id_change_done(old_bpmn_id, new_bpmn_id)
