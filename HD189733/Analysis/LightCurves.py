import numpy as np
import matplotlib.pyplot as plt
import h5py
import Get_data

#get the data first from straight reduced spectra
X = data_reduce["Spectra"][:]
wav = data_reduce["wavelength"][:]
t = data_reduce["Time"][:]
seeing = data_reduce["seeing"][:]
airmass = data_reduce["airmass"][:]
integration_time = data_reduce["int_time"][:]

#inspect the data data around the na doublet
#focus around the doublet D_1 line: around 5890Angstrom
wav0 = 5890.0
delta_wav = 3.0
a = wav0-0.5*delta_wav
b = wav0+0.5*delta_wav

#get central flux
f_mid = np.sum(X[:,(wav>=a)*(wav<=b)],axis=1)
#and left and right spectral bands
a = wav0 - 1.5*delta_wav
b = wav0 - 0.5*delta_wav
f_left = np.sum(X[:,(wav >= a)*(wav <= b)],axis=1)
a = wav0 + 1.5*delta_wav
b = wav0 + 0.5*delta_wav
f_right = np.sum(X[:,(wav>=a)*(wav<=b)],axis=1)

#total flux: mid/avg(left + right)
f_line = 2*f_mid/(f_left + f_right)

plt.plot(t,f_line,'.')
plt.show()

