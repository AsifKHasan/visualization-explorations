#!/usr/bin/env python3

import importlib
from bpmn.bpmn_api import *
from svg.svg_util import *
from helper.logger import *

#   ----------------------------------------------------------------------------------------------------------------
#   Dot objects wrappers
#   ----------------------------------------------------------------------------------------------------------------


''' SVG base object
'''
class SvgObject(object):
    ''' constructor
    '''
    def __init__(self, theme, object_type='bpmn'):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._theme = theme
        self._object_type = object_type

        self._width = self._theme[self._object_type]['min-width']
        self._height = self._theme[self._object_type]['min-height']


    ''' attach label
    '''
    def attach_label(self, attach_to_g, label):
        # label rect height and width depends on block height and width, label position and label rotation
        position = self._theme[self._object_type]['label']['position']
        rotation = self._theme[self._object_type]['label']['rotation']

        text_g, rect_width, rect_height = None, None, None
        gid = f"label__{self._gid}"

        # based on position and rotation create the label
        if position == 'in':
            # just embed the text into the attach group
            # dimension is attach object's dimension without margin
            bounding_width, bounding_height = dimension_without_margin(width=self._width, height=self._height, margin=self._theme[self._object_type]['margin'])
            # handle rotation
            if rotation in ['left', 'right']:
                # swap dimension
                rect_width, rect_height = bounding_height, bounding_width
                text_g = a_text(gid=gid, text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

            elif rotation in ['none']:
                # dimension is attach object's dimension without margin
                rect_width, rect_height = bounding_width, bounding_height
                text_g = a_text(gid=gid, text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

        elif position in ['north', 'south']:
            # handle rotation
            if rotation in ['left', 'right']:
                # width is object's min-height, height is attach object's width
                rect_width, rect_height = self._theme[self._object_type]['label']['min-height'], self._width
                text_g = a_text(gid=gid, text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

            elif rotation in ['none']:
                # width is attach object's width, height is text's min-height
                rect_width, rect_height = self._width, self._theme[self._object_type]['label']['min-height']
                text_g = a_text(gid=gid, text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

        elif position in ['west', 'east']:
            # handle rotation
            if rotation in ['left', 'right']:
                # width is attach object's height, height is text's min-width
                rect_width, rect_height = self._height, self._theme[self._object_type]['label']['min-width']
                text_g = a_text(gid=gid, text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

            elif rotation in ['none']:
                # width is object's min-width, height is attach object's height
                rect_width, rect_height = self._theme[self._object_type]['label']['min-width'], self._height
                text_g = a_text(gid=gid, text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])


        # translate based on rotation
        x = rect_height * ROTATION_MATRIX[rotation]['translation'][0]
        y = rect_width * ROTATION_MATRIX[rotation]['translation'][1]
        text_g.translate(x=x, y=y)

        # group the object and label based on position
        gid = f"group__{self._gid}"
        new_g = group_together(gid=gid, svg_groups=[attach_to_g, text_g], position=position)

        return new_g



    ''' generate the SVG from data
    '''
    def to_svg(self, bpmn_object):
        self._gid = f"{bpmn_object._id}"

        # bpmn to root group
        bpmn_svg = BpmnSvg(theme=self._theme)
        bpmn_g = bpmn_svg.to_svg(bpmn_object=bpmn_object)

        # canvas is bpmn size + margin
        canvas_width, canvas_height = dimension_with_margin(width=bpmn_g.g_width, height=bpmn_g.g_height, margin=self._theme[self._object_type]['margin'])

        # wrap in a SVG drawing
        svg = Svg(0, 0, width=canvas_width, height=canvas_height)
        svg.addElement(bpmn_g.g)

        return svg



''' BPMN SVG object
'''
class BpmnSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(theme=theme, object_type='bpmn')
        self.pool_svgs = []



    ''' generate the bpmn SVG from data
    '''
    def to_svg(self, bpmn_object):
        self._bpmn_object = bpmn_object
        self._gid = f"{bpmn_object._id}"

        # TODO: what about the bands directly under the Bpmn?

        # bpmn to group, get all child pools
        pool_count = len(self._bpmn_object._pools)
        for i in range(0, pool_count):
            # append pool-paths if this is not the first pool
            if i != 0:
                for n in range(0, self._bpmn_object._pool_path_count):
                    pool_path_svg = PoolPathSvg(theme=self._theme)
                    g_pool_path = pool_path_svg.to_svg(parent_id=self._bpmn_object._id, num=n, width=self._width)
                    self.pool_svgs.append(g_pool_path)

            pool_object = self._bpmn_object._pools[i]
            pool_svg = PoolSvg(theme=self._theme)
            g_pool = pool_svg.to_svg(pool_object=pool_object)
            self.pool_svgs.append(g_pool)



        # calculate width, height with all pools embedded
        self._width = max([pool_g.g_width for pool_g in self.pool_svgs] + [self._width])
        self._height = max(sum([pool_g.g_height for pool_g in self.pool_svgs]), self._height)
        self._width, self._height = dimension_with_margin(width=self._width, height=self._height, margin=self._theme[self._object_type]['margin'])

        # finally create the bpmn group
        width = self._width
        height = self._height
        rx = self._theme[self._object_type]['rx']
        ry = self._theme[self._object_type]['ry']
        style = self._theme[self._object_type]['shape-style']
        g_bpmn = a_rect(gid=self._gid, width=width, height=height, rx=rx, ry=ry, style=style)

        # embed the pools
        g_bpmn = g_bpmn.embed_vertically(svg_groups=self.pool_svgs, margin=self._theme[self._object_type]['margin'])

        # if there is a label, attach it
        if self._bpmn_object._hide_label == False:
            g_bpmn = self.attach_label(attach_to_g=g_bpmn, label=self._bpmn_object._label)

        # return group
        return g_bpmn



''' Pool SVG object
'''
class PoolSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(theme=theme, object_type='pool')
        self.lane_svgs = []



    ''' generate the pool SVG from data
    '''
    def to_svg(self, pool_object):
        self._pool_object = pool_object
        self._gid = f"{self._pool_object._id}"

        # TODO: what about the bands directly under the Pool?

        # pool to group, get all child lanes
        lane_count = len(self._pool_object._lanes)
        for i in range(0, lane_count):
            # append lane-paths if this is not the first lane
            if i != 0:
                for n in range(0, self._pool_object._lane_path_count):
                    lane_path_svg = LanePathSvg(theme=self._theme)
                    g_lane_path = lane_path_svg.to_svg(parent_id=self._pool_object._id, num=n, width=self._width)
                    self.lane_svgs.append(g_lane_path)

            lane_object = self._pool_object._lanes[i]
            lane_svg = LaneSvg(theme=self._theme)
            g_lane = lane_svg.to_svg(lane_object=lane_object)
            self.lane_svgs.append(g_lane)

        # calculate width, height with all lanes embedded
        self._width = max([lane_g.g_width for lane_g in self.lane_svgs] + [self._width])
        self._height = max(sum([lane_g.g_height for lane_g in self.lane_svgs]), self._height)
        self._width, self._height = dimension_with_margin(width=self._width, height=self._height, margin=self._theme[self._object_type]['margin'])

        # finally create the pool group
        width = self._width
        height = self._height
        rx = self._theme[self._object_type]['rx']
        ry = self._theme[self._object_type]['ry']
        style = self._theme[self._object_type]['shape-style']
        g_pool = a_rect(gid=self._gid, width=width, height=height, rx=rx, ry=ry, style=style)

        # embed the lanes
        g_pool = g_pool.embed_vertically(svg_groups=self.lane_svgs, margin=self._theme[self._object_type]['margin'])


        # if there is a label, attach it
        if self._pool_object._hide_label == False:
            g_pool = self.attach_label(attach_to_g=g_pool, label=self._pool_object._label)


        # return group
        return g_pool



''' Lane SVG object
'''
class LaneSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(theme=theme, object_type='lane')
        self.band_svgs = []



    ''' generate the lane SVG from data
    '''
    def to_svg(self, lane_object):
        self._lane_object = lane_object
        self._gid = f"{self._lane_object._id}"

        # lane to group, get all child bands
        band_count = len(self._lane_object._bands)
        for i in range(0, band_count):
            # append band-paths if this is not the first band
            if i != 0:
                for n in range(0, self._lane_object._band_path_count):
                    band_path_svg = BandPathSvg(theme=self._theme)
                    g_band_path = band_path_svg.to_svg(parent_id=self._lane_object._id, num=n, width=self._width)
                    self.band_svgs.append(g_band_path)

            band_object = self._lane_object._bands[i]
            band_svg = BandSvg(theme=self._theme)
            g_band = band_svg.to_svg(band_object=band_object)
            self.band_svgs.append(g_band)

        # calculate width, height with all bands embedded
        self._width = max([band_g.g_width for band_g in self.band_svgs] + [self._width])
        self._height = max(sum([band_g.g_height for band_g in self.band_svgs]), self._height)
        self._width, self._height = dimension_with_margin(width=self._width, height=self._height, margin=self._theme[self._object_type]['margin'])

        # finally create the lane group
        width = self._width
        height = self._height
        rx = self._theme[self._object_type]['rx']
        ry = self._theme[self._object_type]['ry']
        style = self._theme[self._object_type]['shape-style']
        g_lane = a_rect(gid=self._gid, width=width, height=height, rx=rx, ry=ry, style=style)

        # embed the bands
        g_lane = g_lane.embed_vertically(svg_groups=self.band_svgs, margin=self._theme[self._object_type]['margin'])


        # if there is a label, attach it
        if self._lane_object._hide_label == False:
            g_lane = self.attach_label(attach_to_g=g_lane, label=self._lane_object._label)


        # return group
        return g_lane



''' Band SVG object
'''
class BandSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(theme=theme, object_type='band')
        self.node_svgs = []



    ''' generate the band SVG from data
    '''
    def to_svg(self, band_object):
        self._band_object = band_object
        self._gid = f"{self._band_object._id}"

        # band to group
        # first we need to get all child nodes
        for node_object in self._band_object._nodes:
            # node_svg = NodeSvg(theme=self._theme)
            # g_node = node_svg.to_svg(node_object=node_object)
            # self.node_svgs.append(g_node)
            pass

        # calculate width, height with all nodes embedded
        self._width = max([node_g.g_width for node_g in self.node_svgs] + [self._width])
        self._height = max(sum([node_g.g_height for node_g in self.node_svgs]), self._height)
        self._width, self._height = dimension_with_margin(width=self._width, height=self._height, margin=self._theme[self._object_type]['margin'])

        # finally create the band group
        width = self._width
        height = self._height
        rx = self._theme[self._object_type]['rx']
        ry = self._theme[self._object_type]['ry']
        style = self._theme[self._object_type]['shape-style']
        g_band = a_rect(gid=self._gid, width=width, height=height, rx=rx, ry=ry, style=style)

        # embed the nodes
        g_band = g_band.embed_vertically(svg_groups=self.node_svgs, margin=self._theme[self._object_type]['margin'])


        # if there is a label, attach it
        if self._band_object._hide_label == False:
            g_band = self.attach_label(attach_to_g=g_band, label=self._band_object._label)


        # return group
        return g_band



''' PoolPath SVG object
'''
class PoolPathSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(theme=theme, object_type='pool-path')



    ''' generate the pool-path SVG
        num     : 0-based sequence of the pool-path between two pools
        width   : width of the pool-path
    '''
    def to_svg(self, parent_id, num, width):
        self._num = num
        self._width = width
        gid = f"{self._object_type}__{parent_id}__{self._num}"

        # TODO: create the pool-path group
        width = self._width
        height = self._height
        rx = self._theme[self._object_type]['rx']
        ry = self._theme[self._object_type]['ry']
        style = self._theme[self._object_type]['shape-style']
        g_pool_path = a_rect(gid=gid, width=width, height=height, rx=rx, ry=ry, style=style)

        # return group
        return g_pool_path



''' LanePath SVG object
'''
class LanePathSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(theme=theme, object_type='lane-path')



    ''' generate the lane-path SVG
        num     : 0-based sequence of the lane-path between two lanes
        width   : width of the lane-path
    '''
    def to_svg(self, parent_id, num, width):
        self._num = num
        self._width = width
        gid = f"{self._object_type}__{parent_id}__{self._num}"

        # TODO: create the lane-path group
        width = self._width
        height = self._height
        rx = self._theme[self._object_type]['rx']
        ry = self._theme[self._object_type]['ry']
        style = self._theme[self._object_type]['shape-style']
        g_lane_path = a_rect(gid=gid, width=width, height=height, rx=rx, ry=ry, style=style)

        # return group
        return g_lane_path



''' BandPath SVG object
'''
class BandPathSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(theme=theme, object_type='band-path')



    ''' generate the band-path SVG
        num     : 0-based sequence of the band-path between two bands
        width   : width of the band-path
    '''
    def to_svg(self, parent_id, num, width):
        self._num = num
        self._width = width
        gid = f"{self._object_type}__{parent_id}__{self._num}"

        # TODO: create the band-path group
        width = self._width
        height = self._height
        rx = self._theme[self._object_type]['rx']
        ry = self._theme[self._object_type]['ry']
        style = self._theme[self._object_type]['shape-style']
        g_band_path = a_rect(gid=gid, width=width, height=height, rx=rx, ry=ry, style=style)

        # return group
        return g_band_path
