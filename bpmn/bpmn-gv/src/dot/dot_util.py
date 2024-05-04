#!/usr/bin/env python3

'''
various utilities for generating (GraphViz) dot code
'''
import re
import random
import string
import html
import textwrap

from helper.logger import *

# LaTeX escape sequences
CONV = {
    '&': r'\&amp;',
}

PROPS_TO_QUOTE = [
    "fontsize",
    "fontname",
    "penwidth",
    "margin",
    "style",
    "shape",
    "width",
    "label",
    "image",
    "xlabel",
]


''' make property lines
'''
def make_property_lines(prop_dict):
    if prop_dict is None or prop_dict == {}:
        return []

    prop_lines = []
    for k, v in prop_dict.items():
        prop_lines.append(make_a_property(prop_key=k, prop_value=v) + ";")

    return prop_lines



''' make a property list
'''
def make_property_list(prop_dict):
    if prop_dict is None or prop_dict == {}:
        return ""

    prop_list = []
    for k, v in prop_dict.items():
        prop_list.append(make_a_property(prop_key=k, prop_value=v))

    prop_str = "; ".join(prop_list)

    return prop_str



''' make a property
'''
def make_a_property(prop_key, prop_value):
    if isinstance(prop_value, str):
        check = r" ,+#\\"
        quote = any(elem in prop_value for elem in check)
    else:
        quote = False

    if prop_key in PROPS_TO_QUOTE:
        quote = True

    if quote:
        prop_str = f'{prop_key}="{prop_value}"'
    else:
        prop_str = f"{prop_key}={prop_value}"

    return prop_str



''' make a dot Node
'''
def make_a_node(id, label, prop_dict, xlabel=False):
    # label_str = make_a_property(prop_key='label', prop_value=table_from_label(label=label, sublabels=sublabels, prop_dict=prop_dict), quote=False)
    if xlabel:
        label_str = make_a_property(prop_key="xlabel", prop_value=label)
        prop_dict["label"] = ""
    else:
        label_str = make_a_property(prop_key="label", prop_value=label)

    node_str = f"{id.ljust(30)} [ id={id}; {label_str}; {make_property_list(prop_dict=prop_dict)}; ]"

    return node_str



''' make a dot Edge
'''
def make_an_edge(from_node, to_node, prop_dict):
    prop_str = make_property_list(prop_dict=prop_dict)

    if prop_str:
        edge_str = f"{from_node.ljust(30)} -> {to_node.ljust(30)} [ {prop_str}; ]"
    else:
        edge_str = f"{from_node.ljust(30)} -> {to_node}"

    return edge_str



''' wrap (in start/stop) and indent dot lines
'''
def indent_and_wrap(lines, wrap_keyword, object_id, wrap_start=" {", wrap_stop="}", indent_level=1):
    output_lines = []

    # subgraph's identifier must be prefixed with 'cluster_'
    if wrap_keyword == "subgraph ":
        object_name = f"cluster_{object_id}"
    else:
        object_name = object_id

    # start wrap
    output_lines.append(f"{wrap_keyword}{object_name}{wrap_start}")

    lines = [f"id={object_id};"] + lines

    # indent
    indent = "\t" * indent_level
    output_lines = output_lines + list(map(lambda x: f"{indent}{x}", lines))

    # stop wrap
    output_lines.append(f"{wrap_stop}")

    return output_lines



''' append single line or list of lines to a list
'''
def append_content(append_to, content):
    if content is None:
        return append_to

    if isinstance(content, str):
        append_to.append(content)

    elif isinstance(content, list):
        append_to = append_to + content

    return append_to



''' convert a text to a valid Dot identifier
'''
def text_to_identifier(text):
    # Replace SPACE with _
    id = re.sub("[ ]+", "_", text)

    # Remove invalid characters
    id = re.sub("[^0-9a-zA-Z_]", "", id)

    # Remove leading characters until we find a letter or underscore
    # id = re.sub('^[^a-zA-Z_]+', '', id)

    # prepoend an underscore if the first char is a digit
    id = re.sub("^([0-9])", r"_\1", id)

    # replace uppercase with a lowercase
    # s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', id)
    # id = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    id = id.lower()

    return id



''' wrap text by \n literal
'''
def wrap_text(text, width=50):
    lines = textwrap.wrap(text=text, width=width, break_long_words=False)
    return "\\n".join(lines)



''' get a random string
'''
def random_string(length=12):
    letters = string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(length))



''' htmlize a string
'''
def htmlize(text):
    output = html.escape(text, quote=True)
    output = output.replace(r"\n", "<BR/>")

    return output



''' text to dictionary
    "fillcolor: #F0F0F0, fontcolor: #202020" is converted to {"fillcolor": "#F0F0F0", "fontcolor": "#202020"}
'''
def text_to_dict(text):
    output_dict = {}
    pairs = text.split(",")
    for pair in pairs:
        kv = pair.split(":")
        if len(kv) == 2:
            output_dict[kv[0].strip()] = kv[1].strip()

    return output_dict



''' props to dictionary
    "fillcolor: #F0F0F0, fontcolor: #202020" is converted to {"fillcolor": "#F0F0F0", "fontcolor": "#202020"}
'''
def props_to_dict(text):
    output_dict = {}
    pairs = text.split(";")
    for pair in pairs:
        kv = pair.split("=")
        if len(kv) == 2:
            output_dict[kv[0].strip()] = kv[1].strip().strip('"').strip("'")

    return output_dict



''' :param text: a plain text message
    :return: the message escaped to appear correctly in SVG
'''
def tex_escape(text):
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(CONV.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: CONV[match.group()], text)



''' wrap a text as CDATA
'''
def wrap_as_cdata(text):
    return f"<![CDATA[{text}]]>"

    

''' output something like this
    <<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="0">
        <TR>
            <TD CELLPADDING="2">
                <FONT COLOR="#202020" FACE="Helvetica" POINT-SIZE="24">
                    Business
                </FONT>
            </TD>
        </TR>
        <TR>
            <TD>
                <FONT COLOR="#a02020" FACE="Helvetica" POINT-SIZE="20">
                    <U><I>Sharafat</I></U>
                </FONT>
            </TD>
        </TR>
        <TR>
            <TD>
                <FONT COLOR="#2020a0" POINT-SIZE="16">
                    Apr 2023
                </FONT>
            </TD>
        </TR>
    </TABLE>>
'''
def table_from_label(label, sublabels, prop_dict):
    text_lines = []

    # the label, wrap in a FONT
    label_lines = []
    label_lines.append(htmlize(label))

    font_props = {
        "COLOR": prop_dict["fontcolor"],
        "FACE": prop_dict["fontname"],
        "POINT-SIZE": prop_dict["fontsize"],
    }
    font_prop_str = make_property_list(prop_dict=font_props)
    font_start = f"<FONT {font_prop_str}>"
    font_end = "</FONT>"
    label_lines = indent_and_wrap(
        label_lines,
        wrap_keyword="",
        object_name="",
        wrap_start=font_start,
        wrap_stop=font_end,
        indent_level=1,
    )

    # wrap in a TD
    td_props = {"CELLPADDING": 2}
    td_prop_str = make_property_list(prop_dict=td_props)
    td_start = f"<TD {td_prop_str}>"
    td_end = "</TD>"
    label_lines = indent_and_wrap(
        label_lines,
        wrap_keyword="",
        object_name="",
        wrap_start=td_start,
        wrap_stop=td_end,
        indent_level=1,
    )

    # wrap in a TR
    label_lines = indent_and_wrap(
        label_lines,
        wrap_keyword="",
        object_name="",
        wrap_start="<TR>",
        wrap_stop="</TR>",
        indent_level=1,
    )

    # sublabel 1, italic and wrap in a FONT
    label1_lines = []
    if len(sublabels) >= 1:
        label1_lines.append(htmlize(sublabels[0]))
        label1_lines = indent_and_wrap(
            label1_lines,
            wrap_keyword="",
            object_name="",
            wrap_start="<I>",
            wrap_stop="</I>",
            indent_level=1,
        )
        if len(sublabels) >= 2:
            label1_lines = indent_and_wrap(
                label1_lines,
                wrap_keyword="",
                object_name="",
                wrap_start="<U>",
                wrap_stop="</U>",
                indent_level=1,
            )

        font_props = {
            "COLOR": prop_dict["fontcolorsub"],
            "FACE": prop_dict["fontname"],
            "POINT-SIZE": int(prop_dict["fontsize"]) * 0.9,
        }
        font_prop_str = make_property_list(prop_dict=font_props)
        font_start = f"<FONT {font_prop_str}>"
        font_end = "</FONT>"
        label1_lines = indent_and_wrap(
            label1_lines,
            wrap_keyword="",
            object_name="",
            wrap_start=font_start,
            wrap_stop=font_end,
            indent_level=1,
        )

        # wrap in a TD
        label1_lines = indent_and_wrap(
            label1_lines,
            wrap_keyword="",
            object_name="",
            wrap_start="<TD>",
            wrap_stop="</TD>",
            indent_level=1,
        )

        # wrap in a TR
        label1_lines = indent_and_wrap(
            label1_lines,
            wrap_keyword="",
            object_name="",
            wrap_start="<TR>",
            wrap_stop="</TR>",
            indent_level=1,
        )

    # sublabel 1, italic and wrap in a FONT
    label2_lines = []
    if len(sublabels) >= 2:
        label2_lines.append(htmlize(sublabels[1]))
        label2_lines = indent_and_wrap(
            label2_lines,
            wrap_keyword="",
            object_name="",
            wrap_start="<I>",
            wrap_stop="</I>",
            indent_level=1,
        )

        font_props = {
            "COLOR": prop_dict["fontcolor"],
            "FACE": prop_dict["fontname"],
            "POINT-SIZE": int(prop_dict["fontsize"]) * 0.8,
        }
        font_prop_str = make_property_list(prop_dict=font_props)
        font_start = f"<FONT {font_prop_str}>"
        font_end = "</FONT>"
        label2_lines = indent_and_wrap(
            label2_lines,
            wrap_keyword="",
            object_name="",
            wrap_start=font_start,
            wrap_stop=font_end,
            indent_level=1,
        )

        # wrap in a TD
        label2_lines = indent_and_wrap(
            label2_lines,
            wrap_keyword="",
            object_name="",
            wrap_start="<TD>",
            wrap_stop="</TD>",
            indent_level=1,
        )

        # wrap in a TR
        label2_lines = indent_and_wrap(
            label2_lines,
            wrap_keyword="",
            object_name="",
            wrap_start="<TR>",
            wrap_stop="</TR>",
            indent_level=1,
        )

    text_lines = label_lines + label1_lines + label2_lines

    # wrap in a TABLE
    table_props = {"BORDER": 0, "CELLSPACING": 0, "CELLPADDING": 0}
    table_prop_str = make_property_list(prop_dict=table_props)
    table_start = f"<<TABLE {table_prop_str}>"
    table_end = "\t\t</TABLE>>"
    text_lines = indent_and_wrap(
        text_lines,
        wrap_keyword="",
        object_name="",
        wrap_start=table_start,
        wrap_stop=table_end,
        indent_level=3,
    )

    text = "\n".join(text_lines)
    # print(text)

    return text
