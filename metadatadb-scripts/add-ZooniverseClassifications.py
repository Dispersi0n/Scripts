#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB
import datetime
import csv

# make sure we have 2 arguments
if len(sys.argv) < 2 :
    print ("format: add-Users <file>")
    exit(1)

infilename = sys.argv[1]

try:
    # connect to the database
    db = MySQLdb.connect(host="mysql.msi.umn.edu",
                         user="kosmala",
                         passwd="uvNaui5sg",
                         db="packerc_snapshot_serengeti")

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
     
            classid = line[0]
            uname = line[1]
            zoonid = line[2]
            createdat = line[4]
            print(createdat)
            species = line[11]
            spcount = line[12]
            standing = line[13]
            resting = line[14]
            moving = line[15]
            eating = line[16]
            interacting = line[17]
            babies = line[18]

            if species=="":
                species = "blank"

            # look up user
            userID = snapshotDB.getUser(uname)
            if userID is None:
                snapshotDB.addUser(uname,"")
                print "Warning: user " + uname + " not found in database"
                userID = snapshotDB.getUser(uname)

            # look up species
            speciesID = snapshotDB.getSpecies(species)

            # look up species count
            countID = snapshotDB.getSpeciesCount(spcount)

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
        
            # see if we can link to a capture
            #capture = snapshotDB.getCaptureEventFromZooniverseID(zoonid)
            #if capture is not None:
            #    snapshotDB.addZooniverseClassification(capture,zoonid,classid,
            #                                           userID,createdat,
            #                                           speciesID,countID,
            #                                           stand, rest, move,
            #                                           eat, interact, baby)
            #else:
            snapshotDB.addUnlinkedZooniverseClassification(zoonid,classid,
                                                       userID,createdat,
                                                       speciesID,countID,
                                                       stand, rest, move,
                                                       eat, interact, baby)
            #    print ("Warning: could not link to capture event for " +
            #           "Zooniverse ID " + zoonid)
                
        # make a note in the log
        snapshotDB.log("Margaret Kosmala",
                       "Added zooniverse classifications from file " +
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
            

