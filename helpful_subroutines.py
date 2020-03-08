#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 10:27:08 2019
@author: John D'Uva (Wang Lab, Princeton University)

A list of short, helpful subroutines for image processing.
---------------------------------------------------------
1) Desktop notification upon script completion
2) Convert TIFF file to JPEG (or other)
3) Crop sagittal lightsheet image and rotate to coronal view
"""

#%% Send notification to Desktop when code is complete
from gi.repository import Notify, GdkPixbuf

Notify.init("Spyder")
notification = Notify.Notification.new(
"Your code has processed.",
" ",
"/home/wanglab/mounts/wang/jduva/sccpre.cat-anaconda-png-842085.png"
)
notification.set_urgency(2) # Highest priority
notification.show()
Notify.uninit()


#%% Convert from .tif to .jpeg
import os
import matplotlib.pyplot as plt

cwd = os.getcwd() + '/'
for filename in os.listdir(cwd): #set the working directory up top^
    if '.' in filename:     
        inpath = os.path.join(cwd, filename)
        print(inpath)
        outpath = inpath.replace('.png','.jpeg')
        img = plt.imread(inpath)   
        print(outpath)
        plt.imsave(outpath, img)


#%% Crop sagittal lightsheet image and rotate to coronal view
from skimage.external import tifffile
import matplotlib.pyplot as plt
import numpy as np

# set processed/sagittal data path
img_pth = '/home/wanglab/mounts/wang/pisano/tracing_output/eaat4/an02_eaat4_031919/elastix/an2_eaat4_031919_1d3x_647_017na_1hfds_z10um_150msec_resized_ch00/result.tif'
img = tifffile.imread(img_pth)

#crop the image
cb = img[:, 220:, :]
plt.imshow(cb[300])

#reslice to posterior-anterior coronal view
cb_coronal = np.rot90(np.transpose(cb, [1, 0, 2]), axes = (2,1))
plt.imshow(cb_coronal[0])

#get max projection
max_cb = np.max(cb_coronal, axis = 0)
plt.imshow(max_cb*1.5)

#export as tif
tifffile.imsave("/home/wanglab/Desktop/jduva_PA_views/an21PA.tif", max_cb)

