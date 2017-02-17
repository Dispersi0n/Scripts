#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB
import datetime


# make sure we have 3 arguments
if len(sys.argv) < 3 :
    print ("format: correct-Timestamps-S1-3 <infile> <outfile>")
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
        outfile.write("imageID,captureID,newtimestamp,invalid\n")

        lastseason = 0
        lastsite = ""
        lastroll = 0

        # go through each line in the file
        for line in infile:

            #chomp and parse
            line = line.rstrip()
            tokens = line.split(',')

#            access_capture = tokens[0]
            seasonnum = tokens[1]
            site = tokens[2]
            rollnum = tokens[3]
            imagename = tokens[4]
            newtimestamp = tokens[5]
            invalid = int(tokens[6])
            exclude = 0

            if imagename == "":
                exclude = 1

            try:

                if not exclude == 1:
                    
                    # if new season, look it up
                    if seasonnum != lastseason or site != lastsite:
                        siteID = snapshotDB.getSite(site)
                        rollID = snapshotDB.getRoll(seasonnum,siteID,rollnum)

                    # if new roll, look it up
                    elif rollnum != lastroll:
                        rollID = snapshotDB.getRoll(seasonnum,siteID,rollnum)

                    # get the correct capture
                    imagepath = ("S" + str(seasonnum) + "/" + site + "/" + site +
                                 "_R" + str(rollnum) + "/" + imagename)
                    imageID = snapshotDB.getImageFromImageName(imagepath)
                    captureID = snapshotDB.getCaptureEventFromImage(imageID)

                    outfile.write(str(imageID)+","+str(captureID)+","+newtimestamp+","+
                                  str(invalid))

                    #print ("invalid = ")
                    #print (invalid)
                    # set the time
#                    if invalid==0:
 #                       snapshotDB.confirmImageTimestamp(imageID,newtimestamp)
                        #print ("confirm")
                    # otherwise, update field and make a note
 #                   else:
  #                      snapshotDB.correctImageTimestamp(imageID,newtimestamp,comment)
                        #print ("correct")

                    # in either case, update the capture timestamp
  #                  snapshotDB.setCaptureTimestamp(captureID,newtimestamp,invalid)

                    # update for speed
                    lastseason = seasonnum
                    lastsite = site
                    lastroll = rollnum

            except TypeError as e:
                print ("Error: Couldn't find image corresponding to line: " +
                       line)
                
        # make a note in the log
        snapshotDB.log("Margaret Kosmala",
                       "Corrected timestamps for Seasons 1-3")
 
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
            

