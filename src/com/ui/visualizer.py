# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visualizer.ui'
#
# Created: Mon Mar 25 21:20:42 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(870, 90, 164, 401))
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
        self.svmBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.svmBtn.setObjectName(_fromUtf8("svmBtn"))
        self.verticalLayout.addWidget(self.svmBtn)
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
        Visualizer.setWindowTitle(QtGui.QApplication.translate("Visualizer", "Analyze Waveform", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Visualizer", "Data File", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshBtn.setText(QtGui.QApplication.translate("Visualizer", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Visualizer", "Statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("Visualizer", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:11pt;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.fourierBtn.setText(QtGui.QApplication.translate("Visualizer", "Fourier Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.svmBtn.setText(QtGui.QApplication.translate("Visualizer", "Generate SVM Problem", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHowdy.setTitle(QtGui.QApplication.translate("Visualizer", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("Visualizer", "About", None, QtGui.QApplication.UnicodeUTF8))


class Visualizer(QtGui.QMainWindow, Ui_Visualizer):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)

