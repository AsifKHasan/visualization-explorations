#!/usr/bin/env python3
'''
'''

from PyQt5.QtCore import QObject, pyqtSignal

class LogStream(QObject):

    log_generated = pyqtSignal(str)

    def write(self, text):
        self.log_generated.emit(str(text))
