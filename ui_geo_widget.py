# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\chris.ohalloran\Documents\GitHub\Sequential_Clearance\geo_widget.ui'
#
# Created: Thu Apr 03 13:45:34 2014
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(502, 287)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 473, 229))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.geolocationWidget = GeoLocationWidget(self.layoutWidget)
        self.geolocationWidget.setObjectName(_fromUtf8("geolocationWidget"))
        self.gridLayout.addWidget(self.geolocationWidget, 0, 0, 1, 1)
        self.globeWidget = GlobeWidget(self.layoutWidget)
        self.globeWidget.setObjectName(_fromUtf8("globeWidget"))
        self.gridLayout.addWidget(self.globeWidget, 0, 1, 2, 1)
        self.dial = QtGui.QDial(self.layoutWidget)
        self.dial.setObjectName(_fromUtf8("dial"))
        self.gridLayout.addWidget(self.dial, 0, 2, 1, 1)
        self.radioButton = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.gridLayout.addWidget(self.radioButton, 1, 0, 1, 1)
        self.horizontalSlider = QtGui.QSlider(self.layoutWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.gridLayout.addWidget(self.horizontalSlider, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 502, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.geolocationWidget, QtCore.SIGNAL(_fromUtf8("latitudeChanged(double)")), self.globeWidget.setLatitude)
        QtCore.QObject.connect(self.geolocationWidget, QtCore.SIGNAL(_fromUtf8("longitudeChanged(double)")), self.globeWidget.setLongitude)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.globeWidget.setPositionShown)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.globeWidget.setAngle)
        QtCore.QObject.connect(self.dial, QtCore.SIGNAL(_fromUtf8("dialMoved(int)")), self.globeWidget.setDivisions)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.radioButton.setText(_translate("MainWindow", "RadioButton", None))

from QQ_Widgets.globewidget import GlobeWidget
from QQ_Widgets.geolocationwidget import GeoLocationWidget
