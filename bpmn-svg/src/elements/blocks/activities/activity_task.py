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

class ActivityTask(BpmnElement):
    def __init__(self):
        self.theme = self.current_theme['ActivityTask']

    def to_svg(self, node_id, node_data):
        info('....processing node [{0}] ...'.format(node_id))

        # to get the width, height we need to calculate the text rendering function
        text_rendering_hint = break_text_inside_rect(
                                    text=node_data['label'],
                                    font_family=self.theme['text-rect']['text-style']['font-family'],
                                    font_size=self.theme['text-rect']['text-style']['font-size'],
                                    max_lines=self.theme['text-rect']['max-lines'],
                                    min_width=self.theme['text-rect']['min-width'],
                                    max_width=self.theme['text-rect']['max-width'],
                                    pad_spec=self.theme['text-rect']['pad-spec'])

        group_width = text_rendering_hint[1]
        group_height = text_rendering_hint[2]
        # debug('{0} : ({1}, {2})'.format(node_id, group_width, group_height))

        # group to hold the objects
        svg_group = G(id=node_id)

        # text rect
        text_rect = Rect(width=group_width, height=group_height, rx=self.theme['text-rect']['rx'], ry=self.theme['text-rect']['ry'])
        text_rect.set_style(StyleBuilder(self.theme['text-rect']['style']).getStyle())

        # render the text
        text_svg = center_text(
                        text=text_rendering_hint[0],
                        shape=text_rect,
                        style=self.theme['text-rect']['text-style'],
                        vertical_text=self.theme['text-rect']['vertical-text'],
                        pad_spec=self.theme['text-rect']['pad-spec'])

        # add into the group
        svg_group.addElement(text_rect)
        svg_group.addElement(text_svg)

        group_specs = {'width': group_width, 'height': group_height}

        info('....processing node [{0}] DONE ...'.format(node_id))

        return SvgElement(group_specs, svg_group)
