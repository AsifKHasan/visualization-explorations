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

class ActivityTask(BpmnElement):
    def __init__(self):
        self.theme = self.current_theme['ActivityTask']

    def to_svg(self, node_id, node_data):
        info('....processing node [{0}] ...'.format(node_id))

        # a task activity is a rounded rectangle with a text inside

        # get the svg element with the text inside a rect
        # we get a list of svg where the first one is the rect and the second one is the text
        svg_list = self.node_svgs(node_data)

        # assemble the two svg's into a final one
        svg_element = self.assemble_element(node_id, svg_list[0], svg_list[1])

        info('....processing node [{0}] DONE ...'.format(node_id))
        return svg_element

    def node_svgs(self, node_data):
        # get the inner svg's in a list
        svg_list = rect_with_text(
                                    text=node_data['label'],
                                    min_width=self.theme['text-rect']['min-width'],
                                    max_width=self.theme['text-rect']['max-width'],
                                    specs=self.theme['text-rect'])

        return svg_list

    def assemble_element(self, node_id, rect_svg, text_svg):
        # wrap it in a svg group
        group_id = 'node-{0}'.format(node_id)
        svg_group = G(id=group_id)

        # place the node rect
        svg_group.addElement(rect_svg)

        # place the node text
        svg_group.addElement(text_svg)

        group_width = rect_svg.get_width()
        group_height = rect_svg.get_height()

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}
        return SvgElement(group_specs, svg_group)
