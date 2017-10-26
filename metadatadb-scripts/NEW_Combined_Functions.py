#!/usr/bin/python

# Imports
import os
import getpass
import datetime
import MySQLdb
import sys
import snapshotDB
import csv
import hashlib
import math
import random
import operator
import shutil
import more_itertools

# Get global variables
#mySqlHost = "mysql.msi.umn.edu"

mySqlHost = "localhost"
mySqlSchema = "packerc_snapshot_serengeti"
msiUserName = raw_input("Please enter your MSI username (x500): ")
dbPasswd = getpass.getpass("Please enter your database password (may be different from your MSI password): ")
seasonNbr = raw_input("Please enter the season number to be analyzed: ")
fullName = raw_input ("Please enter your first and last name (ex. Craig Packer): ")
snapshotFilePath = "/Users/Axl/Desktop/SerengetiPart2/classifications_data/Zooniverse_downloads/snapshot_S"+seasonNbr+".csv"
nonEmptyPath = "/Users/Axl/Desktop/SerengetiPart2/classifications_data/non-blank_captures/snapshot_S"+seasonNbr+"_non_empty.csv"
nonBlankPath = "/Users/Axl/Desktop/SerengetiPart2/classifications_data/non-blank_classifications"
consensusPath = "/Users/Axl/Desktop/SerengetiPart2/data/consensus_classifications"
metadataPath = "/Users/Axl/Desktop/SerengetiPart2/metadata"
classificationsPath = "/Users/Axl/Desktop/SerengetiPart2/classifications_data"
sharedDir = "/Users/Axl/Desktop/SerengetiPart2"
userHashPath = "/Users/Axl/Desktop/SerengetiPart2/data/users/S"+seasonNbr+"_hashes_all_users.csv"
scriptsPath = "/Users/Axl/Desktop/SerengetiPart2/scripts"

# Reduces snapshot file from Zooniverse to only the desired season
def filterSnapshot(snapshotFilePath,outFilePath,seasonNbr):
	with open(snapshotFilePath,'r') as fin, open (outFilePath,'w') as fout:
		writer = csv.writer(fout, delimiter=',')
		for row in csv.reader(fin, delimiter=','):
			if row[6] == 'S'+str(seasonNbr) or row[6] == 'season':
				print row
	#shutil.copy2(snapshotFilePath,snapshotFilePath+"_old")
	#os.rename(outFilePath,snapshotFilePath)

# Function imports clean season metadata file
def importCleanSeasonMetadata(authFilename,seasonFilename,cleanMetadataFileName,outDir):
	# format of the authentication file should be three lines:
	# MSI user name
	# database password
	# full name

	# format of the season file should be one or more comma-separated line(s)
	# with fields:
	# season: integer
	# start date: date in format 'YYYY-MM-DD'
	# end date: date in format 'YYYY-MM-DD'
	# comments: quoted string of up to 500 characters

	# ---

	# format of the clean season metadata file should be:
	# COLUMNS:
	# rownum: integer
	# season: integer
	# site: 3-character alphanumeric
	# roll: integer
	# capture: integer
	# image: integer
	# path: character string
	# newtime: datetime in format 'YYYY-MM-DD HH:MM:SS'
	# oldtime: datetime in format 'YYYY:MM:DD HH:MM:SS'
	# invalid: integer
	# include: 1 for send to Zooniverse, 0 for don't
		# make sure we have 4 arguments
	if len(sys.argv) < 5 :
	    print ("format: import_clean_season_metadata_into_database <authentication file> <season file> <metadata file> <output dir>")
	    exit(1)

	authfilename = sys.argv[1]
	sfilename = sys.argv[2]
	infilename = sys.argv[3]
	outdirname = sys.argv[4]

	with open(authfilename,'rb') as afile:
	    username = afile.readline().strip()
	    password = afile.readline().strip()
	    fullname = afile.readline().strip()


	try:
	    # connect to the database    
	    db = MySQLdb.connect(host=mySqlHost,
	                         user=msiUserName,
	                         passwd=dbPasswd,
	                         db=mySqlSchema,
	                         local_infile = 1)

	    # use the database
	    with db:
	        
	        snapshotDB.cur = db.cursor()

	        print "Validating Season file\n"

	        # add the season information
	        with open(sfilename,'rb') as sfile:

	            # use CSV reader
	            sreader = csv.reader(sfile,delimiter=',',quotechar='"')

	            # usually just 1 file for 1 season, but could handle more
	            for row in sreader:
	              
	                season = row[0]
	                startdate = row[1]
	                enddate = row[2]
	                comments = row[3]

	                # see if this season is already in the DB
	                if not snapshotDB.seasonExists(season):
	                    snapshotDB.addSeason(season,startdate,enddate,comments)
	    
	                    # make a note in the log
	                    snapshotDB.log(fullname,"Added new season " + season)

	        # now the metadata
	        lastseason = "0"
	        lastsite = "0"

	        print "Validating the season and site values in the metadata file\n"
	                
	        # Go through the file once to check seasons and sites
	        # We will not calculate roll start and stop times, as this is easy
	        # to do once the data are loaded, and makes this script cleaner.
	       
	        with open(infilename,'rb') as infile:

	            # use CSV reader
	            freader = csv.reader(infile,delimiter=',',quotechar='"')

	            # ignore header
	            freader.next()

	            # for each image
	            for row in freader:

	                season = row[0]
	                site = row[1]
	                newtime = row[6]

	                # verify season
	                if season != lastseason:
	                    # make sure the season is already in the database
	                    if (lastseason!="0" and 
	                        not snapshotDB.seasonExists(season)):
	                        print "Season " + season + " is not in the database."
	                        print "Please create and import a Season file before uploading metadata for that season."
	                        print "Metadata import ABORTED. No metadata imported."
	                        exit(1)
	                    lastseason = season

	                # verify site
	                if site != lastsite:
	                    # make sure sites are already in the database
	                    if (lastsite!="0" and
	                        not snapshotDB.siteExists(site)):
	                        print "Site " + site + " is not in the database."
	                        print "This Site will need to be created in the database before uploading metadata for it."
	                        print "Metadata import ABORTED. No metadata imported."
	                        exit(1)
	                    lastsite = site

	                # record start and stop date
	                #rsskey = season+site
	                #if rsskey not in rollstartstop:
	                    # add start date
	                #    rollstartstop[rsskey] = [newtime[0:10],None]
	                # add stop date
	                #rollstartstop[rsskey][1] = newtime[0:10]

	        
	        print "Adding rolls from metadata file\n"                
	                
	        # season(s) and sites are okay
	        # now go through and add the rolls, creating two new files in the process
	        # for capture and image imports
	        outfilename1 = outdirname + "temp_captures.csv"
	        outfilename2 = outdirname + "temp_images1.csv"

	        # ugly with python 2.6, but that's what's running at MSI
	        with open(infilename,'rb') as infile:
	            with open(outfilename1,'wb') as outfile1:
	                with open(outfilename2,'wb') as outfile2:

	                    # CSV readers            
	                    freader = csv.reader(infile,delimiter=',',quotechar='"')                      
	                    fwriter1 = csv.writer(outfile1,delimiter=',',quotechar='"')
	                    fwriter2 = csv.writer(outfile2,delimiter=',',quotechar='"')

	                    # remove header line
	                    freader.next()

	                    # write header lines
	                    fwriter1.writerow(["idRoll","capture","newtime","invalid","zoon_status"])
	                    fwriter2.writerow(["idSeason","idSite","idRoll","capture",
	                                      "image","path","newtime","oldtime"])

	                    lastsite = "0"
	                    lastroll = "0"

	                    for row in freader:

	                        season = row[0]
	                        site = row[1]
	                        roll = row[2]
	                        capture = row[3]
	                        image = row[4]
	                        path = row[5]
	                        newtime = row[6]
	                        oldtime = row[7]
	                        invalid = row[8]
	                        include = row[9]

	                        # look up the site
	                        if site!=lastsite:
	                            siteID = snapshotDB.getSite(site)
	                            lastsite = site

	                        # create (or look up) roll
	                        rollcombo = season+site+roll
	                        if rollcombo!=lastroll:

	                            print "adding roll " + season + ", " + site + ", " + roll
	                            rollID = snapshotDB.addRoll(season,site,roll,None,None)
	                            lastroll = rollcombo

	                        # write to captures file using data for first image
	                        if image=="1":
	                            fwriter1.writerow([rollID,capture,newtime,invalid,include])

	                        # write to images file using all data
	                        fwriter2.writerow([season,siteID,rollID,capture,
	                                           image,path,newtime,oldtime])

	        # make a note in the log
	        snapshotDB.log(fullname,"Added rolls for new season from file " + infilename)

	        # now rolls is created
	        # create capture events with temp file
	        snapshotDB.addCaptures(outfilename1)
	                
	        # make a note in the log
	        snapshotDB.log(fullname,"Added capture events for new season from file " + infilename)

	        # modify the image import file with capture event ID numbers
	        outfilename3 = outdirname + "temp_images2.csv"
	        with open(outfilename2,'rb') as infile:
	            with open(outfilename3,'wb') as outfile:
	            
	                # CSV readers            
	                freader = csv.reader(infile,delimiter=',',quotechar='"')                      
	                fwriter = csv.writer(outfile,delimiter=',',quotechar='"')

	                # remove header line
	                freader.next()

	                # write header line
	                fwriter.writerow(["idSeason","idSite","idRoll","idCapture",
	                                  "image","path","newtime","oldtime"])

	                lastcombo = "0"
	                
	                for row in freader:

	                    season = row[0]
	                    siteID = row[1]
	                    rollID = row[2]
	                    capture = row[3]
	                    image = row[4]
	                    path = row[5]
	                    newtime = row[6]
	                    ot = row[7]

	                    # convert the oldtime
	                    oldtime = ot[0:4]+"-"+ot[5:7]+"-"+ot[8:]
	                
	                    # look up capture if necessary
	                    combo = season + siteID + rollID + capture
	                    if combo!=lastcombo:
	                        captureID = snapshotDB.getCaptureEvent(rollID,capture)
	                        lastcombo=combo

	                    # write to new file with capture ID instead of capture number
	                    fwriter.writerow([captureID,image,path,newtime,oldtime])

	        # import the images using this temp file
	        snapshotDB.addImages(outfilename3)
	                
	        # make a note in the log
	        snapshotDB.log(fullname,"Added images for new season from file " + infilename)


	# catch errors
	except MySQLdb.Error, e:
	    print "Error %d: %s" % (e.args[0],e.args[1])
	    sys.exit(1)


	# close connection to the database
	finally:
	    if db:
	        db.close()

# Function creates an authentication file if needed
def createAuthenticationFile(msiUserName,dbPasswd):
	authfile_path = '/Users/Axl/Desktop/SerengetiPart2/scripts/auth_files'
	#authfile_path = '/Users/Axl/shared/metadata_db/scripts/auth_files'

	server = 'localhost'
	
	## Not needed at the moment because of global variables
	#msiUserName = raw_input("Please enter your MSI username (x500): ")
	#dbPasswd = getpass.getpass("Please enter your database password (may be different from your MSI password): ")
	

	schema = 'packerc_snapshot_serengeti'


	# try:
	#     db = MySQLdb.connect(server, msiUserName, 
	#                          dbPasswd, schema)
	#     cursor = db.cursor()        
	#     cursor.execute("SELECT VERSION()")
	#     results = cursor.fetchone()
	#     # Check if anything at all is returned
	#     if results:
	#         print "Connection Successful."
	#     else:
	#         print "Connection Failed, please contact help@msi.umn.edu to ask for access to packerc_snapshot_serengeti MySQL database."
	#         exit(1)
	# except MySQLdb.Error:
	#     print "Connection Failed, please contact help@msi.umn.edu to ask for access to packerc_snapshot_serengeti MySQL database."
	#     exit(1)

	os.chdir(authfile_path)

	#shortName = raw_input("Please enter a short, one-word name for yourself (ex. packer): ")
	#fullName = raw_input ("Please enter your first and last name (ex. Craig Packer): ")
	fileName = "auth-" + msiUserName + ".txt"

	# Open authentication file and write 3 lines
	# 1st line is MSI Username (ex. packer)
	# 2nd line is database password
	# 3rd line is the user's full name (ex. Craig Packer)
	f = open(fileName,"w+")
	f.write(msiUserName+"\n")
	f.write(dbPasswd+"\n")
	f.write(fullName)
	f.close()

	# Set authentication file to be read only
	# File is only accessible to the person running this script
	os.chmod(fileName,0600)

	print "Authentication file created successfully."

# Function creates new metadata file for a particular season
def createMetadataFile(seasonNbr):
	#authfile_path = '/Users/Axl/Desktop/SerengetiPart2/metadata/seasons_files'
	metadata_path = '/Users/Axl/Desktop/SerengetiPart2/metadata/seasons_files'

	def validate(date_text):
	    try:
	        datetime.datetime.strptime(date_text, '%Y-%m-%d')
	    except ValueError:
	        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

	# Get information about the season
	
	## Not needed right now because of global variables
	#seasonNbr = raw_input("\n"+"Please enter the season number: ")
	
	seasonStartDate = raw_input("\n"+"Please enter the season's start date (format: yyyy-mm-dd): ")
	validate(seasonStartDate)
	seasonEndDate = raw_input("\n"+"Please enter the season's end date (format: yyyy-mm-dd): ")
	validate(seasonEndDate)

	while (seasonStartDate > seasonEndDate):
		print "ERROR: Season end date must be after season start date."
		seasonEndDate = raw_input("\n"+"Please enter the season's end date (format: yyyy-mm-dd): ")
		validate(seasonEndDate)


	seasonComments = raw_input("Please enter your comments (500 characters max) about the season (ex. Retrieved by Alex): ")

	# Change to the metadata directory
	os.chdir(metadata_path)

	# Set filename
	fileName = "season" + seasonNbr + "meta.csv"

	# Open authentication file and write header line
	f = open(fileName,"w+")
	f.write(seasonNbr+","+"\""+seasonStartDate+"\",\""+seasonEndDate+"\",\""+seasonComments+"\"")
	f.close()

	print "Season "+seasonNbr+" metadata file created successfully."

#def importCleanSeasonMetadata(authFilename,seasonFilename,metadataFilename,outputDir):


	# Function to upload image metadata once gathered
def uploadImageMetadata(seasonNbr,msiUserName):
	# Get information about the season

	## Not needed right now because of global variables
	#msiUserName = raw_input("\n"+"Please enter your MSI user name (should match your authentication file): ")
	#seasonNbr = raw_input("\n"+"Please enter the season number: ")

	#authfile_path = '/Users/Axl/Desktop/SerengetiPart2/scripts/logfiles'
	log_path = '/Users/Axl/Desktop/SerengetiPart2/scripts/logfiles'
	scriptsPath = '/Users/Axl/Desktop/SerengetiPart2/scripts'
	new_path = '/Users/Axl/Desktop/SerengetiPart2/scripts/logfiles/S'+seasonNbr+"_meta_upload"

	# Change to the metadata directory
	os.chdir(log_path)
	os.mkdir(new_path)

	os.chdir(scriptsPath)

	os.system("./import_clean_season_metadata_into_database.py ./auth_files/auth-"+msiUserName+".txt ../metadata/seasons_files/season"+seasonNbr+"meta.csv ../TimeStampCleaning/CleanedCaptures/S"+seasonNbr+"_cleaned.csv ./logfiles/S"+seasonNbr+"_meta_upload/ > ./logfiles/S"+seasonNbr+"_meta_upload/import_S"+seasonNbr+"_log.txt &")
	
	# importCleanSeasonMetadata(scriptsPath+"/auth_files/auth-"+msiUserName+".txt"
	# 						,metadataPath+"/seasons_files/season"+seasonNbr+"meta.csv"
	# 						,sharedDir+"/TimeStampCleaning/CleanedCaptures/S"+seasonNbr+"_cleaned.csv"
	# 						,new_path)


# Function sets start and stop time for rolls
def setRollUpTimes(msiUserName,dbPasswd,fullName):
	# make sure we have 2 arguments
	#if len(sys.argv) < 2 :
	#    print ("format: load-ConsensusClassifications <infile>")
	#   exit(1)

	#infilename = sys.argv[1]

	try:
	    # connect to the database
	    db = MySQLdb.connect(host=mySqlHost,
	                         user=msiUserName,
	                         passwd=dbPasswd,
	                         db=mySqlSchema,
	                         local_infile = 1)

	    # use the database
	    with db:
	        
	        snapshotDB.cur = db.cursor()
	        snapshotDB.setUptimeForAllRollsNeedingIt()
	  
	        # make a note in the log
	        snapshotDB.log(fullName,
	                       "Set StartDate and StopDate in the Rolls table")

	# catch errors
	except MySQLdb.Error, e:
	    print "Error %d: %s" % (e.args[0],e.args[1])
	    sys.exit(1)


	# close connection to the database
	finally:
	    if db:
	        db.close()


def extractNonEmptySubjects(inFilename,outFilename):

	# get file names from command prompt
	# if len(sys.argv) < 2 :
	#     print ("format: extract_non_empty_subjects.py <infile> <outfile>")
	#     exit(1)

	# inFilename = sys.argv[1]
	# outfilename = sys.argv[2]

	# set of unique zooniverse IDs that retired with 'complete' or 'consensus'
	nonblanks = set()

	# first go through and grab all the capture events that finished
	# as 'complete' or 'consensus'
	with open(inFilename, 'rb') as infile:

	    # set up CSV reader
	    filereader = csv.reader(infile, delimiter=',', quotechar='"')
	    print "reading complete/consensus captures"

	    for line in filereader:
	        if line[5] == "complete" or line[5] == "consensus":
	            nonblanks.add(line[2])

	    print "all captures read"

	# now go through and find all the classifications for the 'complete'
	# and 'consensus' captures
	with open(inFilename, 'rb') as infile:
	    with open(outFilename,'wb') as outfile:

	        # set up CSV reader and writer
	        filereader = csv.reader(infile, delimiter=',', quotechar='"')
	        filewriter = csv.writer(outfile, delimiter=',', quotechar='"',
	                            quoting=csv.QUOTE_ALL)

	        # header line
	        filewriter.writerow(filereader.next())
	        print "Finding classifications"

	        for line in filereader:
	            if line[2] in nonblanks:
	                filewriter.writerow(line)

# Prepare season
def prepSeason(seasonNbr,inFilename):

   # global
   global hashtable
   hashtable = {}

   # for sorting
   def compare_by_species(a,b):
       return cmp(a[11],b[11])

   # combine with an OR operation
   def combineTF(str1,str2):
       if str1.lower()=="true" or str2.lower()=="true":
           return "true"
       return "false"

   # Have we already seen this user? If not, hash it and add to our table.
   def get_user_hash(username):
       global hashtable
       if username in hashtable:
          thehash = hashtable[username]
       else:
           if username[0:13] == "not-logged-in":
               thehash = username
           else:
               thehash = hashlib.sha224(username[0:39]).hexdigest()
           hashtable[username] = thehash
       return thehash

   # For each classification, see if any species is listed more than
   # once. If so, combine.
   def process_classification(classlines):

       # sort by species
       classlines.sort(compare_by_species)
       
       # combine if necessary
       newclasslines = list()
       for line in classlines:

           # first line
           if line == classlines[0]:
               lastline = line

           # same species
           elif line[11] == lastline[11]:

               # animal counts
               if lastline[12] == "11-50" or line[12] == "11-50":
                   lastline[12] = "11-50"
               elif lastline[12] == "51+" or line[12] == "51+":
                   lastline[12] = "51+"
               else:
                   num = int(lastline[12]) + int(line[12])
                   if num>10:
                       lastline[12] = "11-50"
                   else:
                       lastline[12] = str(num)

               # true-false                   
               lastline[13] = combineTF(lastline[13],line[13])
               lastline[14] = combineTF(lastline[14],line[14])
               lastline[15] = combineTF(lastline[15],line[15])
               lastline[16] = combineTF(lastline[16],line[16])
               lastline[17] = combineTF(lastline[17],line[17])
               lastline[18] = combineTF(lastline[18],line[18])

           # different species
           else:
               newclasslines.append(lastline)
               lastline = line
               
       # last line
       newclasslines.append(lastline)

       # get user hash
       userhash = get_user_hash(lastline[1])

       # output lines
       outlines = list()
       for line in newclasslines:
           outlines.append([line[0],userhash] + line[2:10] + line[11:19])

       return outlines

      # --- MAIN ---

   # # get file names from command prompt
   # if len(sys.argv) < 3 :
   #     print ("format: prep_season.py <number> <infile>")
   #     exit(1)

   # seasonnum = sys.argv[1] #int(sys.argv[1])
   # infilename = sys.argv[2]
   seasonnum = seasonNbr
   infilename = inFilename

   outfilename = "season_" + str(seasonnum) + ".csv"
   hashfilename = "season_" + str(seasonnum) + "_hashes.csv"

   infile = open(infilename, 'rb')
   filereader = csv.reader(infile, delimiter=',', quotechar='"')

   outfile = open(outfilename,'wb')
   filewriter = csv.writer(outfile, delimiter=',', quotechar='"',
                           quoting=csv.QUOTE_ALL)

   hashfile = open(hashfilename,'w')
   hashwriter = csv.writer(hashfile, delimiter=',', quotechar='"',
                           quoting=csv.QUOTE_ALL)

   # header line
   filereader.next()
   filewriter.writerow(["class_id","user_hash","subject_zooniverse_id","capture_event_id","created_at",
                        "retire_reason","season","site","roll","filenames","species","species_count",
                        "standing","resting","moving","eating","interacting","babies"])

   # first line
   lastclass = ""
   for line in filereader:
       if line[0] == lastclass:
           thisclass.append(line)
       
       else: # process old classification and start new classification
           if lastclass != "":
               goodclass = process_classification(thisclass)
               for gc in goodclass:
                   filewriter.writerow(gc)
           
           thisclass = list()
           thisclass.append(line)
           lastclass = line[0]
           
   # and the last one
   goodclass = process_classification(thisclass)
   for gc in goodclass:
       filewriter.writerow(gc)

   # and save the hash table
   hashwriter.writerow(["user_name","user_hash"])
   for key,value in hashtable.iteritems():
       hashwriter.writerow([key,value])

   # close up the files
   infile.close()
   outfile.close()
   hashfile.close()

# Function that anonymizes Zooniverse users, input should be an exported Zooniverse file
def createUsersHashTable(inFilename,outFilename):
	# input should be an exported Zooniverse file

	# get file names from command prompt
	# if len(sys.argv) < 3 :
	#     print ("format: create_users_hash_table.py <infile> <outfile>")
	#     exit(1)

	infilename = inFilename
	hashfilename = outFilename

	# a list of all users (unique)
	userset = set()

	with open(infilename, 'r') as infile:
	    
	    filereader = csv.reader(infile, delimiter=',', quotechar='"')

	    # discard header
	    filereader.next()
	    
	    # go through file and collect the users
	    for row in filereader:
	        userset.add(row[1])

	# sort, hash, and print out
	userlist = sorted(list(userset))

	with open(hashfilename,'w+') as hashfile:
	    hashwriter = csv.writer(hashfile, delimiter=',', quotechar='"',
	                            quoting=csv.QUOTE_ALL)

	    # header
	    hashwriter.writerow(["user_name","user_hash"])

	    for username in userlist:
	        thehash = username
	        if username[0:13] != "not-logged-in":
	            thehash = hashlib.sha224(username[0:39]).hexdigest()
	        
	        hashwriter.writerow([username,thehash])

# Gets consensus on every capture event's votes
def getPluralityConsensus(inFilename,outFilename):
	def compare_by_classification(a,b):
	    return cmp(a[0],b[0])

	def get_species_counts(scals):
	    spp = list()
	    for cl in scals:
	        if cl[0][10] != "": # ignore blanks
	            spp.append(len(cl))
	        else:
	            spp.append(0)
	    return spp

	def tally_spp_votes(subject):
	    vote_table = {}
	    for entry in subject:
	        spp = entry[10]
	        if spp != "": # ignore blanks
	            # already in table
	            if spp in vote_table:
	                vote_table[spp] = vote_table[spp] + 1
	            # not in table yet
	            else:
	                vote_table[spp] = 1
	    return vote_table

	def calculate_pielou(nlist):
	    if len(nlist)<2:
	        return 0 
	    # denominator
	    lnS = math.log(len(nlist))
	    # numerator
	    sumlist = sum(nlist)
	    plist = [float(n)/sumlist for n in nlist]
	    plnplist = [n * math.log(n) for n in plist]
	    sumplnp = -sum(plnplist)
	    return sumplnp/lnS    

	def choose_winners(numwin,sppvotes):
	    # sort by votes
	    sorted_sppvotes = sorted(sppvotes.iteritems(),
	                             key=operator.itemgetter(1),
	                             reverse=True)
	    winners = sorted_sppvotes[0:numwin]

	    # check for ties
	    if len(sorted_sppvotes) > numwin:
	        if sorted_sppvotes[numwin-1][1] == sorted_sppvotes[numwin][1]:
	            votes = sorted_sppvotes[numwin-1][1]
	            ties = []
	            # get all the tied species
	            for spp in sorted_sppvotes:
	                if spp[1] == votes:
	                    ties.append(spp)
	            # choose one at random
	            tiewinner = random.choice(ties)
	            winners[numwin-1] = tiewinner

	    return winners

	def calculate_num_animals(noa):
	    
	    nums = []
	    tens = []
	    meds = []
	    many = []
	    for ea in noa:
	        if len(ea)==1:
	            nums.append(ea)
	        elif ea=="10":
	            tens.append(ea)
	        elif ea=="11-50":
	            meds.append(ea)
	        else:
	            many.append(ea)
	    nums.sort()
	    sorted_list = nums + tens + meds + many
	    # round up (gotta choose one or the other)
	    medind = int(math.ceil((len(sorted_list)+1)/2)-1)
	    return [sorted_list[0],sorted_list[medind],sorted_list[-1]]

	def calculate_TF_perc(items):
	    ctr = 0
	    for ea in items:
	        if ea=="true":
	           ctr = ctr + 1
	    return float(ctr) / len(items)

	def winner_info(sppwinners,numclass,numblanks,subject):
	    info = []
	    for spp in sppwinners:
	        # fraction people who voted for this spp
	        fracpeople = float(spp[1]) / (numclass-numblanks)
	        # look through votes
	        noa = []
	        stand = []
	        rest = []
	        move = []
	        eat = []
	        interact = []
	        baby = []

	        for line in subject:
	            if line[10]==spp[0]:
	                noa.append(line[11])
	                stand.append(line[12])
	                rest.append(line[13])
	                move.append(line[14])
	                eat.append(line[15])
	                interact.append(line[16])
	                baby.append(line[17])
	        
	        # number of animals
	        numanimals = calculate_num_animals(noa)
	        
	        # true-false questions
	        stand_frac = calculate_TF_perc(stand)
	        rest_frac = calculate_TF_perc(rest)
	        move_frac = calculate_TF_perc(move)
	        eat_frac = calculate_TF_perc(eat)
	        interact_frac = calculate_TF_perc(interact)
	        baby_frac = calculate_TF_perc(baby)
	        
	        # save it all
	        info.append([spp[0],spp[1],fracpeople] + numanimals +
	                    [stand_frac,rest_frac,move_frac,eat_frac,
	                     interact_frac,baby_frac])
	        
	    return info
	    
	def process_subject(subject,filewriter):
	    # sort by classification
	    subject.sort(compare_by_classification)

	    # then create 2D list to deal with them
	    scals = list()
	    lastclas = ""
	    subcl = list()
	    for entry in subject:
	        if entry[0] == lastclas:
	            subcl.append(entry)
	        else:
	            if len(subcl)>0:
	                scals.append(subcl)
	            subcl = [entry]
	            lastclas = entry[0]
	    scals.append(subcl)

	    # count total number of classifications done
	    numclass = len(scals)

	    # count unique species per classification, ignoring blanks
	    sppcount = get_species_counts(scals)

	    # count and remove the blanks
	    numblanks = sppcount.count(0)
	    sppcount_noblanks = list(value for value in sppcount if value != 0)

	    # take median (rounded up)
	    sppcount_noblanks.sort()
	    medianspp = sppcount_noblanks[int(math.ceil((len(sppcount_noblanks)+1)/2)-1)]

	    # count up votes for each species
	    sppvotes = tally_spp_votes(subject)

	    # total number of (non-blank) votes
	    totalvotes = sum(sppvotes.values())

	    # Pielou evenness index
	    pielou = calculate_pielou(sppvotes.values())

	    # choose winners
	    sppwinners = choose_winners(medianspp,sppvotes)

	    # get winner info
	    winnerstats = winner_info(sppwinners,numclass,numblanks,subject)

	    # output
	    # Fixed: grab last retirement reason instead of first (github issue #65)
	    basic_info = (subject[0][2:4] + [subject[-1][5]] + subject[0][6:10] +
	                  [numclass,totalvotes,numblanks,pielou,medianspp])
	    ctr = 1
	    for winner in winnerstats:
	        spp_info = basic_info + [ctr] + winner
	        filewriter.writerow(spp_info)
	        ctr = ctr + 1



	# --- MAIN ---

	# get file names from command prompt
	# if len(sys.argv) < 3 :
	#     print ("format: plurality_consensus.py <infile> <outfile>")
	#     exit(1)

	infilename = inFilename
	outfilename = outFilename

	infile = open(infilename, 'rb')
	filereader = csv.reader(infile, delimiter=',', quotechar='"')

	outfile = open(outfilename,'w+')
	filewriter = csv.writer(outfile, delimiter=',', quotechar='"',
	                        quoting=csv.QUOTE_NONE)

	# header line
	filereader.next()

	filewriter.writerow(["subject_zooniverse_id","capture_event_id","retire_reason",
	                     "season","site","roll","filenames",
	                     "number_of_classifications","number_of_votes",
	                     "number_of_blanks","pielou_evenness",
	                     "number_of_species","species_index",
	                     "species","species_votes","species_fraction_support",
	                     "species_count_min","species_count_median","species_count_max",
	                     "species_fraction_standing","species_fraction_resting",
	                     "species_fraction_moving","species_fraction_eating",
	                     "species_fraction_interacting","species_fraction_babies"])


	# sort the classifications by subject
	sortedclass = sorted(filereader, key=operator.itemgetter(2))

	# go through the subjects one by one
	lastsubject = sortedclass[0][2]
	subjectlines = []
	for entry in sortedclass:
	    subject = entry[2]
	    if subject == lastsubject:
	        subjectlines.append(entry)
	    else:
	        process_subject(subjectlines,filewriter)
	        subjectlines = [entry]
	        lastsubject = subject
	process_subject(subjectlines,filewriter)
	        
	        


	infile.close()
	outfile.close()

def getBlankCaptures(inFilename,outFilename):
	# make sure we have 3 arguments
	# if len(sys.argv) < 3:
	#     print ("format: get_blank_captures <in_data_file> <out_data_file>")
	#     exit(1)

	infilename = inFilename
	outfilename = outFilename

	# set of unique zooniverse IDs that retired with 'blank' or 'blank_consensus'
	blanks = set()

	# first go through and grab all the capture events that finished
	# as 'blank' or 'blank_consensus'
	with open(infilename, 'rb') as infile:

	    # set up CSV reader
	    filereader = csv.reader(infile, delimiter=',', quotechar='"')

	    for line in filereader:
	        if line[5] == "blank" or line[5] == "blank_consensus":
	            blanks.add(line[2])

	# keep statistics on each capture
	stats = dict.fromkeys(blanks)

	with open(infilename, 'rb') as infile:

	    # set up CSV reader and writer
	    filereader = csv.reader(infile, delimiter=',', quotechar='"')

	    # header line
	    filereader.next()

	    # go through and do stats on all the classifications
	    for line in filereader:
	        zoonid = line[2]
	        if zoonid in blanks:

	            # create a new stats field if necessary
	            if stats[zoonid] is None:
	                stats[zoonid] = ["",0,0]

	            # and add the stats
	            stats[zoonid][1] = stats[zoonid][1] + 1
	            if line[5] != "none":
	                stats[zoonid][0] = line[5]
	            if line[11] == "":
	                stats[zoonid][2] = stats[zoonid][2] + 1         
	                

	# write results
	with open(outfilename,'wb') as outfile:
	                
	    filewriter = csv.writer(outfile, delimiter=',', quotechar='"',
	                            quoting=csv.QUOTE_NONE) 
	    filewriter.writerow(["zooniverse_id","reason","num_class","num_blanks"])

	    sorted_stats = sorted(stats.keys())
	    for key in sorted_stats:
	        value = stats[key]
	        filewriter.writerow([key,value[0],value[1],value[2]])

def exportSeason(seasonNbr,outFilename):
	# make sure we have 2 arguments
	# if len(sys.argv) < 3 :
	#     print ("format: export-season.py <season> <output file>")
	#     exit(1)

	season = seasonNbr
	outfilename = outFilename

	try:
	    # connect to the database
	    db = MySQLdb.connect(host=mySqlHost,
	                         user=msiUserName,
	                         passwd=dbPasswd,
	                         db=mySqlSchema,
	                         local_infile = 1)

	    # use the database
	    with db:
	        snapshotDB.cur = db.cursor()
	        data = snapshotDB.exportSeasonCaptureEvents(season)

	        # write the data to file
	        with open(outfilename,'wb') as outfile:
	            owriter = csv.writer(outfile)
	            owriter.writerow(["idCaptureEvent","Season","GridCell","RollNumber","CaptureEventNum","SequenceNum","PathFilename"])

	            for row in data:
	                owriter.writerow(row)
	                
	      
	# catch errors
	except MySQLdb.Error, e:
	    print "Error %d: %s" % (e.args[0],e.args[1])
	    sys.exit(1)


	# close connection to the database
	finally:
	    if db:
	        db.close()
	            

def snapshotCaptureExtract(inFilename,outFilename):
	# if len(sys.argv) < 3:
 #    		print ("format: snapshot_capture_extract.py <in_data_file> <out_data_file>")
 #    		exit(1)

	infilename = inFilename
	outfilename = outFilename

	infile = open(infilename,'rb')
	filereader = csv.reader(infile, delimiter=',', quotechar='"')
	outfile = open(outfilename,'w')

	# write header for out file
	outfile.write("Season,Site,Roll,Capture,ImageNum,ImageName,Zooniverse_ID\n")

	# get rid of header line in infile
	filereader.next()

	# list of what we've already done
	done = set()

	# list of output lines
	outlist = list()

	# read each line
	for line in filereader:

	    # record each zooniverse_id and don't redo ones we've already done
	    if line[2] not in done:
	        done.update([line[2]])

	        # how many images? count the semicolons
	        images = line[9].split(';')
	        
	        ctr = 1
	        for im in images:
	            outline = line[6][1:],line[7],line[8][0:],line[3],str(ctr),im,line[2]
	            outlist.append(outline)    
	            ctr = ctr + 1

	# now sort the output list
	sorted_outlist = sorted(outlist, key=lambda x: (x[1],x[2],x[5]))

	# and print to a file
	filewriter = csv.writer(outfile) 
	filewriter.writerows(sorted_outlist)

	outfile.close()
	infile.close()

def compareCaptures(databaseFile,uniqueCaptureFile,linkFile):

	# This script takes as input 2 files:
	# 1. a dump from the database for a season using export-season.py
	# 2. the zooniverse unique capture file for a season
	#
	# Its job is to compare the two files and match up Zooniverse IDs
	# to idCaptureEvents. The output is a file that can be directly
	# imported to the CaptureEventsToZooniverseIDs table.
	#
	# The script expects the two input files to be sorted by
	# site, roll, capture number, image name

	def line_match(crow,zrow):

	    # extract the image name from the path
	    im = crow[6].split('/')[-1]

	    # compare
	    match = False
	    if (crow[1]==zrow[0] and
	        crow[2]==zrow[1] and
	        crow[3]==zrow[2] and
	        crow[4]==zrow[3] and
	        crow[5]==zrow[4] and
	        im==zrow[5]):
	        match = True
	    
	    return match


	def why_no_match(crow,zrow):

	    # default return value
	    to_ret = [0,""]
	    
	    if crow[1] < zrow[0]:
	        to_ret[1] = "Capture from the wrong season here: "+str(crow)
	        to_ret[0] = 2
	    elif crow[1] > zrow[0]:
	        to_ret[1] = "Zoon capture from the wrong season here: "+str(zrow)
	        to_ret[0] = 1
	    elif crow[2] < zrow[1]:
	        to_ret[1] = "Site "+crow[2]+" has more images in DB than at Zooniverse"
	        to_ret[0] = 2
	    elif crow[2] > zrow[1]:
	        to_ret[1] = "Site "+zrow[1]+" has fewer images in DB than at Zooniverse"
	        to_ret[0] = 1
	    elif crow[3] < zrow[2]:
	        to_ret[1] = "Roll "+crow[2]+"_R"+crow[3]+" has more images in DB than at Zooniverse"
	        to_ret[0] = 2
	    elif crow[3] > zrow[2]:
	        to_ret[1] = "Roll "+zrow[1]+"_R"+zrow[2]+" has fewer images in DB than at Zooniverse"
	        to_ret[0] = 1
	    elif crow[4] < zrow[3]:
	        to_ret[1] = "Mismatch in captures. DB: "+str(crow)+". Zoon: "+str(zrow)
	        to_ret[0] = 2
	    elif crow[4] > zrow[3]:
	        to_ret[1] = "Mismatch in captures. DB: "+str(crow)+". Zoon: "+str(zrow)
	        to_ret[0] = 1
	    elif crow[5] < zrow[4]:
	        to_ret[1] = "Mismatch in images. DB: "+str(crow)+". Zoon: "+str(zrow)
	        to_ret[0] = 2
	    elif crow[5] > zrow[4]:
	        to_ret[1] = "Mismatch in images. DB: "+str(crow)+". Zoon: "+str(zrow)
	        to_ret[0] = 1
	    elif crow[6].split('/')[-1] < zrow[5]:
	        to_ret[1] = "Mismatch in image name. DB: "+str(crow)+". Zoon: "+str(zrow)
	        to_ret[0] = 2
	    elif crow[6].split('/')[-1] > zrow[5]:
	        to_ret[1] = "Mismatch in image name. DB: "+str(crow)+". Zoon: "+str(zrow)
	        to_ret[0] = 1

	    return to_ret

	#### MAIN ####

	# if len(sys.argv) < 4:
	#     print ("format: compare_captures.py <database_file> <zooniverse_unique_capture_file> <out_file>")
	#     exit(1)

	capture_infilename = databaseFile
	zooniverse_infilename = uniqueCaptureFile
	outfilename = linkFile
	errfilename = outfilename + "_err.txt"

	# store initial results in a big array
	iresults = []
	# store errors in array, too
	errors = []

	# read in the files and match them up
	with open(capture_infilename,'rb') as capture_infile:
	    with open(zooniverse_infilename,'rb') as zooniverse_infile:

	        creader = csv.reader(capture_infile)
	        zreader = csv.reader(zooniverse_infile)

	        # ignore headers
	        creader.next()
	        zreader.next()

	        # do the lines match?
	        crow = creader.next()
	        zrow = zreader.next()

	        keepgoing = True

	        while keepgoing:

	            try:
	        
	                # yes! record the match
	                if line_match(crow,zrow):
	                    iresults.append((crow[0],zrow[6]))

	                    crow = creader.next()
	                    zrow = zreader.next()
	                 
	                # no. oh dear.
	                else:
	                    problem = why_no_match(crow,zrow)
	                    todo = problem[0]
	                    errors.append(problem[1])

	                    # advance        
	                    if todo==1:
	                        zrow = zreader.next()
	                    elif todo==2:
	                        crow = creader.next()
	                    else:
	                        crow = creader.next()
	                        zrow = zreader.next()

	            # end of file
	            except StopIteration:
	                keepgoing = False
	    
	# now look at resulting array and see if there are any problems
	# dedupe
	deduped_results = list(set(iresults))

	# sort by capture event
	capture_sort = sorted(deduped_results, key=lambda tup: tup[0])

	# is there every more than one?
	prev = ""
	for tup in capture_sort:
	    if tup[0]==prev:
	        errors.append("Capture event "+prev+" has multiple Zoon IDs")
	    prev = tup[0]

	# sort by zoon id
	zoon_sort = sorted(deduped_results, key=lambda tup: tup[1])

	# is there every more than one?
	prev = ""
	for tup in zoon_sort:
	    if tup[0]==prev:
	        errors.append("Zooniverse ID "+prev+" has multiple Capture IDs")
	    prev = tup[0]

	# write output file 
	with open(outfilename,'wb') as outfile:
	    owriter = csv.writer(outfile)
	    owriter.writerow(["idCaptureEvent","Zooniverse_ID"])
	    for tup in capture_sort:
	        owriter.writerow(tup)

	# write error file
	with open(errfilename,'wb') as errfile:
	    for line in errors:
	        errfile.write(line+"\n")


def addUsers(allUsersHashFile):
	# make sure we have 2 arguments
	# if len(sys.argv) < 2 :
	#     print ("format: add-Users <file>")
	#     exit(1)

	infilename = allUsersHashFile

	try:
	    # connect to the database
	    db = MySQLdb.connect(host=mySqlHost,
	                         user=msiUserName,
	                         passwd=dbPasswd,
	                         db=mySqlSchema,
	                         local_infile = 1)

	    # open up the file
	    infile = open(infilename,'rb')
	    filereader = csv.reader(infile, delimiter=',', quotechar='"')

	    # use the database
	    with db:
	        snapshotDB.cur = db.cursor()

	        # remove header line
	        filereader.next()

	        # go through each line in the file
	        for line in filereader:
	     
	            uname = line[0]
	            uhash = line[1]

	            userID = snapshotDB.getUser(uname)
	            if userID == None:
	                snapshotDB.addUser(uname,uhash)
	                
	        # make a note in the log
	        snapshotDB.log(fullName,
	                       "Added users from file " +
	                       str(infilename))
	 
	    # close the file
	    infile.close()

	# catch errors
	except MySQLdb.Error, e:
	    print "Error %d: %s" % (e.args[0],e.args[1])
	    sys.exit(1)


	# close connection to the database
	finally:
	    if db:
	        db.close()
            
def transformZooniverseClassifications(inFilename,outFilename):
	# make sure we have 2 arguments
	# if len(sys.argv) < 3 :
	#     print ("format: transform-ZooniverseClassifications <infile> <outfile>")
	#     exit(1)

	infilename = inFilename
	outfilename = outFilename

	# create dictionary for species
	# hard-coded for speed
	speciesDict = dict([('blank',1),
	                    ('aardvark',2),
	                    ('aardwolf',3),
	                    ('baboon',4),
	                    ('batEaredFox',5),
	                    ('buffalo',6),
	                    ('bushbuck',7),
	                    ('caracal',8),
	                    ('cheetah',9),
	                    ('civet',10),
	                    ('dikDik',11),
	                    ('eland',12),
	                    ('elephant',13),
	                    ('gazelleGrants',14),
	                    ('gazelleThomsons',15),
	                    ('genet',16),
	                    ('giraffe',17),
	                    ('guineaFowl',18),
	                    ('hare',19),
	                    ('hartebeest',20),
	                    ('hippopotamus',21),
	                    ('honeyBadger',22),
	                    ('human',23),
	                    ('hyenaSpotted',24),
	                    ('hyenaStriped',25),
	                    ('impala',26),
	                    ('jackal',27),
	                    ('koriBustard',28),
	                    ('leopard',29),
	                    ('lionFemale',30),
	                    ('lionMale',31),
	                    ('mongoose',32),
	                    ('ostrich',33),
	                    ('otherBird',34),
	                    ('porcupine',35),
	                    ('reedbuck',36),
	                    ('reptiles',37),
	                    ('rhinoceros',38),
	                    ('rodents',39),
	                    ('secretaryBird',40),
	                    ('serval',41),
	                    ('topi',42),
	                    ('vervetMonkey',43),
	                    ('warthog',44),
	                    ('waterbuck',45),
	                    ('wildcat',46),
	                    ('wildebeest',47),
	                    ('zebra',48),
	                    ('zorilla',49),
	                    ('duiker',50),
	                    ('steenbok',51),
	                    ('cattle',52),
	                    ('bat',53),
	                    ('insectSpider',54),
	                    ('vulture',55)])

	userDict = dict()

	try:
	    # connect to the database
	    db = MySQLdb.connect(host=mySqlHost,
	                         user=msiUserName,
	                         passwd=dbPasswd,
	                         db=mySqlSchema,
	                         local_infile = 1)

	    # open up the file
	    infile = open(infilename,'rb')
	    filereader = csv.reader(infile, delimiter=',', quotechar='"')

	    outfile = open(outfilename,'w')
	    filewriter = csv.writer(outfile, delimiter=',', quotechar='"')

	    # use the database
	    with db:
	        snapshotDB.cur = db.cursor()

	        # remove header line
	        filereader.next()

	        # write header line
	        filewriter.writerow(["zoon_id","class_id","userID","classDateTime",
	                            "speciesID","speciesCountID","stand","rest",
	                            "move","eat","interact","babies"])

	        # go through each line in the file
	        for line in filereader:
	     
	            classid = line[0]
	            uname = line[1]
	            zoonid = line[2]
	            createdat = line[4]
	            species = line[11]
	            spcount = line[12]
	            standing = line[13]
	            resting = line[14]
	            moving = line[15]
	            eating = line[16]
	            interacting = line[17]
	            babies = line[18]

	            # look up user
	            # save a local table for speed
	            if uname in userDict:
	                userID = userDict[uname]
	            # look up and add to table if not found
	            else:
	                userID = snapshotDB.getUser(uname)
	                if userID is None:
	                    snapshotDB.addUser(uname,"")
	                    print "Warning: user " + uname + " not found in database"
	                    userID = snapshotDB.getUser(uname)
	                userDict[uname] = userID

	            # trim date-time to get rid of " UTC"
	            cdat = createdat[:19]

	            # look up species
	            if species=="":
	                species = "blank"
	            #speciesID = snapshotDB.getSpecies(species)
	            speciesID = speciesDict[species]

	            # look up species count
	            #countID = snapshotDB.getSpeciesCount(spcount)
	            if spcount=="":
	                countID = 0
	            elif spcount=="11-50":
	                countID = 11
	            elif spcount=="51+":
	                countID = 12
	            else:
	                countID = int(spcount)

	            # convert true/false to 1/0
	            if standing == "true":
	                stand = 1
	            else:
	                stand = 0
	            if resting == "true":
	                rest = 1
	            else:
	                rest = 0
	            if moving == "true":
	                move = 1
	            else:
	                move = 0
	            if eating == "true":
	                eat = 1
	            else:
	                eat = 0
	            if interacting == "true":
	                interact = 1
	            else:
	                interact = 0
	            if babies == "true":
	                baby = 1
	            else:
	                baby = 0

	            # write to the new file
	            filewriter.writerow([zoonid,classid,userID,cdat,speciesID,
	                               countID,stand,rest,move,eat,interact,baby])
	            
	 
	    # close the file
	    infile.close()
	    outfile.close()

	# catch errors
	except MySQLdb.Error, e:
	    print "Error %d: %s" % (e.args[0],e.args[1])
	    sys.exit(1)


	# close connection to the database
	finally:
	    if db:
	        db.close()




def loadLinks(inFilename):
	# make sure we have 2 arguments
	# if len(sys.argv) < 2 :
	#     print ("format: load-Links <infile>")
	#     exit(1)

	infilename = inFilename

	try:
	    # connect to the database
	    db = MySQLdb.connect(host=mySqlHost,
	                         user=msiUserName,
	                         passwd=dbPasswd,
	                         db=mySqlSchema,
	                         local_infile = 1)

	    # use the database
	    with db:
	        
	        snapshotDB.cur = db.cursor()
	        snapshotDB.addLinks(infilename)
	  
	        # make a note in the log
	        snapshotDB.log(fullName,
	                       "Loaded links from captures to Zooniverse IDs in " +
	                       str(infilename))

	# catch errors
	except MySQLdb.Error, e:
	    print "Error %d: %s" % (e.args[0],e.args[1])
	    sys.exit(1)


	# close connection to the database
	finally:
	    if db:
	        db.close()

def loadConsensusClassifications(inFilename):

	# make sure we have 2 arguments
	# if len(sys.argv) < 2 :
	#     print ("format: load-ConsensusClassifications <infile>")
	#     exit(1)

	infilename = inFilename

	try:
	    # connect to the database
	    db = MySQLdb.connect(host=mySqlHost,
	                         user=msiUserName,
	                         passwd=dbPasswd,
	                         db=mySqlSchema,
	                         local_infile = 1)

	    # use the database
	    with db:
	        
	        snapshotDB.cur = db.cursor()
	        snapshotDB.addConsensusClassifications(infilename)
	  
	        # make a note in the log
	        snapshotDB.log(fullName,
	                       "Loaded consensus classifications in " +
	                       str(infilename))

	# catch errors
	except MySQLdb.Error, e:
	    print "Error %d: %s" % (e.args[0],e.args[1])
	    sys.exit(1)


	# close connection to the database
	finally:
	    if db:
	        db.close()
	            
def loadBlankClassifications(inFilename):

	# make sure we have 2 arguments
	# if len(sys.argv) < 2 :
	#     print ("format: load-ConsensusBlanks <infile>")
	#     exit(1)

	infilename = inFilename

	try:
	    # connect to the database
	    db = MySQLdb.connect(host=mySqlHost,
	                         user=msiUserName,
	                         passwd=dbPasswd,
	                         db=mySqlSchema,
	                         local_infile = 1)

	    # use the database
	    with db:
	        
	        snapshotDB.cur = db.cursor()
	        snapshotDB.addConsensusBlanks(infilename)
	  
	        # make a note in the log
	        snapshotDB.log(fullName,
	                       "Loaded blank captures from " +
	                       str(infilename))

	# catch errors
	except MySQLdb.Error, e:
	    print "Error %d: %s" % (e.args[0],e.args[1])
	    sys.exit(1)


	# close connection to the database
	finally:
	    if db:
	        db.close()
            
def speciesCount(inFilename,outFilename):
	# if len(sys.argv) < 3:
	#     print ("format: species_count.py <in_data_file> <out_data_file>")
	#     exit(1)

	infilename = inFilename
	outfilename = outFilename

	infile = open(infilename,'r')
	outfile = open(outfilename,'w')

	# write header for out file
	outfile.write("Species,NumberOfCaptures\n")

	# get rid of header line in infile
	infile.readline()

	# create the dictionary
	sppdict = {}

	# read each line
	for line in infile:

	    # chomp and parse
	    line = line.rstrip()
	    tokens = line.split(',')

	    # get the species
	    species = tokens[13]

	    # count it
	    if species in sppdict:
	        sppdict[species] = sppdict[species] + 1
	    else:
	        sppdict[species] = 1

	for key, val in sorted(sppdict.iteritems()):
	    outfile.write(key + "," + str(val) + "\n")

	outfile.close()
	infile.close()


#---------------------------------------- MAIN --------------------------------------

#Connect to MSI
# authenticationFileNeeded = raw_input("Have you already built an authentication file? (y for Yes, n for No): ")
# if authenticationFileNeeded == 'n':
# 	print "Creating authentication file"
# 	createAuthenticationFile(msiUserName,dbPasswd)
# 	print "Authentication file created."

# os.chdir("/Users/Axl/Desktop/SerengetiPart2/metadata/seasons_files")

print "Filtering snapshot file to current season"
#filterSnapshot(snapshotFilePath,classificationsPath+"/Zooniverse_downloads/S"+seasonNbr+"_filteringtemp.csv",seasonNbr)
filterSnapshot("/Users/Axl/Desktop/SerengetiPart2/classifications_data/Zooniverse_downloads/snapshot_S1-9_original.csv","/Users/Axl/Desktop/SerengetiPart2/classifications_data/testfilter.csv",9)
print "Snapshot file has been filtered."

# print "Creating metadata file for season "+seasonNbr
# createMetadataFile(seasonNbr)
# print "Metadata file for season "+seasonNbr+" created."

# print "Uploading image metadata for season "+seasonNbr
# uploadImageMetadata(seasonNbr,msiUserName)
# print "Metadata upload complete."

# print "Setting roll up times"
# setRollUpTimes(msiUserName,dbPasswd,fullName)
# print "Roll up times set in SQL database."

# print "Extracting classifications for capture events containing animals"
# extractNonEmptySubjects(snapshotFilePath,nonEmptyPath)
# print "Classifications extracted."

# print "Preparing season for analysis.."
# os.chdir(classificationsPath)
# prepSeason(seasonNbr,nonEmptyPath)
# print "Season prepared."

# print "Moving season csv to non-blank classifications folder..."
# old_path = classificationsPath+"/season_"+seasonNbr+".csv"
# new_path = classificationsPath+"/non-blank_classifications/season_"+seasonNbr+".csv"
# os.rename(old_path,new_path)
# #os.rename(classificationsPath+"/season_"+seasonNbr+".csv",classificationsPath+"/non-blank_classifications/"+"season_"+seasonNbr+".csv")

# print "Anonymizing users.."
# os.chdir(sharedDir)
# createUsersHashTable(snapshotFilePath,userHashPath)
# print "Users anonymized."

# print "Calculating consensus vote"
# getPluralityConsensus(nonBlankPath+"/season_"+seasonNbr+".csv",consensusPath+"/season_"+seasonNbr+"_plurality.csv")
# print "Consensus calculated"

# print "Getting blank capture events"
# os.chdir(classificationsPath)
# getBlankCaptures(snapshotFilePath,consensusPath+"/season_"+seasonNbr+"_blanks.csv")
# print "Blank capture events recorded."

# print "Comparing capture events in SSDB to Zooniverse"
# print "Season number is: "+seasonNbr
# print "Exporting season to file..."
# exportSeason(seasonNbr,sharedDir+"/data/link_to_zoon_id/S"+seasonNbr+"_db_captures.csv")
# print "Season has been exported."
# os.chdir(classificationsPath)

#snapshotCaptureExtract(classificationsPath+"/Zooniverse_downloads/snapshot_S"+seasonNbr+".csv",classificationsPath+"/capture_to_ZoonID/snapshot_S"+seasonNbr+"_unique_captures.csv")

# compareCaptures(sharedDir+"/data/link_to_zoon_id/S"+seasonNbr+"_db_captures.csv"
#  						,classificationsPath+"/capture_to_ZoonID/snapshot_S"+seasonNbr+"_unique_captures.csv"
#  						,sharedDir+"/data/link_to_zoon_id/S"+seasonNbr+"_links.csv")
# print "SSDB has been compared to Zooniverse"

#print "Adding new users to the database"
#addUsers(sharedDir+"/data/users/S"+seasonNbr+"_hashes_all_users.csv")
#scriptsPath = '/Users/Axl/Desktop/SerengetiPart2/scripts'
#os.chdir(scriptsPath)
#os.system("./add-Users.py ../data/users/S"+seasonNbr+"_hashes_all_users.csv "+mySqlHost+" "+msiUserName+" "+dbPasswd+" "+mySqlSchema+" "+fullName+" > ../data/users/upload_log_S"+seasonNbr+".txt")
#print "New users added"

# print "Transforming raw classifications into importable file"
# os.chdir(scriptsPath)
# os.system("./transform-ZooniverseClassifications.py "+snapshotFilePath+" ../data/zoon_classifications/S"+seasonNbr+"_trans.csv "+mySqlHost+" "+msiUserName+" "+dbPasswd+" "+mySqlSchema+" > ../data/zoon_classifications/log/log_S"+seasonNbr+".txt")
# print "Transformed..."

# print "Uploading Zooniverse classifications to database"
# os.chdir(scriptsPath)
# os.system("./load-Links.py ../data/link_to_zoon_id/S"+seasonNbr+"_links.csv "+mySqlHost+" "+msiUserName+" "+dbPasswd+" "+mySqlSchema+" "+fullName+" > "  "../data/link_to_zoon_id/upload_log_S"+seasonNbr+".txt")
# print "Uploaded"

# print "Uploading Consensus classifications to database"
# os.chdir(scriptsPath)
# os.system("./load-ConsensusClassifications.py ../data/consensus_classifications/season_"+seasonNbr+"_plurality.csv "+mySqlHost+" "+msiUserName+" "+dbPasswd+" "+mySqlSchema+" "+fullName+" > " "../data/consensus_classifications/upload_plurality_log_S"+seasonNbr+".txt")
# print "Uploaded"

# print "Uploading Blank classifications to database"
# os.chdir(scriptsPath)
# os.system("./load-ConsensusBlanks.py ../data/consensus_classifications/season_"+seasonNbr+"_blanks.csv "+mySqlHost+" "+msiUserName+" "+dbPasswd+" "+mySqlSchema+" "+fullName+" > " "../data/consensus_classifications/upload_blanks_log_S"+seasonNbr+".txt")
# print "Uploaded"

# print "Generate final report"
# os.chdir(sharedDir)
# speciesCount(sharedDir+"/data/consensus_classifications/season_"+seasonNbr+"_plurality.csv",sharedDir+"/classifications_data/species_stats/season_"+seasonNbr+"_stats.csv")
# print "Final report generated!"

#------------------------------------------------------------------------------------