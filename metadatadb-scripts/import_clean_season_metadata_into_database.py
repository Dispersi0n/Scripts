#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB
import datetime
import csv

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
    db = MySQLdb.connect(host="localhost",
                         user=username,
                         passwd=password,
                         db="packerc_snapshot_serengeti",
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
            

