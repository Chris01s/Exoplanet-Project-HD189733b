import numpy as np
import matplotlib.pyplot as plt
import h5py

#read data
filepath = "/home/chris/Documents/Exoplanet_Research/HD189733/Analysis/"
#uncalibrated
f = "redl_data.hdf5"
data_reduce = h5py.File(filepath+f)
#flux_calbrated
f = "redl_data_fluxcal.hdf5"
data_fluxcal = h5py.File(filepath+f)
