#!/usr/bin/env python3
'''
'''
from util.logger import *
from elements import *

class SvgElement():
    def __init__(self, specs=None, group=None, snaps=None):
        self.specs = specs
        self.group = group
        self.snaps = snaps
