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

EDGE_TYPE = {
    '-->' : 'Sequence',
    '~~>' : 'Message',
    '...' : 'Association',
    '..>' : 'DirectedAssociation',
    '<.>' : 'BidirectionalAssociation',
}

class BpmnElement():
    theme = None
    # the logical snap points are drawn out away from the actual shape for nice edge visuals
    snap_point_offset = 12

    def to_svg(self, theme):
        return None

    def label_position(self):
        pass

    def switch_label_position(self):
        pass

    '''
        path from snap point to the exact point of the node in node coordinates
        for Gateways, Events, Datas snap points may lie outside the inner Circle, diamond, folded rectangle as they have labels wider than the shape which takes space on top and bottom
    '''
    def to_snap_point(self, side, position, role, direction_hint, peer, edge_type):
        if side is None or role is None:
            return []

        points = []

        # east and west are easier, we just get the point inside
        snap_position = self.svg_element.snap_points[side][position]
        snap_point = snap_position.point
        if side == 'east':
            # the actual point is to the left
            points = [snap_point, snap_point + Point(self.snap_offset_x * -1, 0)]

        elif side == 'west':
            # the actual point is to the right
            points = [snap_point, snap_point + Point(self.snap_offset_x * 1, 0)]

        elif side == 'north':
            # the actual point is below, whether we can go directly below depends on whether we have label on top and if there is any label or not
            if self.svg_element.label_pos is None or self.svg_element.label_pos in ['none', 'bottom', 'middle']:
                # we just go straight south, there is no label
                points = [snap_point, snap_point + Point(0, self.snap_offset_y)]
            elif self.svg_element.label_pos in ['top']:
                # we have a label in the direct path, we have to go roundabout, the roundabout may be from east of the label or west of the label depending on direction_hint
                if direction_hint in ['east']:
                    # we find a path along the eastern edge of the label
                    # move the start point to the eastern end + snap_point_offset
                    north_east_point = Point(self.svg_element.width + self.snap_point_offset, snap_point.y)
                    # move to southern edge vertically
                    south_east_point = Point(north_east_point.x, self.snap_offset_y - self.snap_point_offset * 2)
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
            if self.svg_element.label_pos is None or self.svg_element.label_pos in ['none', 'top', 'middle']:
                # we just go straight north, there is no label
                points = [snap_point, snap_point + Point(0, self.snap_offset_y * -1)]
            elif self.svg_element.label_pos in ['bottom']:
                # we have a label in the direct path, we have to go roundabout, the roundabout may be from east of the label or west of the label depending on direction_hint
                if direction_hint in ['east']:
                    # we find a path along the eastern edge of the label
                    # move the start point to the eastern end + snap_point_offset
                    south_east_point = Point(self.svg_element.width + self.snap_point_offset, snap_point.y)
                    # move to northern edge vertically
                    north_east_point = Point(south_east_point.x, south_east_point.y - (self.snap_offset_y - self.snap_point_offset))
                    # move to west to the original x position of the snap_point
                    just_below_snap_point = Point(snap_point.x, north_east_point.y)
                    # move to final internal snap point
                    final_snap_point = Point(snap_point.x, just_below_snap_point.y - self.snap_point_offset)

                    points = [south_east_point, north_east_point, just_below_snap_point, final_snap_point]

                else:
                    # we find a path along the western edge of the label
                    # move the start point to the western end + snap_point_offset
                    south_west_point = Point(self.snap_point_offset * -2, snap_point.y)
                    # move to northern edge vertically
                    north_west_point = Point(south_west_point.x, south_west_point.y - (self.snap_offset_y - self.snap_point_offset))
                    # move to west to the original x position of the snap_point
                    just_below_snap_point = Point(snap_point.x, north_west_point.y)
                    # move to final internal snap point
                    final_snap_point = Point(snap_point.x, just_below_snap_point.y - self.snap_point_offset)

                    points = [south_west_point, north_west_point, just_below_snap_point, final_snap_point]
                    debug('Direction hint: {0}'.format(direction_hint))

        else:
            return [snap_point]

        # the points are calculated assuming the internal points are coming from snap-point to inside that is role is *to*
        if role == 'from':
            points.reverse()


        # see if the snap points are occupied or not
        if len(snap_position.edge_roles) > 0:
            # TODO: occupied, do something
            # warn('snap-point {0:>30}:{1}-{2} is occupied ... we may want to do something about it'.format(self.node_id, side.upper(), position.upper()))
            pass

        # this snap point is getting a new edge-role
        snap_position.edge_roles.append(EdgeRole(role=role, peer=peer, type=edge_type))

        return points

    def snap_points(self, width, height):
        # a snap point may have zero or more edge roles meaning how many edge connections are there to this snap point
        # an edge-role is a dictionary that looks like {'role': 'from|to', 'peer-node': '[lane]:[pool]:[channel-name]:node_id', 'edge-type': 'edge-type'}
        snaps = {
            'north': {'middle': SnapPoint(point=Point(width * 0.5, self.snap_point_offset * -1))},
            'south': { 'middle': SnapPoint(point=Point(width * 0.5, height + self.snap_point_offset * 1)) },
            'east': {'middle': SnapPoint(point=Point(width + self.snap_point_offset * 1, height * 0.5)) },
            'west': {'middle': SnapPoint(point=Point(self.snap_point_offset * -1, height * 0.5)) },
        }

        return snaps

    def draw_snaps(self, snaps, svg_group, x_offset, y_offset):
        offset_multiplier = {'north': Point(0, 1), 'south': Point(0, -1), 'east': Point(-1, 0), 'west': Point(1, 0)}
        for side in snaps:
            for position in snaps[side]:
                snap_point_group, snap_point_width, snap_point_height = a_snap_point(snaps[side][position].point + Point(x_offset, y_offset).scale(offset_multiplier[side]))
                svg_group.addElement(snap_point_group)


''' ----------------------------------------------------------------------------------------------------------------------------------
    Node Object
'''
class NodeObject:
    def __init__(self, id, category, type, styles, element, instance):
        self.id = id
        self.category = category
        self.type = type
        self.styles = styles
        self.element = element
        self.instance = instance


''' ----------------------------------------------------------------------------------------------------------------------------------
    snap point for a node
'''
class SnapPoint:
    def __init__(self, point):
        self.point = point
        self.edge_roles = []


''' ----------------------------------------------------------------------------------------------------------------------------------
    EdgeRole object for node snap-points
'''
class EdgeRole:
    def __init__(self, role, peer, type):
        self.role = role
        self.peer = peer
        self.type = type
