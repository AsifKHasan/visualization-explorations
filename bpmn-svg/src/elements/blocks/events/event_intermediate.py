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

class EventIntermediate(BpmnElement):
    # an intermediate event is two concentric circles
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.theme = self.current_theme['EventIntermediate']
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.group_id = 'N-{0}:{1}:{2}:{3}'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id)

    def to_svg(self):
        # collect the node elements/svgs
        self.collect_elements()

        # tune the node
        self.tune_elements()

        # assemble the elements/svgs into a final one
        svg_element = self.assemble_elements()
        return svg_element

    def collect_elements(self):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # get the inner svg's in a list
        self.node_svgs = rect_with_text(
                                    text=self.node_data['label'],
                                    min_width=self.theme['text-rect']['min-width'],
                                    max_width=self.theme['text-rect']['max-width'],
                                    specs=self.theme['text-rect'])

        # get the inner svg's in a list
        self.node_circle()

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

    def node_circle(self):
        svg_group = G()

        # outer circle
        outer_circle = Circle(cx=self.theme['outer-circle']['radius'], cy=self.theme['outer-circle']['radius'], r=self.theme['outer-circle']['radius'])
        outer_circle.set_style(StyleBuilder(self.theme['outer-circle']['style']).getStyle())

        # inner circle
        inner_circle = Circle(cx=self.theme['outer-circle']['radius'], cy=self.theme['outer-circle']['radius'], r=self.theme['inner-circle']['radius'])
        inner_circle.set_style(StyleBuilder(self.theme['inner-circle']['style']).getStyle())

        # add to group
        svg_group.addElement(outer_circle)
        svg_group.addElement(inner_circle)

        group_width = self.theme['outer-circle']['radius'] * 2
        group_height = self.theme['outer-circle']['radius'] * 2

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}
        self.node_svgs.append(SvgElement(group_specs, svg_group))

    def assemble_elements(self):
        info('......assembling node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # wrap it in a svg group
        svg_group = G(id=self.group_id)

        # place the node circle
        rect_svg = self.node_svgs[0]
        text_svg = self.node_svgs[1]
        circle_svg_element = self.node_svgs[2]
        circle_svg = circle_svg_element.group

        # the circle is vertically below the label
        circle_svg_xy = '{0},{1}'.format((rect_svg.get_width() - circle_svg_element.specs['width'])/2, rect_svg.get_height())
        transformer = TransformBuilder()
        transformer.setTranslation(circle_svg_xy)
        circle_svg.set_transform(transformer.getTransform())

        # place the node rect
        svg_group.addElement(rect_svg)

        # place the node text
        svg_group.addElement(text_svg)

        # place the diamond
        svg_group.addElement(circle_svg)

        # extend the height so that a blank space of the same height as text is at the bottom so that the circle's left edge is at dead vertical center
        group_width = rect_svg.get_width()
        group_height = rect_svg.get_height() + circle_svg_element.specs['height'] + rect_svg.get_height()

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}

        info('......assembling node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        return SvgElement(group_specs, svg_group)

    def tune_elements(self):
        info('......tuning node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        info('......tuning node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
