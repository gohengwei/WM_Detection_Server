# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visualizer.ui'
#
# Created: Sun Mar 17 15:45:26 2013
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

class Ui_Visualizer(object):
    def setupUi(self, Visualizer):
        Visualizer.setObjectName(_fromUtf8("Visualizer"))
        Visualizer.resize(1076, 687)
        self.centralwidget = QtGui.QWidget(Visualizer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(870, 90, 151, 401))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.verticalLayout.addWidget(self.comboBox)
        self.refreshBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.refreshBtn.setObjectName(_fromUtf8("refreshBtn"))
        self.verticalLayout.addWidget(self.refreshBtn)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.textBrowser = QtGui.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser.setStyleSheet(_fromUtf8("background-color : black; color :green;"))
        self.textBrowser.setLineWrapColumnOrWidth(2)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.fourierBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.fourierBtn.setObjectName(_fromUtf8("fourierBtn"))
        self.verticalLayout.addWidget(self.fourierBtn)
        self.graph = QtGui.QWidget(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(40, 10, 801, 621))
        self.graph.setObjectName(_fromUtf8("graph"))
        Visualizer.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Visualizer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1076, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHowdy = QtGui.QMenu(self.menubar)
        self.menuHowdy.setObjectName(_fromUtf8("menuHowdy"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        Visualizer.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Visualizer)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Visualizer.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHowdy.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(Visualizer)
        QtCore.QMetaObject.connectSlotsByName(Visualizer)

    def retranslateUi(self, Visualizer):
        Visualizer.setWindowTitle(_translate("Visualizer", "Analyze Waveform", None))
        self.label.setText(_translate("Visualizer", "Data File", None))
        self.refreshBtn.setText(_translate("Visualizer", "Refresh", None))
        self.label_2.setText(_translate("Visualizer", "Statistics", None))
        self.textBrowser.setHtml(_translate("Visualizer", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.fourierBtn.setText(_translate("Visualizer", "Fourier Analysis", None))
        self.menuHowdy.setTitle(_translate("Visualizer", "File", None))
        self.menuAbout.setTitle(_translate("Visualizer", "About", None))


class Visualizer(QtGui.QMainWindow, Ui_Visualizer):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)

