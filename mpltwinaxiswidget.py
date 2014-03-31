#!/usr/bin/env python

# Python Qt4 bindings for GUI objects
from PyQt4 import QtGui
#from PySide import QtGui

# import the Qt4Agg FigureCanvas object, that binds Figure to
# Qt4Agg backend. It also inherits from QWidget
#from matplotlib.backends.backend_qt4agg import FigureCanvasAgg

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

# Matplotlib Figure object
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self):
        # setup Matplotlib Figure and Axis
        self.fig = Figure()
        super(MplCanvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax2= self.ax.twinx() # Added the second axis

class MplTwinAxisWidget(QtGui.QWidget):
    """Widget defined in Qt Designer"""
    def __init__(self, parent = None):
        # initialization of Qt MainWindow widget
        super(MplTwinAxisWidget, self).__init__(parent)  #parent is not none
        #QtGui.QWidget.__init__(self, parent)
        # set the canvas to the Matplotlib widget
        self.canvas = MplCanvas()
        # create a vertical box layout
        self.vbl = QtGui.QVBoxLayout()
     
        # Try adding the navigation bar
        self.ntp = NavigationToolbar(self.canvas,self)
        self.vbl.addWidget(self.ntp)
        
        # add mpl widget to the vertical box
        self.vbl.addWidget(self.canvas)        
        
        # set the layout to the vertical box
        self.setLayout(self.vbl)
        
      

