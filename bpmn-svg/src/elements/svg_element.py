#!/usr/bin/env python3
'''
'''
from util.logger import *
from elements import *

class SvgElement():
    def __init__(self, svg=None, width=None, height=None, snap_points=None, label_pos=None):
        self.svg = svg
        self.width = width
        self.height = height
        self.snap_points = snap_points
        self.label_pos = label_pos
