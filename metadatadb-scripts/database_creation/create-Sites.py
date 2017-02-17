#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB

try:
    # connect to the database
    db = MySQLdb.connect(host="mysql.msi.umn.edu",
                         user="kosmala",
                         passwd="uvNaui5sg",
                         db="packerc_snapshot_serengeti")

    # open up the file
    infilename = "../metadata/sites.csv"
    infile = open(infilename)

    # use the database
    with db:
        snapshotDB.cur = db.cursor()

        # get rid of the header line in the file
        infile.readline()

        # go through each line in the file
        for line in infile:

            #chomp and parse
            line = line.rstrip()
            tokens = line.split(',')
            
            site = tokens[0]
            current = tokens[1]
            dateset = tokens[2]
            gridx = tokens[3]
            gridy = tokens[4]
            altitude = tokens[5]
            trailq = tokens[6]
            traild = tokens[7]
            shade = tokens[8]
            trees = tokens[9]
            grass = tokens[10]
            poles = tokens[11]
            comments = tokens[12]

            # put in the data
            # NOTE: we don't have info on facing. Will need to add this later.
            # NOTE: we don't have info on the number of images of each site. To do later.
            snapshotDB.addSite(site,current,gridx,gridy,"X",dateset,
                               altitude,shade,grass,trees,poles,traild,trailq,"NULL",comments)

        # make a note in the log
        snapshotDB.log("Margaret Kosmala","Initialized Sites table")
 
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
            

