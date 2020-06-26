import cv2
import numpy as np
from skimage import filters
from skimage.measure import regionprops
import matplotlib.pyplot as pl
import math
from scipy.ndimage import gaussian_filter


def Centroid_Camera(path, backgroundfile, videofile, x0, x, y0, y): 
    
    # Background matrix
    vidcapback = cv2.VideoCapture(''+str(path)+''+str(backgroundfile)+'')
    # vidcapback = cv2.VideoCapture(path+backgroundfile)
    success,imageback = vidcapback.read()
    
    # Image matrix
    vidcap = cv2.VideoCapture(path+videofile)
    success,image = vidcap.read()
    frameRate = vidcap.get(5)   
    frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    xe = np.zeros(frames-1)
    ye = np.zeros(frames-1)
    
    for i in range(frames-1):
        success,image = vidcap.read()
        subimage = np.float32((np.int32(image)-np.float32(imageback)))
        img = gaussian_filter(cv2.cvtColor(subimage, cv2.COLOR_BGR2GRAY), sigma=1)
        crop_img = img[y0:y, x0:x]
        threshold_value = filters.threshold_isodata(crop_img)
        labeled_foreground = (crop_img < threshold_value).astype(int)
        properties = regionprops(labeled_foreground, crop_img)
        center_of_mass = properties[0].centroid
        weighted_center_of_mass = properties[0].weighted_centroid
        
        # # Show Frames with their respective Center of Mass
        # fig, ax = pl.subplots()
        # ax.imshow(crop_img)
        # ax.scatter(center_of_mass[1], center_of_mass[0], s=160, c='C0', marker='+')
        # pl.show()
        # fig, ax = pl.subplots()
        # ax.imshow(labeled_foreground)
        # pl.show()
    
        xe[i] = center_of_mass[1]
        ye[i] = center_of_mass[0]
        
    return xe, ye

# Image crop
y0 = 30
x0 = 80
y = 120 # Crop in y
x = 160 # Crop in x

# Choose file
path = 'C:/'
backgroundfile = 'bkg.avi'
videofile = 'video.avi'

xe, ye = Centroid_Camera(path, backgroundfile, videofile, x0, x, y0, y)
pl.plot(xe)
pl.plot(ye)
pl.show()
