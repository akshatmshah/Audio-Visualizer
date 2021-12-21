import pyaudio
import numpy as np
from pyqtgraph.Qt import QtGui
from pyqtgraph.Qt import QtCore
import sys
import pyqtgraph as pg
import time 

class Visualizer(object):
    #we add the device and pyaudio
    def __init__(self, device, po):
        self.traces = dict()
        #init pyaudio
        self.time = time.time()
        self.p = po
        self.data = 0
       
       #audio professionals use 44.1kHz
        self.RATE = 44100
        #2048 frames per buffer
        self.CHUNK = 2048
        #only using 1 channel (microphone)
        self.CHANNEL = 1
        self.INPUT = True
        self.DEVICE = device
        #paInt16 is basically a signed 16-bit binary string. range options to be (-32768, 32767)
        self.FORMAT = pyaudio.paInt16

        #open pyaudio stream to obtain inputs
        self.stream = self.p.open(format = self.FORMAT,
                channels = self.CHANNEL,
                rate=self.RATE,
                input=self.INPUT,
                frames_per_buffer=self.CHUNK
                )

        #modified window to look cool
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('visualizer')

        ##create two plots without x or y axis
        self.waveform = self.win.addPlot(title='', row=1, col=1)
        self.waveform.hideAxis('left');
        self.waveform.hideAxis('bottom');

        self.diatonic = self.win.addPlot(title='', row=1, col=1)
        self.diatonic.hideAxis('left');
        self.diatonic.hideAxis('bottom');

    def __str__(self):
        #helped see max to normalize -- now ranges should be from -1 to 1
        return "normalized data: " + " " + str(max(self.data))

    def loop(self):
        #read audio
        self.data = np.frombuffer(self.stream.read(self.CHUNK, exception_on_overflow=False), dtype=np.int16)

        #fft the data
        fft_x = np.fft.fft(self.data)
        #normalize so peaks are one and duplicate data is not there
        fixed_x = np.abs(fft_x[0:self.CHUNK]*2 / (32767 * self.CHUNK)) 


        #normalize waveform data       
        new_data = []
        for point in self.data[:len(self.data)]/2:
            point = point/32767
            new_data.append(point)

        self.data = new_data
        print(self)
        #x value evenly spaced from 0 to chunk but normalized by the sampling rate 
        #y value is the normalized wave form data that ranges from -1 to 1 since it is normalized
        self.trace(name='waveform', data_x= np.arange(0, self.CHUNK)/self.RATE, data_y=self.data)
        #x value : goes from 0 to rate with chunk number of points
        #y value takes a fft of our points, scaled and normalized
        self.trace(name='diatonic', data_x = np.linspace(0,  self.RATE, self.CHUNK), data_y=fixed_x)

    def trace(self, name, data_x, data_y):
        curr = time.time()
        elapsed = curr - self.time
        self.win.setWindowTitle(time.strftime("%Hh%Mm%Ss", time.gmtime(elapsed)))
        #if trace exist then add the data
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            #if we don't see a trace with either of these names then we create a plot with the scales
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='b', width=3)
                #normalized values from -1 to 1
                self.waveform.setYRange(-1, 1) 
                #go from 0 to normalized frequency 
                self.waveform.setXRange(0, self.CHUNK/self.RATE)
            if name == 'diatonic':
                self.traces[name] = self.diatonic.plot(pen='c', width=3)
                #set x limit from 0 to 20k since this is range that humans can hear
                self.diatonic.setXRange(0, self.RATE/2)
                #ylimit just modified because sounds played from speakers can be seen a little better
                self.diatonic.setYRange(-0.25, 0.25)
                

    
    def run(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def animate(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.loop)
        timer.start(20)
        self.run()