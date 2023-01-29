#!/usr/bin/env python3

'''
various utilities for generating SVG code
'''
import re
import random
import string

from os import path

from pysvg.parser import *

from helper.logger import *


''' get and open the template from data
'''
def open_svg_from_file(template_path):
    if not path.exists(template_path):
        error("no svg template [{template_path}]")
        return

    # open as an SVG object
    return parse(template_path)


