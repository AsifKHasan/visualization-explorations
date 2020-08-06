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

class Gateway(BpmnElement):
    # a Gateway is a diamond with label outside the diamond, either on the top or at the bottom
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.theme = self.current_theme['gateways']['Gateway']
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.group_id = 'N-{0}:{1}:{2}:{3}'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id)

    def to_svg(self):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # the label group
        label_group, label_group_width, label_group_height = text_inside_a_rectangle(
                                                                text=self.node_data['label'],
                                                                min_width=self.theme['rectangle']['min-width'],
                                                                max_width=self.theme['rectangle']['max-width'],
                                                                rect_spec=self.theme['rectangle'],
                                                                text_spec=self.theme['text'])

        # the diamond element
        diamond_group, diamond_group_width, diamond_group_height = a_diamond(
                                                                    diagonal_x=self.theme['diamond']['diagonal-x'],
                                                                    diagonal_y=self.theme['diamond']['diagonal-y'],
                                                                    spec=self.theme['diamond'])

        # the inside element
        inside_element = self.get_inside_element()

        # if an element is to be placed inside the diamond group, place it so that the inside object's center and the diamond's center is same
        if inside_element is not None:
            inside_group, inside_group_width, inside_group_height = inside_element.svg, inside_element.width, inside_element.height
            inside_group_xy = '{0},{1}'.format((diamond_group_width - inside_group_width)/2, (diamond_group_height - inside_group_height)/2)
            transformer = TransformBuilder()
            transformer.setTranslation(inside_group_xy)
            inside_group.set_transform(transformer.getTransform())
            diamond_group.addElement(inside_group)

        # wrap it in a svg group
        svg_group = G(id=self.group_id)

        # the diamond is to be positioned vertically after the rect_svg and center should be the center of the rect_svg
        diamond_group_xy = '{0},{1}'.format((label_group_width - diamond_group_width)/2, label_group_height)
        transformer = TransformBuilder()
        transformer.setTranslation(diamond_group_xy)
        diamond_group.set_transform(transformer.getTransform())

        # place the elements
        svg_group.addElement(label_group)
        svg_group.addElement(diamond_group)

        # extend the height so that a blank space of the same height as text is at the bottom so that the diamond left edge is at dead vertical center
        group_width = label_group_width
        group_height = label_group_height + diamond_group_height + label_group_height

        # snap points
        snap_points = self.snap_points(group_width, group_height, (label_group_width - diamond_group_width)/2, label_group_height)
        self.draw_snaps(snap_points, svg_group)

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        self.svg_element =  SvgElement(svg=svg_group, width=group_width, height=group_height, snap_points=snap_points, label_pos='top')
        return self.svg_element

    def snap_points(self, width, height, x_offset, y_offset):
        snaps = {
            'north': {
                'middle': {
                    'point': Point(width * 0.5, y_offset),
                    'edge-roles': []
                },
            },
            'south': {
                'middle': {
                    'point': Point(width * 0.5, height - y_offset),
                    'edge-roles': []
                },
            },
            'east': {
                'middle': {
                    'point': Point(width - x_offset, height * 0.5),
                    'edge-roles': []
                },
            },
            'west': {
                'middle': {
                    'point': Point(x_offset, height * 0.5),
                    'edge-roles': []
                },
            }
        }

        return snaps

    def get_inside_element(self):
        return None
