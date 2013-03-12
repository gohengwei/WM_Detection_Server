'''
Created on Oct 8, 2012

@author: gohew
'''
from tempfile import TemporaryFile
from numpy import *
import serial
from matplotlib import cm
import matplotlib.pyplot as plt
import struct
from scipy import signal
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import os

#Array for Fourier/Wavelet Transforms
data_in = zeros((3,5000))
time_arr = zeros((3,5000)) 
time_in = [0,0,0]
x = 0
xbee_ctr = 0
data_ctr = 0
xbee_ave = [0,0,0]
file_ctr = 0

# Name of data
name = "data"

'''
    *****************************************************
            Signal Processing Function definitions
    *****************************************************
'''
def calcFFT():
    
    plt.figure(2)
    plt.xlabel('Time(ms)')
    plt.ylabel('RSSI')    
    for i in range(1,2) :
        xbee_ave[i] = time_in[i]/data_ctr
        print "xbee_ave:" + str(xbee_ave[i])
        freq = fft.fftfreq(data_ctr, xbee_ave[i])
        freq = fft.fftshift(freq)
        fourier_val = fft.fft(data_in[i,0:data_ctr])
        fourier_val[0] = 1000
        fourier_val = fft.fftshift(fourier_val)
        print "fft"
        #print fourier_val
        
        #print "freq"
        #print freq
        #plt.subplot(2,3,i+1)
        plt.subplot(211)
        plt.xlabel('Time(ms)')
        plt.ylabel('RSSI')
        plt.plot(time_arr[i,0:data_ctr -2],data_in[i,0:data_ctr -2],'r')
        #plt.subplot(2,3 , i + 4)
        plt.subplot(212)
        plt.xlabel('Freq(Hz)')
        plt.ylabel('Amplitude')
        plt.plot(freq,abs(fourier_val),'b')
        plt.show()          
    return

def testWavelet():
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #Time scale
    X = np.arange(0,data_ctr*xbee_ave[1], xbee_ave[1])
    print "X: "
    print X
    #Frequency scale
    Y = np.arange(1, data_ctr, 1)
    widths = Y
    print "Y"
    print Y
    X, Y = np.meshgrid(X, Y)
    data = np.random.rand(20) - 0.5
    wavelet = signal.ricker
    #widths = np.arange(1,data_ctr + 1)
    cwtmatr = signal.cwt(data_in[1,0:data_ctr],wavelet,widths)
    print "cwtr.shape"
    print cwtmatr.shape
    print "cwtr matrix"
    print cwtmatr
    ax.plot_surface(X,Y,cwtmatr, rstride=1,cmap=cm.spectral, cstride=1,linewidth=0, antialiased=False)
    plt.xlabel('Time(ms)')
    plt.ylabel('Scale(1/f)')
    #
    #plt.zlabel('Amplitude')
    plt.show()
    return
    #return
    #widths = arange(1, 11)
   # Z = cwt(data, wavelet, widths)

def sample():
    x = np.arange(100)
    points = 100
    a = 4
    vec2 = signal.ricker(points,a)
    print vec2
    print vec2.shape
    plt.plot(x,vec2,'r')
    return

'''
    *****************************************************
                        Main Program
    *****************************************************
'''

if __name__ == '__main__':
    pass


print "Reading in data from Xbees..."
#surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
 #       linewidth=0, antialiased=True)
#ax.set_zlim(-1.01, 1.01)

#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

#fig.colorbar(surf, shrink=0.5, aspect=5)

#plt.show()
#sample()s
#testWavelet()

ser = serial.Serial('/dev/ttyACM0', 115200, bytesize=8, timeout= 1, parity='N', stopbits=1)
ser.flushInput();
os.chdir("/home/gohew/workspace/WM_Detection_Server/src/data")
#Open data number from page
f = open('manifest','r+')
file_ctr = int(f.read())

print file_ctr
while True :
    while(ser.inWaiting()) :
        x = struct.unpack('B',ser.read()[0])[0]
        if x == 10 :
            xbee_ctr = 0
            data_ctr = data_ctr + 1
            #print "Iteration:"
            #print data_ctr
        elif x == 125 :
            print "data_ctr: " + str(data_ctr)
            #print time_arr[1,data_ctr]
            #print time_arr[1,data_ctr -1];
            #for i in range(1,data_ctr) :
             #   print time_arr[1,i]
            #time = arange(0,data_ctr*30,30);
            if data_ctr > 50 :
                #time = arange(0, data_ctr*30,30)
                '''
                Perform Fast Fourier Transform Analysis
                Sample spacing = 30
                Window length = data_ctr
                '''
                
                print "file_ctr:" + str(file_ctr)
                f = open('/home/gohew/workspace/WM_Detection_Server/src/data/manifest','r+')
                np.save(name + str(file_ctr),data_in[0:3,0:data_ctr])
                np.save(name + str(file_ctr) + "t",time_arr[0:3,0:data_ctr])
                f.seek(0)
                f.write(str(file_ctr))
                f.close()
                file_ctr = file_ctr + 1
                #calcFFT()
                #testWavelet()
                '''
                Perform Continuous Wavelet Transform Analysis
                Sample spacing = 30
                Window length = data_ctr
                '''
            data_ctr = 0
            xbee_ctr = 0
        else: 
            if xbee_ctr % 2:
                '''
                    Save time lapse of Xbee into array
                '''
                time_arr[(xbee_ctr-1)/2,data_ctr] = time_arr[(xbee_ctr-1)/2,data_ctr -1] + x
               # print time_arr[(xbee_ctr -1)/2,data_ctr]
                time_in[(xbee_ctr-1)/2] = time_in[(xbee_ctr - 1)/2] + x;
            else:
                '''
                    Save rssi data of Xbee into array
                '''
                data_in[xbee_ctr/2,data_ctr] = x
                #   print "Xbee Ctr:" +  str(xbee_ctr)
            xbee_ctr = xbee_ctr + 1