#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 13:07:12 2019

@author: John D'Uva (Wang Lab, Princeton University)

Recursively retrieve deleted files by looping through each directory's .snapshot from a desired date/time.

Note: This cannot be done from a local Python/Spyder environment because .snapshot will not be visible

Step 1) You must ssh into the system with the command: ssh <username>@apps.pni.princeton.edu
Step 2) Open a Python environment with the command: python
Step 3) Copy/paste the below code into the environment and execute. Check on the size of the directory to make sure it's increasing.

"""
#%% Function to generate the array of directories to loop through
def retrieve_dir_paths(outer_dir):
    """
    Parameters
    ---------
    outer_dir: str
        file path of the outer-most directory that you want to recover
    
    Returns
    --------
    a str array of all *DIRECTORY* paths within 'outer_dir',(the main directory that is specified when function is invoked)
    """ 
    import os
    dirPaths = []
    # Walk through all directories and subdirectories (ignore 'files', it must be included for 'os.walk' to execute)
    for root, directories, files in os.walk(outer_dir):
        for dirNames in sorted(directories):
            # Create the full dir path by using os module
            dirPath = os.path.join(root, dirNames)
            if dirPath not in dirPaths:
                dirPaths.append(dirPath)
                
    return dirPaths

#%% Set the main directory, call the function, and 'shutil.copy2' each file back to where it belongs
import shutil, os

#Paths (must be set by user)
outer_dir = 'initial parent directory to walk through'
snapshot = '.snapshot/LightSheetData_daily_2019-09-23-_03-30/' #an example of  .snapshot directory

#Retrieve array of all directories within outer_dir
dirPaths = retrieve_dir_paths(outer_dir)

# Loop through the array and copy the files over
num_files=0
for dirPath in dirPaths:
    finalDir = os.path.join(dirPath, snapshot)
    for file in os.listdir(finalDir):
        fullFile = os.path.join(finalDir, file)
        
        try:
            shutil.copy2(fullFile, dirPath)
        except shutil.Error:
            print("File is already here, continuing...")
        else:
            shutil.copy2(fullFile, dirPath)
            print("File copied.")
        finally:
            num_files+=1
            print(num_files)
            
