#!/usr/bin/env python3

''' various exceptions
'''

class BpmnDataMissing(Exception):
    def __init__(self, data, key):
        self.message = f"{data} data missing [{key}] key"
        super().__init__(self.message)


class ThemeDataMissing(Exception):
    def __init__(self, data, key):
        self.message = f"theme {data} missing [{key}] key"
        super().__init__(self.message)


