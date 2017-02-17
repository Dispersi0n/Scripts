#!/usr/bin/python

import sys

if len(sys.argv) < 3:
    print ("format: species_count.py <in_data_file> <out_data_file>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

infile = open(infilename,'r')
outfile = open(outfilename,'w')

# get rid of header line in infile
infile.readline()

# create a list
dirs = []

# read each line
for line in infile:

    # chomp and parse
    line = line.rstrip()
    tokens = line.split(',')

    # get the site and camera
    site = tokens[0]
    cam = tokens[1]
    onedir = site + "_" + cam

    # see if it's in the list and add if not
    if not onedir in dirs:
        dirs.append(onedir)

# now sort the list
dirs.sort()

# and print it
for item in dirs:
    outfile.write(item + "\n")

outfile.close()
infile.close()


