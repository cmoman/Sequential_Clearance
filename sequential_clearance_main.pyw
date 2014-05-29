#!/usr/bin/env python
#encoding utf-8
#12
# used to parse files more easily
from __future__ import with_statement

# Numpy module
import numpy as np

# for command-line arguments
import sys
import time

#sys.path.append('./widgets')
#sys.path.insert(0, './widgets')

#from widgets import mplwidget

#from widgets import *

#import my sequential clearance grunt.
import sequential_clearance_backend as seq

# Qt4 bindings for core Qt functionalities (non-GUI)
from PyQt4 import QtCore

# Python Qt4 bindings for GUI objects
from PyQt4 import QtGui

#from PyQt4 import QtCore.pyqtSignature

import os

if os.name == 'nt': # Windows

    import ctypes
    myappid = 'tesla.sequential_clearance.0.9' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
# import the MainWindow widget from the converted .ui files
from ui_sequential_clearance_mainwindow import Ui_MplMainWindow

from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from PyQt4 import uic
form_class, base_class = uic.loadUiType('sequential_clearance_mainwindow.ui')
#class DesignerMainWindow(QtGui.QMainWindow, form_class):

class DesignerMainWindow(QtGui.QMainWindow, Ui_MplMainWindow):
    """Customization for Qt Designer created window"""
    def __init__(self, parent = None):
        # initialization of the superclass
        super(DesignerMainWindow, self).__init__(parent)
        # setup the GUI --> function generated by pyuic4
        self.setupUi(self)
        
        self.tabWidget.setCurrentIndex(1) # sets which tab is preferred when first opened.
        
        
        bling=['VI','EI','NI']
        self.inc_curve=self.curveComboBox_1.addItems(sorted(bling))
        self.fdr1_curve=self.curveComboBox_2.addItems(sorted(bling))
        self.fdr2_curve=self.curveComboBox_3.addItems(sorted(bling))
        
        self.initUI()
        
        #self.QwtWidget.show()
        
        self.dirty=True
        settings = QtCore.QSettings()
        self.restoreGeometry(settings.value("Geometry").toByteArray()) # method of QWidget
        self.restoreState(settings.value("MainWindow/State").toByteArray()) # method of QManWindow        
        
        #self.webView.setUrl(QtCore.QUrl(_fromUtf8("http://wiki.tesla.local/index.php/Main_Page")))
        
        self.statusBar2()
        self.addDockwidget2()
        self.toolbar2()
        
    def statusBar2(self):
        self.sizeLabel = QtGui.QLabel()
        self.sizeLabel.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Sunken) # this | syntax is something new
        
        status123 = self.statusBar()
        status123.setSizeGripEnabled(False)
        status123.addPermanentWidget(self.sizeLabel)
        status123.showMessage("Ready", 5000)
        #todo
     
    def toolbar2(self) :

        fileNewAction = self.createAction("&New...", self.fileNew, QtGui.QKeySequence.New, "filenew", "Create a project file") # the final text goes to the status bar
        fileOpenAction = self.createAction("&Open...", self.fileOpen, QtGui.QKeySequence.Open, "fileopen", "Open an existing project file") # the KeySequence must connect into some bigger picture that included the short cut and the icon.
        fileSaveAction = self.createAction("&Save", self.fileSave, QtGui.QKeySequence.Save, "filesave", "Save the project")
        fileSaveAsAction = self.createAction("Save &As", self.fileSaveAs, icon="filesaveas", tip="Save the project using a new name")
        filePrintAction = self.createAction("&Print", self.filePrint, QtGui.QKeySequence.Print, "fileprint", "Print the project")
        fileQuitAction = self.createAction("&Quit", self.close, "Cntrl+Q", "filequit", "Close the application")
        self.fileMenu = self.menuBar().addMenu("&File")  #this creates the dropdown on which to now add the title "File"
        self.fileMenuActions = (fileNewAction, fileOpenAction, fileSaveAsAction, None, filePrintAction, fileQuitAction) # this grabs all the actions from above
        self.connect(self.fileMenu, QtCore.SIGNAL("aboutToShow()"),self.updateFileMenu) 
        
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction, fileSaveAsAction))
        
    def createAction(self, text, slot=None, shortcut =None, icon=None, tip=None, checkable=False, signal="triggered()"):
        action = QtGui.QAction(text, self)
        
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/icons/images/%s.png" % icon))  # this is where the icons get attached to the Action.
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, QtCore.SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
    
    def addActions(self, target, actions):
        #print actions
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
                
    def updateFileMenu(self):
        self.fileMenu.clear()
        self.addActions(self.fileMenu, self.fileMenuActions)
        
        #self.addActions(self.fileMenu, self.fileMenuActions[:-1])
        #current = QtCore.QString(self.filename) \
                #if self.filename is not None else None
        #recentFiles = []
        #for fname in self.recentFiles:
            #if fname != current and QtCore.QFile.exists(fname):
                #recentFiles.append(fname)
        #if recentFiles:
            #self.fileMenu.addSeparator()
            #for i, fname in enumerate(recentFiles):
                #action = QtGui.QAction(QtGui.QIcon(":/icons/images/icon.png"), "&%d %s" % (
                        #i + 1, QtCore.QFileInfo(fname).fileName()), self)
                #action.setData(QtCore.QVariant(fname))
                #self.connect(action, QtCore.SIGNAL("triggered()"),
                             #self.loadFile)
                #self.fileMenu.addAction(action)
        #self.fileMenu.addSeparator()
        #self.fileMenu.addAction(self.fileMenuActions[-1])  
        
    def fileNew(self):
        pass
    
    def loadfile(self, fname=None):
        pass
    
    def fileOpen(self):
        file = QtGui.QFileDialog.getOpenFileName()
        # if a file is selected
        if file:
            # update the lineEdit widget text with the selected filename
            self.mpllineEdit.setText(file)        
        #pass
    
    def addRecentFile(self, fname):
        pass
    
    def fileSave(self):
        pass
    
    def fileSaveAs(self):
        pass
    
    def filePrint(self):
        print("file print")
        pass
        
        
    def addDockwidget2(self):
        
        logDockWidget123 = QtGui.QDockWidget("Log", self)
        logDockWidget123.setObjectName("LogDockWidget")
        logDockWidget123.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        
        self.listWidget123 = QtGui.QListWidget()

        logDockWidget123.setWidget(self.listWidget123) #different kinds of widget can go in here
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, logDockWidget123) # set it at right side        
        
    def closeEvent(self, event):
        if self.okToContinue():
            settings = QtCore.QSettings()
            #filename = self.filename #seeing if QVariant is still required
            #recentFiles = self.recentFiles #seeing if QVariant is still required
            '''Using PyQt 4.3 and beyond.  No use of QVariant seems required'''
            #settings.setValue("RecentFiles", recentFiles)
            settings.setValue("Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())  
            
        else:
            event.ignore()
            
    def okToContinue(self):
        if self.dirty:
            reply = QtGui.QMessageBox.question(self, "Sequential Clearance - Unsaved Changes",
                                                "Save unsaved changes?",
                                                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|
                                                QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return False
            elif reply == QtGui.QMessageBox.Yes:
                print('yes') #self.fileSave()
        return True
        
    def initUI(self):
        
        self.ratio=2.0
        self.lineangle=35
        
        self.doubleSpinBox.setValue(self.lineangle) 
        
        self.mplpushButton.clicked.connect(self.update_graph)
        self.mplactionOpen.triggered.connect(self.select_file)

        self.horizontalSlider.valueChanged.connect(self.changeValue)
        self.dial.valueChanged.connect(self.changeValue2)
        self.mpldoubleSpinBox.valueChanged.connect(self.changeValue3)
        self.doubleSpinBox.valueChanged.connect(self.changeValue2)
        
        QtCore.QObject.connect(self.mplactionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT("quit()"))

        self.update_graph() 
        
        self.webViewlineEdit.returnPressed.connect(self.updateBrowser)
        self.webView.urlChanged.connect(self.updateUrl)
        
          
    def updateBrowser(self): 
        url=str(self.webViewlineEdit.text())
        self.webView.load(QtCore.QUrl(url))
        
    def updateUrl(self):
        url=self.webView.url().toString()
        self.webViewlineEdit.setText(url)

        
    def changeValue(self, value):
        
        
        self.ratio = value/20.0
        self.mpldoubleSpinBox.setValue(self.ratio)
        
    def changeValue2(self, value):
        
        
        self.lineangle= value
        self.doubleSpinBox.setValue(self.lineangle)   
        
    def changeValue3(self, value):
        
        #print value
        self.ratio=value
        self.mpldoubleSpinBox.setValue(value) 
        
 
        


      
    def select_file(self):
        """opens a file select dialog"""
        # open the dialog and get the selected file
        file = QtGui.QFileDialog.getOpenFileName()
        # if a file is selected
        if file:
            # update the lineEdit widget text with the selected filename
            self.mpllineEdit.setText(file)

    def parse_file(self, filename): # [CO] this is where we would put the sequential calculation
        """Function to parse a text file to extract letters frequencies"""
        
    def save_file(self):
        pass
        
    
        

        
        
    def update_graph(self): 
        """Updates the graph"""

        self.mult0   =self.mpldoubleSpinBox2.value()
        self.mult1   =self.mpldoubleSpinBox3.value()
        self.mult2   =self.mpldoubleSpinBox10.value()
        self.pickup0 =self.mpldoubleSpinBox4.value()
        self.pickup1 =self.mpldoubleSpinBox5.value()
        self.pickup2 =self.mpldoubleSpinBox9.value()
        self.incct   =self.mpldoubleSpinBox6.value()
        self.feederct1=self.mpldoubleSpinBox7.value()
        self.feederct2=self.mpldoubleSpinBox8.value()
        self.tximp   =self.mplspinBox.value()
        self.inc_checkBox=self.mplinc_checkBox.isChecked()
        self.fdr1_checkBox=self.mplfdr1_checkBox.isChecked()
        self.fdr2_checkBox=self.mplfdr2_checkBox.isChecked()
        
        self.fdr1_cbtime=self.mplfdr1_cbtime_SpinBox.value()
        self.fdr1_highset=self.mplfdr1_highset_spinBox.value()
        self.fdr2_cbtime=self.mplfdr2_cbtime_SpinBox.value()
        self.fdr2_highset=self.mplfdr2_highset_SpinBox.value()        
        self.inc_cbtime=self.mplinc_cbtime_SpinBox.value()
        self.inc_highset=self.mplinc_highset_SpinBox.value()
        self.inc_curve=self.curveComboBox_1.currentText()
        self.fdr1_curve=self.curveComboBox_2.currentText()
        self.fdr2_curve=self.curveComboBox_3.currentText()        

        #self.ratio=self.mpldial.value()/10.0
        
        #m_store,incomer_current,incomer_current_fdr1_open,incomer_current_fdr2_open,bling = seq.main_seq(self.ratio)
        m_store,margin_store,margin_store2,margin_store3,margin_store4,margin_store5,margin_store6,\
            bling,j1,j2,j3,k1,k2,k3,l1,l2,l3,m1,m2,m3,n1,n2,n3,o1,o2,o3,q1,q2,q3 = seq.main_seq(self.ratio,self.mult0,self.mult1,self.mult2,\
                                                  self.pickup0,self.pickup1,self.pickup2,\
                                                  self.incct,self.feederct1,self.feederct2,\
                                                  self.tximp,\
                                                  self.inc_cbtime,self.inc_highset,self.inc_checkBox,
                                                  self.fdr1_cbtime,self.fdr1_highset,self.fdr1_checkBox,\
                                                  self.fdr2_cbtime,self.fdr2_highset,self.fdr2_checkBox,\
                                                  self.inc_curve,self.fdr1_curve,self.fdr2_curve,self.lineangle)
        
        
        #plot the graph tab 2
        self.mpl_1.canvas.ax.clear()
        self.mpl_1.canvas.ax.set_title('Margin between incomer and feeders to trip.')
        self.mpl_1.canvas.ax.set_xlabel('m')  
        self.mpl_1.canvas.ax.set_ylabel('Seconds')
        
        #run the fix scale though check button
        #need to get present scale then apply fix or just apply a fix scale button.
        self.mpl_1.canvas.ax.set_ylim(0,1.2)
        self.mpl_1.canvas.ax.plot(m_store,margin_store,antialiased=True,alpha=.5,color='g', marker=',',label='Inc margin second trip')
        self.mpl_1.canvas.ax.plot(m_store,margin_store4,antialiased=True,alpha=.5,color='b', marker=',',label='Inc margin first trip')
        self.mpl_1.canvas.ax.grid(True) 
        self.mpl_1.canvas.ax.axhline(0.4,color='r')
        self.mpl_1.canvas.ax.legend(loc='upper left')
        
        self.mpl_1.canvas.ax2.clear()
        self.mpl_1.canvas.ax2.set_ylabel('Percentage travel')
        self.mpl_1.canvas.ax2.grid(True) 
        self.mpl_1.canvas.ax2.plot(m_store,margin_store2,antialiased=True,alpha=.5,color='purple', marker=',', label='Inc percent 1st trip')
        self.mpl_1.canvas.ax2.set_ylim(0.0,100)
        self.mpl_1.canvas.ax2.legend(loc='upper right')
        
        
        self.mpl_1.canvas.draw()
        
        #plot the tab 3 graph
        self.mpl_2.canvas.ax.clear()
        
        self.mpl_2.canvas.ax.set_title('Margins and total time to trip (Stage1+2)')
        self.mpl_2.canvas.ax.set_ylabel('Seconds')
        self.mpl_2.canvas.ax.set_xlabel('m')   
        self.mpl_2.canvas.ax.grid(True)
        self.mpl_2.canvas.ax.plot(m_store,margin_store,antialiased=True, alpha=.5,color='g', marker=',',label='Inc margin')
        self.mpl_2.canvas.ax.plot(m_store,margin_store5,antialiased=True,alpha=.5,color='r', marker=',', label='Stage1')
        self.mpl_2.canvas.ax.plot(m_store,margin_store6,antialiased=True,alpha=.5,color='b', marker=',', label='Stage1+2')        
        self.mpl_2.canvas.ax.legend(loc='upper left')
        
        self.mpl_2.canvas.ax2.clear()
        self.mpl_2.canvas.ax2.set_ylabel('Percentage travel')
        self.mpl_2.canvas.ax2.grid(True) 
        self.mpl_2.canvas.ax2.plot(m_store,margin_store2,antialiased=True,alpha=.5,color='purple', marker=',', label='Inc percent 1st trip')
        self.mpl_2.canvas.ax2.set_ylim(0.0,100)
        self.mpl_2.canvas.ax2.legend(loc='upper right')            
            
        self.mpl_2.canvas.draw()
        
     
        #tab 4
        self.mpl_5.canvas.ax.clear()
        self.mpl_5.canvas.ax2.clear()
        self.mpl_5.canvas.ax.set_title('Incomer times and current')
        self.mpl_5.canvas.ax.set_ylabel('Seconds')
        self.mpl_5.canvas.ax2.set_ylabel('Amps')
        self.mpl_5.canvas.ax.set_ylim(0.0,4.0)
        self.mpl_5.canvas.ax.grid(True) 
        self.mpl_5.canvas.ax.plot(m_store,j1,label='Fdr1//Fdr2 t',color='red')
        self.mpl_5.canvas.ax.plot(m_store,j3,label='Fdr2 open t',color='green')

        self.mpl_5.canvas.ax2.plot(m_store,m1,label='Fdr1//Fdr2 I',color='red',linestyle='-.')
        self.mpl_5.canvas.ax2.plot(m_store,m3,label='Fdr2 open I',color='green',linestyle='-.')
        
        self.mpl_5.canvas.ax.legend(loc=2)
        self.mpl_5.canvas.ax2.legend(loc=1)
        self.mpl_5.canvas.draw()
        
        #tab 5
        self.mpl_6.canvas.ax.clear()
        self.mpl_6.canvas.ax2.clear()
        self.mpl_6.canvas.ax.set_title('Feeder One times and current')
        self.mpl_6.canvas.ax.set_ylabel('Seconds')
        self.mpl_6.canvas.ax2.set_ylabel('Amps')
        self.mpl_6.canvas.ax.set_ylim(0.0,2.0)
        self.mpl_6.canvas.ax.grid(True) 
        self.mpl_6.canvas.ax.plot(m_store,k1,label='Fdr1//Fdr2 t',color='red')
        self.mpl_6.canvas.ax.plot(m_store,k3,label='Fdr2 open t',color='green')        
        
        self.mpl_6.canvas.ax2.plot(m_store,n1,label='Fdr1//Fdr2 I',color='red',linestyle='-.')
        self.mpl_6.canvas.ax2.plot(m_store,n3,label='Fdr2 open I',color='green',linestyle='-.')
 
        self.mpl_6.canvas.ax.legend(loc=2)
        self.mpl_6.canvas.ax2.legend(loc=1)
        self.mpl_6.canvas.draw()
        
        self.mpl_8.canvas.ax.clear()
        self.mpl_8.canvas.ax2.clear()
        self.mpl_8.canvas.ax.set_title('Feeder Two times and current')
        self.mpl_8.canvas.ax.set_ylabel('Seconds')
        self.mpl_8.canvas.ax2.set_ylabel('Amps')
        self.mpl_8.canvas.ax.set_ylim(0.0,2.0)
        self.mpl_8.canvas.ax.grid(True) 
        self.mpl_8.canvas.ax.plot(m_store,l1,label='Fdr1//Fdr2 t',color='red')             
        self.mpl_8.canvas.ax.plot(m_store,l2,label='Fdr1 open t',color='blue')

        self.mpl_8.canvas.ax2.plot(m_store,o1,label='Fdr1//Fdr2 I',color='red',linestyle='-.')
        self.mpl_8.canvas.ax2.plot(m_store,o2,label='Fdr1 open I',color='blue',linestyle='-.')

        self.mpl_8.canvas.ax.legend(loc=2)
        self.mpl_8.canvas.ax2.legend(loc=1)
        self.mpl_8.canvas.draw()

        self.mpl_11.canvas.ax.clear()
        self.mpl_11.canvas.ax2.clear()       
        self.mpl_11.canvas.ax.set_title('Incomer times and current')
        self.mpl_11.canvas.ax.set_ylabel('Seconds')
        self.mpl_11.canvas.ax2.set_ylabel('Amps')
        self.mpl_11.canvas.ax.set_ylim(0.0,4.0)
        self.mpl_11.canvas.ax.grid(True) 
        self.mpl_11.canvas.ax.plot(m_store,j1,label='Fdr1//Fdr2 t',color='red')
        self.mpl_11.canvas.ax.plot(m_store,j2,label='Fdr1 open t',color='blue')

        self.mpl_11.canvas.ax2.plot(m_store,m1,label='Fdr1//Fdr2 I',color='red',linestyle='-.')
        self.mpl_11.canvas.ax2.plot(m_store,m2,label='Fdr1 open I' ,color='blue',linestyle='-.')
        
        self.mpl_11.canvas.ax.legend(loc=2)
        self.mpl_11.canvas.ax2.legend(loc=1)
        self.mpl_11.canvas.draw()
        
        #tab 7
        self.mpl_12.canvas.ax.clear()
        self.mpl_12.canvas.ax.set_title("Incomer OC(IT) plot")
        x2 , y2=q1
        self.mpl_12.canvas.ax.loglog(x2,y2,antialiased=True,alpha=.5,color='b', marker=',',label='Inc Time')
        self.mpl_12.canvas.ax.grid(True,which='both') #both adds the minor grid lines.
        self.mpl_12.canvas.ax.set_ylabel('Time')
        self.mpl_12.canvas.ax.set_xlabel('Current')
        self.mpl_12.canvas.ax.legend(loc='best')
        self.mpl_12.canvas.draw()
        
        self.mpl_3.canvas.ax.clear()
        self.mpl_3.canvas.ax.loglog(x2,y2,antialiased=True,alpha=.5,color='b', marker=',',label='Inc Time')
        x3,y3=q2
        self.mpl_3.canvas.ax.set_title("Feeder 1 OC(IT) plot")
        self.mpl_3.canvas.ax.loglog(x3,y3,antialiased=True,alpha=.5,color='g', marker=',', label='Fdr 1Time')
        self.mpl_3.canvas.ax.grid(True,which='both')
        self.mpl_3.canvas.ax.set_ylabel('Time')
        self.mpl_3.canvas.ax.set_xlabel('Current')
        self.mpl_3.canvas.ax.legend(loc='best')
        self.mpl_3.canvas.draw()
        
        self.mpl_4.canvas.ax.clear()
        self.mpl_4.canvas.ax.loglog(x2,y2,antialiased=True,alpha=.5,color='b', marker=',',label='Inc Time')
        self.mpl_4.canvas.ax.set_title("Feeder 2 OC(IT) plot")
        x2,y2=q3
        self.mpl_4.canvas.ax.loglog(x2,y2,antialiased=True,alpha=.5,color='r', marker=',', label='Fdr2 Time')
        self.mpl_4.canvas.ax.grid(True,which='both')
        self.mpl_4.canvas.ax.set_ylabel('Time')
        self.mpl_4.canvas.ax.set_xlabel('Current')
        self.mpl_4.canvas.ax.legend(loc='best')   
        self.mpl_4.canvas.draw()
        
        #tab 6
        self.mpl_7.canvas.ax.clear()
        #self.mpl_7.canvas.ax.plot(m_store,margin_store3,antialiased=True,alpha=.5,color='r', marker='.', label='Case')
        self.mpl_7.canvas.ax.bar(left=m_store, height=margin_store3,width=0.01)
        self.mpl_7.canvas.ax.grid(True,which='both')
        self.mpl_7.canvas.ax.set_ylabel('Case')
        self.mpl_7.canvas.ax.set_xlabel('m')
        self.mpl_7.canvas.ax.legend(loc='best')   
        self.mpl_7.canvas.draw()
        
        self.mpl_9.canvas.ax.clear()
        self.mpl_9.canvas.ax.plot(m_store,margin_store5,antialiased=True,alpha=.5,color='r', marker=',', label='Stage1')
        self.mpl_9.canvas.ax.plot(m_store,margin_store6,antialiased=True,alpha=.5,color='b', marker=',', label='Stage1+2')
        self.mpl_9.canvas.ax.grid(True,which='both')
        self.mpl_9.canvas.ax.set_ylabel('Time')
        self.mpl_9.canvas.ax.set_xlabel('m')
        self.mpl_9.canvas.ax.legend(loc='best')   
        self.mpl_9.canvas.draw()        
      
        
def fakeIt():
    pass

# create the GUI application
def main():
    import time
    app=QtGui.QApplication(sys.argv)
    app.setOrganizationName("cmoman.ltd")
    app.setOrganizationDomain("blahdeblah.co.nz")
    app.setApplicationName("Sequential Clearance")
    
    image = QtGui.QImage(400,400,QtGui.QImage.Format_RGB32)
    pixmap3=QtGui.QPixmap(":/images/images/feeder_plot.png")
    pixmap=pixmap3.scaled(400,400,1)
    
    splash = QtGui.QSplashScreen(pixmap, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(pixmap3.mask())
    
    splash.show()

    splash.showMessage(QtCore.QString("Sequential Clearance"),QtCore.Qt.AlignCenter,QtGui.QColor("Black"))

    app.processEvents()

    dmw = DesignerMainWindow() # instantiate a window
    # show it
    dmw.show()

    splash.finish(dmw)
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

