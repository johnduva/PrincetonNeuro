#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:11:03 2019
@author: John D'Uva (Wang Lab, Princeton University)

Combine each sample's raw data (lightsheet) into a singular binaraized file for pos/neg zebrin banding comparison.

Steps:
1) Combine all indivual fullsize image planes into a single TIFF file (w/ option to save this step)
2) Rotate to coronal view, crop out negative space, and apply CLAHE/rescaling filters to each plane 
3) Binarize planes into zebrin positive/negative pixels with a thresholding algorithm

"""

import os, cv2
import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
import skimage.exposure as skie
from skimage.filters import threshold_otsu, threshold_adaptive
from skimage import img_as_bool
from tools.analysis.analyze_injection import optimize_inj_detect, pool_injections_for_analysis
%matplotlib auto


#%% 
'''Step 1:  Combine all indivual fullsize image planes into a single TIFF file (w/ option to save this step)'''

# Set Input Parameters:
# input path
parent_dir = '/jukebox/wang/pisano/tracing_output/eaat4/'
# output path
output = '/jukebox/wang/jduva/ALL DESKTOP/fullSized_to_segmented/fullsz_noCLAHE/'
 
# Loop through each brain in the parent directory, will have to change this based on folder structure
for directory in sorted(os.listdir(parent_dir)): 
    # keep track of what animal you're working with
    an = directory[0:4] 
    
    #see which brains have already been completed, if none of them have - then create the output directory
    try: 
        if an in os.listdir(output): 
            print(an + " already in " + output)
            continue
    except FileNotFoundError:
        os.makedirs(output)
        print("Output directory created.")
    
    path =  os.path.join(parent_dir + directory + '/full_sizedatafld/')
    for folders in os.listdir(path):
        if '647' in folders:
            newPath = os.path.join(path + folders)
            zPlanes = sorted(os.listdir(newPath))
            array = []
            print(an)
            for i, fls in enumerate(zPlanes):
                wholePath = os.path.join(newPath, fls)
                img = tiff.imread(wholePath)
                array.append(img)
#                print(fls) 
    stack = np.array(array)
# Uncomment to save raw data as one combined tif before you CLAHE filter it
    .imsave(output + an, stack)
    print()
    print("Saving " + an + " to " + output)
    print()

#%% 
    '''Step 2: Rotate to coronal view, crop out negative space, and apply CLAHE/rescaling filters to each plane    ''' 

    img = tiff.imread('/home/wanglab/mounts/LightSheetTransfer/Jess/processed/an12_eaat4_4x/an12_eaat4_031919_cb_4x_488_647_049na_1hfds_z5um_50msec_20povlp_resized_ch01.tif')
    img.shape
    plt.imshow(img[200])
    
    cb_coronal = np.rot90(np.transpose(img, [1,0,2]), axes = (2,1)) # rotate to coronal view
#    cropped = cb_coronal[:, 100:, 300:1850] #crop out negative space
    plt.imshow(cb_coronal[50]*7)
   
    cropped=cb_coronal
    
    #create CLAHE function (to be applied to images in Step 2)
    claheFunc = cv2.createCLAHE(clipLimit=2, tileGridSize=(32,32)) 
    # create an array of zeros of the same size as the 3D cerebellum which we will fill with the 2D filtered planes
    final_array = np.zeros(cropped.shape)     
    # apply the filter in a loop over the first axis
    for i in range(img.shape[0]):#range(final_array.shape[0]): #for all the z planes in (z,y,x):
        clahedImage_i = claheFunc.apply(cropped[i].astype('uint16'))
        two_clahedImage_i = claheFunc.apply(clahedImage_i)
        final_array[i] = two_clahedImage_i
        if i%10 ==0 : print(str(i) + " out of: " + str(len(final_array)))
    
    plt.imshow(final_array[200])
    plt.imshow(final_array[200]*final_array[200]*final_array[200]*final_array[200])
    final_array = final_array*final_array*final_array*final_array
    
    tiff.imsave('/jukebox/wang/jduva/fullSized_to_segmented/fullsz_CLAHE/4ximmult_2Xclahe32_4xOBJ.tif', final_array)
    
    
#%% 
    %matplotlib inline
    
'''Step 3: Binarize planes into zebrin positive/negative pixels
- If a pixel value is greater than a threshold, it is assigned a value of positive (1/white). If not, it is assigned a negative value (0/black).
- Positive values outside of the brain are okay since they will be ignored during registration'''

    img = final_array[90:445]
#    img= tiff.imread('/jukebox/wang/jduva/fullSized_to_segmented/fullsz_CLAHE/4ximmult_2Xclahe32_4xOBJ.tif)
    plt.imshow(img[200])


    array = np.zeros(img.shape)    
    normalizedImg = np.zeros((img.shape[1], img.shape[2]))
    for i, plane in enumerate(range(img.shape[0])):
        # normalize each plane
        normalizedImg = cv2.normalize(img[i],  normalizedImg, 0, 255, cv2.NORM_MINMAX)      
        # threshold each plane (src, threshVal, maxVal, thresh_type)
        ret,thresh1 = cv2.threshold(normalizedImg, 90, 255, cv2.THRESH_BINARY)
        array[i] = thresh1
        if i%40== 0:
            print('Plane ' + str(i) + " of " + str(img.shape[0]))
            plt.imshow(thresh1,cmap='gray')
            plt.show()
            
    tiff.imsave('/jukebox/wang/jduva/fullSized_to_segmented/fullsz_CLAHE/4ximmult_2xclahe_4xOBJ_normalized_cv2Thresh90.tif', array)
 
    # rotate back to saggital orientation depending on needs
    cb_sag = np.transpose(array, [2,0,1])
    plt.imshow(cb_sag[300])
    tiff.imsave('/jukebox/wang/jduva/fullSized_to_segmented/fullsz_CLAHE/segmented_saggital_4ximmult_2xclahe_4xOBJ.tif', cb_sag)

    
#%%
    %matplotlib auto
    
'''Step 3: Binarize planes into zebrin positive/negative pixels
- If a pixel value is greater than a threshold, it is assigned a value of positive (1/white). If not, it is assigned a negative value (0/black).
- Positive values outside of the brain are okay since they will be ignored during registration'''

    img = array[85:475]
    plt.imshow(img[200])

    array = np.zeros(img.shape)    
    normalizedImg = np.zeros((img.shape[1], img.shape[2]))
    for i, plane in enumerate(range(img.shape[0])):
        # normalize each plane
        normalizedImg = cv.normalize(img[i],  normalizedImg, 0, 255, cv.NORM_MINMAX)
        
        # threshold each plane (src, threshVal, maxVal, thresh_type)
        ret,thresh1 = cv.threshold(normalizedImg, 100, 255, cv.THRESH_BINARY)

        binary_adaptive = threshold_adaptive(img[i], block_size, offset=10)
        array[i] = binary_adaptive
        print(str(i) + " out of: " + str(img.shape[0]))
       
        if i%10== 0:
            plt.imshow(binary_adaptive)
            plt.show()
    
    tiff.imsave('/jukebox/wang/jduva/fullSized_to_segmented/fullsz_CLAHE/4ximmult_2xclahe_4xOBJ_thresh_adapt.tif', array)
 
    # rotate back to saggital orientation
    cb_sag = np.transpose(array, [2,0,1])
    plt.imshow(cb_sag[300])
    tiff.imsave('/jukebox/wang/jduva/fullSized_to_segmented/fullsz_CLAHE/segmented_saggital_4ximmult_2xclahe_4xOBJ.tif', cb_sag)
    

    # max projection function for visualization purposes when necessary
    #IM_MAX = np.max(cb_sag[:], axis=0)
    #plt.imsave('/jukebox/wang/jduva/ALL DESKTOP/fullSized_to_segmented/fullsz_noCLAHE/resclaedClAHEd', IM_MAX)
    
