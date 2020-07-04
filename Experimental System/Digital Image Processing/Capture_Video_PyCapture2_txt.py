# Choose parameters
num_images = 100

### Installation 
# Download Anaconda 32-bit (Just for me)
# Create environment wiht Python 3.6 called py36 with 'conda create -n py36 -c anaconda python=3.6' cmd
# Download file FlyCapture2/Windows/python/PyCapture2-2.13.61.win32-py3.6.msi on link: https://meta.box.lenovo.com/v/link/view/ea3d78f8daaa499eaff33fef95251b41
# (Installing For all) > (Entire feature will be...) with location C:\Users\LabMTQ\anaconda3\envs\py36

# Link https://github.com/dwells35/alien_eye/blob/fd7ce13fa0e63b8ca250a9542c4c0537b556926a/PyCapture2-2.13.31/examples/python2/SaveImageToAVIEx.py
import time
import PyCapture2
import numpy as np

def print_camera_info(cam):
    cam_info = cam.getCameraInfo()
    print('\n*** CAMERA INFORMATION ***\n')
    print('Serial number - %d' % cam_info.serialNumber)
    print('Camera model - %s' % cam_info.modelName)
    print('Camera vendor - %s' % cam_info.vendorName)
    print('Sensor - %s' % cam_info.sensorInfo)
    print('Resolution - %s' % cam_info.sensorResolution)
    print('Firmware version - %s' % cam_info.firmwareVersion)
    print('Firmware build time - %s' % cam_info.firmwareBuildTime)
    print

def record_video(camera, num_images):
    image_list = [] 
    t = np.zeros(num_images)
    for i in range(num_images):
#        try:
#            image = camera.retrieveBuffer()
#        except PyCapture2.Fc2error as fc2Err:
#            print('Error retrieving buffer : %s' % fc2Err)
#            exit()
        t[i]=time.time()
        image = camera.retrieveBuffer()
        image_list.append(list(image.getData()))
    return image_list, image.getRows(), image.getCols(), t
    
# Iniciate camera record 
bus = PyCapture2.BusManager()
camera = PyCapture2.Camera()
camera.connect(bus.getCameraFromIndex(0))

# Print camera details
print_camera_info(camera)

# Size of window
camera.setFormat7Configuration(float(50), offsetX = 308, offsetY = 108, width = 320, height = 228, pixelFormat = PyCapture2.PIXEL_FORMAT.MONO8)

# Starting capture
print('Starting capture...')
camera.startCapture()

# Setting frame rate
print('Detecting frame rate from Camera')
framerate_property = camera.getProperty(PyCapture2.PROPERTY_TYPE.FRAME_RATE)
framerate = framerate_property.absValue

print('Using frame rate of {} fps'.format(framerate))

# Saving file
image_list, Rows, Cols, t = record_video(camera, num_images)

filename = 'Save_video_('+str(Rows)+','+str(Cols)+').txt'
np.savetxt(filename, np.array(image_list), delimiter="\t", fmt="%s")

## Remember: 
#camera_shape = (image.getRows(), image.getCols())
#image_array = image_list[i].reshape(camera_shape)


# Stop Capture
print('Stopping capture...')
camera.stopCapture()
camera.disconnect()

print('Real frame rate of '+str(num_images/(t[-1]-t[0]))+' fps')


