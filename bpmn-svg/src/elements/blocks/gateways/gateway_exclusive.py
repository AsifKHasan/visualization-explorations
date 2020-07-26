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
from util.geometry import Point

from elements.bpmn_element import BpmnElement
from elements.svg_element import SvgElement

class GatewayExclusive(BpmnElement):
    # an exclusive Gateway is a diamond with a X inside the diamond and label outside the diamong either on top or bottom
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.theme = self.current_theme['GatewayExclusive']
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

        self.node_diamond()

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

    def node_diamond(self):
        svg_group = G()

        # make the diamond
        diagonal = self.theme['diamond']['diagonal']
        points = [Point(0, diagonal/2), Point(diagonal/2, 0), Point(diagonal, diagonal/2), Point(diagonal/2, diagonal), Point(0, diagonal/2)]
        diamond_svg = Polyline(points=points_to_str(points))
        diamond_svg.set_style(StyleBuilder(self.theme['diamond']['style']).getStyle())

        # make the X inside the diamond
        line1_svg = Line(x1=diagonal * 0.33, y1=diagonal * 0.33, x2=diagonal * 0.67, y2=diagonal * 0.67)
        line1_svg.set_style(StyleBuilder(self.theme['diamond']['inner-shape-style']).getStyle())

        line2_svg = Line(x1=diagonal * 0.67, y1=diagonal * 0.33, x2=diagonal * 0.33, y2=diagonal * 0.67)
        line2_svg.set_style(StyleBuilder(self.theme['diamond']['inner-shape-style']).getStyle())

        # add to group
        svg_group.addElement(diamond_svg)
        svg_group.addElement(line1_svg)
        svg_group.addElement(line2_svg)

        group_width = diagonal
        group_height = diagonal

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}
        self.node_svgs.append(SvgElement(group_specs, svg_group))

    def assemble_elements(self):
        info('......assembling node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # wrap it in a svg group
        svg_group = G(id=self.group_id)

        rect_svg = self.node_svgs[0]
        text_svg = self.node_svgs[1]
        diamond_svg_element = self.node_svgs[2]
        diamond_svg = diamond_svg_element.group

        # the diamond is to be positioned vertically after the rect_svg and center should be the center of the rect_svg
        diamond_svg_xy = '{0},{1}'.format((rect_svg.get_width() - diamond_svg_element.specs['width'])/2, rect_svg.get_height())
        transformer = TransformBuilder()
        transformer.setTranslation(diamond_svg_xy)
        diamond_svg.set_transform(transformer.getTransform())

        # place the node rect
        svg_group.addElement(rect_svg)

        # place the node text
        svg_group.addElement(text_svg)

        # place the diamond
        svg_group.addElement(diamond_svg)

        # extend the height so that a blank space of the same height as text is at the bottom so that the diamond left edge is at dead vertical center
        group_width = rect_svg.get_width()
        group_height = rect_svg.get_height() + diamond_svg_element.specs['height'] + rect_svg.get_height()

        # wrap it in a svg element
        group_specs = {'width': group_width, 'height': group_height}

        info('......assembling node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        return SvgElement(group_specs, svg_group)

    def tune_elements(self):
        info('......tuning node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        info('......tuning node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
