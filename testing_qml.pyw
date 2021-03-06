#!/usr/bin/env python
# -*- coding: utf-8 -*-
# used to parse files more easily
from __future__ import with_statement

# Numpy module
#import numpy as np

# for command-line arguments
import sys
import time
from PyQt4 import QtCore

# Python Qt4 bindings for GUI objects
from PyQt4 import QtGui

from PyQt4 import QtDeclarative
from PyQt4 import QtNetwork

import os

if os.name == 'nt': # Windows

    import ctypes
    myappid = 'tesla.sequential_clearance.0.9' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
# import the MainWindow widget from the converted .ui files
from ui_testQML import Ui_MainWindow

class Now(QtCore.QObject):

    now = QtCore.pyqtSignal(str)

    def emit_now(self):
        formatted_date = QtCore.QDateTime.currentDateTime().toString()
        self.now.emit(formatted_date) 

class DesignerMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """Customization for Qt Designer created window"""
    def __init__(self, parent = None):
        # initialization of the superclass
        super(DesignerMainWindow, self).__init__(parent)
        # setup the GUI --> function generated by pyuic4
        self.setupUi(self)
        
        self.initUI()
        

        settings = QtCore.QSettings()
        self.restoreGeometry(settings.value("Geometry").toByteArray()) # method of QWidget
        self.restoreState(settings.value("MainWindow/State").toByteArray()) # method of QManWindow 
    
    def initUI(self):
        
        self.now = Now()
        #From http://developer.ubuntu.com/api/qml/sdk-1.0/QtQuick.qtquick-deployment/ qrc resources loaded as a url must be loaded with qrc: prefix.
        b=QtCore.QUrl("qrc:/res/message.qml") # is important to use qrc: syntax if using pyinstaller.
    
        self.declarativeView.setSource(b)

        #self.declarativeView.setSource((':./res/message.qml'))
        self.declarativeView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        
        # Get the root object of the user interface.  It defines a
        # 'messageRequired' signal and JavaScript 'updateMessage' function.  Both
        # can be accessed transparently from Python.
        rootObject = self.declarativeView.rootObject()
        
        # Provide the current date and time when requested by the user interface.
        rootObject.messageRequired.connect(self.now.emit_now)
        
        # Update the user interface with the current date and time.
        self.now.now.connect(rootObject.updateMessage)
        
        # Provide an initial message as a prompt.
        rootObject.updateMessage("Click to get the current date and time")
        
        # Display the user interface and allow the user to interact with it.
        self.declarativeView.setGeometry(100, 100, 400, 240)
        self.declarativeView.show()        
        

# create the GUI application
        
def main():
    import time
    app=QtGui.QApplication(sys.argv)
    
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

