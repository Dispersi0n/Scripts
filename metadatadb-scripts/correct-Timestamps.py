#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB
import datetime


# make sure we have 3 arguments
if len(sys.argv) < 2 :
    print ("format: correct-Timestamps <file>")
    exit(1)

infilename = sys.argv[1]

try:
    # connect to the database
    db = MySQLdb.connect(host="mysql.msi.umn.edu",
                         user="kosmala",
                         passwd="uvNaui5sg",
                         db="packerc_snapshot_serengeti")

    # open up the file
    infile = open(infilename)

    # use the database
    with db:
        snapshotDB.cur = db.cursor()

        # get current day
        today = datetime.date.today()
        comment = "Corrected by script, " + str(today)

        # remove header line
        infile.readline()

        lastseason = 0
        lastsite = ""
        lastroll = 0
        lastcapture = 0

        # go through each line in the file
        for line in infile:

            #chomp and parse
            line = line.rstrip()
            tokens = line.split(',')
          
            seasonnum = tokens[0]
            site = tokens[1]
            rollnum = tokens[2]
            capturenum = tokens[3]
            imagenum = tokens[4]
            #path = tokens[5]
            newtimestamp = tokens[6]
            oldtime = tokens[7]
            invalid = tokens[8]
#            include = tokens[9]

            # timestamps to proper format
            oldtimestamp = oldtime[0:4] + "-" + oldtime[5:7] + "-" + oldtime[8:]

            same = 0
            if oldtimestamp == newtimestamp:
                same = 1

            try:
                # if new season, look it up
                if seasonnum != lastseason or site != lastsite:
                    siteID = snapshotDB.getSite(site)
                    rollID = snapshotDB.getRoll(seasonnum,siteID,rollnum)
                    captureID = snapshotDB.getCaptureEvent(rollID,capturenum)

                # if new roll, look it up
                elif rollnum != lastroll:
                    rollID = snapshotDB.getRoll(seasonnum,siteID,rollnum)
                    captureID = snapshotDB.getCaptureEvent(rollID,capturenum)

                # if new capture, look it up
                elif capturenum != lastcapture:
                    captureID = snapshotDB.getCaptureEvent(rollID,capturenum)

                # look up the image
                imageID = snapshotDB.getImage(captureID,imagenum)

                # if time didn't change (majority) update a field
                if same:
                    snapshotDB.confirmImageTimestamp(imageID,newtimestamp)
                # otherwise, update field and make a note
                else:
                    snapshotDB.correctImageTimestamp(imageID,newtimestamp,comment)

                if int(imagenum)==1:
                    snapshotDB.setCaptureTimestamp(captureID,newtimestamp,invalid)

                # update for speed
                lastseason = seasonnum
                lastsite = site
                lastroll = rollnum
                lastcapture = capturenum

            except TypeError as e:
                print ("Error: Couldn't find image corresponding to line: " +
                       line)
                
        # make a note in the log
        snapshotDB.log("Margaret Kosmala",
                       "Corrected timestamps for Season " + str(seasonnum))
 
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
            

