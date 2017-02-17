#!/usr/bin/python

# remember to change path delimiter!!!

import sys   	
import os	
import time	

from PIL import Image
from PIL.ExifTags import TAGS

# return specific field from image metadata
def get_field (exif,field) :
  for (k,v) in exif.iteritems():
     if TAGS.get(k) == field:
        return v

# make sure we have 3 arguments
if len(sys.argv) < 3 :		
    print ("format: extract_date <name> <dir>")
    exit(1)

outfilename = sys.argv[1] + "_date_times.csv"
errfilename = sys.argv[1] + "_errfile.txt"
basedir = sys.argv[2]

# open the output file
outfile = open(outfilename,'w')		
errfile = open(errfilename,'w')		

# column headers
outfile.write("site,roll,filename,exif-datetime,filedatetime\n")

# recurse through all subdirectories looking for files
for dirname, dirnames, filenames in os.walk(basedir):

    #  path to all files within the base ## whichever directory in ## directory
    for filename in filenames:
        fileLoc = os.path.join(dirname, filename)	

        # check that the file is .JPG
	rhs=""
	if "." in filename:	
            lhs, rhs = filename.split(".",1)
	if (rhs=="JPG"):
		
            # parse apart the directory names
	    dirparts = dirname.split("/")
            dirpartslen = len(dirparts)
           
	    site = ""  
            roll = ""
            if "_" in dirparts[dirpartslen-1]:		
	        site, roll = dirparts[dirpartslen-1].split("_",1)	  
	    if "_" in dirparts[dirpartslen-1]:
		site, roll = dirparts[dirpartslen-1].split("_",1)
            if (len(roll)<2 or roll[0] != "R" or not ((roll[1:]).isdigit())):
                errfile.write("Error in file name: " + fileLoc + "\n")
            
            # open the image file
            try:
                img = Image.open(fileLoc)
            except IOError:
                errfile.write("Cannot open file: " + fileLoc + "\n")
            else:
                exif = img._getexif()
 
                # deal with empty exif
                if (exif==None):
                    errfile.write("No EXIF data: " + fileLoc + "\n")
                    #outfile.write(site+","+roll+","+filename+",")
                else:

                    # extract date info
                    imgDate = get_field(exif,'DateTime')
                    #imgDTorig = get_field(exif,'DateTimeOriginal')
                    #imgDTdig = get_field(exif,'DateTimeDigitized')

                    # check for the rare blank
                    if imgDate=="" or imgDate==None:
                        errfile.write("Blank EXIF data: " + fileLoc + "\n")

                    else:
                        # write to file
                        ltw = (site+","+roll+","+filename+","+imgDate)
                        outfile.write(ltw)

                    # get file creation date info
                    s = os.stat(fileLoc)
                    file_time = s[8]
                    cdate = time.strftime("%Y:%m:%d %H:%M:%S", time.gmtime(file_time))
                    outfile.write(","+cdate+"\n")

        else:
            errfile.write("Not a JPG: " + fileLoc + "\n")


# close file
outfile.close()
errfile.close()