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
    infilename = "../metadata/grid_cells.csv"
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
            gridx = tokens[1]
            gridy = tokens[2]

            snapshotDB.addGridCell(site,gridx,gridy)
        snapshotDB.log("Margaret Kosmala","Initialized GridCells table")
 
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
            
