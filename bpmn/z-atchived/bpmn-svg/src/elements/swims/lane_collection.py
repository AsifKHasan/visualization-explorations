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

from elements.swims.swim_lane import SwimLane
from elements.flows.flow_object import EdgeObject
from elements.flows.bpmn_flow import BpmnFlow

'''
    a lane collection is a vertical stack of lanes
'''
class LaneCollection(BpmnElement):
    def __init__(self, current_theme, bpmn_id, lanes, edges):
        self.current_theme = current_theme
        self.theme = self.current_theme['swims']['LaneCollection']
        self.bpmn_id, self.lanes, self.edges = bpmn_id, lanes, edges

    def lay_edges(self):
        # first lay the intra-lane edges
        for child_lane_class in self.child_lane_classes:
            child_lane_class.lay_edges()

        # print(self.lane_collection)

        # lay inter-pool edges - get a filtered list of edges containing only those where from-node and to-node both are in this lane but are in different pools
        for edge in self.edges:
            from_node, to_node = self.lane_collection.get_if_from_different_lanes(edge['from'], edge['to'])
            if from_node is not None and to_node is not None:
                edge_type = EDGE_TYPE[edge['type']]
                edge_label = edge.get('label', None)
                edge_style = edge.get('styles', None)

                # create an appropriate flow object, use BpmnFlow which manages flows inside a Bpmn
                flow_object = BpmnFlow(self.current_theme, edge_type, self.lane_collection)
                flow_svg_element = flow_object.create_flow(from_node, to_node, edge_label, edge_style)

                # add to channel svg group
                if flow_svg_element is not None and flow_svg_element.svg is not None:
                    self.lane_collection.element.svg.addElement(flow_svg_element.svg)

                    # store object for future reference
                    self.lane_collection.edge_list.append(EdgeObject(edge=edge, type=edge_type, element=flow_svg_element))

    def assemble_labels(self):
        group_id = '{0}-lanes-label'.format(self.bpmn_id)
        svg_group = G(id=group_id)

        group_width = 0
        transformer = TransformBuilder()
        for child_lane_class in self.child_lane_classes:
            child_label_element = child_lane_class.assemble_labels()
            if child_label_element is None:
                continue

            # the y position of this lane label in the group will be its corresponding swim-lane's y position
            child_label_xy = Point(0, child_lane_class.svg_element.xy.y)
            transformer.setTranslation(child_label_xy)
            child_label_element.svg.set_transform(transformer.getTransform())
            svg_group.addElement(child_label_element.svg)

            group_width = max(child_label_element.width, group_width)

        group_height = self.svg_element.height

        # wrap it in a svg element
        self.label_element = SvgElement(svg=svg_group, width=group_width, height=group_height)
        return self.label_element

    def collect_elements(self):
        info('processing lanes for [{0}]'.format(self.bpmn_id))

        # get the inner lane svg elements in a list
        self.child_lane_classes = []
        self.lane_collection = LaneCollectionObject(self.bpmn_id, self.theme)
        for lane_id, lane_data in self.lanes.items():
            child_lane_class = SwimLane(self.current_theme, self.bpmn_id, lane_id, lane_data)
            child_lane_class.collect_elements()
            # each child SwimLane's PoolCollectionObject is a member of its own lane_collection
            self.lane_collection.pool_collection_list.append(child_lane_class.pool_collection_instance.pool_collection)
            self.child_lane_classes.append(child_lane_class)

        info('processing lanes for [{0}] DONE'.format(self.bpmn_id))

    def assemble_elements(self):
        info('assembling lanes for [{0}] DONE'.format(self.bpmn_id))

        # wrap it in a svg group
        group_id = '{0}-lanes'.format(self.bpmn_id)
        svg_group = G(id=group_id)

        # height of the lane collection is sum of height of all lanes with gaps between lanes
        max_lane_width = self.theme['pad-spec']['left']
        current_y = self.theme['pad-spec']['top']
        transformer = TransformBuilder()
        for child_lane_class in self.child_lane_classes:
            swim_lane_element = child_lane_class.assemble_elements()
            current_x = self.theme['pad-spec']['left'] + float(child_lane_class.lane_data['styles'].get('move_x', 0))
            swim_lane_element.xy = Point(current_x, current_y)
            transformer.setTranslation(swim_lane_element.xy)
            swim_lane_element.svg.set_transform(transformer.getTransform())
            svg_group.addElement(swim_lane_element.svg)

            max_lane_width = max(max_lane_width, current_x + swim_lane_element.width)
            current_y = current_y + swim_lane_element.height + self.theme['dy-between-lanes']

        group_width = self.theme['pad-spec']['left'] + max_lane_width + self.theme['pad-spec']['right']
        group_height = current_y - self.theme['dy-between-lanes'] + self.theme['pad-spec']['bottom']

        # add the ractangle
        lane_collection_rect_svg = Rect(width=group_width, height=group_height)
        lane_collection_rect_svg.set_style(StyleBuilder(self.theme['style']).getStyle())
        svg_group.addElement(lane_collection_rect_svg)

        # wrap it in a svg element
        self.svg_element = SvgElement(svg=svg_group, width=group_width, height=group_height)
        self.lane_collection.element = self.svg_element
        info('assembling lanes for [{0}] DONE'.format(self.bpmn_id))
        return self.svg_element


''' ----------------------------------------------------------------------------------------------------------------------------------
    collection of pool collections (lanes)
'''
class LaneCollectionObject:

    def __init__(self, bpmn_id, theme):
        self.bpmn_id = bpmn_id
        self.theme = theme
        self.pool_collection_list = []
        self.edge_list = []
        self.element = None


    '''
        connects two points in two lanes only through straight lines.
        a. The points are asumed to be outside a lane's outer rectangle inside the routing area between lanes
        b. point_from must be above point_to

        1. We start by trying to go straight to the same y position of *point_to* (let us call it *target_point*) so that we can draw a straight horizontal line from there to *point_to*
        2. but going straight to the *target_point* from *point_from* may not be possible as there may be a whole lanes in between
        3. so, if there is a lane in between, we bypass the lane (by moving either to left or right) to the routing area east or west of the lane in the middle and now try to reach the *target_point* in a recursive manner
    '''
    def connect_southward(self, from_lane_number, point_from, to_lane_number, point_to):
        # see if there is one or more lanes between the from-lane and to-lane
        if to_lane_number > from_lane_number + 1:
            # yes we have lanes in between

            # we bypass the northmost (first) lane
            lane_number_to_bypass = from_lane_number + 1
            lane_to_bypass = self.pool_collection_list[lane_number_to_bypass]
            margin_spec = self.margin_spec(lane_number_to_bypass)
            points_to_bypass_the_lane = lane_to_bypass.bypass_vertically(coming_from=point_from, going_to=point_to, margin_spec=margin_spec)

            return [point_from] + points_to_bypass_the_lane + self.connect_southward(lane_number_to_bypass, points_to_bypass_the_lane[-1], to_lane_number, point_to)

        else:
            # there is no lane in between
            if point_from.y == point_to.y:
                # they are on the same horizontal line - inside a lane routing area
                return [point_from, Point(point_from.x, point_to.y), point_to]
            else:
                # they are not on a line, we need a connecting path, looks like one or both of them are at eastern/western boundary
                # the north (point_from) needs to come down to southern boundary
                point_from_next = Point(point_from.x, self.pool_collection_list[from_lane_number].element.xy.y + self.pool_collection_list[from_lane_number].element.height + self.margin_spec(to_lane_number)['bottom'])

                # the south (point_to) needs to move up to northern boundary
                point_to_next = Point(point_to.x, self.pool_collection_list[to_lane_number].element.xy.y - self.margin_spec(to_lane_number)['top'])

                return [point_from, point_from_next, point_to_next, point_to]


    '''
        the path connects node to the boundary point outside the lane in bpmn coordinate
        the path is for getting outside of the lane from a node or getting into a node from outside the lane
        boundary is the side through which the path should get out of the lane or get into the lane [north|south|east|west]
        approach_snap_point_from is the direction from which the path should approach the snap-point specially when the snap-point can not be approached directly due to the presence of a label (for north and south snap-points for gateway, event and data)
        TODO
    '''
    def outside_the_lane(self, lane_boundary, lane_number, pool_boundary, pool_number, channel_boundary, channel, node, side, position, role, approach_snap_point_from, peer, edge_type):
        points_in_lane_coordinate = self.pool_collection_list[lane_number].outside_the_lane(lane_boundary, pool_boundary, pool_number, channel_boundary, channel, node, side, position, role, approach_snap_point_from, peer, edge_type, lane_margin_spec=self.margin_spec(lane_number))
        points_in_bpmn_coordinate = [self.pool_collection_list[lane_number].element.xy + p for p in points_in_lane_coordinate]
        return points_in_bpmn_coordinate


    '''
        given a node get its lane and pool number and id
    '''
    def lane_and_pool_number_and_id(self, node):
        return self.lane_and_pool_number_id_and_node(node.id)


    '''
        given to node id's, return the corresponding nodes only if the nodes are in different lanes of the same lane
    '''
    def get_if_from_different_lanes(self, from_node_id, to_node_id):
        from_lane_number, _, _, _, from_node = self.lane_and_pool_number_id_and_node(from_node_id)
        to_lane_number, _, _, _, to_node = self.lane_and_pool_number_id_and_node(to_node_id)

        if from_lane_number != -1 and to_lane_number != -1 and from_lane_number != to_lane_number:
            return from_node, to_node

        return None, None


    '''
        given a node's id returns its lane and pool number and the node
    '''
    def lane_and_pool_number_id_and_node(self, node_id):
        lane_number = 0
        for pool_collection in self.pool_collection_list:
            pool_number, pool_id, node = pool_collection.pool_number_id_and_node(node_id)
            if pool_number != -1:
                return lane_number, pool_collection.lane_id, pool_number, pool_id, node

            lane_number = lane_number + 1

        return -1, None, -1, None, None


    '''
        given a node returns its channel and the node's ordinal position in the channel
    '''
    def channel_and_ordinal(self, node):
        for pool_collection in self.pool_collection_list:
            node_channel, node_ordinal = pool_collection.channel_and_ordinal(node)
            if node_channel is not None:
                return node_channel, node_ordinal

        return None, -1

    '''
        a lane's margin spec is the margin outside the lane outer boundary through which the inter-lane edges are routed
        1. if it is a top-most lane within the lane-collection (lane) then we assume that 1/2 of lane's top pad-spec is the top margin, else it is 1/2 of dy-between-lanes
        2. if it is a bottom-most lane within the lane-collection (lane) then we assume that 1/2 of lane's bottom pad-spec is the top margin, else it is 1/2 of dy-between-lanes
        3. 1/2 of lane's left pad-spec is the left margin, else it is 1/2 of dx-between-lanes
        4. 1/2 of lane's right pad-spec is the right margin, else it is 1/2 of dx-between-lanes
    '''
    def margin_spec(self, lane_number):
        margin_spec = {'left': 12, 'top': 12, 'right': 12, 'bottom': 12}

        # is it the top-most channel?
        if lane_number == 0:
            margin_spec['top'] = self.theme['pad-spec']['top']/2
        else:
            margin_spec['top'] = self.theme['dy-between-lanes']/2

        # is it the bottom-most channel?
        if lane_number == len(self.pool_collection_list) - 1:
            margin_spec['bottom'] = self.theme['pad-spec']['bottom']/2
        else:
            margin_spec['bottom'] = self.theme['dy-between-lanes']/2

        # left and right margin
        margin_spec['left'] = self.theme['pad-spec']['left']/2
        margin_spec['right'] = self.theme['pad-spec']['right']/2

        return margin_spec


    '''
        the str representation of a ChannelCollectionObject
    '''
    def __repr__(self):
        lane_number = 0
        s = '\r\n----------------------------------'
        for pool_collection in self.pool_collection_list:
            s = '{0}\r\n[{1}:{2} xy: {3} ({4} x {5})'.format(s, lane_number, pool_collection.lane_id, pool_collection.element.xy, pool_collection.element.width, pool_collection.element.height)
            lane_number = lane_number + 1

        return s
