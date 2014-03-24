#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtSvg
from PyQt4 import QtGui
from PyQt4 import QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class widget4svg(QtSvg.QSvgWidget):
    
    def __init__(self, parent=None):
        super(widget4svg, self).__init__(parent)
        
        self.load(_fromUtf8(':images/images/schematic_from_model_view.svg'))


