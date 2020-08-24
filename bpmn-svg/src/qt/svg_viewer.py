#!/usr/bin/env python3
'''
'''
import json

from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

from qt.qt_utils import *

from util.logger import *

class SvgViewer(QObject):
    def __init__(self, ui, zoom_factor):
        QObject.__init__(self)
        self.ui = ui
        self.zoom_factor = zoom_factor

        self.ui.svgwidget_svg = QWebEngineView()
        self.ui.gridLayout_svgarea.addWidget(self.ui.svgwidget_svg)
        self.ui.svgwidget_svg.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.ui.svgwidget_svg.setStyleSheet("background-color: '#f8f8f8'")

        self.ui.graphicsView_svg.hide()

        self.signals_and_slots()

    def signals_and_slots(self):
        self.ui.button_zoom_100.clicked.connect(self.on_zoom_100)
        self.ui.button_zoom_out.clicked.connect(self.on_zoom_out)
        self.ui.button_zoom_in.clicked.connect(self.on_zoom_in)

    @pyqtSlot(str)
    def on_svg_generated(self, svg_str):
        self.svg_str = svg_str

        html = '''<html>
        <body>''' + self.svg_str + '''</body>
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
