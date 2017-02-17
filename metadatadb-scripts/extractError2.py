#!/usr/bin/python

import sys

# make sure we have 3 arguments
if len(sys.argv) < 3 :
    print ("format: extractError2 <infile> <outfile>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

infile = open(infilename)
outfile = open(outfilename,'w')

# remove header line
infile.readline()

# header line for outfile
outfile.write("Season,Site,Roll,CaptureNum,ZooniverseID\n")

for line in infile:

    line = line.rstrip()

    if line is not "":
        tokens = line.split(',')

        if tokens[0].startswith("Multiple"):
            outline = (tokens[1] + "," + tokens[2] + "," + tokens[3] +
                       "," + tokens[5] + "," + tokens[6])
            outfile.write(outline + "\n")

outfile.close()
infile.close()
