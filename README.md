/************************Source Code for Monitoring Moving Objects with Motes*****************************/

To install the Python dependencies perform the following steps:

1. Install SIP: http://www.riverbankcomputing.com/software/sip/download
2. Install PyQt: http://www.riverbankcomputing.com/software/pyqt/download
3. Install PyQwt: http://pyqwt.sourceforge.net/
4. Install Numpy: http://docs.scipy.org/doc/numpy/user/install.html
5. Install Scipy: http://www.scipy.org/Installing_SciPy
6. Install PySerial: http://pyserial.sourceforge.net/

If you are using Ubuntu or linux, pip install will actually install everything so that way is much faster.

Running the application:
The main python application is: DetectionCollector.pyw
It is in the folder src.

Type python DetectionCollector.pyw to run the application

The python packages are in the folder com.

Uploading the Arduino firmware:

The main Arduino program is in the folder Arduino, titled WMDetection_Arduino.ino

To upload the program to an Arduino Mega, first copy the libraries folder to your Arduino libraries folder. Then compile
and upload in the Arduino IDE.

