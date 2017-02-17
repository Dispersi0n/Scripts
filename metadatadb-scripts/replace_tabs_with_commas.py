#!/usr/bin/python

import sys
import csv
import operator

# make sure we have 4 arguments
if len(sys.argv) < 3:
    print ("format: replace_tabs_with_commas <in_data_file> <out_data_file>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

infile = open(infilename,'rb')
filereader = csv.reader(infile, delimiter='\t', quotechar='"')
outfile = open(outfilename,'w')
filewriter = csv.writer(outfile, delimiter=',', quotechar='"')

for line in filereader:
    filewriter.writerow(line)   

outfile.close()
infile.close()
