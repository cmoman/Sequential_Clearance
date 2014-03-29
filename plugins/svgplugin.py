# -*- coding: utf-8 -*-
#
# Copyright © 2009 Pierre Raybaut
# Licensed under the terms of the MIT License

from PyQt4.QtGui import QIcon
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin

import os
from matplotlib import rcParams
from widget4svg import widget4svg

rcParams['font.size'] = 9

class SVGPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        QPyDesignerCustomWidgetPlugin.__init__(self)

        self._initialized = False

    def initialize(self, formEditor):
        if self._initialized:
            return

        self._initialized = True

    def isInitialized(self):
        return self._initialized

    def createWidget(self, parent):
        return widget4svg(parent)

    def name(self):
        return "widget4svg"

    def group(self):
        return "Matplotlib4devs"

    def icon(self):
        image = os.path.join(rcParams['datapath'], 'images', 'matplotlib.png')
        return QIcon(image)

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def domXml(self):
        return '<widget class="widget4svg" name="widget4svg">\n' \
               '</widget>\n'

    def includeFile(self):
        return "widget4svg"


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    widget = widget4svg()
    widget.show()
    sys.exit(app.exec_())
