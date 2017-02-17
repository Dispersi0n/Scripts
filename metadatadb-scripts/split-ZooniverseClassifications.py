#!/usr/bin/python

import sys
import csv

# make sure we have 2 arguments
if len(sys.argv) < 3 :
    print ("format: split-ZooniverseClassifications <infile> <outfile>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

# open up the file
infile = open(infilename,'rb')
filereader = csv.reader(infile, delimiter=',', quotechar='"')

outfile = open(outfilename,'w')
filewriter = csv.writer(outfile, delimiter=',', quotechar='"')

#header
filewriter.writerow(filereader.next())

offon = 0
    
for line in filereader:

    if offon==1:
        filewriter.writerow(line)
        
    if line[2]=="ASG0002iqe":
        offon=1

# close the file
infile.close()
outfile.close()

