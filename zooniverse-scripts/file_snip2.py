#!/usr/bin/python

import sys

infilename = sys.argv[1]
outfilename = sys.argv[2]
infile = open(infilename,'r')
outfile = open(outfilename,'w')


for i in range(30):
    line = infile.readline()
    outfile.write(line)


infile.close()
outfile.close()
