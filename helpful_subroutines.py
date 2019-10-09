#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 10:27:08 2019

@author: wanglab
"""

#%% if directory doesn't exist, create it and save as 'dst'
import os
import matplotlib.pyplot as plt

path = 'the desired filepath (whether it exists or not) ending with a backslash'
if not os.path.isdir(path):
    os.mkdir(path)
dst = os.path.join(path + str(i) + '.tif' )
print(dst) #check if dst is correct
plt.imsave(dst, IM_MAX, cmap='bone')


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


#%% From 'Full Size Data' format to 'Tiff Stack' format (takes ~2 min to load into ImageJ)
import os
import tifffile as tiff
import numpy as np

# Uncomment if walking through a directory of numbered brains
#for i in range(0,25):
#    if i<10 and os.path.isdir('/home/wanglab/mounts/wang/pisano/tracing_output/eaat4/an0'+str(i)+'_eaat4_031919'):
#        path = os.path.join('/home/wanglab/mounts/wang/pisano/tracing_output/eaat4/an0' + str(i) + '_eaat4_031919/full_sizedatafld/an' + str(i) + '_eaat4_031919_1d3x_647_017na_1hfds_z10um_150msec_ch00')
#        
#    elif i>=10 and os.path.isdir('/home/wanglab/mounts/wang/pisano/tracing_output/eaat4/an'+str(i)+'_eaat4_031919'):
#        path = os.path.join('/home/wanglab/mounts/wang/pisano/tracing_output/eaat4/an' + str(i) + '_eaat4_031919/full_sizedatafld/an' + str(i) + '_eaat4_031919_1d3x_647_017na_1hfds_z10um_150msec_ch00')
    
path= '/home/wanglab/mounts/wang/pisano/tracing_output/aav/20171130_pcp2_dcn02_4x/full_sizedatafld_old/20171130_pcp2_dcn02_488_050na_1hfds_z7d5um_50msec_10povlp_ch00'
zPlanes = sorted(os.listdir(path))
array = []

for i, fls in enumerate(zPlanes):
    wholePath = os.path.join(path, fls)
    img = tiff.imread(wholePath)
    array.append(img)
    print("Processing plane: "+ str(i))
print("Processing Complete")    
stack = np.array(array)
tiff.imsave('/home/wanglab/Desktop/aavMAXIPS/FSDoutput488.tif', stack)

#Uncomment if walking through a directory of numbered brains
#if "an"+str(i) in path:
#    tiff.imsave('/home/wanglab/Desktop/3D_CLAHE/an'+str(i)+ 'FSDtoTIFF.tiff', stack)
#elif "an0"+str(i) in path:
#    tiff.imsave('/home/wanglab/Desktop/3D_CLAHE/an0'+str(i)+ 'FSDtoTIFF.tiff', stack)


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


#%% Crop and rotate
from skimage.external import tifffile
import matplotlib.pyplot as plt
import numpy as np

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
plt.imshow(max_cb)

#export as tif
tifffile.imsave("/home/wanglab/Desktop/jduva_PA_views/an21PA.tif", max_cb)


#%% File Compression
import zipfile, os

# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dirName):
 
  # setup file paths variable
  filePaths = []
   
  # Read all directory, subdirectories and file lists
  for root, directories, files in os.walk(dirName):
    for filename in sorted(files):
        # Create the full filepath by using os module.
        filePath = os.path.join(root, filename)
        filePaths.append(filePath)
         
  # return all paths
  return filePaths

# Assign the name of the directory to zip
dir_name = '/home/wanglab/Desktop/zip_test/161026_rat_ctx_1dot3x_w4xzoom_z10um_488_647_200msec_fullna_19-08-01'
# Call the function to retrieve all files and folders of the assigned directory
filePaths = retrieve_file_paths(dir_name)

  
# printing the list of all files to be zipped
print('The following list of files will be zipped:')
for fileName in filePaths:
    print(fileName)
 
# writing files to a zipfile
zip_file = zipfile.ZipFile(dir_name+'.zip', 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
with zip_file:
# writing each file one by one
    for file in filePaths:
        zip_file.write(file)
        print(file)
        os.remove(file)
print()
print(dir_name+'.zip file is created successfully!')
os.rmdir(dir_name)