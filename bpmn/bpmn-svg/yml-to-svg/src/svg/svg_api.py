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
    def __init__(self, config, theme, object_type='bpmn'):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._config = config
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

        # based on position and rotation create the label
        if position == 'in':
            # just embed the text into the attach group
            # dimension is attach object's dimension without margin
            bounding_width, bounding_height = dimension_without_margin(width=self._width, height=self._height, margin=self._theme[self._object_type]['margin'])
            # handle rotation
            if rotation in ['left', 'right']:
                # swap dimension
                rect_width, rect_height = bounding_height, bounding_width
                text_g = a_text(text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

            elif rotation in ['none']:
                # dimension is attach object's dimension without margin
                rect_width, rect_height = bounding_width, bounding_height
                text_g = a_text(text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

        elif position in ['north', 'south']:
            # handle rotation
            if rotation in ['left', 'right']:
                # width is object's min-height, height is attach object's width
                rect_width, rect_height = self._theme[self._object_type]['label']['min-height'], self._width
                text_g = a_text(text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

            elif rotation in ['none']:
                # width is attach object's width, height is text's min-height
                rect_width, rect_height = self._width, self._theme[self._object_type]['label']['min-height']
                text_g = a_text(text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

        elif position in ['west', 'east']:
            # handle rotation
            if rotation in ['left', 'right']:
                # width is attach object's height, height is text's min-width
                rect_width, rect_height = self._height, self._theme[self._object_type]['label']['min-width']
                text_g = a_text(text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

            elif rotation in ['none']:
                # width is object's min-width, height is attach object's height
                rect_width, rect_height = self._theme[self._object_type]['label']['min-width'], self._height
                text_g = a_text(text=label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])


        # translate based on rotation
        text_g.translate(rect_height * ROTATION_MATRIX[rotation]['translation'][0], rect_width * ROTATION_MATRIX[rotation]['translation'][1])

        # group the object and label based on position
        new_g = group_together(svg_groups=[attach_to_g, text_g], position=position)

        return new_g



    ''' generate the SVG from data
    '''
    def to_svg(self, bpmn_object):
        # bpmn to root group
        bpmn_svg = BpmnSvg(config=self._config, theme=self._theme)
        bpmn_g = bpmn_svg.to_svg(bpmn_object=bpmn_object)

        # canvas is bpmn size + margin
        canvas_width, canvas_height = dimension_with_margin(width=bpmn_g.g_width, height=bpmn_g.g_height, margin=self._theme[self._object_type]['margin'])

        # wrap in a SVG drawing
        svg = Svg(0, 0, width=canvas_width, height=canvas_height)
        svg.addElement(bpmn_g.g)

        # finally save the svg
        svg.save(self._config['files']['output-svg'], encoding="UTF-8")



''' BPMN SVG object
'''
class BpmnSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, config, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, theme=theme, object_type='bpmn')
        self.pool_svgs = []



    ''' generate the bpmn SVG from data
    '''
    def to_svg(self, bpmn_object):
        self._bpmn_object = bpmn_object

        # bpmn to group
        # first we need to get all child pools
        for pool_object in self._bpmn_object._pools:
            pool_svg = PoolSvg(config=self._config, theme=self._theme)
            g_pool = pool_svg.to_svg(pool_object=pool_object)
            self.pool_svgs.append(g_pool)

        # calculate width, height with all pools embedded
        self._width = max([pool_g.g_width for pool_g in self.pool_svgs] + [self._width])
        self._height = max(sum([pool_g.g_height for pool_g in self.pool_svgs]), self._height)
        self._width, self._height = dimension_with_margin(width=self._width, height=self._height, margin=self._theme[self._object_type]['margin'])

        # finally create the bpmn group
        g_bpmn = a_rect(width=self._width, height=self._height, rx=self._theme[self._object_type]['rx'], ry=self._theme[self._object_type]['ry'], style=self._theme[self._object_type]['shape-style'])

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
    def __init__(self, config, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, theme=theme, object_type='pool')
        self.lane_svgs = []



    ''' generate the pool SVG from data
    '''
    def to_svg(self, pool_object):
        self._pool_object = pool_object

        # pool to group
        # first we need to get all child lanes
        for lane_object in self._pool_object._lanes:
            lane_svg = LaneSvg(config=self._config, theme=self._theme)
            g_lane = lane_svg.to_svg(lane_object=lane_object)
            self.lane_svgs.append(g_lane)

        # calculate width, height with all lanes embedded
        self._width = max([lane_g.g_width for lane_g in self.lane_svgs] + [self._width])
        self._height = max(sum([lane_g.g_height for lane_g in self.lane_svgs]), self._height)
        self._width, self._height = dimension_with_margin(width=self._width, height=self._height, margin=self._theme[self._object_type]['margin'])

        # finally create the pool group
        g_pool = a_rect(width=self._width, height=self._height, rx=self._theme[self._object_type]['rx'], ry=self._theme[self._object_type]['ry'], style=self._theme[self._object_type]['shape-style'])

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
    def __init__(self, config, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(config=config, theme=theme, object_type='lane')
        self.band_svgs = []



    ''' generate the lane SVG from data
    '''
    def to_svg(self, lane_object):
        self._lane_object = lane_object

        # lane to group
        # first we need to get all child bands
        for band_object in self._lane_object._bands:
            band_svg = BandSvg(config=self._config, theme=self._theme)
            g_band = band_svg.to_svg(band_object=band_object)
            self.band_svgs.append(g_band)

        # calculate width, height with all bands embedded
        self._width = max([band_g.g_width for band_g in self.band_svgs] + [self._width])
        self._height = max(sum([band_g.g_height for band_g in self.band_svgs]), self._height)
        self._width, self._height = dimension_with_margin(width=self._width, height=self._height, margin=self._theme[self._object_type]['margin'])

        # finally create the lane group
        g_lane = a_rect(width=self._width, height=self._height, rx=self._theme[self._object_type]['rx'], ry=self._theme[self._object_type]['ry'], style=self._theme[self._object_type]['shape-style'])

        # embed the lanes
        g_lane = g_lane.embed_vertically(svg_groups=self.band_svgs, margin=self._theme[self._object_type]['margin'])


        # if there is a label, attach it
        if self._lane_object._hide_label == False:
            g_lane = self.attach_label(attach_to_g=g_lane, label=self._lane_object._label)


        # return group
        return g_lane
