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
        label_group, label_group_width, label_group_height = text_inside_a_rectangle(
                                    text=self.node_data['label'],
                                    min_width=self.theme['rectangle']['min-width'],
                                    max_width=self.theme['rectangle']['max-width'],
                                    rect_spec=self.theme['rectangle'],
                                    text_spec=self.theme['text'])

        if self.node_data['label'] is None or self.node_data['label'] == '':
            label_pos = 'none'
        else:
            label_pos = 'top'

        # the circle element
        if 'inner-circle' in self.theme:
            circle_group, circle_group_width, circle_group_height = two_concentric_circles(outer_radius=self.theme['circle']['radius'], inner_radius=self.theme['inner-circle']['radius'], outer_circle_spec=self.theme['circle'], inner_circle_spec=self.theme['inner-circle'])
        else:
            circle_group, circle_group_width, circle_group_height = a_circle(radius=self.theme['circle']['radius'], spec=self.theme['circle'])

        # get the inside element
        inside_element = self.get_inside_element()

        # if an inside element is to be placed inside the circle group, place it so that the inside object's center and the circle's center is same
        if inside_element is not None:
            inside_group, inside_group_width, inside_group_height = inside_element.svg, inside_element.width, inside_element.height
            inside_group_xy = '{0},{1}'.format((circle_group_width - inside_group_width)/2, (circle_group_height - inside_group_height)/2)
            transformer = TransformBuilder()
            transformer.setTranslation(inside_group_xy)
            inside_group.set_transform(transformer.getTransform())
            circle_group.addElement(inside_group)

        # wrap it in a svg group
        svg_group = G(id=self.group_id)

        # the circle is vertically below the label, keep a gap of *snap_point_offset*
        circle_group_xy = '{0},{1}'.format((label_group_width - circle_group_width)/2, label_group_height + self.snap_point_offset)
        transformer = TransformBuilder()
        transformer.setTranslation(circle_group_xy)
        circle_group.set_transform(transformer.getTransform())

        # place the elements
        svg_group.addElement(label_group)
        svg_group.addElement(circle_group)

        # extend the height so that a blank space of the same height as text is at the bottom so that the circle's left edge is at dead vertical center
        group_width = label_group_width
        group_height = label_group_height + self.snap_point_offset + circle_group_height + self.snap_point_offset + label_group_height
        
        # snap points
        snap_points = self.snap_points(group_width, group_height)
        self.snap_offset_x = (label_group_width - circle_group_width)/2 + self.snap_point_offset
        self.snap_offset_y = label_group_height + self.snap_point_offset * 2
        self.draw_snaps(snap_points, svg_group, x_offset=self.snap_offset_x, y_offset=self.snap_offset_y)

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        self.svg_element = SvgElement(svg=svg_group, width=group_width, height=group_height, snap_points=snap_points, label_pos=label_pos)
        return self.svg_element

    def get_inside_element(self):
        return None
