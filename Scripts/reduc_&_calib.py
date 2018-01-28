from astropy.io import fits
from astropy.table import Table
import numpy as np
import os
import SOFs

os.system("python FitsCatg.py")
hdulist = fits.open('HD189733.fits')
tbdata = hdulist[1].data
hdulist.close()
pro_path = "/home/chris/Documents/Exoplanet_Research/HD189733/pro_path/"

#gain sudo access
os.system('sudo apt-get update')


for arm in ['BLUE','RED']:
	#MASTER BIAS FRAME
	#create master bias sof
	SOFs.uves_cal_mbias(tbdata,arm)
	#run esorex master_bias recipe
	os.system("esorex --check-sof-exist=true uves_cal_mbias uves_cal_mbias_"+arm+".sof")
	 
	#LINE GUESS
	#create line guess sof
	SOFs.uves_cal_predict(tbdata,arm)
	#run esorex line guess recipe
	os.system("esorex --check-sof-exist=true uves_cal_predict uves_cal_predict"+arm+".sof")

	#ORDER TABLE
	#create order table sof
	SOFs.uves_cal_orderpos(tbdata,arm)
	#run esorex order table recipe
	os.system("esorex --check-sof-exist=true uves_cal_orderpos uves_cal_orderpos"+arm+".sof")

	#MASTER FLAT
	#create master_flat sof
	SOFs.uves_cal_mflat(tbdata,arm)
	#run esorex master_flat recipe
	os.system("esorex --check-sof-exist=true uves_cal_mflat uves_cal_mflat"+arm+".sof")

		
	#MASTER WAVELENGTH CALIBRATION
	#create wave_cal sof
	SOFs.uves_cal_wavecal(tbdata,arm)
	#run esorex master_flat recipe
	os.system("esorex --check-sof-exist=true uves_cal_wavecal uves_cal_wavecal"+arm+".sof")

	#move all fits files into product directory
	os.system("./move_fits_files.sh")

	
	#SCIENCE FRAMES
	#get science frames from data table
	sci_indices = np.where((tbdata['Category']=='SCIENCE')&(tbdata['Arm']==arm))[0]

	#Extinction coefficient table and it's file path
	extCoeff_index = np.where(tbdata.Type=='EXTCOEFF_TABLE')[0]
	extCoeff_file = list(tbdata['File_path'][extCoeff_index])

	#for each science frame, create an sof using the calibration files obtained above
	#and run esorex pipeline recipe for science reduction
	for i,sci_index in enumerate(sci_indices):
		SOFs.uves_obs_scired(tbdata,arm,sci_index,extCoeff_file)
		os.system("esorex --check-sof-exist=true uves_obs_scired uves_obs_scired"+arm+'.sof')
		#move all science data to a different directory
		if arm == 'RED':
			os.system('./move_redframes.sh	%d'%(i))
		else:
			os.system('./move_blueframes.sh	%d'%(i))


	
	
	
	 

	 
	 
	 
	 
