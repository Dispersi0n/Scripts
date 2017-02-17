#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB
import datetime
import csv


# make sure we have 3 arguments
if len(sys.argv) < 3 :
    print ("format: add-Users <file> <algorithm>")
    exit(1)

infilename = sys.argv[1]
algorithm = sys.argv[2]

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

        last_consensus = -1
  
        # go through each line in the file
        for line in filereader:
     
            zoonid = line[0]
            #capture_event = line[1]
            retire_reason = line[2]
            #seasonnum = line[3]
            #site = line[4]
            #rollnum = line[5]
            #image_name = line[6]
            num_of_classifications = line[7]
            num_of_votes = line[8]
            num_of_blanks = line[9]
            pielou = line[10]
            num_of_species = line[11]
            species_index = line[12]
            species = line[13]
            species_votes = line[14]
            species_count_min = line[16]
            species_count_median = line[17]
            species_count_max = line[18]
            standing = line[19]
            resting = line[20]
            moving = line[21]
            eating = line[22]
            interacting = line[23]
            babies = line[24]
            
            try:
                # look up capture by zooniverse ID
                captureID = snapshotDB.getCaptureEventFromZooniverseID(zoonid)

                # look up or create consensus for this capture
                consensusID = snapshotDB.addConsensus(captureID,retire_reason,
                                                      num_of_classifications,
                                                      num_of_votes,num_of_blanks,
                                                      pielou,num_of_species,
                                                      algorithm)

                if consensusID == last_consensus:
                    vote_index = vote_index + 1
                else:
                    vote_index = 1
                    last_consensus = consensusID

                # look up the species
                speciesID = getSpecies(species)

                # create the vote
                snapshotDB.addVote(consensusID,vote_index,speciesID,
                                   species_votes,species_count_min,
                                   species_count_median,species_count_max,
                                   standing,resting,moving,eating,
                                   interacting,babies)
            
                
            except TypeError as e:
                print ("Error: Couldn't find image corresponding to line: " +
                       line)
         
        # make a note in the log
        snapshotDB.log("Margaret Kosmala",
                       "Added consensus classifications from file " +
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
            
