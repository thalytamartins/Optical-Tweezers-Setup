### Installation 
# Download Anaconda 32-bit (Just for me)
# Create environment wiht Python 3.6 called py36 with 'conda create -n py36 -c anaconda python=3.6' cmd
# Download file FlyCapture2/Windows/python/PyCapture2-2.13.61.win32-py3.6.msi on link: https://meta.box.lenovo.com/v/link/view/ea3d78f8daaa499eaff33fef95251b41
# (Installing For all) > (Entire feature will be...) with location C:\Users\LabMTQ\anaconda3\envs\py36

## Taking single image with PyCapture2
import PyCapture2
import numpy as np
import matplotlib.pyplot as pl
bus = PyCapture2.BusManager()
camera = PyCapture2.Camera()
camera.connect(bus.getCameraFromIndex(0))
camera.startCapture()
image = camera.retrieveBuffer()
camera_shape = (image.getRows(), image.getCols())
image_array = np.array(image.getData(), dtype='uint8').reshape(camera_shape)
fig, ax = pl.subplots()
ax.imshow(image_array)
