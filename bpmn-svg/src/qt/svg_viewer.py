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
        self.svg_str = ''
        self.zoom_factor = zoom_factor
        self.ui.button_zoom_100.setText('{0}%'.format(int(self.zoom_factor * 100)))

        self.ui.svgwidget_svg = QWebEngineView()
        self.ui.gridLayout_svgarea.addWidget(self.ui.svgwidget_svg)
        self.ui.svgwidget_svg.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.ui.svgwidget_svg.setStyleSheet("background-color: '#f8f8f8'")

        self.ui.graphicsView_svg.hide()
        self.ui.button_save_svg.setEnabled(False)

        self.signals_and_slots()

    def signals_and_slots(self):
        self.ui.button_save_svg.clicked.connect(self.save_svg)

        self.ui.button_zoom_100.clicked.connect(self.on_zoom_100)
        self.ui.button_zoom_out.clicked.connect(self.on_zoom_out)
        self.ui.button_zoom_in.clicked.connect(self.on_zoom_in)

    @pyqtSlot(str, str)
    def on_svg_generated(self, bpmn_id, svg_str):
        self.bpmn_id = bpmn_id
        self.svg_str = svg_str
        self.show_svg()
        self.ui.button_save_svg.setEnabled(True)

    def clear_svg(self):
        self.bpmn_id = ''
        self.svg_str = ''
        self.zoom_factor = 1.0
        self.show_svg()
        self.ui.button_save_svg.setEnabled(False)

    def show_svg(self):
        html = '''<html>
        <body>''' + self.svg_str + '''</body>
        </html>'''

        self.ui.svgwidget_svg.setHtml(html)
        self.ui.svgwidget_svg.setZoomFactor(self.zoom_factor)

    def save_svg(self):
        if self.bpmn_id == '' or self.svg_str == '':
            return

        output_svg_file_path = '../out/{0}.svg'.format(self.bpmn_id)
        with open(output_svg_file_path, mode='w') as f:
            f.write(self.svg_str)

        info('SVG saved at {0}'.format(output_svg_file_path))

    def on_zoom_100(self):
        self.zoom_factor = 1.0
        self.ui.svgwidget_svg.setZoomFactor(self.zoom_factor)
        self.ui.button_zoom_100.setText('{0}%'.format(int(self.zoom_factor * 100)))

    def on_zoom_out(self):
        self.zoom_factor = self.zoom_factor/1.1
        self.ui.svgwidget_svg.setZoomFactor(self.zoom_factor)
        self.ui.button_zoom_100.setText('{0}%'.format(int(self.zoom_factor * 100)))

    def on_zoom_in(self):
        self.zoom_factor = self.zoom_factor * 1.1
        self.ui.svgwidget_svg.setZoomFactor(self.zoom_factor)
        self.ui.button_zoom_100.setText('{0}%'.format(int(self.zoom_factor * 100)))

    def on_bpmn_id_change_done(self, old_bpmn_id, new_bpmn_id):
        self.bpmn_id = new_bpmn_id
