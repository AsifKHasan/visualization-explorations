import sys
from pathlib import Path

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import QFileDialog


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
