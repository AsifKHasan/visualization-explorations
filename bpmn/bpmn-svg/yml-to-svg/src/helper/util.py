#!/usr/bin/env python3
import re
import random
import string
import textwrap

from helper.logger import *

'''various utilities
'''

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