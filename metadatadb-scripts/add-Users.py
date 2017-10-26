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
        snapshotDB.log(name,
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
            

