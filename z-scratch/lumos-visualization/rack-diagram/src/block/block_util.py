#!/usr/bin/env python3

'''
various utilities for working with blocks
'''
import re
import random
import string

from helper.logger import *


''' convert a text to Pascal cased literal
'''
def pascal_case(text):
    output_text = text.title()

    return output_text