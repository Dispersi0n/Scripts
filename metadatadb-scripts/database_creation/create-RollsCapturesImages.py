#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB


# make sure we have 3 arguments
if len(sys.argv) < 2 :
    print ("format: create-RollsCapturesImages <file>")
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

        # remove header line
        infile.readline()

        lastroll = ""
        lastcapture = 0
        # go through each line in the file
        for line in infile:

            #chomp and parse
            line = line.rstrip()
            tokens = line.split(',')

            #print "\n" + line
            
            seasonnum = tokens[0]
            site = tokens[1]
            rollnum = tokens[2]
            capture = tokens[3]
            imagenum = tokens[4]
            path = tokens[5]
            tsj = tokens[6]

            # convert timestamp to proper format
            timestampjpg = tsj[0:4] + "-" + tsj[5:7] + "-" + tsj[8:]

            # this roll, in brief
            thisroll = "S" + str(seasonnum) + site + "R" + str(rollnum)

            # need to create a new roll if it's a new roll
            if thisroll != lastroll:
                rollID = snapshotDB.addRoll(seasonnum,site,rollnum)

            # create the capture if it's a new capture
            if capture != lastcapture:
                captureID = snapshotDB.addCapture(rollID,capture)

            # create the image
            snapshotDB.addImage(captureID,imagenum,path,timestampjpg)

            # update for speed
            lastroll = thisroll
            lastcapture = capture
                
        # make a note in the log
        snapshotDB.log("Margaret Kosmala",
                       ("Filled in Rolls, CaptureEvents, and Images " +
                        "tables for Season " + str(seasonnum)))
 
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
            

