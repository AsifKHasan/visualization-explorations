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

        self.child_svgs = []

        self._width = self._theme[self._object_type]['min-width']
        self._height = self._theme[self._object_type]['min-height']

        self.g_outer, self.g_label, self.g_content = None, None, None



    ''' generate the SVG from data
    '''
    def to_svg(self, bpmn_object):
        self._gid = f"{bpmn_object._id}"

        # bpmn to root group
        bpmn_svg = BpmnSvg(theme=self._theme)
        bpmn_g = bpmn_svg.to_svg(data_object=bpmn_object)

        # canvas is bpmn size + margin
        canvas_width, canvas_height = dimension_with_margin(width=bpmn_g.g_width, height=bpmn_g.g_height, margin=self._theme[self._object_type]['margin'])

        # wrap in a SVG drawing
        svg = Svg(0, 0, width=canvas_width, height=canvas_height)
        svg.addElement(bpmn_g.g)

        return svg



    ''' add paths to the content group and extend group height accordingly
    '''
    def add_paths(self, svg_groups):
        previous_content_height = self.g_content.g_height
        self.g_content.extend_vertically(svg_groups=svg_groups)
        current_content_height = self.g_content.g_height
        height_to_add = current_content_height - previous_content_height
        if height_to_add > 0:
            self.g_outer.g_height = self.g_outer.g_height + height_to_add



    ''' post process the svg element
        1. attach label
    '''
    def post_process(self):
        # if there is a label, attach it
        if self._data_object._hide_label == True:
            gid = f"group__{self._gid}"
            self.g_outer = self.g_content.wrap(gid=gid)
            # self.g_outer = self.g_content
            return

        # label rect height and width depends on block height and width, label position and label rotation
        position = self._theme[self._object_type]['label']['position']
        rotation = self._theme[self._object_type]['label']['rotation']

        self.g_label, rect_width, rect_height = None, None, None
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
                self.g_label = a_text(gid=gid, text=self._data_object._label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

            elif rotation in ['none']:
                # dimension is attach object's dimension without margin
                rect_width, rect_height = bounding_width, bounding_height
                self.g_label = a_text(gid=gid, text=self._data_object._label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

        elif position in ['north', 'south']:
            # handle rotation
            if rotation in ['left', 'right']:
                # width is object's min-height, height is attach object's width
                rect_width, rect_height = self._theme[self._object_type]['label']['min-height'], self._width
                self.g_label = a_text(gid=gid, text=self._data_object._label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

            elif rotation in ['none']:
                # width is attach object's width, height is text's min-height
                rect_width, rect_height = self._width, self._theme[self._object_type]['label']['min-height']
                self.g_label = a_text(gid=gid, text=self._data_object._label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

        elif position in ['west', 'east']:
            # handle rotation
            if rotation in ['left', 'right']:
                # width is attach object's height, height is text's min-width
                rect_width, rect_height = self._height, self._theme[self._object_type]['label']['min-width']
                self.g_label = a_text(gid=gid, text=self._data_object._label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])

            elif rotation in ['none']:
                # width is object's min-width, height is attach object's height
                rect_width, rect_height = self._theme[self._object_type]['label']['min-width'], self._height
                self.g_label = a_text(gid=gid, text=self._data_object._label, width=rect_width, height=rect_height, spec=self._theme[self._object_type]['label'])


        # translate based on rotation
        x = rect_height * ROTATION_MATRIX[rotation]['translation'][0]
        y = rect_width * ROTATION_MATRIX[rotation]['translation'][1]
        self.g_label.translate(x=x, y=y)

        # group the object and label based on position
        gid = f"group__{self._gid}"
        self.g_outer = group_together(gid=gid, svg_groups=[self.g_content, self.g_label], position=position)



    ''' generate the bpmn SVG from data
    '''
    def create_svg_block(self):
        self._gid = f"{self._data_object._id}"

        # TODO: what about the bands directly under the Bpmn?

        # get all children
        child_objects = self.get_children()
        count = len(child_objects)
        for i in range(0, count):
            # append paths if this is not the first child
            if i != 0:
                path_svgs = []
                path_width = preceding_svg.g_content.g_width
                for n in range(0, self.get_path_count()):
                    path_svg = self.instantiate_path_svg(theme=self._theme)
                    g_path = path_svg.to_svg(parent_id=self._data_object._id, num=n, width=path_width)
                    path_svgs.append(g_path)

                # add paths to the preceding svg
                preceding_svg.add_paths(svg_groups=path_svgs)

            bpmn_object = child_objects[i]
            bpmn_svg = self.instantiate_block_svg(theme=self._theme)
            g_bpmn = bpmn_svg.to_svg(data_object=bpmn_object)
            self.child_svgs.append(g_bpmn)
            preceding_svg = bpmn_svg


        # calculate width, height with all pools embedded
        self._width = max([child_g.g_width for child_g in self.child_svgs] + [self._width])
        self._height = max(sum([child_g.g_height for child_g in self.child_svgs]), self._height)
        self._width, self._height = dimension_with_margin(width=self._width, height=self._height, margin=self._theme[self._object_type]['margin'])

        # finally create the bpmn group
        width = self._width
        height = self._height
        rx = self._theme[self._object_type]['rx']
        ry = self._theme[self._object_type]['ry']
        style = self._theme[self._object_type]['shape-style']
        self.g_content = a_rect(gid=self._gid, width=width, height=height, rx=rx, ry=ry, style=style)

        # embed the pools
        self.g_content = self.g_content.embed_vertically(svg_groups=self.child_svgs, margin=self._theme[self._object_type]['margin'])

        # finalize the group
        self.post_process()



    ''' generate the path SVG
        num     : 0-based sequence of the paths between two pools/lanes/bands
        width   : width of the path
    '''
    def create_path_svg(self, parent_id, num, width):
        self._num = num
        self._width = width
        gid = f"{self._object_type}__{parent_id}__{self._num}"

        # create the path group
        width = self._width
        height = self._height
        rx = self._theme[self._object_type]['rx']
        ry = self._theme[self._object_type]['ry']
        style = self._theme[self._object_type]['shape-style']
        self.g_content = a_rect(gid=gid, width=width, height=height, rx=rx, ry=ry, style=style)



''' BPMN SVG object
'''
class BpmnSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(theme=theme, object_type='bpmn')



    ''' return how many path-svgs are to be created
    '''
    def get_path_count(self):
        return self._data_object._pool_path_count
    

    
    ''' return child objects to process
    '''
    def get_children(self):
        return self._data_object._pools



    ''' instantiate and return concrete bpmn-svg object
    '''
    def instantiate_block_svg(self, theme):
        return PoolSvg(theme=theme)
    


    ''' instantiate and return concrete path-svg object
    '''
    def instantiate_path_svg(self, theme):
        return PoolPathSvg(theme=theme)
    


    ''' generate the bpmn SVG from data
    '''
    def to_svg(self, data_object):
        self._data_object = data_object

        self.create_svg_block()

        # return group
        return self.g_outer



''' Pool SVG object
'''
class PoolSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(theme=theme, object_type='pool')



    ''' instantiate and return concrete bpmn-svg object
    '''
    def instantiate_block_svg(self, theme):
        return LaneSvg(theme=theme)
    


    ''' instantiate and return concrete path-svg object
    '''
    def instantiate_path_svg(self, theme):
        return LanePathSvg(theme=theme)
    


    ''' return how many path-svgs are to be created
    '''
    def get_path_count(self):
        return self._data_object._lane_path_count
    

    
    ''' return child objects to process
    '''
    def get_children(self):
        return self._data_object._lanes



    ''' generate the pool SVG from data
    '''
    def to_svg(self, data_object):
        self._data_object = data_object
        self.create_svg_block()

        # return group
        return self.g_outer



''' Lane SVG object
'''
class LaneSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(theme=theme, object_type='lane')



    ''' instantiate and return concrete bpmn-svg object
    '''
    def instantiate_block_svg(self, theme):
        return BandSvg(theme=theme)
    


    ''' instantiate and return concrete path-svg object
    '''
    def instantiate_path_svg(self, theme):
        return BandPathSvg(theme=theme)
    


    ''' return how many path-svgs are to be created
    '''
    def get_path_count(self):
        return self._data_object._band_path_count
    

    
    ''' return child objects to process
    '''
    def get_children(self):
        return self._data_object._bands



    ''' generate the lane SVG from data
    '''
    def to_svg(self, data_object):
        self._data_object = data_object
        self.create_svg_block()

        # return group
        return self.g_outer



''' Band SVG object
'''
class BandSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        super().__init__(theme=theme, object_type='band')



    ''' return child objects to process
    '''
    def get_children(self):
        # return self._data_object._nodes
        return []



    ''' generate the band SVG from data
    '''
    def to_svg(self, data_object):
        self._data_object = data_object
        self.create_svg_block()

        # return group
        return self.g_outer



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
        self.create_path_svg(parent_id=parent_id, num=num, width=width)

        # return group
        return self.g_content



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
        self.create_path_svg(parent_id=parent_id, num=num, width=width)

        # return group
        return self.g_content



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
        self.create_path_svg(parent_id=parent_id, num=num, width=width)

        # return group
        return self.g_content



''' node-svg base object
             _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
            |                                     |
            |             NORTH-LABEL             |
     _ _ _ _|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|_ _ _ _
    |       |                                     |       |
    |       |              edge route             |       |
    |       |          _________________          |       |
    |       |         |                 |         |       |
    |    L  |   e r   |      Actual     |   e r   |     L |
    |  W A  |   d o   |       Node      |   d o   |  E  A |
    |  E B  |   g u   |                 |   g u   |  A  B |
    |  S E  |   e t   |     IN-LABEL    |   e t   |  S  E |
    |  T L  |     e   |_________________|     e   |  T  L |
    |       |                                     |       |
    |       |              edge route             |       |
    |_ _ _ _|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|_ _ _ _|
            |                                     |
            |             SOUTH-LABEL             |
            |_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|



             _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
            |                                     |
            |             NORTH-LABEL             |
     _ _ _ _|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|_ _ _ _
    |       |                                     |       |
    |       |              edge route             |       |
    |       |                                     |       |
    |       |                 / \                 |       |
    |    L  |   e r        /       \        e r   |     L |
    |  W A  |   d o      /           \      d o   |  E  A |
    |  E B  |   g u    /     Actual    \    g u   |  A  B |
    |  S E  |   e t    \      Node     /    e t   |  S  E |
    |  T L  |     e      \           /        e   |  T  L |
    |       |              \       /              |       |
    |       |                 \ /                 |       |
    |       |                                     |       |
    |       |              edge route             |       |
    |_ _ _ _|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|_ _ _ _|
            |                                     |
            |             SOUTH-LABEL             |
            |_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|

'''
class NodeSvg(SvgObject):
    ''' constructor
    '''
    def __init__(self, theme):
        # debug(f". {self.__class__.__name__} : {inspect.stack()[0][3]}")
        self._x, self._y = 0, 0

        self.g_container, self.g_route_area, self.g_node, self.g_in_label, self.g_west_label, self.g_noth_label, self.g_east_label, self.g_south_label = None, None, None, None, None, None, None, None



    ''' generate svg from node_data
    '''
    def to_svg(self, node_data):
        
        return self.g_container
