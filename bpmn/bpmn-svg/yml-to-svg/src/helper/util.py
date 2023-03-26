#!/usr/bin/env python3
import sys
import math
import re
import random
import string
import textwrap
from PIL import ImageFont

from helper.logger import *

'''various utilities
'''

FONT_SPEC = {
    'arial' : {
        'win32' : 'arial',
        'linux' : '/usr/share/fonts/truetype/msttcorefonts/arial.ttf',
        'darwin' : '/Library/Fonts/Arial.ttf'
    },
    'arial-bold' : {
        'win32' : 'arialbd',
        'linux' : 'A/usr/share/fonts/truetype/msttcorefonts/arialbd.ttf',
        'darwin' : '/Library/Fonts/Arial Bold.ttf'
    },
    'calibri' : {
        'win32' : 'calibri',
        'linux' : 'Calibri.ttf',
        'darwin' : '/Library/Fonts/Calibri.ttf'
    },
    'calibri-bold' : {
        'win32' : 'calibrib',
        'linux' : 'Calibri Bold.ttf',
        'darwin' : '/Library/Fonts/Calibri Bold.ttf'
    },
}


''' convert a text to a valid Dot identifier
'''
def text_to_identifier(text):
    # Replace SPACE with _
    id = re.sub('[ ]+', '_', text)

    # Remove invalid characters
    id = re.sub('[^0-9a-zA-Z_]', '', id)

    # prepoend an underscore if the first char is a digit
    id = re.sub('^([0-9])', r'_\1', id)

    # replace uppercase with a lowercase
    id = id.lower()

    return id


''' get a random string
'''
def random_string(length=12):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))


''' props to dictionary
    north="10" south="10" west="10" east="10" is converted to {"north": "10", "south": "10", "west": "10", "east": "10"}
'''
def props_to_dict(text):
    output_dict = {}
    if text:
        pairs = text.split(' ')
        for pair in pairs:
            kv = pair.split('=')
            if len(kv) == 2:
                output_dict[kv[0].strip()] = kv[1].strip().strip('"').strip("'")
            
    return output_dict



''' given a number return a balanced range half of which is -ve, half of which is +ve
'''
def balanced_range(n):
    if n == 1:
        return [0]

    m = int(n/2)
    if (n % 2) == 1:
        return [x for x in range(-m, m+1)]

    else:
        return [x+0.5 for x in range(-m, m)]
    


''' get the rough size of text in pixel
'''
def text_size_in_pixels(text, font_family, font_size, font_weight='', stroke_width=0):
    adjusted_text = ' ' + text + ' '
    if font_weight != '':
        font_key = font_family + '-' + font_weight
    else:
        font_key = font_family

    try:
        font_path = FONT_SPEC[font_key][sys.platform]
        font = ImageFont.truetype(font_path, font_size, layout_engine=ImageFont.LAYOUT_BASIC)
    except:
        font_path = FONT_SPEC['arial-bold'][sys.platform]
        font = ImageFont.truetype(font_path, font_size, layout_engine=ImageFont.LAYOUT_BASIC)

    # debug('sizing [{0}] with font {1} size {2}'.format(text, font_path, font_size))
    size = font.getsize(adjusted_text, stroke_width=stroke_width)

    return size

