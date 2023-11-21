#!/usr/bin/env python3
import re

from helper.geometry import Point
from helper.logger import *

TRANSFORM_RE = re.compile(r"[a-zA-Z]+?\([0-9\.\,\-\s]+?\)")
ARGUMENT_RE = re.compile(r"[0-9\.\-]+")
# TRANSFORMS = {
#     "translate": translate_matrix,
#     "scale": scale_matrix,
#     "rotate": rotate_matrix,
#     "skewx": skewx_matrix,
#     "skewy": skewy_matrix,
#     "matrix": matrix_matrix,
# }


def points_from_polygon(path_str):
    return [Point.from_str(xy_str) for xy_str in path_str.split(' ')]


def parse_transform(trans_str):
    transformlist = TRANSFORM_RE.findall(trans_str)
    transforms = {}
    for xform in transformlist:
        action, params = xform.split("(")
        params = [float(x) for x in ARGUMENT_RE.findall(params)]
        transforms[action] = params
    
    return transforms


def build_transform(transforms):
    trans_str = ''
    for action, params in transforms.items():
        trans_str = trans_str + f"{action}({' '.join(map(str, params))}) "

    return trans_str
