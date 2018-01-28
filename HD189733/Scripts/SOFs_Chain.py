from astropy.io import fits
from astropy.table import Table
import os
import numpy as np


#create directories to store data if they do not exist
os.system("mkdir -p /home/chris/Documents/Exoplanet_Research/sofs/")
os.system("mkdir -p /home/chris/Documents/Exoplanet_Research/reduced_data/RED/")
os.system("mkdir -p /home/chris/Documents/Exoplanet_Research/reduced_data/BLUE/")
sofs = "/home/chris/Documents/Exoplanet_Research/sofs/"
reduced_data = "/home/chris/Documents/Exoplanet_Research/reduced_data/"

##run categoriser and get data
os.system("python FitsCatg.py")
hdulist = fits.open('HD189733.fits')
tbdata = hdulist[1].data
hdulist.close()


for arm in ['BLUE','RED']:

	sci_indices = np.where((tbdata['Category']=='SCIENCE')&(tbdata['Arm']==arm))[0]
	
	for i,sci_index in enumerate(sci_indices):
		#Get locations for the calib frames and science frames
		bias_index = np.where((tbdata['Type']=='BIAS') & (tbdata['Arm']==arm))[0]
		flat_index = np.where((tbdata['Type']=='LAMP,FLAT')&(tbdata['Arm']==arm))[0]
		fmtchk_index = np.where((tbdata['Type']=='LAMP,FMTCHK')&(tbdata['Arm']==arm))[0]
		ordDef_index = np.where((tbdata['Type']=='LAMP,ORDERDEF')&(tbdata['Arm']==arm))[0]
		arcLamp_index = np.where((tbdata['Type']=='LAMP,WAVE')&(tbdata['Arm']==arm))[0]
		lineref_index = np.where((tbdata['Type']=='LINE_REFER_TABLE'))[0]
		extCoeff_index = np.where(tbdata.Type=='EXTCOEFF_TABLE')[0]
	
		#create a list of all the corresponding filenames to 
		#be put into sof files
		Filenames = ['BIAS_'+arm for index in bias_index] +\
						['FLAT_'+arm for index in flat_index] +\
						['ARC_LAMP_FORM_'+arm for index in fmtchk_index] +\
						['ORDER_FLAT_'+arm for index in ordDef_index] +\
						['ARC_LAMP_'+arm for index in arcLamp_index] +\
						['SCIENCE_'+arm] + ['LINE_REFER_TABLE'] + ['EXTCOEFF_TABLE']

		#retrieve all file paths for the 
		#corresponding sets of indices above and make a list of them
		#to be put into uves sof files
		Filepaths = list(tbdata['File_path'][bias_index]) +\
						list(tbdata['File_path'][flat_index]) +\
						list(tbdata['File_path'][fmtchk_index]) +\
						list(tbdata['File_path'][ordDef_index]) +\
						list(tbdata['File_path'][arcLamp_index]) +\
						[tbdata['File_path'][sci_index]] +\
						list(tbdata['File_path'][lineref_index]) +\
						list(tbdata['File_path'][extCoeff_index])
	
		#create sof	
		SOF = Table([Filepaths, Filenames])
		SOF.write("uves_obs_redchain%d_%s.sof"%(i,arm),format="ascii.no_header")

		#run the reduction chain
		os.system("esorex uves_obs_redchain uves_obs_redchain%d_%s.sof"%(i,arm))
		os.system("mv *.sof "+sofs)
		os.system("mv *.fits "reduced_data+arm+"/")
		print "Chain Completed"

	 
   	
   	
   	
   			
						
						

