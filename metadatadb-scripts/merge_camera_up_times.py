#!/usr/bin/python

import sys
import csv

# make sure we have 4 arguments
if len(sys.argv) < 3:
    print ("format: get_blank_captures <in_data_file> <out_data_file>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

infile = open(infilename,'rb')
filereader = csv.reader(infile, delimiter=',', quotechar='"')
outfile = open(outfilename,'w')
filewriter = csv.writer(outfile, delimiter=',', quotechar='"')

# header line
filereader.next()

oldline = ['GridCell','StartDate','StopDate']
for entry in filereader:
    if entry[0] == oldline[0] and entry[1] == oldline[2]:
        oldline[2] = entry[2]
    else:
        filewriter.writerow(oldline)
        oldline = entry
filewriter.writerow(oldline)
   

outfile.close()
infile.close()
