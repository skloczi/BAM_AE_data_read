# -*- coding: utf-8 -*-
"""
Created on Tue May 30 16:22:16 2023

@author: asklodow

Code to read *.pridb data recorded via Vallen system
"""

#%% importing libraries

import vallenae as vae
import os
import fnmatch
import matplotlib.pyplot as plt

#%% importing data

path = r'C:\Users\asklodow\Desktop\AE\Sensor_callibration\20230526_sensor_callibration_test'    # defining path

# extracting parametric data file 
for file in os.listdir(path):
    if fnmatch.fnmatch(file, '*.pridb'):
        data_file = file
        print(data_file)
file_path = path + "/" + data_file
pridb = vae.io.PriDatabase(file_path)  
df = pridb.read_hits()  # save all hits to pandas dataframe

df[["time", "channel", "trai"]] 

#%% extracting wave traces

for file in os.listdir(path):
    if fnmatch.fnmatch(file, '*.tradb'):
        data_file = file
        print(data_file)
file_path = path + "/" + data_file
trace = vae.io.TraDatabase(file_path)

kk = trace.read_wave(63471)

fig, ax = plt.subplots()
ax.plot(kk[1], kk[0])
ax.set_xlim(-0.00005, 0.00005)