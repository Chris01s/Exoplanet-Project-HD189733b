from astropy.io import fits
import numpy as np
import h5py

##Get filepath as string
propath = "/home/chris/Documents/Exoplanet_Research/HD189733/pro_path/"
filepaths = {'blue': propath+"blue/red_science_blue",
	     'redl': propath+"redl/red_science_redl",
	     'redu': propath+"redu/red_science_redu"}


for arm in ('blue','redl','redu'):

	##get initial spectrum
	head = fits.getheader(filepaths[arm]+str(0)+".fits")
	spectra = fits.getdata(filepaths[arm]+str(0)+".fits")
	if arm == 'redu':
		spectra = spectra[1:]
	
	#other values
	wavelength = head['CRVAL1']
	wav_uncert = head['CRDER1']
	cdelt1 = head['CDELT1']
	time = [head['MJD-OBS']]
	length = head['NAXIS1']
	seeing = [head['ESO TEL IA FWHM']]
	int_time = [head["EXPTIME"]]

	#average airmass readings over the length of the exposure
	airmass_start = head["ESO TEL AIRM START"]
	airmass_end = head["ESO TEL AIRM END"]
	av_airm = (airmass_start + airmass_end)/2
	airmass = [av_airm]
	
	##stack subsequent spectra
	for i in range(1,244):
		head = fits.getheader(filepaths[arm]+str(i)+".fits")
		data = fits.getdata(filepaths[arm]+str(i)+".fits")
		#start time
		time.append(head['MJD-OBS'])
		#seeing
		seeing.append(head['ESO TEL IA FWHM'])
		#integration time
		int_time.append(head["EXPTIME"])
		#airmass
		airmass_start = head["ESO TEL AIRM START"]
		airmass_end = head["ESO TEL AIRM END"]
		av_airm = (airmass_start + airmass_end)/2
		airmass.append(av_airm)
		#combine the spectra
		spectra = np.vstack((spectra,data))
	
	##CREATE HDF5 DATA STRUCTURE
	f = h5py.File(arm+"_data.hdf5",'w')
	f["Spectra"] = spectra
	f["Time"] = np.array(time)
	f["wavelength"] = wavelength + np.arange(length)*cdelt1
	f["seeing"] = np.array(seeing)
	f["airmass"] = np.array(airmass)
	f["int_time"] = np.array(int_time)
	f.close()
	
		
	#MEDIAN DIVIDE
	spectra = spectra.T/np.median(spectra,axis=1)
	spectra = spectra.T
	
	##CREATE HDF5 DATA STRUCTURE
	f = h5py.File(arm+"_data_medidiv.hdf5",'w')
	f["Spectra"] = spectra
	f["Time"] = np.array(time)
	f["wavelength"] = wavelength + np.arange(length)*cdelt1
	f["seeing"] = np.array(seeing)
	f["airmass"] = np.array(airmass)
	f["int_time"] = np.array(int_time)
	f.close()
