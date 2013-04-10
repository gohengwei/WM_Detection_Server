'''
Created on Mar 17, 2013

@author: gohew
'''
import os
from numpy import *
import sys
from com.ui.fourierUI import FourierWindow
from matplotlib import cm
import matplotlib.pyplot as plt

import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import matplotlib.mlab as mlab
import numpy as np
from com.signal.SignalProcessing import SignalClass

class FourierAnalysis(QWidget):
    dir = '/home/gohew/workspace/WM_Detection_Server/src/data'
    ave_sample_rate = 4
    fourier_ave = None
    list_ctr = 0;
    freq_scale = np.arange(0,150,1)
    color = array(['r','b','g'])
    xbee = array(['top','mid','bot'])
    fourier_std = None
    def __init__(self):
        '''
        Constructor
        '''
        super(FourierAnalysis, self).__init__()
        #FourierWindow.__init__(self)
        self.signal = SignalClass()
        self.initUI()
        self.center()
        self.show()
        self.openDir()
        
    def initUI(self):
        self.dpi = 100
        self.fig = Figure((10,5), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.ax = self.fig.add_subplot(211,autoscale_on='True',title="Mean of Fourier Transform")
        self.bx = self.fig.add_subplot(212,autoscale_on='True',title="Standard Deviation of Fourier Transform")
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        
        self.data_l2 = QLabel("Select Directory")
        self.dirBtn = QPushButton("Select")
        self.dirLineEdit = QLineEdit()
        self.dirLineEdit.setEnabled(False)
        
        self.data_l = QLabel("Select Person")
        self.refreshBtn = QPushButton('Refresh')
        self.comboBox = QComboBox()
        self.textBrowser = QTextBrowser()
        dataPanel_layout = QVBoxLayout()
        dataPanel_layout.addWidget(self.data_l2)
        dataPanel_layout.addWidget(self.dirBtn)
        dataPanel_layout.addWidget(self.dirLineEdit)
        dataPanel_layout.addWidget(self.data_l)
        dataPanel_layout.addWidget(self.refreshBtn)
        
        dataPanel_layout.addWidget(self.comboBox)
        dataPanel_layout.addWidget(self.textBrowser)
        
        hbox = QHBoxLayout()
        
        hbox.addLayout(vbox)
        hbox.addLayout(dataPanel_layout)
        self.setLayout(hbox)
        #self.setCentralWidget(self.centralwidget)
        self.comboBox.activated[str].connect(self.onActivated)
        
        self.connect(self.dirBtn,SIGNAL("clicked()"),self.save_dir)
        self.connect(self.refreshBtn,SIGNAL("clicked()"),self.refreshDir)
    
    def refreshDir(self):
        self.comboBox.clear()
        self.openDir()
        
    def save_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Test","/home/gohew/workspace/WM_Detection_Server/src/data/")
        
        if path:
            self.dirLineEdit.setText(str(path))
            self.dir = str(path)
            
    def onActivated(self,text):
        self.ax.clear()
        self.bx.clear()
        #self.bx.clear()
        self.list_ctr = 0
        self.fourier_ave = zeros((3,150))
        self.fourier_std = zeros((3,150))
        self.std_val = zeros((3,150))
        self.calcStatistics(text)
        for j in range(0,3):
            self.fourier_std[j] = np.delete(self.fourier_std[j],s_[self.list_ctr], axis=0)
            print self.fourier_std[j].shape
            for i in range(0,len(self.freq_scale)):
                self.fourier_ave[j,i] = self.fourier_ave[j,i] / self.list_ctr
                self.std_val[j,:] = np.std(self.fourier_std[j],axis=0)
        #print self.std_val
        print self.std_val.shape
        self.plotGraph()
    
    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def plotGraph(self):
        for i in range(0,3):
            self.ax.set_xlabel('Freq(Hz)')
            self.ax.set_ylabel('Amplitude')
            #print self.data_in
            self.textBrowser.setText("No. of Samples: <b>" + str(self.list_ctr) + "</b><br>")
            #print self.fourier_ave
            self.ax.axis([0,130,0,150])
            self.ax.plot(self.freq_scale[0:self.freq_scale.size],self.fourier_ave[i,0:self.freq_scale.size],self.color[i],label=self.xbee[i])
            self.ax.set_title("Mean of Fourier Transform")
            #plt.subplot(2,3 , i + 4)
            #print freq
            self.bx.set_xlabel('Freq(Hz)')
            self.bx.set_ylabel('Amplitude')
            self.bx.axis([0,150,0,130])
            self.bx.set_title("Standard Deviation of Fourier Transform")
            self.bx.plot(self.freq_scale[0:self.freq_scale.size],self.std_val[i,0:self.freq_scale.size],self.color[i],label=self.xbee[i]) 
        handles, labels = self.ax.get_legend_handles_labels()
        self.ax.legend(handles, labels,loc="upper right",
           ncol=2)
        self.fig.tight_layout()
        '''
        handles, labels = self.bx.get_legend_handles_labels()
        self.bx.legend(handles, labels,loc="upper right",
           ncol=2)
        '''
        self.canvas.draw();
        
    def openDir(self):
        for dirname, dirnames, filenames in os.walk(self.dir):
        # print path to all subdirectories first.
            for subdirname in dirnames:
                print os.path.join(dirname, subdirname)
                self.comboBox.addItem(str(subdirname))

    
    def calcStatistics(self,name):
        checkDirectory = self.dir + "/" + name
        temp = list()
        self.fourier_std = [zeros((1,150)),zeros((1,150)),zeros((1,150))]
        for filename in os.listdir(checkDirectory):
                if filename.endswith("t.npy"):
                    print "t"
                else: 
                    cur_data, cur_time, cur_ctr = self.openFile(checkDirectory,filename)
                    for i in range(0,3):
                        fourier_val,freq, rate = self.signal.calcFFT(cur_data[i,0:cur_ctr],cur_time[i,0:cur_ctr])
                        #'''print fourier_val
                        j = 0
                        m = 0
                        while freq[m] < 0:
                            m = m + 1
                        #Loop to iterate over all the data points
                        while j < self.freq_scale.size and m < freq.size:
                            if abs(freq[m] - self.freq_scale[j]) < 0.5:
                                k = 0
                                temp = list()
                                while abs(freq[m+k] - self.freq_scale[j]) < 0.5:
                                    # print str(freq.size) + " m " + str(m) + "k " + str(k)
                                    temp.append(fourier_val[m + k])
                                    k = k + 1
                                    if  m + k > freq.size -1:
                                        break
                                #Find mean of range of values
                                mean_val = 0
                                '''
                                print str(j) + ":"
                                print temp
                                '''
                                #Calculate the mean of all the values within +-0.5
                                for l in range(0,len(temp)):
                                    mean_val = temp[l] + mean_val
                                mean_val = mean_val/len(temp)
                                self.fourier_ave[i,j] = mean_val + self.fourier_ave[i,j] 
                                self.fourier_std[i][self.list_ctr,j] = mean_val
                                # self.fourier_std[i][self.list_ctr,j] = mean_val
                                # print self.fourier_std[i]
                                m = m + k
                            else:
                                j = j + 1
                        self.fourier_std[i] = np.concatenate((self.fourier_std[i],zeros((1,150))),axis=0)
                    print self.fourier_std[2]
                    print self.fourier_std[0].shape
                    self.list_ctr = self.list_ctr + 1
                
    def openFile(self,dir,filename):
        index = str(filename).find(".npy")
        try:
            data_in = np.load(str(dir + "/"+ filename))
        except IOError as io:
            print io 
        data_ctr = data_in.size/3
        time_arr = np.load(str(dir) + "/" + str(filename[0:index]) +"t.npy")            
        return data_in, time_arr, data_ctr   
        
   