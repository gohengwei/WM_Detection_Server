""" 
A simple demonstration of a serial port monitor that plots live
data using PyQwt.

The monitor expects to receive single-byte data packets on the 
serial port. Each received byte is understood as a temperature
reading and is shown on a live chart.

When the monitor is active, you can turn the 'Update speed' knob
to control the frequency of screen updates.

Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 07.08.2009
"""
import random, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.Qwt5 as Qwt
import Queue
import numpy as np
from numpy import *
from com.signal.SignalProcessing import SignalClass
from com.processor.FourierClass import FourierClass
from svm import *
from svmutil import *
from com.processor.DetectionProcessor import VisualizerClass
from com_monitor import ComMonitorThread
from eblib.serialutils import full_port_name, enumerate_serial_ports
from eblib.utils import get_all_from_queue, get_item_from_queue
from livedatafeed import LiveDataFeed

class PlottingDataMonitor(QMainWindow):
    xbee = ["TOP","MID","BOT"]
    penColor = ["red","limegreen","blue"]
    def __init__(self, parent=None):
        self.signal = SignalClass()
        super(PlottingDataMonitor, self).__init__(parent)
        self.setWindowTitle("Detection Monitor and Collector")
        self.setWindowIcon(QIcon('/home/gohew/workspace/WM_Detection_Server/src/Linux-Client-32.png'))
        self.monitor_active = False
        self.com_monitor = None
        self.com_data_q = None
        self.com_error_q = None
        self.time_arr = None
        self.data_arr = None
        self.msg = None
        self.model = None
        self.min = None
        self.max = None
        self.predicted = 0
        self.livefeed = [LiveDataFeed(),LiveDataFeed(),LiveDataFeed()]
        self.temperature_samples = [list(),list(),list()]
        self.timer = QTimer()
        self.Visualizer = VisualizerClass()
        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
        self.initSVM()
        
    def make_data_box(self, name):
        label = QLabel(name)
        qle = QLineEdit()
        qle.setEnabled(False)
        qle.setFrame(False)
        return (label, qle)
        
    def create_plot(self):
        plot = Qwt.QwtPlot(self)
        plot.setCanvasBackground(Qt.black)
        plot.setAxisTitle(Qwt.QwtPlot.xBottom, 'Time')
        plot.setAxisScale(Qwt.QwtPlot.xBottom, 0, 10, 1)
        plot.setAxisTitle(Qwt.QwtPlot.yLeft, 'RSSI')
        plot.setAxisScale(Qwt.QwtPlot.yLeft, 30, 75, 20)
        plot.replot()
        
        curve = Qwt.QwtPlotCurve('')
        curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
        curve.attach(plot)
        
        return plot, curve

    def create_fftPlot(self):
        self.fftplot1 = Qwt.QwtPlot(self)
        self.fftplot1.setCanvasBackground(Qt.black)
        self.fftplot1.setAxisTitle(Qwt.QwtPlot.xBottom, 'Time')
        self.fftplot1.setAxisScale(Qwt.QwtPlot.xBottom, 0, 2500, 500)
        self.fftplot1.setAxisTitle(Qwt.QwtPlot.yLeft, 'RSSI')
        self.fftplot1.setAxisScale(Qwt.QwtPlot.yLeft, 40, 75, 10)
        self.fftplot1.replot()
        
        self.fftplot2 = Qwt.QwtPlot(self)
        self.fftplot2.setCanvasBackground(Qt.black)
        self.fftplot2.setAxisTitle(Qwt.QwtPlot.xBottom, 'Frequency')
        self.fftplot2.setAxisScale(Qwt.QwtPlot.xBottom, -150, 150, 20)
        self.fftplot2.setAxisTitle(Qwt.QwtPlot.yLeft, 'Amplitude')
        self.fftplot2.setAxisScale(Qwt.QwtPlot.yLeft, 0,200, 50)
        self.fftplot2.replot()
        self.fftcurve = [Qwt.QwtPlotCurve(''),Qwt.QwtPlotCurve(''),Qwt.QwtPlotCurve('')]
        self.fftcurve2 = [Qwt.QwtPlotCurve(''),Qwt.QwtPlotCurve(''),Qwt.QwtPlotCurve('')]
        for i in range(0,3):
            self.fftcurve[i].setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
            pen = QPen(QColor(self.penColor[i]))
            pen.setWidth(2)
            self.fftcurve[i].setPen(pen)
            self.fftcurve[i].attach(self.fftplot1)
        for i in range(0,3):
            self.fftcurve2[i].setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
            pen = QPen(QColor(self.penColor[i]))
            pen.setWidth(2)
            self.fftcurve2[i].setPen(pen)
            self.fftcurve2[i].attach(self.fftplot2)
        
    def create_thermo(self):
        thermo = Qwt.QwtThermo(self)
        thermo.setPipeWidth(6)
        thermo.setRange(0, 120)
        thermo.setAlarmLevel(80)
        thermo.setAlarmEnabled(True)
        thermo.setFillColor(Qt.green)
        thermo.setAlarmColor(Qt.red)
        thermo.setOrientation(Qt.Horizontal, Qwt.QwtThermo.BottomScale)
        
        return thermo

    def create_knob(self):
        knob = Qwt.QwtKnob(self)
        knob.setRange(0, 250, 0, 1)
        knob.setScaleMaxMajor(10)
        knob.setKnobWidth(50)
        knob.setValue(20)
        return knob

    def create_status_bar(self):
        self.status_text = QLabel('Monitor idle')
        self.statusBar().addWidget(self.status_text, 1)

    def create_main_frame(self):
        # Port name
        #
        portname_l, self.portname = self.make_data_box('Port:')
        dataname_l, self.dataname = self.make_data_box('File Descriptor')
        self.maniBtn = QPushButton("Reset Manifest")
        self.connect(self.maniBtn,SIGNAL("clicked()"),self.ResetManifest)
        self.dataname.setEnabled(True)
        portname_layout = QVBoxLayout()
        portname_layout.addWidget(portname_l)
        portname_layout.addWidget(self.portname, 0)
        portname_layout.addWidget(dataname_l)
        portname_layout.addWidget(self.dataname)
        portname_layout.addWidget(self.maniBtn)
        portname_layout.addStretch(2)
        portname_groupbox = QGroupBox('COM Port')
        portname_groupbox.setLayout(portname_layout)
        # Plot and thermo
        #
        self.plot = [Qwt.QwtPlot(),Qwt.QwtPlot(),Qwt.QwtPlot()]
        self.curve = [Qwt.QwtPlotCurve(),Qwt.QwtPlotCurve(),Qwt.QwtPlotCurve()]
        for i in range(0,3):
            self.plot[i], self.curve[i] = self.create_plot()
            pen = QPen(QColor(self.penColor[i]))
            pen.setWidth(2)
            self.curve[i].setPen(pen)
        '''
        self.thermo = self.create_thermo()
        thermo_l = QLabel('Average')
        thermo_layout = QHBoxLayout()
        thermo_layout.addWidget(thermo_l)
        thermo_layout.addWidget(self.thermo)
        thermo_layout.setSpacing(5)
        '''
        self.create_fftPlot()
        self.updatespeed_knob = self.create_knob()
        self.connect(self.updatespeed_knob, SIGNAL('valueChanged(double)'),
            self.on_knob_change)
        self.knob_l = QLabel('Update speed = %s (Hz)' % self.updatespeed_knob.value())
        self.knob_l.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        knob_layout = QVBoxLayout()
        knob_layout.addWidget(self.updatespeed_knob)
        knob_layout.addWidget(self.knob_l)
        
        self.debug_l = QLabel('Messages Panel')
        self.debug_l.setAlignment(Qt.AlignLeft)
        self.debugPanel = QTextBrowser()
        self.debugPanel.setStyleSheet("QTextBrowser { background-color : black; color :green; }")
        panel_layout = QVBoxLayout()
        panel_layout.addWidget(self.debug_l)
        panel_layout.addWidget(self.debugPanel)
        
        self.stats_l = QLabel('System Statistics')
        self.stats_l.setAlignment(Qt.AlignLeft)
        self.statsPanel = QTextBrowser()
        self.statsPanel.setStyleSheet("QTextBrowser { background-color : black; color :green; }")
        stats_layout = QVBoxLayout()
        stats_layout.addWidget(self.stats_l)
        stats_layout.addWidget(self.statsPanel)
        
        self.lcd = [QLCDNumber(self),QLCDNumber(self),QLCDNumber(self)]
        self.lcd_l1 = QLabel("RSSI:",self)
        self.lcd[0].setStyleSheet("QLCDNumber { background-color : black; color :yellow; }")
        self.lcd[0].setSegmentStyle(QLCDNumber.Flat)
        self.lcd_layout = QHBoxLayout()
        self.lcd_layout.addWidget(self.lcd_l1)
        self.lcd_layout.addWidget(self.lcd[0])
        self.lcd_l2 = QLabel("RSSI:",self)
        # self.lcd[1] = QLCDNumber(self)
        self.lcd[1].setStyleSheet("QLCDNumber { background-color : black; color :yellow;}")
        self.lcd[1].setSegmentStyle(QLCDNumber.Flat)
        self.lcd_layout2 = QHBoxLayout()
        self.lcd_layout2.addWidget(self.lcd_l2)
        self.lcd_layout2.addWidget(self.lcd[1])
        self.lcd_l3 = QLabel("RSSI:",self)
        #self.lcd[2] = QLCDNumber(self)
        self.lcd[2].setStyleSheet("QLCDNumber { background-color : black; color :yellow; }")
        self.lcd[2].setSegmentStyle(QLCDNumber.Flat)
        self.lcd_layout3 = QHBoxLayout()
        self.lcd_layout3.addWidget(self.lcd_l3)
        self.lcd_layout3.addWidget(self.lcd[2])
        
        stats_layout.addLayout(self.lcd_layout)
        stats_layout.addLayout(self.lcd_layout2)
        stats_layout.addLayout(self.lcd_layout3)
        
        debug_layout = QHBoxLayout()
        debug_layout.addLayout(panel_layout)
        debug_layout.addLayout(stats_layout)
        debug_layout.addWidget(portname_groupbox)
        #debug_layout.addWidget(self.debugPanel)
        debug_layout.addLayout(knob_layout)
        
        fftplot_layout = QVBoxLayout()
        fft_groupbox = QGroupBox('Current Data Analysis')
        fftplot_layout.addWidget(self.fftplot1)
        fftplot_layout.addWidget(self.fftplot2)
        fft_groupbox.setLayout(fftplot_layout)
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.plot[0])
        plot_layout.addWidget(self.plot[1])
        plot_layout.addWidget(self.plot[2])
        #plot_layout.addLayout(thermo_layout)
        plot_groupbox = QGroupBox('Xbee RSSI Stream')
        plot_groupbox.setLayout(plot_layout)
        overallplot_layout = QHBoxLayout()
        overallplot_layout.addWidget(plot_groupbox)
        overallplot_layout.addWidget(fft_groupbox)
        
        top_layout = QVBoxLayout()
        top_layout.addLayout(overallplot_layout)
        top_layout.addLayout(debug_layout)
    
        
        # Main frame and layout
        #
        self.main_tab = QTabWidget()
        
        self.main_frame = QWidget()
        main_layout = QVBoxLayout()
        #main_layout.addWidget(portname_groupbox)
        main_layout.addLayout(top_layout)
        main_layout.addStretch(1)
        self.main_frame.setLayout(main_layout)
        
        self.main_tab.addTab(self.main_frame, "Data Collection")
        self.main_tab.addTab(self.Visualizer, "Waveform Analysis")
        self.main_tab.addTab(FourierClass(), "Fourier Analysis")
        self.setCentralWidget(self.main_tab)
        self.set_actions_enable_state()
        
    def openAnalysis(self):
        #self.Analysis = VisualizerClass()
        #self.Analysis.show()
        '''
        '''
    
    def ResetManifest(self):
        num = "0"
        f = open('/home/gohew/workspace/WM_Detection_Server/src/data/fresh/manifest','w+')
        f.seek(0)
        f.write(num)
        f.close()
        if self.com_monitor:
            self.com_monitor.msg = self.com_monitor.msg + "<b>[Manifest reset]</b><br>"
            self.com_monitor.file_ctr = 0
        else: 
            self.debugPanel.setText("<b>[Manifest reset]</b><br>")
        
            
        
    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")
        
        selectport_action = self.create_action("Select COM &Port...",
            shortcut="Ctrl+P", slot=self.on_select_port, tip="Select a COM port")
        self.start_action = self.create_action("&Start monitor",
            shortcut="Ctrl+M", slot=self.on_start, tip="Start the data monitor")
        self.stop_action = self.create_action("&Stop monitor",
            shortcut="Ctrl+T", slot=self.on_stop, tip="Stop the data monitor")
        exit_action = self.create_action("E&xit", slot=self.close, 
            shortcut="Ctrl+X", tip="Exit the application")
        
        self.start_action.setEnabled(False)
        self.stop_action.setEnabled(False)
        
        self.add_actions(self.file_menu, 
            (   selectport_action, self.start_action, self.stop_action,
                None, exit_action))
            
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About", 
            shortcut='F1', slot=self.on_about, 
            tip='About the monitor')
        
        self.add_actions(self.help_menu, (about_action,))

    def set_actions_enable_state(self):
        if self.portname.text() == '':
            start_enable = stop_enable = False
        else:
            start_enable = not self.monitor_active
            stop_enable = self.monitor_active
        
        self.start_action.setEnabled(start_enable)
        self.stop_action.setEnabled(stop_enable)

    def on_about(self):
        msg = __doc__
        QMessageBox.about(self, "About the demo", msg.strip())
    
    def on_select_port(self):
        ports = list(enumerate_serial_ports())
        if len(ports) == 0:
            QMessageBox.critical(self, 'No ports',
                'No serial ports found')
            return
        
        item, ok = QInputDialog.getItem(self, 'Select a port',
                    'Serial port:', ports, 0, False)
        
        if ok and not item.isEmpty():
            self.portname.setText(item)            
            self.set_actions_enable_state()

    def on_stop(self):
        """ Stop the monitor
        """
        if self.com_monitor is not None:
            self.com_monitor.join(0.01)
            self.com_monitor = None

        self.monitor_active = False
        self.timer.stop()
        self.set_actions_enable_state()
        
        self.status_text.setText('Monitor idle')
    
    def on_start(self):
       
        """ Start the monitor: com_monitor thread and the update
            timer
        """
        if self.com_monitor is not None or self.portname.text() == '':
            return
        
        self.data_q = [Queue.Queue(),Queue.Queue(),Queue.Queue()]
        self.error_q = Queue.Queue()
        self.msg = ""
        self.com_monitor = ComMonitorThread(self,
            self.data_q,
            self.error_q,
            self.msg, self.dataname.text(),
            str(self.portname.text()),
            115200)
        self.com_monitor.start()
        
        com_error = get_item_from_queue(self.error_q)
        if com_error is not None:
            QMessageBox.critical(self, 'ComMonitorThread error',
                com_error)
            self.com_monitor = None

        self.monitor_active = True
        self.set_actions_enable_state()
        
        self.timer = QTimer()
        self.connect(self.timer, SIGNAL('timeout()'), self.on_timer)
        
        update_freq = self.updatespeed_knob.value()
        if update_freq > 0:
            self.timer.start(1000.0 / update_freq)
        
        self.status_text.setText('Monitor running')
    
    def on_timer(self):
        """ Executed periodically when the monitor update timer
            is fired.
        """
        self.read_serial_data()
        self.update_monitor()

    def on_knob_change(self):
        """ When the knob is rotated, it sets the update interval
            of the timer.
        """
        update_freq = self.updatespeed_knob.value()
        self.knob_l.setText('Update speed = %s (Hz)' % self.updatespeed_knob.value())

        if self.timer.isActive():
            update_freq = max(0.01, update_freq)
            self.timer.setInterval(1000.0 / update_freq)

    def update_monitor(self):
        """ Updates the state of the monitor window with new 
            data. The livefeed is used to find out whether new,b
            data was received since the last update. If not, 
            nothing is updated.
        """
        statsMsg = ""    
        if self.com_monitor:
            if self.data_arr != None and self.time_arr != None:
                tempStd =  np.std(self.data_arr[1,:])
                if tempStd > 0.5:
                    for i in range(0,3):
                        self.fftcurve[i].setData(self.time_arr[i,:], self.data_arr[i,:])
                        self.fftplot1.replot()
                    self.fftplot1.setAxisScale(Qwt.QwtPlot.xBottom, 0, self.time_arr[1,self.time_arr.size/3 -1], 500)
                    for i in range(0,3):
                        fourier_val ,freq, rate = self.signal.calcFFT(self.data_arr[i,:], self.time_arr[i,:])
                        self.fftcurve2[i].setData(freq, fourier_val)
                        self.fftplot2.replot()
            self.debugPanel.setText(self.com_monitor.msg)
        self.debugPanel.verticalScrollBar().setValue(
    self.debugPanel.verticalScrollBar().maximum())
        for i in range(0,3):
            if self.livefeed[i].has_new_data:
                data = self.livefeed[i].read_data()
                self.temperature_samples[i].append(
                    (data['timestamp'], data['temperature']))
                self.lcd[i].display(data['temperature'])
                if len(self.temperature_samples[i]) > 2500:
                    self.temperature_samples[i].pop(0)
                
                xdata = [s[0] for s in self.temperature_samples[i]]
                ydata = [s[1] for s in self.temperature_samples[i]]
                
                avg = sum(ydata) / (len(ydata))
                std = np.std(np.array(ydata))
                statsMsg = statsMsg + "<b>XBEE" + self.xbee[i] + ": mean</b>:" + str(round(avg,2)) + " " + " <b>std</b>:" + str(round(std,2)) + "<br>"
                self.plot[i].setAxisScale(Qwt.QwtPlot.xBottom, xdata[0], max(20, xdata[-1]))
                self.curve[i].setData(xdata, ydata)
                self.plot[i].replot()
        predictedStr = ""
        if self.predicted == 0:
            predictedStr = "None"
        elif self.predicted == 1:
            predictedStr = "Running"
        elif self.predicted == 2:
            predictedStr = "Slow Walking"
        elif self.predicted == 3:       
            predictedStr = "Walking"
            
        statsMsg = statsMsg + "Predicted Output:<font color=red size=66><b>" + predictedStr + "</b></font><"; 
        self.statsPanel.setText(statsMsg)
                #self.thermo.setValue(avg)
    
    def plotCapture(self,data_arr,time_arr):
        self.data_arr = data_arr
        self.time_arr = time_arr
        svm_dict = [dict()]
        #svm_dict = dict()
        fourier_data ,freq_data, rate_data = self.signal.calcFFT(self.data_arr[0,:], self.time_arr[0,:])
        norm_fourier = self.Visualizer.SVMClass.normalizeFreq(fourier_data, freq_data)
        svm_label = [2]
        for i in range(0,norm_fourier.size):
            normScale = self.Visualizer.SVMClass.normalizeScale(norm_fourier[0,i],0,1, float(self.min[i]), float(self.max[i]))
            tempDict = {i + 1:normScale}
            svm_dict[0].update(tempDict)
        #print svm_dict
        #print svm_label
        print svm_dict[0]
        p_labs, p_acc, p_vals = svm_predict(svm_label, svm_dict, self.model)
        
        self.predicted = p_labs[0]
        print p_labs
        print p_acc
        print p_vals
        
    def read_serial_data(self):
        """ Called periodically by the update timer to read data
            from the serial port.
        """
        for i in range(0,3):
            qdata = list(get_all_from_queue(self.data_q[i]))
            if len(qdata) > 0:
                data = dict(timestamp=qdata[-1][1], 
                            temperature=ord(qdata[-1][0]))
                self.livefeed[i].add_data(data)
    
    # The following two methods are utilities for simpler creation
    # and assignment of actions
    #
    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def initSVM(self):
        self.model = svm_load_model("/home/gohew/workspace/WM_Detection_Server/src/problem/motion10top.scale.model")
        self.min,self.max = self.Visualizer.SVMClass.loadRange("/home/gohew/workspace/WM_Detection_Server/src/problem/range10")
def main():
    app = QApplication(sys.argv)
    form = PlottingDataMonitor()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
    
    

