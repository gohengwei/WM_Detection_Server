import Queue
import threading
import time
import os
import serial
from decimal import *
from numpy import *


class ComMonitorThread(threading.Thread):
    """ A thread for monitoring a COM port. The COM port is 
        opened when the thread is started.
    
        data_q:
            Queue for received data. Items in the queue are
            (data, timestamp) pairs, where data is a binary 
            string representing the received data, and timestamp
            is the time elapsed from the thread's start (in 
            seconds).
        
        error_q:
            Queue for error messages. In particular, if the 
            serial port fails to open for some reason, an error
            is placed into this queue.
        
        port:
            The COM port to open. Must be recognized by the 
            system.
        
        port_baud/stopbits/parity: 
            Serial communication parameters
        
        port_timeout:
            The timeout used for reading the COM port. If this
            value is low, the thread will return data in finer
            grained chunks, with more accurate timestamps, but
            it will also consume more CPU.
    """
    data_ctr = 0
    file_ctr = 0
    xbee_ctr = 0
    data_in = zeros((3,10000))
    time_arr = zeros((3,10000)) 
    time_in = [0,0,0]
    xbee_ave = [0,0,0]
    name = "data"
    isMotion = False
    
    def __init__(   self, outer,
                    data_q, error_q, msg,file_t,  
                    port_num,
                    port_baud,
                    port_stopbits=serial.STOPBITS_ONE,
                    port_parity=serial.PARITY_NONE,
                    port_timeout=0.01):
        threading.Thread.__init__(self)
        
        self.outerPlot = outer
        self.serial_port = None
        self.serial_arg = dict( port=port_num,
                                baudrate=port_baud,
                                stopbits=port_stopbits,
                                parity=port_parity,
                                timeout=port_timeout)

        self.data_q = data_q
        self.error_q = error_q
        self.msg = msg
        self.alive = threading.Event()
        self.alive.set()
        self.name = str(file_t)
        
    def run(self):
        try:
            if self.serial_port: 
                self.serial_port.close()
            self.serial_port = serial.Serial(**self.serial_arg)
        except serial.SerialException, e:
            self.error_q.put(e.message)
            return
        self.serial_port.flushOutput()
        self.serial_port.flushInput()
        self.msg = self.msg + "Thread started <br>"
        # Restart the clock
        time.clock()
        
        self.openFile()
        while self.alive.isSet() and self.serial_port.inWaiting > 0:
            # Reading 1 byte, followed by whatever is left in the
            # read buffer, as suggested by the developer of 
            # PySerial.
            # 
            data = self.serial_port.read(1)
            #print str(data)
            #x = struct.unpack('B',data[0])[0]
            #data += self.serial_port.read(self.serial_port.inWaiting())
            if str(data) == '\n' :
                self.xbee_ctr = 0
                if self.isMotion:
                    self.data_ctr = self.data_ctr + 1
            elif str(data) == "{":
                self.msg = self.msg + "incoming...<br>"
                self.isMotion = True         
                self.data_ctr = 0       
            elif str(data) == '}' :
                self.isMotion = False
                #print time_arr[1,data_ctr]
                #print time_arr[1,data_ctr -1];
                if self.data_ctr > 50 :      
                    # print "file_ctr:" + str(self.file_ctr)
                    #print self.time_arr[:,self.data_ctr -1]
                    #print self.time_in
                    f = open('/home/gohew/workspace/WM_Detection_Server/src/data/fresh/manifest','r+')
                    save(self.name + str(self.file_ctr),self.data_in[0:3,0:self.data_ctr])
                    save(self.name + str(self.file_ctr) + "t",self.time_arr[0:3,0:self.data_ctr])
                    f.seek(0)
                    f.write(str(self.file_ctr))
                    f.close()
                    self.msg = self.msg + "Saved [" + str(time.clock()) + "]: " + self.name + str(self.file_ctr) + " Data points:"+ str(self.data_ctr) +"<br>"
                    self.outerPlot.plotCapture(self.data_in[0:3,0:self.data_ctr],self.time_arr[0:3,0:self.data_ctr])
                    self.file_ctr = self.file_ctr + 1
                self.data_ctr = 0
                self.xbee_ctr = 0
            elif self.xbee_ctr == 6:
                self.xbee_ctr = 0
            #    self.xbee_ctr = 0
            elif self.xbee_ctr % 2:
                '''
                    Save time lapse of Xbee into array
                '''
                if self.isMotion:
                    temp = self.data_ctr -1
                    xbee_ptr = (self.xbee_ctr -1)/2
                    self.time_arr[xbee_ptr,self.data_ctr] = self.time_arr[xbee_ptr,temp] + ord(data)
                    #print "1:" + str(self.time_arr[(self.xbee_ctr -1)/2,self.data_ctr]) + "2:" + str(self.time_arr[(self.xbee_ctr-1)/2,self.data_ctr -1])
                    #self.time_in[(self.xbee_ctr-1)/2] = self.time_in[(self.xbee_ctr - 1)/2] + ord(data);
            elif len(data) > 0:
                '''
                    Save rssi data of Xbee into array
                '''
                if self.isMotion:
                    self.data_in[self.xbee_ctr/2,self.data_ctr] = ord(data)
                timestamp = time.clock()
                self.data_q[self.xbee_ctr/2].put((data, timestamp))
                
                #self.xbee_ctr = self.xbee_ctr + 1
            if len(data) > 0 and str(data) != '\n' and str(data)!= '}' and str(data)!='{': 
                self.xbee_ctr = self.xbee_ctr + 1 
                # print str(ord(data))+ " " + str(self.xbee_ctr)
        # clean up
        if self.serial_port:
            self.msg = self.msg + "Thread started <br>"
            self.serial_port.close()
    
    def openFile(self):
        os.chdir("/home/gohew/workspace/WM_Detection_Server/src/data/fresh")
        #Open data number from page
        f = open('manifest','r+')
        self.file_ctr = int(f.read())
 
    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)