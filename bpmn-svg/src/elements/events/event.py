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

class Event(BpmnElement):
    # an event is a circle
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.theme = self.current_theme['events']['Event']
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.group_id = 'N-{0}:{1}:{2}:{3}'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id)

    def to_svg(self):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # the label element
        label_group, label_group_width, label_group_height = rectangle_with_text_inside(
                                    text=self.node_data['label'],
                                    min_width=self.theme['rectangle']['min-width'],
                                    max_width=self.theme['rectangle']['max-width'],
                                    rect_specs=self.theme['rectangle'],
                                    text_specs=self.theme['text'])

        # the circle element
        if 'inner-circle' in self.theme:
            circle_group, circle_group_width, circle_group_height = two_concentric_circles(outer_radius=self.theme['circle']['radius'], inner_radius=self.theme['inner-circle']['radius'], outer_style=self.theme['circle']['style'], inner_style=self.theme['inner-circle']['style'])
        else:
            circle_group, circle_group_width, circle_group_height = a_circle(radius=self.theme['circle']['radius'], style=self.theme['circle']['style'])

        # get the inside element
        inside_element = self.get_inside_element()

        # if an inside element is to be placed inside the circle group, place it so that the inside object's center and the circle's center is same
        if inside_element is not None:
            inside_group, inside_group_width, inside_group_height = inside_element.group, inside_element.specs['width'], inside_element.specs['height']
            inside_group_xy = '{0},{1}'.format((circle_group_width - inside_group_width)/2, (circle_group_height - inside_group_height)/2)
            transformer = TransformBuilder()
            transformer.setTranslation(inside_group_xy)
            inside_group.set_transform(transformer.getTransform())
            circle_group.addElement(inside_group)

        # wrap it in a svg group
        svg_group = G(id=self.group_id)

        # the circle is vertically below the label
        circle_group_xy = '{0},{1}'.format((label_group_width - circle_group_width)/2, label_group_height)
        transformer = TransformBuilder()
        transformer.setTranslation(circle_group_xy)
        circle_group.set_transform(transformer.getTransform())

        # place the elements
        svg_group.addElement(label_group)
        svg_group.addElement(circle_group)

        # extend the height so that a blank space of the same height as text is at the bottom so that the circle's left edge is at dead vertical center
        group_width = label_group_width
        group_height = label_group_height + circle_group_height + label_group_height

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        return SvgElement({'width': group_width, 'height': group_height}, svg_group)

    def get_inside_element(self):
        return None
