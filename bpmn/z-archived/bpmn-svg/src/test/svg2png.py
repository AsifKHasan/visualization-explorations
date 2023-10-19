#!/usr/bin/env python

"""Convert an SVG file to a PNG file.
    svg2png.py --file "D:/projects/asif@github/visualization-explorations/bpmn-svg/out/cas_tld.svg" --size 1000
"""

from argparse import ArgumentParser
import subprocess
import os.path


def main():
    args = parse_args()
    if not args.out:
        args.out = os.path.splitext(args.file)[0] + '.png'

    # convert_with_cairosvg_simple(args)
    # convert_with_cairosvg_sizes(args)
    convert_with_svglib(args)
    # convert_with_rsvg(args)


def convert_with_cairosvg_simple(args):
    # import cairocffi as cairo
    from cairosvg import svg2png
    svg2png(open(args.file, 'rb').read(), write_to=open(args.out, 'wb'))


def convert_with_cairosvg_sizes(args):
    from cairosvg.surface import PNGSurface
    width, height = args.size.split('x')
    with open(args.file, 'rb') as svg_file:
        PNGSurface.convert(
            bytestring=svg_file.read(),
            width=width,
            height=height,
            write_to=open(args.out, 'wb')
            )


def convert_with_svglib(args):
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    from reportlab.lib import colors

    drawing = svg2rlg(args.file)
    renderPM.drawToFile(drawing, args.out, bg=colors.HexColor('#ffffff'), fmt="PNG")


def convert_with_rsvg(args):
    import cairo
    import rsvg

    width, height = args.size.split('x')
    img =  cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
    ctx = cairo.Context(img)
    handler= rsvg.Handle(args.file)
    handler.render_cairo(ctx)
    img.write_to_png(args.out)


def convert_with_inkscape(args):
    try:
        inkscape_path = subprocess.check_output(["which", "inkscape"]).strip()
    except subprocess.CalledProcessError:
        print("ERROR: You need inkscape installed to use this script.")
        exit(1)

    export_width, export_height = args.size.split('x')

    args = [
        inkscape_path,
        "--without-gui",
        "-f", args.file,
        "--export-area-page",
        "-w", export_width,
        "-h", export_height,
        "--export-png=" + args.out
    ]
    print(args)
    subprocess.check_call(args)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help="SVG file to open")
    parser.add_argument('-s', '--size', required=True, help="target size to render")
    parser.add_argument('-o', '--out', help="Destination file")
    return parser.parse_args()


if __name__ == '__main__':
    main()



'''
set SOURCE_SVG="D:/projects/asif@github/visualization-explorations/bpmn-svg/out/cas_tld.svg"
set DEST_PNG="D:/projects/asif@github/visualization-explorations/bpmn-svg/out/cas_tld-4.png"
inkscape -z -f %SOURCE_SVG% -w 1000 -j -e %DEST_PNG%
inkscape --export-background="rgb(100, 100, 100)" --export-background-opacity=0 --export-filename=%DEST_PNG% --export-area-drawing %SOURCE_SVG%


svg_path = "D:/projects/asif@github/visualization-explorations/bpmn-svg/out/cas_tld.svg"
png_path1 = "D:/projects/asif@github/visualization-explorations/bpmn-svg/out/cas_tld-1.png"
png_path2 = "D:/projects/asif@github/visualization-explorations/bpmn-svg/out/cas_tld-2.png"
png_path3 = "D:/projects/asif@github/visualization-explorations/bpmn-svg/out/cas_tld-3.png"


from cairosvg import svg2png

with open(svg_path, "r") as f:
  svg_code = f.read()

svg2png(bytestring=svg_code,write_to=png_path1)



from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

drawing = svg2rlg(svg_path)
renderPM.drawToFile(drawing, png_path2, fmt="PNG")


def convert_with_cairosvg_sizes(args):
    from cairosvg.surface import PNGSurface
    width, height = args.size.split('x')
    with open(args.file, 'rb') as svg_file:
        PNGSurface.convert(
            bytestring=svg_file.read(),
            width=width,
            height=height,
            write_to=open(args.out, 'wb')
            )



import cairo
import rsvg

img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 640,480)

ctx = cairo.Context(img)

handle = rsvg.Handle(svg_path)

handle.render_cairo(ctx)

img.write_to_png(png_path3)
'''
