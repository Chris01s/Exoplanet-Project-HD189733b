#!/bin/bash

python Spectra.py 
python Spectra_fluxcal.py

mv *data.hdf5 red_Spectra
mv *data_medidiv.hdf5 med_div_Spectra/
mv *data_fluxcal.hdf5 fluxcal/
mv *data_fluxcal_med*.hdf5 fluxcal_med_div/

