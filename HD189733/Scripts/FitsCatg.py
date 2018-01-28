from astropy.io import fits #module to deal with fits files
from astropy.table import Table
from glob import glob #module to create a list of all fits files in a directory
from numpy import array,where

def getInfo(header):
    '''Function to obtain essential info from header of the fits file. Pass
    arg as a header, returns info from the header'''

    #if header has DPR TYPE or DPR CATG, we know it is a SCI,CALIB,or ACQUIS
    #frame and we can therefore test whether it "has arms".
    #If not, throw exception and test for STATIC CALIBS or if
    #the file is UNKNOWN.
    try:
        getCatg = header["ESO DPR CATG"]
        getType = header['ESO DPR TYPE']
        getArm = isArm(header)
    except KeyError:
        try:
            getType = header['ESO PRO CATG']
            getCatg = getType
            getArm = isArm(header)
        except KeyError:
            return None
            
    #retrieve date; will not be returned if the funtion returns None
    getDate = header["DATE"]
    getObject = header["OBJECT"]
    return getCatg, getType, getArm, getDate, getObject


def isArm(header):
    '''Function to check if file used ccd chips and to return which arm
    (blue or red) was used '''
    try:
        getArm = header['ESO DET CHIPS']
        getArm = "BLUE" if getArm == 1 else "RED"
    except KeyError:
        getArm ="N/A"
    return getArm
    
    

if __name__ == '__main__':
	#filepath to be piped in from command line/textfile
	#run FitsCatg.bat
	filepath = "/home/chris/Documents/Exoplanet_Research/HD189733/raw_data/*.*fits"
	FILES = glob(filepath)
	FILES.sort()
	#Initialise lists to be populated with header info
	CATGS = []
	ARMS = []
	DATES = []
	TYPES = []
	OBJECT=[]
	UNKNOWN = []

	for FILE in FILES:
		 #Open fits file and get header extension
		 header = fits.getheader(FILE)

		 #Retrieve essential info from header file and delete header
		 Info = getInfo(header)
		 del header
		 #Sort the data into unknowns, sciences, and calibs etc.
		 if Info == None:
		     UNKNOWN.append(FILE)
		 else:
		     Catg, Type, Arm, Date, Object = Info
		     CATGS.append(Catg) 
		     ARMS.append(Arm)
		     DATES.append(Date)
		     TYPES.append(Type)
		     OBJECT.append(Object)

	CATGS = array(CATGS)
	FILES = array(FILES)
	
	t = Table([FILES,CATGS,TYPES,ARMS,DATES,OBJECT],
		       names=('File_path','Category','Type','Arm','Date','Object'))
	t.write('HD189733.fits',format='fits')
	
for unknown in UNKNOWN:
	print unknown
