#!/usr/bin/python

import sys
import csv

# get file names from command prompt
if len(sys.argv) < 3 :
    print ("format: file_divide_1_to_6.py <season> <infile>")
    exit(1)

season = sys.argv[1]
infilename = sys.argv[2]

infile = open(infilename, 'rb')
filereader = csv.reader(infile, delimiter=',', quotechar='"')

outfilename ="snapshot_" + season + ".csv"
outfile = open(outfilename,'wb')
filewriter = csv.writer(outfile, delimiter=',', quotechar='"',
                       quoting=csv.QUOTE_ALL)

# header line
line = filereader.next()
filewriter.writerow(line)
    
for line in filereader:
    if line[6] == season:
        filewriter.writerow(line)
        
infile.close()
outfile.close()
