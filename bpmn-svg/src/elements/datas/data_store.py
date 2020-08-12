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

from elements.svg_element import SvgElement
from elements.datas.data_object import DataObject

class DataStore(DataObject):
    def __init__(self, bpmn_id, lane_id, pool_id, node_id, node_data):
        super().__init__(bpmn_id, lane_id, pool_id, node_id, node_data)
        self.theme = {**self.theme, **self.current_theme['datas']['DataStore']}

    def to_svg(self):
        info('......processing node [{0}:{1}:{2}:{3}]'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))

        # the label element
        label_group, label_group_width, label_group_height = text_inside_a_rectangle(
                                    text=self.node_data['label'],
                                    min_width=self.theme['rectangle']['min-width'],
                                    max_width=self.theme['rectangle']['max-width'],
                                    rect_spec=self.theme['rectangle'],
                                    text_spec=self.theme['text'])

        # the data store svg
        data_store_group, data_store_group_width, data_store_group_height = include_and_scale_svg(spec=self.theme['shape-spec'])

        # wrap them in a svg group -----------------------------------------------------------------
        svg_group = G(id=self.group_id)

        # the folded rectangle is below an empty space of the same height of the label
        d_x = max((label_group_width - data_store_group_width)/2, 0)
        # debug(label_group_width)
        # debug(label_group_height)
        # debug(data_store_group_width)
        # debug(data_store_group_height)
        # debug(d_x)
        data_store_group_xy = '{0},{1}'.format((label_group_width - data_store_group_width)/2, label_group_height + self.snap_point_offset)
        transformer = TransformBuilder()
        transformer.setTranslation(data_store_group_xy)
        data_store_group.set_transform(transformer.getTransform())

        # the label is vertically below the folded rectangle
        label_group_xy = '{0},{1}'.format(0, label_group_height + self.snap_point_offset + data_store_group_height)
        transformer = TransformBuilder()
        transformer.setTranslation(label_group_xy)
        label_group.set_transform(transformer.getTransform())

        # place the elements
        svg_group.addElement(data_store_group)
        svg_group.addElement(label_group)

        # extend the height so that a blank space of the same height as text is at the bottom so that the circle's left edge is at dead vertical center
        group_width = label_group_width
        group_height = label_group_height + self.snap_point_offset + data_store_group_height + self.snap_point_offset + label_group_height

        # snap points
        snap_points = self.snap_points(group_width, group_height)
        self.snap_offset_x = (label_group_width - data_store_group_width)/2 + self.snap_point_offset
        self.snap_offset_y = label_group_height + self.snap_point_offset * 2
        self.draw_snaps(snap_points, svg_group, x_offset=self.snap_offset_x, y_offset=self.snap_offset_y)

        info('......processing node [{0}:{1}:{2}:{3}] DONE'.format(self.bpmn_id, self.lane_id, self.pool_id, self.node_id))
        self.svg_element = SvgElement(svg=svg_group, width=group_width, height=group_height, snap_points=snap_points, label_pos='bottom')
        return self.svg_element
