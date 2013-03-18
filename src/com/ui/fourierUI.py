# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fourierUI.ui'
#
# Created: Sun Mar 17 16:44:13 2013
#      by: PyQt4 UI code generator 4.10
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

class Ui_FourierWindow(object):
    def setupUi(self, FourierWindow):
        FourierWindow.setObjectName(_fromUtf8("FourierWindow"))
        FourierWindow.resize(722, 550)
        self.centralwidget = QtGui.QWidget(FourierWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 481, 481))
        self.widget.setObjectName(_fromUtf8("widget"))
        FourierWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(FourierWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 722, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        FourierWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(FourierWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        FourierWindow.setStatusBar(self.statusbar)

        self.retranslateUi(FourierWindow)
        QtCore.QMetaObject.connectSlotsByName(FourierWindow)

    def retranslateUi(self, FourierWindow):
        FourierWindow.setWindowTitle(_translate("FourierWindow", "Mean and Standard Deviation of Fourier Spectrum", None))


class FourierWindow(QtGui.QMainWindow, Ui_FourierWindow):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)

