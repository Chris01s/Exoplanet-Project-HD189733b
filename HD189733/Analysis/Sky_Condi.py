import numpy as np
import matplotlib.pyplot as plt
import h5py
#import Get_data

#read data
filepath = "/home/chris/Documents/Exoplanet_Research/HD189733/Analysis/"
#uncalibrated
f = "red_Spectra/redl_data.hdf5"
data_reduce = h5py.File(filepath+f)
#flux_calbrated
f = "fluxcal/redl_data_fluxcal.hdf5"
data_fluxcal = h5py.File(filepath+f)

#get the data first from straight reduced spectra
X = data_reduce["Spectra"][:]
wav = data_reduce["wavelength"][:]
t = data_reduce["Time"][:]
seeing = data_reduce["seeing"][:]
airmass = data_reduce["airmass"][:]
integration_time = data_reduce["int_time"][:]

#plot the seeing and airmass on the same graph
#seeing
fig, ax1 = plt.subplots()
ax1.plot(t,seeing,'r.')
ax1.set_xlabel("time (MJD)")
ax1.set_ylabel("Seeing",color='r')
ax1.tick_params('y',colors='r')
#airmass
ax2 = ax1.twinx()
ax2.plot(t,airmass,'b.')
ax2.set_xlabel("Exposure Number")
ax2.set_ylabel("Airmass",color='b')
ax2.tick_params('y',colors='b')
#plot
fig.tight_layout()
plt.show()


#FIT FOR SEEING AND AIRMASS

