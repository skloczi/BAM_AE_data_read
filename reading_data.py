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
import seaborn as sns
import pandas as pd

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



#%% extracting labels and TRAIs


kk = pd.read_excel(r'C:\Users\asklodow\Desktop\AE\Sensor_callibration\20230526_sensor_callibration_test/PLB_test.xlsx', index_col= None )

headers = kk.columns.values

ids = headers[0]
trais = headers[-1]
label = headers[1]

trais_dict = {}
keys = []

rows = 0
while rows < len(kk)-1:
    if kk.iloc[rows][ids] == "La" and kk.iloc[rows+1][ids] == "Ht":
        name = kk.iloc[rows][label].split(" ")      
        key = name[-1]
        keys.append(key)
        values = []
        rows += 1
    
    if kk.iloc[rows][ids] == "Ht":
        values.append(kk.iloc[rows][trais])
        trais_dict[f'{key}'] = values
        
    rows += 1
        
#%% redefining the dictionary
data_dict = {}

pp = 0
for keys, values in trais_dict.items():
    sensor_angle = keys.split("_")
    angle = sensor_angle[1] 
    if pp == 0:
        sensor = sensor_angle[0]       
        data_dict[f"{sensor}"] = {angle: values} 
        pp = 1
    else:     
        if sensor == sensor_angle[0]:
            data_dict[f"{sensor}"][f'{angle}'] = values
        else:
            sensor = sensor_angle[0]
            data_dict[f"{sensor}"] = {angle: values} 


#%% Creating the dataframe
lol = []
for sensors, angles in data_dict.items():
    for angle, values in angles.items():
        print(sensors, angle, values)
        for value in values:
            amplitude = hit_df[hit_df["trai"] == value]
            ampl = amplitude.loc[amplitude.index[0]]["amplitude"]
            lol.append([sensors, angle, ampl, value])
new_df = pd.DataFrame(lol, columns = ['Sensor', 'Angle', 'Amplitude', 'Trai'])

# plotting the data
fig, ax = plt.subplots(figsize = (15,5))
sns.boxplot(new_df, x = 'Angle', y = 'Amplitude', hue = 'Sensor')








