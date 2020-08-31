import sys
from pathlib import Path

from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtCore import QObject, QRegExp, QPoint, QPointF, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

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


class CollapsibleFrame(QWidget):
    def __init__(self, parent=None, title=None):
        QFrame.__init__(self, parent=parent)

        self._is_collasped = True
        self._title_frame = None
        self._content, self._content_layout = (None, None)

        self._main_v_layout = QVBoxLayout(self)
        self._main_v_layout.addWidget(self.initTitleFrame(title, self._is_collasped))
        self._main_v_layout.addWidget(self.initContent(self._is_collasped))

        self.initCollapsable()

    def initTitleFrame(self, title, collapsed):
        self._title_frame = self.TitleFrame(title=title, collapsed=collapsed)

        return self._title_frame

    def initContent(self, collapsed):
        self._content = QWidget()
        self._content_layout = QVBoxLayout()

        self._content.setLayout(self._content_layout)
        self._content.setVisible(not collapsed)

        return self._content

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def initCollapsable(self):
        self._title_frame.clicked.connect(self.toggleCollapsed)
        # QtCore.connect(self._title_frame, QtCore.SIGNAL('clicked()'), self.toggleCollapsed)

    def toggleCollapsed(self):
        self._content.setVisible(self._is_collasped)
        self._is_collasped = not self._is_collasped
        self._title_frame._arrow.setArrow(int(self._is_collasped))

    ############################
    #           TITLE          #
    ############################
    class TitleFrame(QFrame):
        clicked = pyqtSignal()

        def __init__(self, parent=None, title="", collapsed=False):
            super(QFrame, self).__init__(parent=parent)

            self.setMinimumHeight(24)
            self.move(QPoint(24, 0))
            # self.setStyleSheet("border:1px solid rgb(41, 41, 41); ")

            self._hlayout = QHBoxLayout(self)
            self._hlayout.setContentsMargins(0, 0, 0, 0)
            self._hlayout.setSpacing(0)

            self._arrow = None
            self._title = None

            self._hlayout.addWidget(self.initArrow(collapsed))
            self._hlayout.addWidget(self.initTitle(title))

        def initArrow(self, collapsed):
            self._arrow = CollapsibleFrame.Arrow(collapsed=collapsed)
            self._arrow.setStyleSheet("border:0px")

            return self._arrow

        def initTitle(self, title=None):
            self._title = QLabel(title)
            self._title.setMinimumHeight(24)
            self._title.move(QtCore.QPoint(24, 0))
            self._title.setStyleSheet("border:0px")

            return self._title

        def mousePressEvent(self, event):
            self.clicked.emit()


    #############################
    #           ARROW           #
    #############################
    class Arrow(QFrame):
        def __init__(self, parent=None, collapsed=False):
            super(QFrame, self).__init__(parent=parent)

            self.setMaximumSize(24, 24)

            # horizontal == 0
            self._arrow_horizontal = (QPointF(7.0, 8.0), QPointF(17.0, 8.0), QPointF(12.0, 13.0))
            # vertical == 1
            self._arrow_vertical = (QPointF(8.0, 7.0), QPointF(13.0, 12.0), QPointF(8.0, 17.0))
            # arrow
            self._arrow = None
            self.setArrow(int(collapsed))

        def setArrow(self, arrow_dir):
            if arrow_dir:
                self._arrow = self._arrow_vertical
            else:
                self._arrow = self._arrow_horizontal

        def paintEvent(self, event):
            painter = QPainter()
            painter.begin(self)
            painter.setBrush(QtGui.QColor(192, 192, 192))
            painter.setPen(QtGui.QColor(64, 64, 64))
            painter.drawPolygon(*self._arrow)
            painter.end()


class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, text='', parent=None):
        super().__init__(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.toggle_button = QtWidgets.QToolButton(text=text, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        self.content_area = QtWidgets.QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self.content_area, b"maximumHeight"))

    @QtCore.pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
        self.toggle_animation.setDirection(QtCore.QAbstractAnimation.Forward if not checked else QtCore.QAbstractAnimation.Backward)
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (self.sizeHint().height() - self.content_area.maximumHeight())
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(200)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(200)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


class CollapsibleDialog(QDialog):
    '''a dialog to which collapsible sections can be added;
    subclass and reimplement define_sections() to define sections and
    add them as (title, widget) tuples to self.sections
    '''
    def __init__(self, sections):
        super().__init__()
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)
        self.tree.setIndentation(0)
        self.tree.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.sections = sections
        self.add_sections()

    def add_sections(self):
        '''adds a collapsible sections for every (title, widget) tuple in self.sections
        '''
        for (title, widget) in self.sections:
            button1 = self.add_button(title)
            section1 = self.add_widget(button1, widget)
            button1.addChild(section1)

    def define_sections(self):
        '''reimplement this to define all your sections and add them as (title, widget) tuples to self.sections
        '''
        widget = QFrame(self.tree)
        layout = QHBoxLayout(widget)
        layout.addWidget(QLabel(self.bpmn_id))
        layout.addWidget(QLabel(self.bpmn_data['label']))
        title = self.title
        self.sections.append((title, widget))

    def add_button(self, title):
        '''creates a QTreeWidgetItem containing a button to expand or collapse its section
        '''
        item = QTreeWidgetItem()
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 0, SectionExpandButton(item, text=title))
        return item

    def add_widget(self, button, widget):
        '''creates a QWidgetItem containing the widget, as child of the button-QWidgetItem
        '''
        section = QTreeWidgetItem(button)
        section.setDisabled(True)
        self.tree.setItemWidget(section, 0, widget)
        return section

class SectionExpandButton(QPushButton):
    '''a QPushbutton that can expand or collapse its section
    '''
    def __init__(self, section, text='', parent=None):
        super().__init__(text, parent)
        self.section = section
        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        '''toggle expand/collapse of section by clicking
        '''
        if self.section.isExpanded():
            self.section.setExpanded(False)
        else:
            self.section.setExpanded(True)
