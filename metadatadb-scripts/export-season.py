#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB
import csv

# make sure we have 2 arguments
if len(sys.argv) < 3 :
    print ("format: export-season.py <season> <output file>")
    exit(1)

season = sys.argv[1]
outfilename = sys.argv[2]

try:
    # connect to the database
    db = MySQLdb.connect(host="mysql.msi.umn.edu",
                         user="kosmala",
                         passwd="uvNaui5sg",
                         db="packerc_snapshot_serengeti")

    # use the database
    with db:
        snapshotDB.cur = db.cursor()
        data = snapshotDB.exportSeasonCaptureEvents(season)

        # write the data to file
        with open(outfilename,'wb') as outfile:
            owriter = csv.writer(outfile)
            owriter.writerow(["idCaptureEvent","Season","GridCell","RollNumber","CaptureEventNum","SequenceNum","PathFilename"])

            for row in data:
                owriter.writerow(row)
                
      
# catch errors
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)


# close connection to the database
finally:
    if db:
        db.close()
            

