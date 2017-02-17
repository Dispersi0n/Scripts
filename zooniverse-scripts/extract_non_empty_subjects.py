#!/usr/bin/python

import sys
import csv

# get file names from command prompt
if len(sys.argv) < 3 :
    print ("format: extract_non_empty_subjects.py <infile> <outfile>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

# set of unique zooniverse IDs that retired with 'complete' or 'consensus'
nonblanks = set()

# first go through and grab all the capture events that finished
# as 'complete' or 'consensus'
with open(infilename, 'rb') as infile:

    # set up CSV reader
    filereader = csv.reader(infile, delimiter=',', quotechar='"')
    print "reading complete/consensus captures"

    for line in filereader:
        if line[5] == "complete" or line[5] == "consensus":
            nonblanks.add(line[2])

    print "all captures read"

# now go through and find all the classifications for the 'complete'
# and 'consensus' captures
with open(infilename, 'rb') as infile:
    with open(outfilename,'wb') as outfile:

        # set up CSV reader and writer
        filereader = csv.reader(infile, delimiter=',', quotechar='"')
        filewriter = csv.writer(outfile, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL)

        # header line
        filewriter.writerow(filereader.next())
        print "Finding classifications"

        for line in filereader:
            if line[2] in nonblanks:
                filewriter.writerow(line)

