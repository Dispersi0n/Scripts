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
     
            uname = line[0]
            uhash = line[1]

            userID = snapshotDB.getUser(uname)
            if userID == None:
                snapshotDB.addUser(uname,uhash)
                
        # make a note in the log
        snapshotDB.log("Margaret Kosmala",
                       "Added users from file " +
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
            

