# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 19:38:32 2025

@author: istahilissa
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import periodogram



Fs = 50  # sampling frequency = 50 Hz
Vstep = (3.3/(65536-1))*1000
gain=1
acc_x = []
acc_y = []
acc_z = []
gyro_x = []
gyro_y = []
gyro_z = []

with open ('imu_walk_swayl4.csv',mode='r') as file:
     
     csv_reader = csv.reader(file)
     acc_x = np.array(acc_x)
     acc_y = np.array(acc_y)
     acc_z = np.array(acc_z)
     gyro_x = np.array(gyro_x)
     gyro_y = np.array(gyro_y)
     gyro_z = np.array(gyro_z)
     
     next(csv_reader, None)
     
     for row in csv_reader:
         acc_x=np.append(acc_x,float(row[0]))
         acc_y=np.append(acc_y,float(row[1]))
         acc_z=np.append(acc_z,float(row[2]))
         gyro_x=np.append(gyro_x,float(row[3]))
         gyro_y=np.append(gyro_y,float(row[4]))
         gyro_z=np.append(gyro_z,float(row[5]))




N = len(acc_x) #længden af mine samples
time = np.arange(N) / Fs

plt.plot(time, acc_x, label="acc_x")
plt.plot(time, acc_y, label="acc_y")
plt.plot(time, acc_z, label="acc_z")
plt.xlabel("Time ")
plt.ylabel("Acceleration")
plt.title("Accelerometer data RAW")
plt.legend()
plt.grid()
plt.show()

plt.plot(time, gyro_x, label="gyro_x")
plt.plot(time, gyro_y, label="gyro_y")
plt.plot(time, gyro_z, label="gyro_z")
plt.xlabel("Time ")
plt.ylabel("Gyroscope")
plt.title("Gyroscope data RAW")
plt.legend()
plt.grid()
plt.show()

#fjerner offset
acc_x = acc_x - np.mean(acc_x)
acc_y = acc_y - np.mean(acc_y)
acc_z = acc_z - np.mean(acc_z)


# Skær tid fra i starten(sletter de første 2.5 sekunder)
start1 = 0
slut1 = 3

start_index = int(start1 * Fs)
slut_index = int(slut1 * Fs)

acc_x = np.delete(acc_x, range(start_index, slut_index))
acc_y = np.delete(acc_y, range(start_index, slut_index))
acc_z = np.delete(acc_z, range(start_index, slut_index))
gyro_x = np.delete(gyro_x, range(start_index, slut_index))
gyro_y = np.delete(gyro_y, range(start_index, slut_index))
gyro_z = np.delete(gyro_z, range(start_index, slut_index))
time = np.delete(time, range(start_index, slut_index))

#konvertere til mv
acc_x = acc_x * Vstep
acc_y = acc_y * Vstep
acc_z = acc_z * Vstep
gyro_x = gyro_x * Vstep
gyro_y = gyro_y * Vstep
gyro_z = gyro_z * Vstep

# Plot i mV
plt.plot(time, acc_x, label="acc_x")
plt.plot(time, acc_y, label="acc_y")
plt.plot(time, acc_z, label="acc_z")
plt.xlabel("Time ")
plt.ylabel("mV")
plt.title("Accelerometer data ")
plt.legend()
plt.grid()
plt.show()

plt.plot(time, gyro_x, label="gyro_x")
plt.plot(time, gyro_y, label="gyro_y")
plt.plot(time, gyro_z, label="gyro_z")
plt.xlabel("Time ")
plt.ylabel("mV")
plt.title("Gyroscope data")
plt.legend()
plt.grid()
plt.show()


# ACC
length_periodogram = N #finder frekvensområdet som PSD kan beregne
f, pxx = periodogram(acc_x, fs=Fs, window='boxcar', nfft=length_periodogram, scaling='density')
f2, pxx2 = periodogram(acc_y, fs=Fs, window='boxcar', nfft=length_periodogram, scaling='density')
f3, pxx3 = periodogram(acc_z, fs=Fs, window='boxcar', nfft=length_periodogram, scaling='density')

#Gyro
f4, pxx4 = periodogram(gyro_x, fs=Fs, window='boxcar', nfft=length_periodogram, scaling='density')
f5, pxx5 = periodogram(gyro_y, fs=Fs, window='boxcar', nfft=length_periodogram, scaling='density')
f6, pxx6 = periodogram(gyro_z, fs=Fs, window='boxcar', nfft=length_periodogram, scaling='density')



#Plotting - #'PSD_unfilteredACC'
plt.plot(f, pxx,label="acc_x")
plt.plot(f2, pxx2,label="acc_y")
plt.plot(f3, pxx3,label="acc_z")
plt.xlabel('frequency (Hz)')
plt.ylabel('power')
plt.title('power spectral analysis -  ACC')
plt.show()

#Gyro
plt.plot(f4, pxx4,label="gyro_x")
plt.plot(f5, pxx5,label="gyro_y")
plt.plot(f6, pxx6,label="gyro_z")
plt.xlabel('frequency (Hz)')
plt.ylabel('power')
plt.title('power spectral analysis - GYRO')
plt.show()

