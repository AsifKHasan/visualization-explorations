#!/usr/bin/env python3
'''
'''
import sys

from PyQt5 import QtWidgets

from qt.main_window import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app.primaryScreen())
    app.exec()
