#!/usr/bin/python

import MySQLdb
import sys
import csv
import snapshotDB

try:
    # connect to the database
    db = MySQLdb.connect(host="mysql.msi.umn.edu",
                         user="kosmala",
                         passwd="uvNaui5sg",
                         db="packerc_snapshot_serengeti")

    # open up the file
    infilename = "../metadata/site_checks.csv"
    infile = open(infilename)

    # use the database
    with db:
        snapshotDB.cur = db.cursor()

        # get rid of the header line in the file
        infile.readline()

        # read file as a properly formed .csv file
        csvread = csv.reader(infile)      
 
        # go through each line in the file
        for tokens in csvread:

            # we've got to be able to parse CSV files. There are "s in there.

            #chomp and parse
            #line = line.rstrip()
            #tokens = line.split(',')
            
            accessID = tokens[0]
            season = tokens[1]
            dateCheck = tokens[2]
            site = tokens[3]
            # ignore "check number" [4]
            siteComments = tokens[5]
            action = tokens[6]
            dateUpload = tokens[7]
            upload = tokens[8]
            # ignore "species" [9]
            initials = tokens[10]
            timeChange = tokens[11]
            timeFrom = tokens[12]
            timeTo = tokens[13]
            moreComments = tokens[14]

            # combine comments
            comments = ""
            if siteComments != "":
                if moreComments != "":
                    comments = siteComments + ". " + moreComments
                else:
                    comments = siteComments
            elif moreComments != "":
                comments = moreComments

            actionNum=""
            uploadNum=""
            if action!="": actionNum = int(action)
            if upload!="": uploadNum = int(upload)

            # put in the data
            snapshotDB.addSiteCheck(accessID,season,site,initials,dateCheck,dateUpload,
                                    actionNum,uploadNum,timeChange,timeFrom,timeTo,
                                    comments)

        # make a note in the log
        snapshotDB.log("Margaret Kosmala","Initialized SiteChecks table")
 
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
            

