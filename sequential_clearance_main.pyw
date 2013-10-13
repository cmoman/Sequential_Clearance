#!/usr/bin/env python

# used to parse files more easily
from __future__ import with_statement

# Numpy module
import numpy as np

# for command-line arguments
import sys
import time

#import my sequential clearance grunt.
import sequential_clearance_backend as seq

# Qt4 bindings for core Qt functionalities (non-GUI)
from PyQt4 import QtCore

# Python Qt4 bindings for GUI objects
from PyQt4 import QtGui

# import the MainWindow widget from the converted .ui files
from ui_sequential_clearance_mainwindow import Ui_MplMainWindow

from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

class DesignerMainWindow(QtGui.QMainWindow, Ui_MplMainWindow):
    """Customization for Qt Designer created window"""
    def __init__(self, parent = None):
        # initialization of the superclass
        super(DesignerMainWindow, self).__init__(parent)
        # setup the GUI --> function generated by pyuic4
        self.setupUi(self)
        bling=['VI','EI','NI']
        self.inc_curve=self.curveComboBox_1.addItems(sorted(bling))
        self.fdr1_curve=self.curveComboBox_2.addItems(sorted(bling))
        self.fdr2_curve=self.curveComboBox_3.addItems(sorted(bling))
        
        time.sleep(2)
        
        self.initUI()
        
        self.dirty=True
        settings = QtCore.QSettings()
        self.restoreGeometry(settings.value("Geometry").toByteArray()) # method of QWidget
        self.restoreState(settings.value("MainWindow/State").toByteArray()) # method of QManWindow        
        
        #self.webView.setUrl(QtCore.QUrl(_fromUtf8("http://wiki.tesla.local/index.php/Main_Page")))
        
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
            reply = QtGui.QMessageBox.question(self, "Image Changer - Unsaved Changes",
                                                "Save unsaved changes?",
                                                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|
                                                QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return False
            elif reply == QtGui.QMessageBox.Yes:
                print('yes') #self.fileSave()
        return True
        
    def initUI(self):
        self.ratio   =self.mpldoubleSpinBox.value()

        
        # connect the signals with the slots
        QtCore.QObject.connect(self.mplpushButton, QtCore.SIGNAL("clicked()"), self.update_graph)
        QtCore.QObject.connect(self.mplactionOpen, QtCore.SIGNAL('triggered()'), self.select_file)
        QtCore.QObject.connect(self.mplactionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL('valueChanged(int)'), self.changeValue)    
        
        self.update_graph()        
        
        
        
    def changeValue(self, value):
        
        #self.mpldoubleSpinBox.value(value)
        self.ratio = value/20.0
        self.update_graph()

      
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
        

        
        
    def update_graph(self): 
        """Updates the graph"""

        # clear the Axes
        self.mpl.canvas.ax.clear()
        self.mpl_2.canvas.ax.clear()
        
        self.mpl_5.canvas.ax.clear()
        self.mpl_6.canvas.ax.clear()
        self.mpl_7.canvas.ax.clear()
        self.mpl_8.canvas.ax.clear()
        
        #Clear second axis
        self.mpl.canvas.ax2.clear()
        self.mpl_2.canvas.ax2.clear()
        self.mpl_5.canvas.ax2.clear()
        self.mpl_6.canvas.ax2.clear()
        self.mpl_7.canvas.ax2.clear()
        self.mpl_8.canvas.ax2.clear()
        
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
        m_store,margin_store,margin_store2,margin_store3,margin_store4,margin_store5,margin_store6,bling,j1,j2,j3,k1,k2,k3,l1,l2,l3,m1,m2,m3,n1,n2,n3,o1,o2,o3 = seq.main_seq(self.ratio,self.mult0,self.mult1,self.mult2,\
                                                  self.pickup0,self.pickup1,self.pickup2,\
                                                  self.incct,self.feederct1,self.feederct2,\
                                                  self.tximp,\
                                                  self.inc_cbtime,self.inc_highset,self.inc_checkBox,
                                                  self.fdr1_cbtime,self.fdr1_highset,self.fdr1_checkBox,\
                                                  self.fdr2_cbtime,self.fdr2_highset,self.fdr2_checkBox,\
                                                  self.inc_curve,self.fdr1_curve,self.fdr2_curve)
        
        #plot the graph on tab 2
        self.mpl.canvas.ax.set_title('Margin between incomer and feeders to trip.')
        self.mpl.canvas.ax.set_ylabel('Margin in seconds')
        self.mpl.canvas.ax.set_xlabel('m')           
        self.mpl.canvas.ax.grid(True) 
        self.mpl.canvas.ax2.axhline(0.4,color='r')
        self.mpl.canvas.ax.set_ylabel('percentage')
        self.mpl.canvas.ax.plot(m_store,margin_store,antialiased=True,alpha=.5,color='g', marker=',',label='Incomer percentage')
        self.mpl.canvas.ax.plot(m_store,margin_store2,antialiased=True,alpha=.5,color='r', marker=',', label='Feeder percentage')
        self.mpl.canvas.ax.set_ylim(0.0,1.1)
        
        #self.mpl.canvas.ax2.plot(m_store,margin_store2,antialiased=True,alpha=.5,color='r', marker=',', label='First trip')
        self.mpl.canvas.ax2.set_ylabel('Time')
        self.mpl.canvas.ax2.plot(m_store,margin_store3,antialiased=True,alpha=.5,color='g', marker='x', label='Incomer time for 2nd trip')
        self.mpl.canvas.ax2.plot(m_store,margin_store4,antialiased=True,alpha=.5,color='r', marker='x', label='Feeder time for 2nd trip')
        self.mpl.canvas.ax2.plot(m_store,margin_store5,antialiased=True,alpha=.5,color='b', marker='x', label='Second trip margin')
        self.mpl.canvas.ax2.plot(m_store,margin_store6,antialiased=True,alpha=.5,color='black', marker='x', label='First trip Margin')
        #self.mpl.canvas.ax2.set_ylim(0.0,5.0)
        
        self.mpl.canvas.ax.legend(loc='best')
        self.mpl.canvas.ax2.legend(loc='best')
        
        #self.mpl.canvas.draw()
        
        #plot the tab 2 graph
        self.mpl_2.canvas.ax.set_title('Margin between incomer and feeders to trip.')
        self.mpl_2.canvas.ax.set_ylabel('Margin in seconds')
        self.mpl_2.canvas.ax.grid(True)
        #self.mpl_2.canvas.ax.plot(m_store,margin_store,antialiased=True, alpha=.5,color='g', marker=',',label='Second trip')
        self.mpl_2.canvas.ax.set_ylabel('Incomer')
        self.mpl_2.canvas.ax.plot(m_store,margin_store,antialiased=True, alpha=.5,color='g', marker=',',label='Incomer percentage')
        self.mpl_2.canvas.ax2.grid(True) 
        #self.mpl_2.canvas.ax2.plot(m_store,margin_store2,antialiased=True,alpha=.5,color='r', marker=',', label='First trip')
        self.mpl_2.canvas.ax2.set_ylabel('Feeder')
        self.mpl_2.canvas.ax2.plot(m_store,margin_store2,antialiased=True,alpha=.5,color='r', marker=',', label='Feeder percentage')
 
        self.mpl_2.canvas.ax.legend(loc=1)
        self.mpl_2.canvas.ax2.legend(loc=2)        
        #self.mpl_2.canvas.draw()
        
        self.mpl_5.canvas.ax.set_title('Incomer times and current')
        self.mpl_5.canvas.ax.set_ylabel('Seconds')
        self.mpl_5.canvas.ax2.set_ylabel('Amps')
        self.mpl_5.canvas.ax.set_ylim(0.0,4.0)
        self.mpl_5.canvas.ax.grid(True) 
        self.mpl_5.canvas.ax.plot(m_store,j1,label='Fdr1//Fdr2 t',color='red')
        self.mpl_5.canvas.ax.plot(m_store,j2,label='Fdr1 open t',color='green')
        self.mpl_5.canvas.ax.plot(m_store,j3,label='Fdr2 open t',color='blue')

        self.mpl_5.canvas.ax2.plot(m_store,m1,label='Fdr1//Fdr2 I',color='red',linestyle='-.')
        self.mpl_5.canvas.ax2.plot(m_store,m2,label='Fdr1 open I' ,color='green',linestyle='-.')
        self.mpl_5.canvas.ax2.plot(m_store,m3,label='Fdr2 open I',color='blue',linestyle='-.')
        
        self.mpl_5.canvas.ax.legend(loc=2)
        self.mpl_5.canvas.ax2.legend(loc=1)
        #self.mpl_5.canvas.draw()
        
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
        #self.mpl_6.canvas.draw()
        
        self.mpl_7.canvas.ax.set_title('Feeder Two times and current')
        self.mpl_7.canvas.ax.set_ylabel('Seconds')
        self.mpl_7.canvas.ax2.set_ylabel('Amps')
        self.mpl_7.canvas.ax.set_ylim(0.0,2.0)
        self.mpl_7.canvas.ax.grid(True) 
        self.mpl_7.canvas.ax.plot(m_store,l1,label='Fdr1//Fdr2 t',color='red')             
        self.mpl_7.canvas.ax.plot(m_store,l2,label='Fdr1 open t',color='blue')

        self.mpl_7.canvas.ax2.plot(m_store,o1,label='Fdr1//Fdr2 I',color='red',linestyle='-.')
        self.mpl_7.canvas.ax2.plot(m_store,o2,label='Fdr1 open I',color='blue',linestyle='-.')

        self.mpl_7.canvas.ax.legend(loc=2)
        self.mpl_7.canvas.ax2.legend(loc=1)
        
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
        
      
        
        self.mpl.canvas.draw()  
        self.mpl_2.canvas.draw()  
        #self.mpl_3.canvas.draw()  
        #self.mpl_4.canvas.draw()  
        self.mpl_5.canvas.draw()
        self.mpl_6.canvas.draw()  
        self.mpl_7.canvas.draw()
        self.mpl_8.canvas.draw()
        
def fakeIt():
    pass

# create the GUI application
def main():
    app=QtGui.QApplication(sys.argv)
    app.setOrganizationName("cmoman.ltd")
    app.setOrganizationDomain("blahdeblah.co.nz")
    app.setApplicationName("Sequential Clearance")
    
    image = QtGui.QImage(400,400,QtGui.QImage.Format_RGB32)
    #image.setColor(2,2)
    pixmap3=QtGui.QPixmap("images/blank.png")
    pixmap2=QtGui.QPixmap("images/schematic_from_model_view.svg")
    #pixmap=QtGui.QPixmap("blank.png")
    #pixmap=QtGui.QPixmap(400,400)
    pixmap=pixmap3.scaled(400,400,1)
    
    splash = QtGui.QSplashScreen(pixmap)
    
    splash.show()
    #QtCore.QTimer.singleShot(100000, fakeIt)
    splash.showMessage(QtCore.QString("bling"),QtCore.Qt.AlignCenter,QtGui.QColor("Red"))
    #time.sleep(2)
    #splash.showMessage(QtCore.QString("more text"),QtCore.Qt.AlignLeft,QtGui.QColor("Blue")) # seems to replace the previous message
    #time.sleep(2)
    #app.processEvents()

    #app.setWindowIcon(QtGui.QIcon(":/save.png"))
    dmw = DesignerMainWindow() # instantiate a window
    # show it
    dmw.show()
    
    
    
    splash.finish(dmw)
    sys.exit(app.exec_())
    
main()

#app = QtGui.QApplication(sys.argv)
#pixmap=QtGui.QPixmap("images/schematic_from_model_view.svg")
##pixmap2=pixmap.scaled(400,400,QtCore.Qt.KeepAspectRatio)
#pixmap2=pixmap.scaled(400,400,1)
#splash = QtGui.QSplashScreen(pixmap2)
#splash.show()
#splash.showMessage("bling")

## instantiate the main window
#dmw = DesignerMainWindow()
## show it
#dmw.show()
##Insert timer
#splash.finish(dmw)
## start the Qt main loop execution, exiting from this script
## with the same return code of Qt application
#sys.exit(app.exec_())

#mino