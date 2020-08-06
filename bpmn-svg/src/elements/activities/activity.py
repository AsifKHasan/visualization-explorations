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

class Activity(BpmnElement):
    # a task activity is a rounded rectangle with a text inside
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        self.theme = self.current_theme['activities']['Activity']
        self.bpmn_id, self.lane_id, self.pool_id, self.node_id, self.node_data = bpmn_id, lane_id, pool_id, node_id, node_data
        self.group_id = 'N-{0}:{1}:{2}:{3}'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id)

    def to_svg(self):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # the rectangle element
        rectangle_group, rectangle_group_width, rectangle_group_height = text_inside_a_rectangle(
                                    text=self.node_data['label'],
                                    min_width=self.theme['rectangle']['min-width'],
                                    max_width=self.theme['rectangle']['max-width'],
                                    rect_spec=self.theme['rectangle'],
                                    text_spec=self.theme['text'])

        # get the inside bottom center element
        bottom_center_element = self.get_bottom_center_element()

        # if an inside bottom center element is to be placed, the element should have a gap from the rectangle bottom
        if bottom_center_element is not None:
            bottom_center_group, bottom_center_group_width, bottom_center_group_height = bottom_center_element.svg, bottom_center_element.width, bottom_center_element.height
            bottom_center_group_xy = '{0},{1}'.format((rectangle_group_width - bottom_center_group_width)/2, rectangle_group_height - bottom_center_group_height - self.theme['rectangle']['inner-shape-margin-spec']['bottom'])
            transformer = TransformBuilder()
            transformer.setTranslation(bottom_center_group_xy)
            bottom_center_group.set_transform(transformer.getTransform())
            rectangle_group.addElement(bottom_center_group)

        # get the inside top left element
        top_left_element = self.get_top_left_element()

        # if an inside bottom center element is to be placed, the element should have a gap from the rectangle bottom
        if top_left_element is not None:
            top_left_group, top_left_group_width, top_left_group_height = top_left_element.svg, top_left_element.width, top_left_element.height
            top_left_group_xy = '{0},{1}'.format(self.theme['rectangle']['inner-shape-margin-spec']['left'], self.theme['rectangle']['inner-shape-margin-spec']['top'])
            transformer = TransformBuilder()
            transformer.setTranslation(top_left_group_xy)
            top_left_group.set_transform(transformer.getTransform())
            rectangle_group.addElement(top_left_group)

        # if there is an outer rectangle process that
        if 'outer-rectangle' in self.theme:
            rectangle_group, rectangle_group_width, rectangle_group_height = envelop_and_center_in_a_rectangle(
                                                                                svg=rectangle_group,
                                                                                svg_width=rectangle_group_width,
                                                                                svg_height=rectangle_group_height,
                                                                                rect_spec=self.theme['outer-rectangle'])

        # snap points
        snap_points = self.snap_points(rectangle_group_width, rectangle_group_height)
        self.draw_snaps(snap_points, rectangle_group)

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        self.svg_element = SvgElement(svg=rectangle_group, width=rectangle_group_width, height=rectangle_group_height, snap_points=snap_points, label_pos='middle')
        return self.svg_element

    def snap_points(self, width, height):
        # a snap point may have zero or more edge roles meaning how many edge connections are there to this snap point
        # an edge-role is a dictionary that looks like {'role': 'head|tail', 'peer-node': '[lane]:[pool]:[channel-name]:node_id', 'edge-type': 'edge-type'}
        snaps = {
            'north': {
                'middle': {
                    'point': Point(width * 0.5, 0),
                    'edge-roles': []
                },
                'left': {
                    'point': Point(width * 0.25, 0),
                    'edge-roles': []
                },
                'right': {
                    'point': Point(width * 0.75, 0),
                    'edge-roles': []
                },
            },
            'south': {
                'middle': {
                    'point': Point(width * 0.5, height),
                    'edge-roles': []
                },
                'left': {
                    'point': Point(width * 0.25, height),
                    'edge-roles': []
                },
                'right': {
                    'point': Point(width * 0.75, height),
                    'edge-roles': []
                },
            },
            'east': {
                'middle': {
                    'point': Point(width, height * 0.5),
                    'edge-roles': []
                },
                'top': {
                    'point': Point(width, height * 0.25),
                    'edge-roles': []
                },
                'bottom': {
                    'point': Point(width, height * 0.75),
                    'edge-roles': []
                },
            },
            'west': {
                'middle': {
                    'point': Point(0, height * 0.5),
                    'edge-roles': []
                },
                'top': {
                    'point': Point(0, height * 0.25),
                    'edge-roles': []
                },
                'bottom': {
                    'point': Point(0, height * 0.75),
                    'edge-roles': []
                },
            }
        }

        return snaps

    def label_position(self):
        return 'middle'

    def switch_label_position(self):
        pass

    def get_top_left_element(self):
        return None

    def get_bottom_center_element(self):
        return None
