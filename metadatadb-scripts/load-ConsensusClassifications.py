#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB
import datetime
import csv

# make sure we have 2 arguments
if len(sys.argv) < 2 :
    print ("format: load-ConsensusClassifications <infile>")
    exit(1)

infilename = sys.argv[1]
mysqlhost = sys.argv[2]
mysqluser = sys.argv[3]
mysqlpass = sys.argv[4]
mysqldb = sys.argv[5]
name = sys.argv[6]

try:
    # connect to the database
    db = MySQLdb.connect(host=mysqlhost,
                         user=mysqluser,
                         passwd=mysqlpass,
                         db=mysqldb,
                         local_infile=1)

    # use the database
    with db:
        
        snapshotDB.cur = db.cursor()
        snapshotDB.addConsensusClassifications(infilename)
  
        # make a note in the log
        snapshotDB.log(name,
                       "Loaded consensus classifications in " +
                       str(infilename))

# catch errors
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)


# close connection to the database
finally:
    if db:
        db.close()
            

