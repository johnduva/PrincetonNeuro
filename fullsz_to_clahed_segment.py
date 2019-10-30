#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:11:03 2019

@author: John D'Uva (Wang Lab, Prineton University)

Combine each sample's raw data (lightsheet) into a singular binaraized file for pos/neg zebrin banding comparison.

Steps:
1) Combine all indivual fullsize image planes into a single TIFF file (w/ option to save this step)

2) 


"""

import os, cv2
import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
import skimage.exposure as skie
from tools.analysis.analyze_injection import optimize_inj_detect, pool_injections_for_analysis
%matplotlib auto


#%% Step 1:  Combine all indivual fullsize image planes into a single TIFF file (w/ option to save this step)

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

#%% Step 2: Rotate to coronal view, crop out negative space, and apply CLAHE/rescaling filters to each plane 
    
    img = tiff.imread('/home/wanglab/mounts/wang/jduva/ALL DESKTOP/fullSized_to_segmented/fullsz_noCLAHE/an09')
    
    cb_coronal = np.transpose(img, [1,0,2]) # rotate to coronal view
    cropped = cb_coronal[:, 100:, 300:1850] #crop out negative space
#    plt.imshow(cropped[1700]*7)
   
    #create CLAHE function (to be applied to images in Step 2)
    claheFunc = cv2.createCLAHE(clipLimit=2, tileGridSize=(32,32)) 
    # create an array of zeros of the same size as the 3D cerebellum which we will fill with the 2D filtered planes
    final_array = np.zeros(cropped.shape)     
    # apply the filter in a loop over the first axis
    for i in range(1640,2300):#range(final_array.shape[0]): #for all the z planes in (z,y,x):
        clahedImage_i = claheFunc.apply(cropped[i].astype('uint16'))
        rescaled = skie.rescale_intensity(clahedImage_i, in_range=(1, 25000), out_range=(0, 35000))
        final_array[i] = clahedImage_i
#        if i%20 ==0 : print(str(i) + " out of: " + str(len(final_array)))
#    plt.imshow(final_array[1800]*10)
    tiff.imsave('/jukebox/wang/jduva/fullSized_to_segmented/fullsz_CLAHE/clahe632_rescale_25_35.tif', final_array[1640:2300])
    
    
    #%% Step 3: 
    img = tiff.imread('/jukebox/wang/jduva/fullSized_to_segmented/fullsz_CLAHE/clahe32_rescale_25_35.tif')
    print(img.shape)
    plt.imshow(img)
    
    # Function to test detection parameters
    optimize_inj_detect(img, threshold=2.5, filter_kernel=(3,3,3), dst='/jukebox/wang/jduva/fullSized_to_segmented/fullsz_CLAHE/opt_inj_det/2d5_333.tif')
    
    
    kwargs = {'inputlist': inputlist, 
              'filter_kernel': (3,3),
              'threshold': .6,
              'num_sites_to_keep': 1,
              'injectionscale': 45000, 
              'imagescale': 2,
              'dst': '/home/wanglab/Desktop/testing',
              'save_individual': True, 
              'colormap': 'bone', 
              'crop': False,
              'atlas': "/home/wanglab/mounts/LightSheetTransfer/atlas/sagittal_atlas_20um_iso.tif",
              'annotation':"/home/wanglab/mounts/LightSheetTransfer/atlas/annotation_sagittal_atlas_20um_iso.tif",
              'id_table': "/home/wanglab/mounts/LightSheetTransfer/atlas/ls_id_table_w_voxelcounts.xlsx"
            }              
              
    df = pool_injections_for_analysis(**kwargs)
    
    #1640:2300
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    IM_MAX = np.max(final_array[1800:], axis=0)
    plt.imsave('/jukebox/wang/jduva/ALL DESKTOP/fullSized_to_segmented/fullsz_noCLAHE/resclaedClAHEd', IM_MAX)
    
    
    
    
    
    
    
    
    
#    
#    #check the shape of the output files
#    for directory in sorted(os.listdir(output)): 
#    an = directory[0:4]
#    print(an)
#    
#    
    