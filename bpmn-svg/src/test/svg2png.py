from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

svg_path = "../../out/req_for_aw_user_01.svg"
png_path = "../../out/req_for_aw_user_01.png"

drawing = svg2rlg(svg_path)
renderPM.drawToFile(drawing, png_path, fmt="PNG")
