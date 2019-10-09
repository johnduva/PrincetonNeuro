#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:10:52 2019

@author: 
@author: John D'Uva (Wang Lab, Princeton University)



"""
#%%
import zipfile, os

# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dirName):
    '''
     Parameters
    ---------
    dir_name: str
        file path of the outer-most directory that you want to compress
    
    Returns
    --------
    a str array of all file paths within 'dir_name',(the main directory that is specified when function is invoked)
    """ 
    '''
    # setup file paths variable
    filePaths = []
   
    # walk through all directories, subdirectories, and files
    for root, directories, files in os.walk(dirName):
        for filename in sorted(files):
            # Create the full filepath by using os module.
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
     
    # return all paths
    return filePaths

#%% assign the name of the directory to zip
dir_name = 'the parent directory'
# call the function to retrieve all files 'dir_name'
filePaths = retrieve_file_paths(dir_name)

print('The following list of files will be zipped:')
for fileName in filePaths:
    print(fileName)
 
# writing files to a zipfile
zip_file = zipfile.ZipFile(dir_name+'.zip', 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
with zip_file:
# writing each file one by one, uncomment the last line to remove each file after it is zipped
    for file in filePaths:
        zip_file.write(file)
        print(file)
        print()
        #os.remove(file)
print()
print(dir_name+'.zip file is created successfully!')
#os.rmdir(dir_name)    #uncomment this line to remove the parent directory upon compression completion
