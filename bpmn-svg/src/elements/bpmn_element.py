#!/usr/bin/env python3
'''
    spec_def is a dictionary with Element specific inputs
    returns a SvgElement
'''
from util.logger import *

from elements import *

class BpmnElement():
    current_theme = default_theme

    def to_svg(self, spec_def):
        return None
