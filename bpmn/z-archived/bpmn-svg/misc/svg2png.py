#!/usr/bin/env python3
 
'''svgtopng - SVG to PNG converter
Copyright (c) 2007 Guillaume Seguin <guillaume@segu.in>
Licensed under GNU GPLv2'''

import cairo
import rsvg
from sys import argv
from os.path import exists
import getopt

def usage ():
    print "Usage : %s [--width WIDTH] [--height HEIGHT] [-o OUTPUTFILE] FILE" % argv[0]
    raise SystemExit

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt (argv[1:], 'o:h',
                                    ['width=', 'height=', 'output=', 'help'])
    except getopt.GetoptError:
        usage ()
    output = None
    width = None
    height = None
    for o, a in opts:
            if o in ('-o', '--output'):
                output = str (a)
            elif o == '--width':
                width = int (a)
            elif o == '--height':
                height = int (a)
            elif o in ('-h', '--help'):
                usage ()
    if len (args) == 0:
        usage ()
    file = args[0]

    if not exists (file):
        usage ()

    svg = rsvg.Handle (file = file)

    if not output:
        if file[-4:] == ".svg":
            file = file[:-4]
        output = "%s.png" % file
        base = "%s%d.png"
        i = 1
        while exists (output):
            output = base % (file, i)
            i += 1

    if width == 0 and height == 0:
        width = svg.props.width
        height = svg.props.width
    elif width != 0:
        ratio = float (width) / svg.props.width
        height = int (ratio * svg.props.height)
    elif height != 0:
        ratio = float (height) / svg.props.height
        width = int (ratio * svg.props.width)

    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context (surface)

    wscale = float (width) / svg.props.width
    hscale = float (height) / svg.props.height

    cr.scale (wscale, hscale)

    svg.render_cairo (cr)

    surface.write_to_png (output)
