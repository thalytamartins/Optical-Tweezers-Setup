import numpy as np
import nidaqmx
from nidaqmx.constants import *
from nidaqmx.stream_writers import (AnalogSingleChannelWriter)

ttime = 10 # Total time (s)
sigRate = 1 # Frequency
nsamples = 100 # Number of samples per cycle
writingRate = nsamples*sigRate # Signal generation frequency
Ax = 10 # Amplitude (V) 

nv = int(ttime*sigRate)
output = np.tile(np.linspace(-Ax, Ax, int(nsamples)), nv)

with nidaqmx.Task() as writeTask: 
        writeTask.ao_channels.add_ao_voltage_chan("Dev1/ao0")   
        writeTask.timing.cfg_samp_clk_timing(rate = writingRate,
                                             sample_mode = nidaqmx.constants.AcquisitionType.FINITE,
                                             samps_per_chan = int(nsamples*nv))
        writer = AnalogSingleChannelWriter(writeTask.out_stream)
        writer.write_many_sample(output, timeout = ttime + 5)
        writeTask.start()  
        print("Start writing")    
        writeTask.wait_until_done(timeout = ttime + 5)
        print("Done with data")
