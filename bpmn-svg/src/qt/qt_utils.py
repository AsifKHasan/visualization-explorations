import sys
import textwrap
from pathlib import Path

from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtCore import QObject, QRegExp, QPoint, QPointF, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

from qt import *

def lane_pool_type_of_node(node_id, bpmn_data):
    for lane_id in bpmn_data['lanes']:
        for pool_id in bpmn_data['lanes'][lane_id]['pools']:
            if node_id in bpmn_data['lanes'][lane_id]['pools'][pool_id]['nodes']:
                return lane_id, pool_id, bpmn_data['lanes'][lane_id]['pools'][pool_id]['nodes'][node_id]['type']

    return None, None, None

class NodeSelectionDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setWindowTitle('Node selection')
        self.setMinimumSize(300, 400)
        self.setWindowFlags(QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint)

        self.selected_lane, self.selected_pool, self.selected_node = None, None, None

        self.init_ui()
        self.signals_and_slots()

    def init_ui(self):
        layout = QVBoxLayout()

        # the node tree
        self.node_tree = QTreeWidget(self)
        self.node_tree.setStyleSheet('background-color: "#F8F8F8"')
        self.node_tree.setHeaderHidden(True)
        layout.addWidget(self.node_tree)

        # the select button
        self.select = QPushButton('Select node')
        # self.select.setStyleSheet('background-color: "#D8D8D8"')
        self.select.setStyleSheet('QPushButton:disabled {background-color:#E8E8E8;}')
        self.select.setEnabled(False)
        layout.addWidget(self.select)

        self.setLayout(layout)

    def init_tree(self):
        # populate the tree
        for lane_id in self.bpmn_data['lanes']:
            # if scope is 'bpmn' and it is a to node, then we do not allow the lane from from_node
            if self.scope in ['bpmn'] and self.role == 'to' and lane_id == self.other_node_values[0]:
                continue

            # if scope is lane or pool and lane_id is not None, we only show the specific lane
            print(self.scope, self.lane_id, self.pool_id)
            if self.scope in ['lane', 'pool'] and self.lane_id is not None and lane_id != self.lane_id:
                continue

            lane_item = QTreeWidgetItem(self.node_tree, 0)
            lane_item.setText(0, lane_id)
            for pool_id in self.bpmn_data['lanes'][lane_id]['pools']:
                # if scope is pool and pool_id is not None, we only show the specific pool
                if self.scope in ['pool'] and self.lane_id is not None and self.pool_id is not None and lane_id == self.lane_id and pool_id != self.pool_id:
                    continue

                pool_item = QTreeWidgetItem(lane_item, 1)
                pool_item.setText(0, pool_id)
                for node_id in self.bpmn_data['lanes'][lane_id]['pools'][pool_id]['nodes']:
                    node_item = QTreeWidgetItem(pool_item, 2)
                    node_item.setText(0, node_id)
                    # preselect node if passed (not None)
                    if self.node_id and node_id == self.node_id:
                        self.node_tree.setCurrentItem(node_item)

    def signals_and_slots(self):
        self.select.clicked.connect(self.on_accept)
        self.node_tree.currentItemChanged.connect(self.on_current_item_change)

    def on_current_item_change(self, current, previous):
        if current.type() == 2:
            # print(current.text(0))
            self.select.setEnabled(True)
        else:
            self.select.setEnabled(False)

    def on_accept(self):
        selected_node_item = self.node_tree.currentItem()
        if selected_node_item:
            self.selected_node = selected_node_item.text(0)
            selected_pool_item = selected_node_item.parent()
            self.selected_pool = selected_pool_item.text(0)
            selected_lane_item = selected_pool_item.parent()
            self.selected_lane = selected_lane_item.text(0)
        else:
            self.selected_lane, self.selected_pool, self.selected_node = None, None, None

        self.accept()

    @staticmethod
    def open(parent, lane_id, pool_id, node_id, bpmn_data, scope, role, other_node_values):

        dialog = NodeSelectionDialog(parent)
        dialog.parent, dialog.lane_id, dialog.pool_id, dialog.node_id, dialog.bpmn_data, dialog.scope, dialog.role, dialog.other_node_values = parent, lane_id, pool_id, node_id, bpmn_data, scope, role, other_node_values
        dialog.init_tree()

        result = dialog.exec_()

        if result == QDialog.Accepted:
            return dialog.selected_lane, dialog.selected_pool, dialog.selected_node
        else:
            return None, None, None


class EdgeNodeWidget(QWidget):
    nodeChanged = pyqtSignal()

    def __init__(self, lane_id, pool_id, node_id, bpmn_data, scope='bpmn', role='from', parent=None):
        QFrame.__init__(self, parent=parent)
        self.node_id, self.bpmn_data, self.scope, self.role = node_id, bpmn_data, scope, role
        self.lane_id, self.pool_id, self.node_type, self.other_node_values = lane_id, pool_id, None, None
        self.init_widget()
        self.signals_and_slots()
        self.populate()

    def init_widget(self):
        self.content_layout = QGridLayout(self)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # lane and pool
        self.lane_and_pool = QLineEdit()
        self.lane_and_pool.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lane_and_pool.setStyleSheet('background-color: "#D8D8D8"')
        self.lane_and_pool.setReadOnly(True)
        self.content_layout.addWidget(self.lane_and_pool, 0, 0, 1, 3)

        # node_id
        self.id = QLineEdit()
        self.id.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.id.setStyleSheet('background-color: "#F8F8F8"')
        self.id.setReadOnly(True)
        self.content_layout.addWidget(self.id, 1, 0, 1, 2)

        # node_type
        self.icon = QPushButton()
        self.content_layout.addWidget(self.icon, 1, 2, 1, 1)

        for c in range(0, self.content_layout.columnCount()):
            self.content_layout.setColumnStretch(c, 1)


    def signals_and_slots(self):
        self.icon.clicked.connect(self.on_selection_dialog)

    def populate(self):
        lane_id, pool_id, node_type = lane_pool_type_of_node(self.node_id, self.bpmn_data)
        if self.scope == 'bpmn':
            self.lane_id, self.pool_id, self.node_type = lane_id, pool_id, node_type

        elif self.scope == 'lane':
            self.pool_id, self.node_type = pool_id, node_type

        elif self.scope == 'pool':
            self.node_type = node_type


        if self.lane_id:
            self.lane_and_pool.setText('{0} : {1}'.format(self.lane_id, self.pool_id))

        if self.node_id:
            self.id.setText(self.node_id)

        if self.node_type:
            pixmap = QPixmap(ICONS[self.node_type])
            # pixmap = pixmap.scaledToHeight(24)
            self.icon.setIcon(QIcon(pixmap))

    def on_selection_dialog(self):
        lane_id, pool_id, node_id = NodeSelectionDialog.open(self, self.lane_id, self.pool_id, self.node_id, self.bpmn_data, self.scope, self.role, self.other_node_values)
        # print(lane_id, pool_id, node_id)
        if node_id and node_id != self.node_id:
            self.lane_id, self.pool_id, self.node_id = lane_id, pool_id, node_id
            self.populate()
            self.nodeChanged.emit()

    def values(self):
        return self.lane_id, self.pool_id, self.node_id, self.node_type

    def set_other_node_values(self, val):
        self.other_node_values = val


class WarningWidget(QWidget):
    def __init__(self, warning='', parent=None):
        QFrame.__init__(self, parent=parent)
        self.content_layout = QGridLayout(self)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # warning
        self.warning_label = QLabel()
        self.warning_label.setStyleSheet('color: "#cc4125"')
        self.content_layout.addWidget(self.warning_label, 0, 0, 1, 1)

        self.warning_label.setText(warning)

        # self.addWidget(content)

        for c in range(0, self.content_layout.columnCount()):
            self.content_layout.setColumnStretch(c, 1)


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

        self.initCollapsible()

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

    def clearContent(self):
        # clear the layout safely
        for i in reversed(range(self._content_layout.count())):
            widgetToRemove = self._content_layout.itemAt(i).widget()
            # remove it from the layout list
            self._content_layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def initCollapsible(self):
        self._title_frame.clicked.connect(self.toggleCollapsed)

    def toggleCollapsed(self):
        self._content.setVisible(self._is_collasped)
        self._is_collasped = not self._is_collasped

    def set_styles(self, title_style, content_style):
        self._title_frame.setStyleSheet(title_style)
        self._content.setStyleSheet(content_style)

    def change_title(self, text=None, icon=None, err=False):
        self._title_frame.change_title(text, icon, err)

    def add_button(self, widget, key):
        self._title_frame.add_button(widget, key)

    # TITLE
    class TitleFrame(QFrame):
        clicked = pyqtSignal()

        def __init__(self, parent=None, icon='bpmn', text='', collapsed=False):
            super(QFrame, self).__init__(parent=parent)

            self.setMinimumHeight(25)
            self.move(QPoint(25, 0))
            # self.setStyleSheet("border:1px solid rgb(41, 41, 41); ")

            self._hlayout = QHBoxLayout(self)
            self._hlayout.setContentsMargins(0, 0, 0, 0)
            self._hlayout.setSpacing(0)

            self._arrow, self._icon, self._title = None, None, None

            self._hlayout.addWidget(self.init_arrow())
            self._hlayout.addWidget(self.init_title(text))
            self._hlayout.addStretch()
            self._hlayout.addWidget(self.init_icon(icon))
            self._hlayout.addStretch()
            self._hlayout.addWidget(self.init_buttons())
            # self._hlayout.addStretch()

        def init_arrow(self):
            self._arrow = QtWidgets.QToolButton(checkable=True, checked=False)
            self._arrow.setStyleSheet("QToolButton { border: none; }")
            self._arrow.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            self._arrow.setArrowType(QtCore.Qt.RightArrow)
            self._arrow.pressed.connect(self.on_pressed)

            return self._arrow

        def init_title(self, text=None):
            # make the text at least 40 char wide
            t = textwrap.fill(text, width=100)
            self._title = QLabel(text)
            self._title.setMinimumHeight(25)
            self._title.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            # self._title.move(QtCore.QPoint(12, 0))
            # self._title.setStyleSheet("border:1px; border-color: #FF0000;")

            return self._title

        def init_icon(self, icon='bpmn'):
            self._icon = QLabel()

            # print(icon, ICONS)
            pixmap = QPixmap(ICONS[icon])
            pixmap = pixmap.scaledToHeight(25)
            self._icon.setPixmap(pixmap)
            # self._icon.setMask(pixmap.mask())
            # self._icon.setMinimumHeight(25)
            # self._icon.setFixedSize(64, 64)
            # self._icon.move(QPoint(24, 0))
            # self._icon.show()
            # self._icon.setStyleSheet("border:2px; border-color: #FF0000;")

            return self._icon

        def init_buttons(self):
            self._buttons = QWidget()
            self._buttons.setMinimumHeight(25)
            # self._title.move(QtCore.QPoint(12, 0))
            # self._title.setStyleSheet("border:1px; border-color: #FF0000;")
            self._buttons_layout = QHBoxLayout(self._buttons)
            self._buttons_layout.setContentsMargins(0, 0, 0, 0)
            self._buttons_layout.setSpacing(0)
            self._buttons_layout.addStretch()

            self._button_list = {}

            return self._buttons

        def add_button(self, widget, key):
            self._button_list[key] = widget
            self._buttons_layout.addWidget(widget)

        def change_title(self, text=None, icon=None, err=False):
            self._title.setText(text)
            self._title.setMinimumHeight(25)

            pixmap = QPixmap(ICONS[icon])
            pixmap = pixmap.scaledToHeight(25)
            self._icon.setPixmap(pixmap)

            if err:
                self.setStyleSheet("background-color: #F4CCCC; ")
            else:
                self.setStyleSheet("background-color: none; ")


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
