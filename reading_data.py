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

# defining the hits threshold
db_threshold = 89
volt_threshold = 10**(db_threshold /20) * 10**-6

hit_df = df[df["amplitude"] > volt_threshold]
print(hit_df)

# plotting hits amplitudes above threshold
fig, ax = plt.subplots()
ax.scatter(hit_df.trai, hit_df.amplitude)
ax.set_xlabel("Trai")
ax.set_ylabel("Amplitude [mV]")
ax.set_title(f"Hits above {db_threshold} dB amplitude threshold")

#%% extracting wave traces

for file in os.listdir(path):
    if fnmatch.fnmatch(file, '*.tradb'):
        data_file = file
        print(data_file)
file_path = path + "/" + data_file
trace = vae.io.TraDatabase(file_path)

trai = 62393
waveform = trace.read_wave(trai)

fig, ax = plt.subplots()
ax.plot(waveform[1], waveform[0])
ax.set_xlabel("time [ms]")
ax.set_ylabel("amplitude [mV]")
ax.set_title(f"waveform hit #trai {trai}")
