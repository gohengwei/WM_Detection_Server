'''
Created on Mar 17, 2013

@author: gohew
'''

class SignalClass(object):
    '''
    classdocs
    '''


    def __init__(self:):
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