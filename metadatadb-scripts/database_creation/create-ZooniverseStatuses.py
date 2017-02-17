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
    infilename = "../metadata/zooniverse_statuses.csv"
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
            
            index = tokens[0]
            meaning = tokens[1]

            # put in the data
            snapshotDB.addZooniverseStatus(index,meaning)

        # make a note in the log
        snapshotDB.log("Margaret Kosmala","Initialized ZooniverseStatus table")
 
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
            

