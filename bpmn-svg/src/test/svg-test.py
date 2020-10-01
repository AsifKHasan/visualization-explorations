#!/usr/bin/env python3
'''
cd C:\projects\asifhasan@github\bpmn-svg\src
python svg-test.py > ../out/svg-test.svg
'''
import sys, json;

from pysvg.parser import *
from pysvg.builders import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *

import textwrap

def parse_svg(svg_path):
    root_obj = parse(svg_path)
    print(root_obj.getXML())

if __name__ == "__main__":
    parse_svg('../out/svg-test.svg')
