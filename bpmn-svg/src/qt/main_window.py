#!/usr/bin/env python3
'''
'''
import json

from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

from qt.qt_utils import *

from util.logger import *
from bpmn_parser import *
from bpmn_svg import *

class MainWindow(QMainWindow):
    def __init__(self, screen, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.zoom_factor = 1.0

        self.screen = screen
        self.ui = uic.loadUi("./bpmn-svg.ui", self)

        self.ui.centralwidget.setContentsMargins(0, 0, 0, 0)

        self.ui.splitter_vertical.setSizes([1000, 50])
        self.ui.splitter_horizontal.setSizes([400, 800])

        self.ui.svgwidget_svg = QWebEngineView()
        self.ui.gridLayout_svgarea.addWidget(self.ui.svgwidget_svg)
        self.ui.svgwidget_svg.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.ui.svgwidget_svg.setStyleSheet("background-color: '#f8f8f8'")


        self.ui.graphicsView_svg.hide()

        # debug('Screen: %s' % self.screen.name())
        # size = self.screen.size()
        # debug('Size: %d x %d' % (size.width(), size.height()))
        # rect = self.screen.availableGeometry()
        # debug('Available: %d x %d' % (rect.width(), rect.height()))

        self.signals_and_slots()

        self.ui.show()

    def signals_and_slots(self):
        self.ui.button_open_file.clicked.connect(self.on_open_file)
        self.ui.button_generate.clicked.connect(self.on_generate)
        self.ui.toolButton_zoom_100.clicked.connect(self.on_zoom_100)
        self.ui.toolButton_zoom_out.clicked.connect(self.on_zoom_out)
        self.ui.toolButton_zoom_in.clicked.connect(self.on_zoom_in)

    def on_open_file(self):
        self.current_file_path, _ = open_file(self, dialog_title='Open bpmn script', dialog_location=Path("../data").as_posix(), file_filter='*.bpmn')
        if self.current_file_path is not None and self.current_file_path != '':
            with open(self.current_file_path, mode='r') as f:
                self.ui.plainTextEdit_file.insertPlainText(f.read())

    def on_generate(self):
        bpmn_script_content = self.ui.plainTextEdit_file.toPlainText()
        if bpmn_script_content is not None and bpmn_script_content.strip() != '':
            self.bpmn_json_data = parse_to_json(self.ui.plainTextEdit_file.toPlainText())
            if self.bpmn_json_data is not None:
                self.svg, self.bpmn_id = to_svg(self.bpmn_json_data)

                html = '''<html>
                <body>''' + self.svg.getXML() + '''</body>
                </html>'''

                self.ui.svgwidget_svg.setHtml(html)
                self.ui.svgwidget_svg.setZoomFactor(self.zoom_factor)

    def on_zoom_100(self):
        self.zoom_factor = 1.0
        self.ui.svgwidget_svg.setZoomFactor(self.zoom_factor)

    def on_zoom_out(self):
        self.zoom_factor = self.zoom_factor/1.25
        self.ui.svgwidget_svg.setZoomFactor(self.zoom_factor)

    def on_zoom_in(self):
        self.zoom_factor = self.zoom_factor * 1.25
        self.ui.svgwidget_svg.setZoomFactor(self.zoom_factor)
