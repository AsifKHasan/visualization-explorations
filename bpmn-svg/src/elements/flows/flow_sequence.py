#!/usr/bin/env python3
'''
'''
from pysvg.builders import *
from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *

from util.logger import *
from util.svg_util import *

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

class FlowSequence(BpmnElement):
    def __init__(self, bpmn_id, lane_id, pool_id):
        self.theme = self.current_theme['FlowSequence']

    def to_svg(spec_def):
        pass
