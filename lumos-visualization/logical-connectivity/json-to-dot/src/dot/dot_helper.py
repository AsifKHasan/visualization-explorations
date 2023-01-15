#!/usr/bin/env python3

''' (GraphViz) dot wrapper objects
'''

import time
import yaml
import datetime

from dot.dot_util import *
from helper.logger import *

class DotHelper(object):

    ''' constructor
    '''
    def __init__(self, config):
        self._config = config
        self.document_lines = None



    ''' generate and save the dot
    '''
    def generate_and_save(self, structure):


        # wrap in start/stop text
        self.document_lines = indent_and_wrap(lines=self.document_lines, wrap_in='text', indent_level=1)

        # wrap in BEGIN/end comments
        self.document_lines = wrap_with_comment(lines=self.document_lines, object_type='Text', object_id=None)

        # Document END comment
        self.document_lines.append("% END   Document")


        # save the markdown document string in a file
        with open(self._config['files']['output-dot'], "w", encoding="utf-8") as f:
            f.write('\n'.join(self.document_lines))
