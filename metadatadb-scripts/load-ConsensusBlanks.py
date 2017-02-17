#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB
import datetime
import csv

# make sure we have 2 arguments
if len(sys.argv) < 2 :
    print ("format: load-ConsensusBlanks <infile>")
    exit(1)

infilename = sys.argv[1]

try:
    # connect to the database
    db = MySQLdb.connect(host="mysql.msi.umn.edu",
                         user="kosmala",
                         passwd="uvNaui5sg",
                         db="packerc_snapshot_serengeti")

    # use the database
    with db:
        
        snapshotDB.cur = db.cursor()
        snapshotDB.addConsensusBlanks(infilename)
  
        # make a note in the log
        snapshotDB.log("Margaret Kosmala",
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
            

