# Choose parameters
sigtype = 'sinusoidal' # Can be constant, linear, square, triangular or sinusoidal
ttime = 10 # Total time (s)
sigRate = 2 # Frequency
#nsamples = 100 # Number of samples per cycle
Ax = 10 # Amplitude (V) 
A0 = 0 # Central Value (V)

import numpy as np
import nidaqmx
from nidaqmx.constants import *
from nidaqmx.stream_writers import AnalogSingleChannelWriter
import PyCapture2
import numpy as np
import time
from scipy import signal

def generate_signal(camera, filename, framerate, channel, output):
    video = PyCapture2.FlyCapture2Video()
    video.AVIOpen(filename, framerate)
    t = np.zeros(len(output))
    with nidaqmx.Task() as writeTask: 
        writeTask.ao_channels.add_ao_voltage_chan("Dev1/ao0")   
        writeTask.start()  
        for i in range(len(output)):
            writeTask.write(output[i])
            t[i]=time.time()
            image = camera.retrieveBuffer()
            video.append(image)        
        writeTask.stop() 
        print('Appended {} images to AVI file: {}...'.format(len(output), filename))
        video.close()  
        print("Done with data")
    return t        
        
def signal_type(sigtype, Ax, A0, nsamples, nv):
    if sigtype=='constant':
        output = np.tile(np.ones(nsamples)*Ax, nv) + A0
    elif sigtype=='linear':
        output = np.tile(np.linspace(-Ax, Ax, nsamples), nv) + A0
    elif sigtype=='square':
        output = np.tile(Ax*signal.square(np.pi *np.linspace(0, 1, nsamples, endpoint=False)-np.pi/2), nv) + A0
    elif sigtype=='triangular':
        output = np.tile(Ax*np.concatenate((np.linspace(-1,1,int(nsamples/2), endpoint=False), np.linspace(1,-1,int(nsamples/2), endpoint=False))) , nv) + A0
    elif sigtype=='sinusoidal':
        output = Ax*np.sin(np.arange(0,2*nv*np.pi,2*np.pi/nsamples)) + A0
    return output
        
# Iniciate camera record 
bus = PyCapture2.BusManager()
camera = PyCapture2.Camera()
camera.connect(bus.getCameraFromIndex(0))

# Size of window
#camera.setFormat7Configuration(float(50), offsetX = 308, offsetY = 108, width = 320, height = 228, pixelFormat = PyCapture2.PIXEL_FORMAT.MONO8)

# Starting capture
print('Starting capture...')
camera.startCapture()

# Setting frame rate
framerate_property = camera.getProperty(PyCapture2.PROPERTY_TYPE.FRAME_RATE)
framerate = framerate_property.absValue
print('Using frame rate of {} fps'.format(framerate))

# Signal
nsamples = int(framerate/sigRate) # Signal generation frequency
nv = int(ttime*sigRate)
output = signal_type(sigtype, Ax, A0, nsamples, nv)


# Saving file
filename = b'Save_video.avi'
t = generate_signal(camera, filename, framerate, "Dev1/ao0", output)

print('Stopping capture...')
camera.stopCapture()
camera.disconnect()

print('Real frame rate of '+str(len(output)/(t[-1]-t[0]))+' fps')
