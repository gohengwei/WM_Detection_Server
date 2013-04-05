'''
Created on Mar 17, 2013

@author: gohew
'''
from numpy import *

class SignalClass(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
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
        freq = fft.fftfreq(_data_ctr,sample_rate/1000)
        freq = fft.fftshift(freq)
            
        #Calculate Fourier Transform with Mean Normalization 
        u = mean(_data_arr)
        sigma = std(_data_arr)
        data_norm = copy(_data_arr) #To prevent original data array from being modified due to lists being mutable
        for i in range(0,_data_ctr) :
            temp = (data_norm[i] - u)/sigma
            data_norm[i] = temp
        fourier_val = fft.fft(data_norm)
        fourier_val = fft.fftshift(fourier_val)
        fourier_val = abs(fourier_val)
    
        return (fourier_val,freq, sample_rate)