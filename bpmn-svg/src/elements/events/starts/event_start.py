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
    # a start event is circle. get a list of svg where the first one is the node circle
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data, non_interrupting=False):
        self.theme = self.current_theme['events']['starts']['EventStart']
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.group_id = 'N-{0}:{1}:{2}:{3}'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id)
        self.non_interrupting = non_interrupting

    def to_svg(self, element_inside_circle_group=None):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # the label element
        label_group, label_group_width, label_group_height = rectangle_with_text_inside(
                                    text=self.node_data['label'],
                                    min_width=self.theme['text-rect']['min-width'],
                                    max_width=self.theme['text-rect']['max-width'],
                                    specs=self.theme['text-rect'])

        # the circle element
        if self.non_interrupting:
            circle_group, circle_group_width, circle_group_height = circle(radius=self.theme['outer-circle-non-interrupting']['radius'], style=self.theme['outer-circle-non-interrupting']['style'])
        else:
            circle_group, circle_group_width, circle_group_height = circle(radius=self.theme['outer-circle']['radius'], style=self.theme['outer-circle']['style'])

        # if an element was passed to be placed inside the circle group, place it so that the inside object's center and the circle's center is same
        if element_inside_circle_group is not None:
            inside_group, inside_group_width, inside_group_height = element_inside_circle_group.group, element_inside_circle_group.specs['width'], element_inside_circle_group.specs['height']
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
