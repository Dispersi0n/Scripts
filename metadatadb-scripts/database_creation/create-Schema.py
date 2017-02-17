#!/usr/bin/python

import MySQLdb
import sys

try:
    # connect to the database
    db = MySQLdb.connect(host="mysql.msi.umn.edu",
                         user="kosmala",
                         passwd="uvNaui5sg",
                         db="packerc_snapshot_serengeti")

    # open up the file
    infilename = "schema-set-up.sql"
    infile = open(infilename)

    # use the database
    with db:
        cur = db.cursor()

        text = infile.read()
        statements = text.split(';')

        # go through each line in the file
        for stmt in statements:

            # print line
            print(stmt)

            # run sql lines
            if stmt!="":
                cur.execute(stmt)       
        
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
            

