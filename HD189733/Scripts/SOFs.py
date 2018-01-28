from astropy.io import fits
from astropy.table import Table
import numpy as np

pro_path = "/home/chris/Documents/Exoplanet_Research/HD189733/pro_path/"


def uves_cal_mbias(tbdata,arm):
	'''tbdata = data from the fits table
	arm = which arm was used
	function will produce a set of frames for the master bias recipe'''
	
	#Get locations for the BIAS frames
	index = np.where((tbdata['Type']=='BIAS') & (tbdata['Arm']==arm))[0]
	
	#Use the indices to get the corresponding file_paths and their Types
	Filepaths = tbdata['File_path'][index]
	Filenames = ['BIAS_'+arm for i in index]
	
	#Make a set of BIAS frames using the above
	SOF = Table([Filepaths, Filenames])
	SOF.write("uves_cal_mbias_"+arm+".sof",format="ascii.no_header")




def uves_cal_predict(tbdata,arm):
	'''tbdata = data from the fits table
	arm = which arm was used'''

	#Get locations for the formatcheck frames and line ref. table
	fmtchk_index = np.where((tbdata['Type']=='LAMP,FMTCHK')&(tbdata['Arm']==arm))[0]
	lineref_index = np.where((tbdata['Type']=='LINE_REFER_TABLE'))[0]
	
	#Use the indices to get the corresponding file_paths and their Types
	Filepaths = list(tbdata['File_path'][fmtchk_index]) +\
					list(tbdata['File_path'][lineref_index])
	Filenames = ['ARC_LAMP_FORM_'+arm for index in fmtchk_index] + ['LINE_REFER_TABLE']
	
	#Get location of master bias frames
	if arm=='BLUE':
		mBIAS = ["masterbias_blue.fits"]
		Filenames += ['MASTER_BIAS_BLUE']
		Filepaths += mBIAS
	else:
		mBIAS = ["masterbias_redl.fits","masterbias_redu.fits"]
		mFORML_index = np.where(tbdata['Type'] == 'MASTER_FORM_REDL')[0]
		mFORML = list(tbdata['File_path'][mFORML_index])
		mFORMU_index = np.where(tbdata['Type'] == 'MASTER_FORM_REDU')[0]
		mFORMU = list(tbdata['File_path'][mFORMU_index])
		Filepaths += mBIAS + mFORML + mFORMU
		Filenames += ['MASTER_BIAS_REDL','MASTER_BIAS_REDU','MASTER_FORM_REDL','MASTER_FORM_REDU']
	
	#Make a set of frames using the above
	SOF = Table([Filepaths, Filenames])
	SOF.write("uves_cal_predict"+arm+".sof",format="ascii.no_header")




def uves_cal_orderpos(tbdata,arm):
	'''tbdata = data from the fits table
	arm = which arm was used'''
	
	#Get locations for the BIAS frames
	ordDef_index = np.where((tbdata['Type']=='LAMP,ORDERDEF')&(tbdata['Arm']==arm))[0]
	
	#Use the indices to get the corresponding file_paths and their Types
	Filepaths = list(tbdata['File_path'][ordDef_index])
	Filenames = ['ORDER_FLAT_'+arm for index in ordDef_index]
	
	#Get location of master bias frames
	if arm=='BLUE':
		mBIAS = ["masterbias_blue.fits"]
		orderGUESS = ["orderguesstable_blue.fits"]
		Filenames += ['ORDER_GUESS_TAB_BLUE','MASTER_BIAS_BLUE']
	else:
		mBIAS = ["masterbias_redl.fits","masterbias_redu.fits"]	
		orderGUESS = ["orderguesstable_redl.fits","orderguesstable_redu.fits"]				
		Filenames += ['ORDER_GUESS_TAB_REDL','ORDER_GUESS_TAB_REDU','MASTER_BIAS_REDL','MASTER_BIAS_REDU']
	
	Filepaths += orderGUESS + mBIAS	
	#Make a set of BIAS frames using the above
	SOF = Table([Filepaths, Filenames])
	SOF.write("uves_cal_orderpos"+arm+".sof",format="ascii.no_header")




def uves_cal_mflat(tbdata,arm):
	'''tbdata = data from the fits table
	arm = which arm was used'''

	#Get locations for the BIAS frames
	Flat_index = np.where((tbdata['Type']=='LAMP,FLAT')&(tbdata['Arm']==arm))[0]

	#Use the indices to get the corresponding file_paths and their Types
	Filepaths = list(tbdata['File_path'][Flat_index])
	Filenames = ['FLAT_'+arm for index in Flat_index]

	if arm=='BLUE':
		mBIAS = ["masterbias_blue.fits"]
		orderTABLE = ['ordertable_blue.fits']
		Filenames += ['MASTER_BIAS_BLUE','ORDER_TABLE_BLUE']
	else:
		mBIAS = ["masterbias_redl.fits",
					"masterbias_redu.fits"]
			
		orderTABLE = ['ordertable_redl.fits',
							'ordertable_redu.fits']
					
		Filenames += ['MASTER_BIAS_REDL','MASTER_BIAS_REDU',
							'ORDER_TABLE_REDL','ORDER_TABLE_REDU']

	Filepaths += mBIAS + orderTABLE
	#Make a set of BIAS frames using the above
	SOF = Table([Filepaths, Filenames])
	SOF.write("uves_cal_mflat"+arm+".sof",format="ascii.no_header")




def uves_cal_wavecal(tbdata,arm):
	#get indices for arc lamps and line reference table
	arcLamp_index = np.where((tbdata['Type']=='LAMP,WAVE')&(tbdata['Arm']==arm))[0]
	lineref_index = np.where((tbdata['Type']=='LINE_REFER_TABLE'))[0]
	lineintmon_index = np.where((tbdata['Type']=='LINE_INTMON_TABLE'))[0]

	#get corresponding file paths andcreate list of file names
	Filepaths = list(tbdata['File_path'][arcLamp_index]) 
	Filenames = ['ARC_LAMP_'+arm for index in arcLamp_index]
	lineREFER = list(tbdata['File_path'][lineref_index])
	lineINTMON = list(tbdata['File_path'][lineintmon_index])

	#obtain the master calibration files according to their chip
	if arm=='BLUE':
		orderTABLE = ['ordertable_blue.fits']
		lineGUESS = ['lineguesstable_blue.fits']
		mBIAS = ["masterbias_blue.fits"]
		mFLAT = ['masterflat_blue.fits']
		
		Filenames += ['ORDER_TABLE_'+arm, 'LINE_GUESS_TAB_'+arm,
							'LINE_REFER_TABLE', 'LINE_INTMON_TABLE',
							'MASTER_BIAS_'+arm,'MASTER_FLAT_'+arm]
	else:
		orderTABLE = ['ordertable_redl.fits',
						  'ordertable_redu.fits']
	
		lineGUESS = ['lineguesstable_redl.fits',
						 'lineguesstable_redu.fits']
		
		mBIAS = ["masterbias_redl.fits",
					"masterbias_redu.fits"]
		
		mFLAT = ['masterflat_redl.fits',
					'masterflat_redu.fits']
					
		Filenames += ['ORDER_TABLE_'+arm+'L','ORDER_TABLE_'+arm+'U',
							'LINE_GUESS_TAB_'+arm+'L','LINE_GUESS_TAB_'+arm+'U',
							'LINE_REFER_TABLE', 'LINE_INTMON_TABLE',
							'MASTER_BIAS_'+arm+'L','MASTER_BIAS_'+arm+'U',
							'MASTER_FLAT_'+arm+'L','MASTER_FLAT_'+arm+'U']
						
	Filepaths += orderTABLE + lineGUESS + lineREFER + lineINTMON + mBIAS + mFLAT

	SOF = Table([Filepaths, Filenames])
	SOF.write("uves_cal_wavecal"+arm+".sof", format="ascii.no_header")





def uves_obs_scired(tbdata,arm,sci_index,extCoeff_file):

	#Need to make seperate sof for each science frame
	Filepaths = [tbdata['File_path'][sci_index]]

	if arm=='BLUE':
		orderTABLE = [pro_path+'ordertable_blue.fits']
		lineGUESS = [pro_path+'lineguesstable_blue.fits']
		mBIAS = [pro_path+"masterbias_blue.fits"]
		mFLAT = [pro_path+'masterflat_blue.fits']
		lineTABLE = [pro_path+'linetable_blue.fits']
		mresp_index = np.where(tbdata['Type']=='MASTER_RESPONSE_BLUE')
		mresp = [tbdata['File_path'][mresp_index][0]]
	
		Filenames = ['SCIENCE_'+arm, 'ORDER_TABLE_'+arm,'LINE_TABLE_'+arm,
						'MASTER_BIAS_'+arm,'MASTER_FLAT_'+arm,
						'EXTCOEFF_TABLE','MASTER_RESPONSE_BLUE']
					
		Filepaths += orderTABLE + lineTABLE + mBIAS + mFLAT + extCoeff_file + mresp
	else:
		orderTABLE = [pro_path+'ordertable_redl.fits',
						  pro_path+'ordertable_redu.fits']
						  
		lineGUESS = [pro_path+'lineguesstable_redl.fits',
						 pro_path+'lineguesstable_redu.fits']

		mBIAS = [pro_path+"masterbias_redl.fits",
					pro_path+"masterbias_redu.fits"]

		mFLAT = [pro_path+'masterflat_redl.fits',
					pro_path+'masterflat_redu.fits']
	
		lineTABLE = [pro_path+'linetable_redl.fits',
						 pro_path+'linetable_redu.fits']
	
		mrespLOWER_index = np.where(tbdata['Type']=='MASTER_RESPONSE_REDL')
		mrespUPPER_index = np.where(tbdata['Type']=='MASTER_RESPONSE_REDU') 
		mrespLOWER = [tbdata['File_path'][mrespLOWER_index][0]]
		mrespUPPER = [tbdata['File_path'][mrespUPPER_index][0]]  
		 				
		Filenames = ['SCIENCE_'+arm, 'ORDER_TABLE_'+arm+'L','ORDER_TABLE_'+arm+'U',
						'LINE_TABLE_'+arm+'L','LINE_TABLE_'+arm+'U','MASTER_BIAS_'+arm+'L',
						'MASTER_BIAS_'+arm+'U','MASTER_FLAT_'+arm+'L','MASTER_FLAT_'+arm+'U',
						'EXTCOEFF_TABLE','MASTER_RESPONSE_REDL','MASTER_RESPONSE_REDU']
						
		Filepaths += orderTABLE + lineTABLE + mBIAS + mFLAT + extCoeff_file + mrespLOWER + mrespUPPER

	SOF = Table([Filepaths, Filenames])
	SOF.write("uves_obs_scired"+arm+".sof", format="ascii.no_header")



