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

class EventEnd(BpmnElement):
    def __init__(self):
        self.theme = self.current_theme['EventEnd']

    def to_svg(self, node_id, node_data):
        debug('....processing node [{0}] ...'.format(node_id))

        group_width = self.theme['outer-circle']['radius'] * 2
        group_height = self.theme['outer-circle']['radius'] * 2

        # group to hold the objects
        svg_group = G(id=node_id)

        # outer circle
        outer_circle = Circle(cx=self.theme['outer-circle']['radius'], cy=self.theme['outer-circle']['radius'], r=self.theme['outer-circle']['radius'])
        outer_circle.set_style(StyleBuilder(self.theme['outer-circle']['style']).getStyle())

        # add into the group
        svg_group.addElement(outer_circle)

        group_specs = {'width': group_width, 'height': group_height}

        debug('....processing node [{0}] DONE ...'.format(node_id))

        return SvgElement(group_specs, svg_group)
