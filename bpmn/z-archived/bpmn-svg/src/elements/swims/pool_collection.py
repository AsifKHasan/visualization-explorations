#!/usr/bin/env python3
'''
'''
from pprint import pprint

from pysvg.structure import *
from pysvg.builders import *

from util.geometry import Point
from util.logger import *

from elements.bpmn_element import BpmnElement, EDGE_TYPE
from elements.svg_element import SvgElement

from elements.swims.swim_pool import SwimPool
from elements.flows.flow_object import EdgeObject
from elements.flows.lane_flow import LaneFlow

'''
    a pool collection is a vertical stack of pools
'''
class PoolCollection(BpmnElement):
    def __init__(self, current_theme, bpmn_id, lane_id, pools, edges):
        self.current_theme = current_theme
        self.theme = self.current_theme['swims']['PoolCollection']
        self.bpmn_id, self.lane_id, self.pools, self.edges = bpmn_id, lane_id, pools, edges

    def lay_edges(self):
        # first lay the intra-pool edges
        for child_pool_class in self.child_pool_classes:
            child_pool_class.lay_edges()

        # print(self.pool_collection)

        # lay inter-pool edges - get a filtered list of edges containing only those where from-node and to-node both are in this lane but are in different pools
        for edge in self.edges:
            from_node, to_node = self.pool_collection.get_if_from_different_pools(edge['from'], edge['to'])
            if from_node is not None and to_node is not None:
                edge_type = EDGE_TYPE[edge['type']]
                edge_label = edge.get('label', None)
                edge_style = edge.get('styles', None)

                # create an appropriate flow object, use LaneFlow which manages flows inside a SwimLane
                flow_object = LaneFlow(self.current_theme, edge_type, self.pool_collection)
                flow_svg_element = flow_object.create_flow(from_node, to_node, edge_label, edge_style)

                # add to channel svg group
                if flow_svg_element is not None and flow_svg_element.svg is not None:
                    self.pool_collection.element.svg.addElement(flow_svg_element.svg)

                    # store object for future reference
                    self.pool_collection.edge_list.append(EdgeObject(edge=edge, type=edge_type, element=flow_svg_element))

    def assemble_labels(self):
        group_id = '{0}:{1}-pools-labels'.format(self.bpmn_id, self.lane_id)
        svg_group = G(id=group_id)

        group_width = 0
        transformer = TransformBuilder()
        for child_pool_class in self.child_pool_classes:
            child_label_element = child_pool_class.assemble_labels()
            if child_label_element is None:
                continue

            # the y position of this pool label in the group will be its corresponding swim-pool's y position
            child_label_xy = Point(0, child_pool_class.svg_element.xy.y)
            transformer.setTranslation(child_label_xy)
            child_label_element.svg.set_transform(transformer.getTransform())
            svg_group.addElement(child_label_element.svg)

            group_width = max(child_label_element.width, group_width)

        group_height = self.svg_element.height

        # wrap it in a svg element
        self.label_element = SvgElement(svg=svg_group, width=group_width, height=group_height)
        return self.label_element

    def collect_elements(self):
        info('..processing pools for [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # get the inner pool svg elements in a list
        self.child_pool_classes = []
        self.pool_collection = PoolCollectionObject(self.lane_id, self.theme)
        for pool_id, pool_data in self.pools.items():
            child_pool_class = SwimPool(self.current_theme, self.bpmn_id, self.lane_id, pool_id, pool_data)
            child_pool_class.collect_elements()
            # each child SwimPool's ChannelCollectionObject is a member of its own pool_collection
            self.pool_collection.channel_collection_list.append(child_pool_class.channel_collection_instance.channel_collection)
            self.child_pool_classes.append(child_pool_class)

        info('..processing pools for [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))

    def assemble_elements(self):
        info('..assembling pools for [{0}:{1}]'.format(self.bpmn_id, self.lane_id))

        # wrap it in a svg group
        group_id = '{0}:{1}-pools'.format(self.bpmn_id, self.lane_id)
        svg_group = G(id=group_id)

        # height of the pool collection is sum of height of all pools with gaps between pools
        max_pool_width = self.theme['pad-spec']['left']
        current_y = self.theme['pad-spec']['top']
        transformer = TransformBuilder()
        for child_pool_class in self.child_pool_classes:
            swim_pool_element = child_pool_class.assemble_elements()
            current_x = self.theme['pad-spec']['left'] + float(child_pool_class.pool_data['styles'].get('move_x', 0))
            swim_pool_element.xy = Point(current_x, current_y)
            transformer.setTranslation(swim_pool_element.xy)
            swim_pool_element.svg.set_transform(transformer.getTransform())
            svg_group.addElement(swim_pool_element.svg)

            max_pool_width = max(max_pool_width, current_x + swim_pool_element.width)
            current_y = current_y + swim_pool_element.height + self.theme['dy-between-pools']

        group_width = max_pool_width + self.theme['pad-spec']['right']
        group_height = current_y - self.theme['dy-between-pools'] + self.theme['pad-spec']['bottom']

        # add the ractangle
        pool_collection_rect_svg = Rect(width=group_width, height=group_height)
        pool_collection_rect_svg.set_style(StyleBuilder(self.theme['style']).getStyle())
        svg_group.addElement(pool_collection_rect_svg)

        # wrap it in a svg element
        self.svg_element = SvgElement(svg=svg_group, width=group_width, height=group_height)
        self.pool_collection.element = self.svg_element
        info('..assembling pools for [{0}:{1}] DONE'.format(self.bpmn_id, self.lane_id))
        return self.svg_element


''' ----------------------------------------------------------------------------------------------------------------------------------
    collection of channel-collections (pools)
'''
class PoolCollectionObject:

    def __init__(self, lane_id, theme):
        self.lane_id = lane_id
        self.theme = theme
        self.channel_collection_list = []
        self.edge_list = []
        self.element = None


    '''
        connects two points in a lane only through straight lines.
        a. The points are asumed to be outside a Pool's outer rectangle inside the routing area between pools
        b. point_from must be above point_to

        1. We start by trying to go straight to the same y position of *point_to* (let us call it *target_point*) so that we can draw a straight horizontal line from there to *point_to*
        2. but going straight to the *target_point* from *point_from* may not be possible as there may be a whole pools in between
        3. so, if there is a pool in between, we bypass the pool (by moving either to left or right) to the routing area east or west of the pool in the middle and now try to reach the *target_point* in a recursive manner
    '''
    def connect_southward(self, from_pool_number, point_from, to_pool_number, point_to):
        # see if there is one or more pools between the from-pool and to-pool
        if to_pool_number > from_pool_number + 1:
            # yes we have pools in between

            # we bypass the northmost (first) pool
            pool_number_to_bypass = from_pool_number + 1
            pool_to_bypass = self.channel_collection_list[pool_number_to_bypass]
            margin_spec = self.margin_spec(pool_number_to_bypass)
            points_to_bypass_the_pool = pool_to_bypass.bypass_vertically(coming_from=point_from, going_to=point_to, margin_spec=margin_spec)

            return [point_from] + points_to_bypass_the_pool + self.connect_southward(pool_number_to_bypass, points_to_bypass_the_pool[-1], to_pool_number, point_to)

        else:
            # there is no pool in between,
            if point_from.y == point_to.y:
                # they are on the same horizontal line - inside a pool routing area
                return [point_from, Point(point_from.x, point_to.y), point_to]
            else:
                # they are not on a line, we need a connecting path, looks like one or both of them are at eastern/western boundary
                # the north (point_from) needs to come down to southern boundary
                point_from_next = Point(point_from.x, self.channel_collection_list[from_pool_number].element.xy.y + self.channel_collection_list[from_pool_number].element.height + self.margin_spec(to_pool_number)['bottom'])

                # the south (point_to) needs to move up to northern boundary
                point_to_next = Point(point_to.x, self.channel_collection_list[to_pool_number].element.xy.y - self.margin_spec(to_pool_number)['top'])

                return [point_from, point_from_next, point_to_next, point_to]


    def outside_the_lane(self, lane_boundary, pool_boundary, pool_number, channel_boundary, channel, node, side, position, role, approach_snap_point_from, peer, edge_type, lane_margin_spec):
        # first get outside the lane
        points_in_lane_coordinate = self.outside_the_pool(pool_boundary, pool_number, channel_boundary, channel, node, side, position, role, approach_snap_point_from, peer, edge_type)

        # now get outside the lane (pool_collection) - to do so we we either go south or north depending on lane_boundary
        last_pool_number = len(self.channel_collection_list) - 1
        if lane_boundary == 'south':
            # we have to get to the southern boundary of the lane
            if role == 'from':
                the_point = Point(points_in_lane_coordinate[-1].x, self.element.height + lane_margin_spec['bottom'])
                the_points = self.connect_southward(pool_number, points_in_lane_coordinate[-1], last_pool_number, the_point)
            else:
                the_point = Point(points_in_lane_coordinate[0].x, self.element.height + lane_margin_spec['bottom'])
                the_points = self.connect_southward(pool_number, points_in_lane_coordinate[0], last_pool_number, the_point)

        elif lane_boundary == 'north':
            # we have to get to the northern boundary of the lane
            if role == 'from':
                the_point = Point(points_in_lane_coordinate[-1].x, -lane_margin_spec['top'])
                the_points = self.connect_southward(0, points_in_lane_coordinate[-1], pool_number, the_point)
            else:
                the_point = Point(points_in_lane_coordinate[0].x, -lane_margin_spec['top'])
                the_points = self.connect_southward(0, points_in_lane_coordinate[0], pool_number, the_point)

        elif lane_boundary == 'west':
            # we have to get to the western boundary of the lane
            if role == 'from':
                the_points = [Point(-lane_margin_spec['left'], points_in_lane_coordinate[-1].y)]
                # the_points = self.connect_southward(points_in_lane_coordinate[-1], the_point)
            else:
                the_points = [Point(-lane_margin_spec['left'], points_in_lane_coordinate[0].y)]
                # the_points = self.connect_southward(points_in_lane_coordinate[0], the_point)

        elif lane_boundary == 'east':
            # we have to get to the eastern boundary of the lane
            if role == 'from':
                the_points = [Point(self.element.width + lane_margin_spec['right'], points_in_lane_coordinate[-1].y)]
                # the_points = self.connect_southward(points_in_lane_coordinate[-1], the_point)
            else:
                the_points = [Point(self.element.width + lane_margin_spec['right'], points_in_lane_coordinate[0].y)]
                # the_points = self.connect_southward(points_in_lane_coordinate[0], the_point)

        else:
            # should never happen
            warn('lane boundary is unknown')
            return points_in_lane_coordinate

        # debug('{0} outside point for pool [{1}] xy: {2} ({3} x {4}) is at {5}'.format(pool_boundary, self.pool_id, self.element.xy, self.element.width, self.element.height, the_point))

        if role == 'to':
            return the_points + points_in_lane_coordinate
        else:
            return points_in_lane_coordinate + the_points


    '''
        the path connects node to the boundary point outside the pool in lane coordinate
        the path is for getting outside of the pool from a node or getting into a node from outside the pool
        boundary is the side through which the path should get out of the pool or get into the pool [north|south|east|west]
        approach_snap_point_from is the direction from which the path should approach the snap-point specially when the snap-point can not be approached directly due to the presence of a label (for north and south snap-points for gateway, event and data)
    '''
    def outside_the_pool(self, pool_boundary, pool_number, channel_boundary, channel, node, side, position, role, approach_snap_point_from, peer, edge_type):
        points_in_pool_coordinate = self.channel_collection_list[pool_number].outside_the_pool(pool_boundary, channel_boundary, channel, node, side, position, role, approach_snap_point_from, peer, edge_type, pool_margin_spec=self.margin_spec(pool_number))
        # print(node.id, points_in_pool_coordinate)
        points_in_lane_coordinate = [self.channel_collection_list[pool_number].element.xy + p for p in points_in_pool_coordinate]
        return points_in_lane_coordinate

    '''
        we want a path to bypass the lane through the routing area
    '''
    def bypass_vertically(self, coming_from, going_to, margin_spec):
        # the coming_from point is north of going_to, so we have to reach a point south of the lane either through east or west or directly dpending on which direction we are going_to
        if coming_from.north_of(going_to):
            # if the coming_from point is already below the lane, we have no point
            if coming_from.y >= self.element.xy.y + self.element.height + margin_spec['bottom']:
                return []

            # if the coming_from point's x position is outside the lane, we can directly go south
            elif (self.element.xy.x - margin_spec['left']) >= coming_from.x or coming_from.x >= (self.element.xy.x + self.element.width + margin_spec['right']):
                return [Point(coming_from.x, self.element.xy.y + self.element.height + margin_spec['bottom'])]

            # if the coming_from point is properly above the lane, we make a path
            else:
                # to the lane north vertically below coming_from
                p1 = Point(coming_from.x, self.element.xy.y - margin_spec['top'])
                if going_to.east_of(coming_from):
                    # to the lane north-east
                    p2 = Point(self.element.xy.x + self.element.width + margin_spec['right'], p1.y)
                    # debug('southward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))
                else:
                    # to the lane north-west
                    p2 = Point(self.element.xy.x - margin_spec['left'] , p1.y)
                    # debug('northward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))

                # to the lane south vertically below p2
                p3 = Point(p2.x, self.element.xy.y + self.element.height + margin_spec['bottom'])

        # the coming_from point is south of lane, so we have to reach a point north of the lane either through east or west dpending on which direction we are going_to
        else:
            # if the coming_from point is already above the pool, we have no point
            if coming_from.y <= self.element.xy.y - margin_spec['top']:
                return []

            # if the coming_from point's x position is outside the lane, we can directly go north
            elif (self.element.xy.x - margin_spec['left']) >= coming_from.x or coming_from.x >= (self.element.xy.x + self.element.width + margin_spec['right']):
                return [Point(coming_from.x, self.element.xy.y - margin_spec['top'])]

            # if the coming_from point is properly below the lane, we make a path
            else:
                # to the lane south vertically above coming_from
                p1 = Point(coming_from.x, self.element.xy.y + self.element.height + margin_spec['bottom'])
                if going_to.east_of(coming_from):
                    # to the lane south-east
                    p2 = Point(self.element.xy.x + self.element.width + margin_spec['right'], p1.y)
                    # debug('southward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))
                else:
                    # to the lane south-west
                    p2 = Point(self.element.xy.x - margin_spec['left'] , p1.y)
                    # debug('northward from: {0} to {1} new {2}'.format(point_from, point_to, new_target_point))

                # to the lane north vertically above p2
                p3 = Point(p2.x, self.element.xy.y - margin_spec['top'])

        return [p1, p2, p3]


    '''
        given a node get its pool number and id
    '''
    def pool_number_and_id(self, node):
        pool_number, pool_id, _ = self.pool_number_id_and_node(node.id)

        return pool_number, pool_id


    '''
        given to node id's, return the corresponding nodes only if the nodes are in different pools of the same lane
    '''
    def get_if_from_different_pools(self, from_node_id, to_node_id):
        from_pool_number, from_pool_id, from_node = self.pool_number_id_and_node(from_node_id)
        to_pool_number, to_pool_id, to_node = self.pool_number_id_and_node(to_node_id)

        if from_pool_number != -1 and to_pool_number != -1 and from_pool_number != to_pool_number:
            if from_node is not None and to_node is not None:
                return from_node, to_node

        return None, None


    '''
        given a node's id returns its pool number and the node
    '''
    def pool_number_id_and_node(self, node_id):
        pool_number = 0
        for channel_collection in self.channel_collection_list:
            channel_number, node = channel_collection.channel_number_and_node(node_id)
            if channel_number != -1:
                return pool_number, channel_collection.pool_id, node

            pool_number = pool_number + 1

        return -1, None, None


    '''
        given a node returns its channel and the node's ordinal position in the channel
    '''
    def channel_and_ordinal(self, node):
        for channel_collection in self.channel_collection_list:
            node_channel, node_ordinal = channel_collection.channel_and_ordinal(node)
            if node_channel is not None:
                return node_channel, node_ordinal

        return None, -1

    '''
        a pool's margin spec is the margin outside the pool outer boundary through which the inter-pool edges are routed
        1. if it is a top-most pool within the pool-collection (lane) then we assume that 1/2 of lane's top pad-spec is the top margin, else it is 1/2 of dy-between-pools
        2. if it is a bottom-most pool within the pool-collection (lane) then we assume that 1/2 of lane's bottom pad-spec is the top margin, else it is 1/2 of dy-between-pools
        3. 1/2 of lane's left pad-spec is the left margin, else it is 1/2 of dx-between-pools
        4. 1/2 of lane's right pad-spec is the right margin, else it is 1/2 of dx-between-pools
    '''
    def margin_spec(self, pool_number):
        margin_spec = {'left': 12, 'top': 12, 'right': 12, 'bottom': 12}

        # is it the top-most channel?
        if pool_number == 0:
            margin_spec['top'] = self.theme['pad-spec']['top']/2
        else:
            margin_spec['top'] = self.theme['dy-between-pools']/2

        # is it the bottom-most channel?
        if pool_number == len(self.channel_collection_list) - 1:
            margin_spec['bottom'] = self.theme['pad-spec']['bottom']/2
        else:
            margin_spec['bottom'] = self.theme['dy-between-pools']/2

        # left and right margin
        margin_spec['left'] = self.theme['pad-spec']['left']/2
        margin_spec['right'] = self.theme['pad-spec']['right']/2

        return margin_spec


    '''
        the str representation of a ChannelCollectionObject
    '''
    def __repr__(self):
        pool_number = 0
        s = '\r\n----------------------------------'
        for channel_collection in self.channel_collection_list:
            s = '{0}\r\n[{1}:{2} xy: {3} ({4} x {5})'.format(s, pool_number, channel_collection.pool_id, channel_collection.element.xy, channel_collection.element.width, channel_collection.element.height)
            pool_number = pool_number + 1

        return s
