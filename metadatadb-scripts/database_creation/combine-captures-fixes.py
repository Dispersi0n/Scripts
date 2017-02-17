#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB
import datetime


# make sure we have 2 arguments
if len(sys.argv) < 2 :
    print ("format: link-Captures-and-ZoonIDs-fixes <file>")
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

        # go through each line in the file
        for line in infile:

            #chomp and parse
            line = line.rstrip()
            tokens = line.split(',')
          
            capture1 = int(tokens[0])
            capture2 = int(tokens[1])

            try:
                snapshotDB.combineCaptures(capture1,capture2)

            except TypeError as e:
                print ("Error: Error combining captures corresponding to line: " +
                       line)
                
        # make a note in the log
        snapshotDB.log("Margaret Kosmala",
                       "Combined captures from file " +
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
            

