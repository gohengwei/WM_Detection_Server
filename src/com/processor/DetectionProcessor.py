'''
Created on Feb 25, 2013

@author: gohew
'''
from numpy import *
from matplotlib import cm
import matplotlib.pyplot as plt
import struct
from scipy import signal
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.mlab as mlab
from com.ui.visualizer import Visualizer
import numpy as np
#UI imports
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os



'''
    *****************************************************
            Global Variables
    *****************************************************
'''
class VisualizerClass(Visualizer):
    data_in = zeros((3,5000)) 
    time_arr = zeros((3,5000)) 
    sample_rate = [0,0,0]
    fourier_val = zeros((3,5000)) 
    data_ctr = 0
    name = "data"
    color = array(['r','b','g'])
    xbee = array(['top','mid','bot'])
    
    def __init__(self):
        super(VisualizerClass, self).__init__()
        
        Visualizer.__init__(self)
        self.initUI()
        self.center()
        
    def initUI(self):               
        
        #Initialize various UI components
        '''
        self.main_frame = QWidget()
        self.setWindowTitle("Analyze Waveform")
        self.refreshBtn = QPushButton('Refresh',self)
        self.textBrowser = QTextBrowser(self)
        self.graph = QGroupBox("test",self)
        '''

        self.graph.setToolTip('This is a <b>QWidget</b> widget')
        self.dpi = 50
        #testLayout = QVBoxLayout()
        #testLayout.addWidget(self.graph)
        #self.graph.setLayout(testLayout)
        self.fig = Figure((16,12), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.graph)
        self.ax = self.fig.add_subplot(211,autoscale_on='True',title="RSSI vs Time")
        self.bx = self.fig.add_subplot(212,autoscale_on='True',title="Frequency Amplitude vs Frequency")
        
        #self.initGraph()
        '''
        self.data_l = QLabel("Data Panel")
        self.comboBox = QComboBox()
        dataPanel_layout = QVBoxLayout()
        dataPanel_layout.addWidget(self.data_l)
        dataPanel_layout.addWidget(self.refreshBtn)
        dataPanel_layout.addWidget(self.comboBox)
        dataPanel_layout.addWidget(self.textBrowser)
        # Main frame and layout
        #
        main_layout = QHBoxLayout()
        #main_layout.addLayout(testLayout)
        #main_layout.addStretch(1)
        main_layout.addLayout(dataPanel_layout)
        main_layout.addWidget(self.graph)
        self.main_frame.setLayout(main_layout)
        self.setCentralWidget(self.main_frame)
        '''
        self.initRefreshBtn()
        #self.center()
        self.initCB() 
        #self.setGeometry(500,500,500,500)
        self.show()
        
        #self.setWindowTitle('Menubar')    

        
    
    def center(self):
        #self.setGeometry(500,500,500,300)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
       
        
    #  def initGraph(self):    
        
        
    def initRefreshBtn(self):
        self.refreshBtn.clicked.connect(self.buttonClicked)
        
    def buttonClicked(self):
        self.initCB()
    def generateGraph(self):
        for i in range(0,3):
            self.fourier_val[i,0:self.data_ctr],freq, self.sample_rate[i] = self.calcFFT(self.data_in[i,0:self.data_ctr], self.time_arr[i,0:self.data_ctr])
            self.ax.set_xlabel('Time(ms)')
            self.ax.set_ylabel('RSSI')
            print self.data_in
            self.ax.plot(self.time_arr[i,0:self.data_ctr -2],self.data_in[i,0:self.data_ctr -2],self.color[i],label=self.xbee[i])
            #plt.subplot(2,3 , i + 4)
            self.bx.set_xlabel('Freq(Hz)')
            self.bx.set_ylabel('Amplitude')
            self.bx.plot(freq,self.fourier_val[i,0:self.data_ctr],self.color[i],label=self.xbee[i]) 
        '''     
        handles, labels = self.ax.get_legend_handles_labels()
        self.ax.legend(handles, labels,loc="lower right",
           ncol=2)
        '''
        handles, labels = self.bx.get_legend_handles_labels()
        self.bx.legend(handles, labels,loc="upper right",
           ncol=2)
        self.canvas.draw();
            
    def initCB(self):
        
        self.comboBox.clear()
        os.chdir("/home/gohew/workspace/WM_Detection_Server/src/data")
        for files in os.listdir("."):
            if files.endswith(".npy"):
                if files.endswith("t.npy"):
                    print "t"
                else: 
                    self.comboBox.addItem(str(files))
        self.comboBox.activated[str].connect(self.onActivated)
           
    def onActivated(self,text):
        self.ax.clear()
        self.bx.clear()
        self.openFile(text)
        self.generateGraph()
        
    def openFile(self,filename):
        #Open data number from page
        index = filename.indexOf(".npy")
        self.data_in = np.load(str(filename))
        self.data_ctr = self.data_in.size/3
        print filename[0:index] +"t.npy"
        self.time_arr = np.load(str(filename[0:index]) +"t.npy")
        
    '''
    *****************************************************
            Signal Processing Function definitions
    *****************************************************
    ''' 
    def calcFFT(self,_data_arr,_time_arr):
        
        #Calculate Sample spacing for DFT
        _data_ctr = _data_arr.size
        sample_rate = _time_arr[_data_ctr -1]/_data_ctr
        
        #Calculate Frequency bins with frequency shifting
        freq = fft.fftfreq(_data_ctr,sample_rate)
        freq = fft.fftshift(freq)
            
        #Calculate Fourier Transform with Mean Normalization 
        u = np.mean(_data_arr)
        sigma = np.std(_data_arr)
        data_norm = np.copy(_data_arr) #To prevent original data array from being modified due to lists being mutable
        self.textBrowser.setText("mean: <b>" + str(round(u,2)) + "</b><br>" +"std: <b>" + str(round(sigma,2)) + "</b>" + "<br>Sampling rate:<b>" 
                                 + str(round(sample_rate,2)) + "</b>" + "<br>Data pts: <b>" + str(_data_ctr) + "</b><br>")
        for i in range(0,_data_ctr) :
            data_norm[i] = (data_norm[i] - u)/sigma
        fourier_val = fft.fft(data_norm)
        fourier_val = fft.fftshift(fourier_val)
        #print fourier_val
        
        #print "freq"
        #print freq
        #plt.subplot(2,3,i+1)
        fourier_val = abs(fourier_val)
    
        return (fourier_val,freq, sample_rate)
          
'''
def main():

    #time_in = time_arr.sum(axis=1)
    app = QtGui.QApplication(sys.argv)
    gui = VisualizerClass()

    #calcFFT()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
'''