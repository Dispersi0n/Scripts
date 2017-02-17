#!/usr/bin/python

import sys

if len(sys.argv) < 3:
    print ("format: species_count.py <in_data_file> <out_data_file>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

infile = open(infilename,'r')
outfile = open(outfilename,'w')

# write header for out file
outfile.write("Species,NumberOfCaptures\n")

# get rid of header line in infile
infile.readline()

# create the dictionary
sppdict = {}

# read each line
for line in infile:

    # chomp and parse
    line = line.rstrip()
    tokens = line.split(',')

    # get the species
    species = tokens[13]

    # count it
    if species in sppdict:
        sppdict[species] = sppdict[species] + 1
    else:
        sppdict[species] = 1

for key, val in sorted(sppdict.iteritems()):
    outfile.write(key + "," + str(val) + "\n")

outfile.close()
infile.close()
