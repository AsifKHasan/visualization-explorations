#!/usr/bin/env python3
from enum import Enum

''' enumeration for a Point's location with respect to a Channel
'''
class PointInChannel(Enum):
    INSIDE = 1
    WEST = 2
    WEST_NORTH = 3
    NORTH = 4
    NORTH_EAST = 5
    EAST = 6
    EAST_SOUTH = 7
    SOUTH = 8
    SOUTH_WEST = 9
    OUTSIDE = 10
