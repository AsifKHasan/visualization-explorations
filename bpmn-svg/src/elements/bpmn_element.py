#!/usr/bin/env python3
'''
    returns a SvgElement
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

from elements import *

class BpmnElement():
    current_theme = default_theme
    # the logical snap points are drawn out away from the actual shape for nice edge visuals
    snap_point_offset = 12

    def to_svg(self):
        return None

    def label_position(self):
        pass

    def switch_label_position(self):
        pass

    # for Gateways, Events, Datas snap points may lie outside the innser Circle, diamond, folded rectangle as they have labels wider than the shape and taking space on top and bottom
    def inner_points_for_snapping(self, side=None, position='middle', role='from', direction_hint=None):
        if side is None or role is None:
            return []

        points = []

        # east and west are easier, we just get the point inside
        snap_point = self.svg_element.snap_points[side][position]['point']
        if side == 'east':
            # the actual point is to the left
            points = [snap_point, snap_point + Point(self.snap_offset_x * -1, 0)]

        elif side == 'west':
            # the actual point is to the right
            points = [snap_point, snap_point + Point(self.snap_offset_x * 1, 0)]

        elif side == 'north':
            # the actual point is below, whether we can go directly below depends on whether we have label on top and if there is any label or not
            if self.svg_element.label_pos in ['none', 'bottom']:
                # we just go straight south, there is no label
                points = [snap_point, snap_point + Point(0, self.snap_offset_y)]
            elif self.svg_element.label_pos in ['top']:
                # we have a label in the direct path, we have to go roundabout, the roundabout may be from east of the label or west of the label depending on direction_hint
                if direction_hint in ['east']:
                    # we find a path along the eastern edge of the label
                    # move the start point to the eastern end + snap_point_offset
                    north_east_point = Point(self.svg_element.width + self.snap_point_offset, snap_point.y)
                    # move to southern edge vertically
                    south_east_point = Point(north_east_point.x, self.snap_offset_y)
                    # move to west to the original x position of the snap_point
                    just_above_snap_point = Point(snap_point.x, south_east_point.y)
                    # move to final internal snap point
                    final_snap_point = Point(snap_point.x, just_above_snap_point.y + self.snap_point_offset)

                    points = [north_east_point, south_east_point, just_above_snap_point, final_snap_point]

                else:
                    # we find a path along the western edge of the label
                    # move the start point to the western end - snap_point_offset
                    north_west_point = Point(self.snap_point_offset * -2, snap_point.y)
                    # move to southern edge vertically
                    south_west_point = Point(north_west_point.x, self.snap_offset_y - self.snap_point_offset * 2)
                    # move to east to the original x position of the snap_point
                    just_above_snap_point = Point(snap_point.x, south_west_point.y)
                    # move to final internal snap point
                    final_snap_point = Point(snap_point.x, just_above_snap_point.y + self.snap_point_offset)

                    points = [north_west_point, south_west_point, just_above_snap_point, final_snap_point]

        elif side == 'south':
            # the actual point is above, whether we can go directly above depends on whether we have label below and if there is any label or not
            if self.svg_element.label_pos in ['none', 'top']:
                # we just go straight north, there is no label
                points = [snap_point, snap_point + Point(0, self.snap_offset_y * -1)]
            elif self.svg_element.label_pos in ['bottom']:
                # we have a label in the direct path, we have to go roundabout, the roundabout may be from east of the label or west of the label depending on direction_hint
                if direction_hint in ['east']:
                    # we find a path along the eastern edge of the label
                    pass
                else:
                    # we find a path along the western edge of the label
                    pass

        else:
            return [snap_point]

        # the points are calculated assuming the internal points are coming from snap-point to inside that is role is *to*
        if role == 'from':
            points.reverse()

        return points

    def snap_points(self, width, height):
        # a snap point may have zero or more edge roles meaning how many edge connections are there to this snap point
        # an edge-role is a dictionary that looks like {'role': 'from|to', 'peer-node': '[lane]:[pool]:[channel-name]:node_id', 'edge-type': 'edge-type'}
        snaps = {
            'north': {
                'middle': {
                    'point': Point(width * 0.5, self.snap_point_offset * -1),
                    'edge-roles': []
                },
            },
            'south': {
                'middle': {
                    'point': Point(width * 0.5, height + self.snap_point_offset * 1),
                    'edge-roles': []
                },
            },
            'east': {
                'middle': {
                    'point': Point(width + self.snap_point_offset * 1, height * 0.5),
                    'edge-roles': []
                },
            },
            'west': {
                'middle': {
                    'point': Point(self.snap_point_offset * -1, height * 0.5),
                    'edge-roles': []
                },
            }
        }

        return snaps

    def draw_snaps(self, snaps, svg_group, x_offset, y_offset):
        offset_multiplier = {'north': Point(0, 1), 'south': Point(0, -1), 'east': Point(-1, 0), 'west': Point(1, 0)}
        for side in snaps:
            for position in snaps[side]:
                snap_point_group, snap_point_width, snap_point_height = a_snap_point(snaps[side][position]['point'] + Point(x_offset, y_offset).scale(offset_multiplier[side]))
                svg_group.addElement(snap_point_group)
