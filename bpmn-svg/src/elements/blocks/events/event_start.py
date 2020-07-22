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

class EventStart(BpmnElement):
    def __init__(self):
        self.theme = self.current_theme['EventStart']

    def to_svg(self, node_id, node_data):
        info('....processing node [{0}] ...'.format(node_id))

        # a start event is circle. get a list of svg where the first one is the node circle
        svg_list = self.node_svgs(node_data)

        # assemble the two svg's into a final one
        svg_element = self.assemble_element(node_id, svg_list[0])

        info('....processing node [{0}] DONE ...'.format(node_id))
        return svg_element

    def node_svgs(self, node_data):
        # get the inner svg's in a list
        circle_svg = Circle(cx=self.theme['outer-circle']['radius'], cy=self.theme['outer-circle']['radius'], r=self.theme['outer-circle']['radius'])
        circle_svg.set_style(StyleBuilder(self.theme['outer-circle']['style']).getStyle())

        return [circle_svg]

    def assemble_element(self, node_id, circle_svg):
        # wrap it in a svg group
        group_id = 'node-{0}'.format(node_id)
        svg_group = G(id=group_id)

        # place the node circle
        svg_group.addElement(circle_svg)

        group_width = circle_svg.get_r() * 2
        group_height = circle_svg.get_r() * 2

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}
        return SvgElement(group_specs, svg_group)
