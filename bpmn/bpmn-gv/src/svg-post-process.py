#!/usr/bin/env python3

import argparse
import yaml
from pathlib import Path

from pysvg.core import TextContent
from pysvg.shape import Polygon
from pysvg.structure import G, Svg
from pysvg.text import Text
from pysvg.parser import parse

from helper.geometry import Point
from helper.logger import *
from helper.svg_parselets import *
from dot.dot_util import *

def update_svg(svg_root):

    # view box
    vp_str = svg_root.get_viewBox()
    vp_strs = vp_str.split(' ')
    # add 100 to width
    new_vp_width = float(vp_strs[2]) + 100
    new_vp_str = f"{vp_strs[0]} {vp_strs[1]} {new_vp_width:.2f} {vp_strs[3]}"

    # svg width
    w_str = svg_root.get_width()
    w = w_str[0:-2]
    new_w = float(w) + 100

    svg_root.set_viewBox(new_vp_str)
    svg_root.set_width(f"{new_w}pt")

    # graph node
    graph_node = svg_root.getElementByID(GRAPH_ID)[0]
    trans_str = graph_node.get_transform()
    transforms = parse_transform(trans_str)
    transforms['translate'][0] = transforms['translate'][0] + 100
    new_trans_str = build_transform(transforms)
    graph_node.set_transform(new_trans_str)

    print(new_vp_str)
    print(new_w)
    print(new_trans_str)

    return svg_root
    

def update_label_node(svg_root, cluster_id, direction='LR'):
    # graph node
    graph_node = None
    for node in svg_root.getElementsByType(G):
        if node.get_class() == 'graph':
            graph_node = node
            break

    if graph_node is None:
        warn(f"root [graph] node not found")
        return
    

    trans_str = graph_node.get_transform()
    transforms = parse_transform(trans_str)
    translate_x = transforms['translate'][0]

    # get the cluster node
    cluster_node = graph_node.getElementByID(cluster_id)[0]
    if cluster_node is None:
        warn(f"cluster node [{cluster_id}] not found")
        return

    # get the Polygon under cluster node
    cluster_polygons = cluster_node.getElementsByType(Polygon)
    if len(cluster_polygons) == 0:
        warn(f"no Polygon found under cluster node [{cluster_id}]")
        return
    else:
        cluster_polygon = cluster_polygons[0]

    # get the corresponding label node
    label_node = graph_node.getElementByID(cluster_id + '_label')[0]
    if label_node is None:
        warn(f"label node [{cluster_id}_label] not found")
        return

    # get the Text under label_node
    label_texts = label_node.getElementsByType(Text)
    for label_text in label_texts:
        for text_content in label_text.getElementsByType(TextContent):
            text_content.setContent(wrap_as_cdata(text_content.content))
            # print(f"label = {text_content.content}")

    # get the Polygon under label_node
    label_polygons = label_node.getElementsByType(Polygon)
    if len(label_polygons) == 0:
        warn(f"no Polygon found under label node [{cluster_id}_label]")
        return
    else:
        label_polygon = label_polygons[0]

    # label polygon y1, y2 should be equal to cluster polygon y1, y2
    cluster_points = points_from_polygon(cluster_polygon.get_points())
    label_points = points_from_polygon(label_polygon.get_points())


    cluster_x1 = min([p.x for p in cluster_points])
    cluster_x2 = max([p.x for p in cluster_points])
    cluster_y1 = max([p.y for p in cluster_points])
    cluster_y2 = min([p.y for p in cluster_points])

    label_x1 = min([p.x for p in label_points])
    label_x2 = max([p.x for p in label_points])
    label_y1 = max([p.y for p in label_points])
    label_y2 = min([p.y for p in label_points])

    if direction == 'LR':
        label_points = [Point(label_x1, cluster_y1), Point(label_x1, cluster_y2), Point(label_x2, cluster_y2), Point(label_x2, cluster_y1), Point(label_x1, cluster_y1)]
    else:
        label_points = [Point(cluster_x1, label_y1), Point(cluster_x1, label_y2), Point(cluster_x2, label_y2), Point(cluster_x2, label_y1), Point(cluster_x1, label_y1)]

    label_points_str = [str(p) for p in label_points]
    label_polygon.set_points(' '.join(label_points_str))


    if direction == 'LR':
        # get the Text under label_node
        label_texts = label_node.getElementsByType(Text)
        if len(label_texts) == 0:
            warn(f"no Text found under label node [{cluster_id}_label]")
        else:
            label_text = label_texts[0]

        # translate and rotate text
        text_x = float(label_text.get_x())
        text_y = float(label_text.get_y())
        translate_x = (label_x1 + label_x2) / 2 - text_y + translate_x
        translate_y = (cluster_y1 + cluster_y2) / 2 + text_x
        transform_str = f"translate({Point(translate_x, translate_y)}) rotate(-90)"
        label_text.set_transform(transform_str)


    # print(cluster_polygon.get_points())
    # print(label_polygon.get_points())
    # print()



if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", required=True, help="configuration yml path")
    ap.add_argument("-s", "--svg", required=True, help="svg file name to process")
    ap.add_argument("-d", "--dir", required=True, help="direction LR/TB")
    args = vars(ap.parse_args())

    # configuration
    config_path = Path(args['config']).resolve()
    config = yaml.load(open(config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    config_dir = config_path.parent

    output_dir = config_dir / config['dirs']['output-dir']

    svg_path = output_dir / args['svg']
    svg_root = parse(inFileName=str(svg_path))
    
    cluster_ids = []
    for node in svg_root.getElementsByType(G):
        if node.get_class() == 'cluster':
            cluster_ids.append(node.get_id())

    for cluster_id in cluster_ids:
        update_label_node(svg_root=svg_root, cluster_id=cluster_id, direction=args['dir'])

    svg_root.save(filename=svg_path, encoding="UTF-8")
