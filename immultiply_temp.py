#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 16:55:06 2019

@author: wanglab
"""
from skimage.external import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np
import cv2

#%% Step 2: Rotate to coronal view, crop out negative space, and apply CLAHE/rescaling filters to each plane 

img = tiff.imread('/jukebox/wang/jduva/fullSized_to_segmented/fullsz_CLAHE/clahe32_rescale_25_35.tif')
plt.imshow(img[300])
   
immultiply = img*img*100
plt.imshow((immultiply[300]*100))


#create CLAHE function (to be applied to images in Step 2)
claheFunc = cv2.createCLAHE(clipLimit=2, tileGridSize=(32,32)) 
# create an array of zeros of the same size as the 3D cerebellum which we will fill with the 2D filtered planes
final_array = np.zeros(blah.shape)     
# apply the filter in a loop over the first axis
for i in range(blah.shape[0]):#range(final_array.shape[0]): #for all the z planes in (z,y,x):
#    clahedImage_i = claheFunc.apply(blah[i].astype('uint16'))
##    rescaled = skie.rescale_intensity(clahedImage_i, in_range=(1, 25000), out_range=(0, 35000))
#    final_array[i] = clahedImage_i
    if i%20 ==0 : print(str(i) + " out of: " + str(len(final_array)))
#    plt.imshow(final_array[300]*10)
    blah[i] *= 10
plt.imshow(blah[300])
    


tiff.imsave('/jukebox/wang/jduva/fullSized_to_segmented/fullsz_CLAHE/clahe632_rescale_25_35.tif', final_array[1640:2300])
    