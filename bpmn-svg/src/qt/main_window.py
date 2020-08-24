#!/usr/bin/env python3
'''
'''
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

from qt.qt_utils import *

from util.logger import *

from qt.bpmn_editor import BpmnEditor
from qt.svg_viewer import SvgViewer

class MainWindow(QMainWindow):
    def __init__(self, screen, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        settings = QtCore.QSettings('spectrum', 'bpmn-svg')

        self.screen = screen
        self.ui = uic.loadUi("./bpmn-svg.ui", self)

        self.ui.centralwidget.setContentsMargins(0, 0, 0, 0)

        vertical_splitter_size = settings.value('vertical-splitter', [], int)
        if vertical_splitter_size:
            print(vertical_splitter_size)
            self.ui.splitter_vertical.setSizes(vertical_splitter_size)

        horizontal_splitter_size = settings.value('horizontal-splitter', [], int)
        if horizontal_splitter_size:
            self.ui.splitter_horizontal.setSizes(horizontal_splitter_size)

        zoom_factor = int(settings.value('zoom-factor', int))
        if zoom_factor is None or zoom_factor == 0:
            zoom_factor = 1.0

        # get previously loaded bpmn path from settings
        bpmn_path = settings.value('bpmn-path')

        self.bpmn_editor = BpmnEditor(self.ui, bpmn_path)
        self.svg_viewer = SvgViewer(self.ui, zoom_factor)

        self.signals_and_slots()

        self.ui.show()

    def closeEvent(self, event):
        settings = QtCore.QSettings('spectrum', 'bpmn-svg')
        settings.setValue('zoom-factor', self.svg_viewer.zoom_factor)
        settings.setValue('bpmn-path', self.bpmn_editor.current_file_path)
        settings.setValue('vertical-splitter', self.ui.splitter_vertical.sizes())
        settings.setValue('horizontal-splitter', self.ui.splitter_vertical.sizes())

    def signals_and_slots(self):
        self.bpmn_editor.svg_generated.connect(self.svg_viewer.on_svg_generated)
