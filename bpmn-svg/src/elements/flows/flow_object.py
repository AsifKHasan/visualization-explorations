#!/usr/bin/env python3
'''
TODO: Udemy
https://www.udemy.com/course/mega-course-vmware-vsphere-67-bootcamp-100-hands-on-labs/
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

from elements.bpmn_element import BpmnElement

from util.logger import *

class FlowObject(BpmnElement):
    def __init__(self, edge_type):
        self.edge_type = edge_type
        self.theme = self.current_theme['flows'][edge_type]
