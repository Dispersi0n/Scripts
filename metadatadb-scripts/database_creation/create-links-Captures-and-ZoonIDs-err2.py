#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB
import datetime


# make sure we have 2 arguments
if len(sys.argv) < 3 :
    print ("format: create-links-Captures-and-ZoonIDs-err2 <infile> <outfile>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

try:
    # connect to the database
    db = MySQLdb.connect(host="mysql.msi.umn.edu",
                         user="kosmala",
                         passwd="uvNaui5sg",
                         db="packerc_snapshot_serengeti")

    # open up the file
    infile = open(infilename)
    outfile = open(outfilename,'w')

    # use the database
    with db:
        snapshotDB.cur = db.cursor()

        # remove header line
        infile.readline()
        # write header line
        outfile.write("idCaptureEvent,ZoonID\n")

        lastseason = 0
        lastsite = ""
        lastroll = 0
        lastcapture = 0

        try:
            # go through each line in the file
            for line in infile:
    
                #chomp and parse
                line = line.rstrip()
                tokens = line.split(',')
          
                seasonnum = tokens[0]
                site = tokens[1]
                rollnum = tokens[2]
                capturenum = tokens[3]
                zoonid = tokens[4]

                # if new season, look it up
                if seasonnum != lastseason or site != lastsite:
                    siteID = snapshotDB.getSite(site)
                    rollID = snapshotDB.getRoll(seasonnum,siteID,rollnum)
 
                # if new roll, look it up
                elif rollnum != lastroll:
                    rollID = snapshotDB.getRoll(seasonnum,siteID,rollnum)

                # if new capture, look it up, and link
                if capturenum != lastcapture:

                    captureID = snapshotDB.getCaptureEvent(rollID,capturenum)
                    outfile.write(str(captureID)+","+zoonid+"\n")

                # update for speed
                lastseason = seasonnum
                lastsite = site
                lastroll = rollnum
                lastcapture = capturenum

        except TypeError as e:
            print ("Error: Couldn't find capture corresponding to line: " +
                    line)
                
        # make a note in the log
#        snapshotDB.log("Margaret Kosmala",
 #                      "Linked capture events and zooniverse IDs from file " +
  #                     str(infilename))
 
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
            

