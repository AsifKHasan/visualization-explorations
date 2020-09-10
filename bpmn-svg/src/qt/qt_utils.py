import sys
from pathlib import Path

from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QPainter, QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtCore import QObject, QRegExp, QPoint, QPointF, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt import *

class CollapsibleFrame(QWidget):
    def __init__(self, parent=None, text=None, icon='bpmn', title_style=None, content_style=None):
        QFrame.__init__(self, parent=parent)

        self._is_collasped = True
        self._title_frame = None
        self._content, self._content_layout = (None, None)

        self._main_v_layout = QVBoxLayout(self)
        self._main_v_layout.setSpacing(0)
        self._main_v_layout.setContentsMargins(0, 0, 0, 0)
        self._main_v_layout.addWidget(self.initTitleFrame(text, self._is_collasped, icon, title_style))
        self._main_v_layout.addWidget(self.initContent(self._is_collasped, content_style))

        self.initCollapsable()

    def initTitleFrame(self, text, collapsed, icon='bpmn', title_style=None):
        self._title_frame = self.TitleFrame(icon=icon, text=text, collapsed=collapsed)
        self._title_frame.setStyleSheet(title_style)

        return self._title_frame

    def initContent(self, collapsed, content_style=None):
        self._content = QWidget()
        self._content.setStyleSheet(content_style)
        self._content_layout = QVBoxLayout()

        self._content.setLayout(self._content_layout)
        self._content.setVisible(not collapsed)

        return self._content

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def initCollapsable(self):
        self._title_frame.clicked.connect(self.toggleCollapsed)

    def toggleCollapsed(self):
        self._content.setVisible(self._is_collasped)
        self._is_collasped = not self._is_collasped

    def set_styles(self, title_style, content_style):
        self._title_frame.setStyleSheet(title_style)
        self._content.setStyleSheet(content_style)


    # TITLE
    class TitleFrame(QFrame):
        clicked = pyqtSignal()

        def __init__(self, parent=None, icon='bpmn', text='', collapsed=False):
            super(QFrame, self).__init__(parent=parent)

            self.setMinimumHeight(24)
            self.move(QPoint(24, 0))
            # self.setStyleSheet("border:1px solid rgb(41, 41, 41); ")

            self._hlayout = QHBoxLayout(self)
            self._hlayout.setContentsMargins(0, 0, 0, 0)
            self._hlayout.setSpacing(0)

            self._arrow, self._icon, self._title = None, None, None

            self._hlayout.addWidget(self.init_arrow())
            self._hlayout.addWidget(self.init_title(text))
            self._hlayout.addWidget(self.init_icon(icon))
            # self._hlayout.addStretch()

        def init_arrow(self):
            self._arrow = QtWidgets.QToolButton(checkable=True, checked=False)
            self._arrow.setStyleSheet("QToolButton { border: none; }")
            self._arrow.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            self._arrow.setArrowType(QtCore.Qt.RightArrow)
            self._arrow.pressed.connect(self.on_pressed)

            return self._arrow

        def init_icon(self, icon='bpmn'):
            self._icon = QLabel()

            # print(icon, ICONS)
            pixmap = QPixmap(ICONS[icon])
            pixmap = pixmap.scaledToHeight(24)
            self._icon.setPixmap(pixmap)
            self._icon.setMask(pixmap.mask())
            self._icon.setMinimumHeight(24)
            # self._icon.setFixedSize(64, 64)
            # self._icon.move(QPoint(24, 0))
            # self._icon.show()
            # self._icon.setStyleSheet("border:2px; border-color: #FF0000;")

            return self._icon

        def init_title(self, text=None):
            self._title = QLabel(text)
            self._title.setMinimumHeight(24)
            # self._title.move(QtCore.QPoint(12, 0))
            # self._title.setStyleSheet("border:1px; border-color: #FF0000;")

            return self._title

        def on_pressed(self):
            checked = self._arrow.isChecked()
            self._arrow.setArrowType(QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
            self.clicked.emit()

        def mousePressEvent(self, event):
            self.clicked.emit()


def open_file(parent, dialog_title, dialog_location=Path("~").expanduser().as_posix(), file_filter=None, ):
    return QFileDialog.getOpenFileName(parent, caption=dialog_title, directory=dialog_location, filter=file_filter)


def save_file(parent, dialog_title, dialog_location=Path("~").expanduser().as_posix(), file_filter=None, ):
    return QFileDialog.getSaveFileName(parent, caption=dialog_title, directory=dialog_location, filter=file_filter)


'''
    Return a QTextCharFormat with the given attributes.
'''
def format(color, style=''):
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format

# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format('red'),
    'operator': format('darkMagenta'),
    'brace': format('darkMagenta'),
    'elements': format('blue'),
    'string': format('darkGreen'),
    'multiline-comment': format('darkGray'),
    'comment': format('darkGray', 'italic'),
    'numbers': format('brown'),
}

'''
    Syntax highlighter for the Bpmn language.
'''
class BpmnHighlighter (QSyntaxHighlighter):
    # Bpmn keywords
    keywords = [
        'graph', 'lane', 'pool',
        'label', 'hide_labels', 'hide_label', 'move_x', 'label_pos',
    ]

    # Bpmn operators
    operators = [
        '=',
        # edges
        '-->', '~~>', '\.\.\.>', '\.\.\.', '<\.\.',
    ]

    # Bpmn braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    # Bpmn elements
    elements = [
        'task', 'businessRuleTask', 'manualTask', 'receiveTask', 'scriptTask', 'sendTask', 'serviceTask', 'userTask',
        'call', 'businessRuleCall', 'manualCall', 'scriptCall', 'userCall',
        'process', 'adhoc', 'transaction',
        'event', 'eventCompensation', 'eventConditional', 'eventConditionalNon', 'eventError', 'eventEscalation', 'eventEscalationNon', 'eventMessage', 'eventMessageNon', 'eventMultiple', 'eventMultipleNon', 'eventParallelMultiple', 'eventParallelMultipleNon', 'eventSignal', 'eventSignalNon', 'eventTimer', 'eventTimerNon',
        'group', 'annotation',
        'data', 'dataCollection', 'dataInput', 'dataInputCollection', 'dataOutput', 'dataOutputCollection', 'dataStore',
        'start', 'startCompensation', 'startConditional', 'startConditionalNon', 'startError', 'startEscalation', 'startEscalationNon', 'startMessage', 'startMessageNon', 'startMultiple', 'startMultipleNon', 'startParallelMultiple', 'startParallelMultipleNon', 'startSignal', 'startSignalNon', 'startTimer', 'startTimerNon',
        'end', 'endCancel', 'endCompensation', 'endError', 'endEscalation', 'endMessage', 'endMultiple', 'endSignal', 'endTerminate',
        'intermediate', 'catchCancel', 'catchCompensation', 'throwCompensation', 'catchError', 'catchEscalation', 'catchEscalationNon', 'throwEscalation', 'catchLink', 'throwLink', 'catchMessage', 'catchMessageNon', 'throwMessage', 'catchMultiple', 'catchMultipleNon', 'throwMultiple', 'catchParallelMultiple', 'catchParallelMultipleNon', 'catchSignal', 'catchSignalNon', 'throwSignal', 'conditional', 'conditionalNon', 'timer', 'timerNon',
        'inclusive', 'exclusive', 'parallel', 'complex', 'eventBased', 'eventBasedStart', 'eventBasedParallelStart'
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        # Multi-line comments
        self.comment_start_expression = QRegExp("/\\*")
        self.comment_end_expression = QRegExp("\\*/")

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in BpmnHighlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator']) for o in BpmnHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace']) for b in BpmnHighlighter.braces]
        rules += [(r'\b%s\b' % b, 0, STYLES['elements']) for b in BpmnHighlighter.elements]

        # All other rules
        rules += [
            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # From '#' until a newline
            (r'#[^\n]*', 0, STYLES['comment']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]


    '''
    Apply syntax highlighting to the given block of text.
    '''
    def highlightBlock(self, text):
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                # length = expression.cap(nth).length()
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.comment_start_expression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.comment_end_expression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.comment_end_expression.matchedLength()

            self.setFormat(startIndex, commentLength, STYLES['multiline-comment'])
            startIndex = self.comment_start_expression.indexIn(text, startIndex + commentLength);


        # Do multi-line strings
        # in_multiline = self.match_multiline(text, *self.tri_single)
        # if not in_multiline:
        #     in_multiline = self.match_multiline(text, *self.tri_double)


    '''
    Do highlighting of multi-line strings. ``delimiter`` should be a
    ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
    ``in_state`` should be a unique integer to represent the corresponding
    state changes when inside those strings. Returns True if we're still
    inside a multi-line string when this function is finished.
    '''
    def match_multiline(self, text, delimiter, in_state, style):
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = text.length() - start + add

            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
