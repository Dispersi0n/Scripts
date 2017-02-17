#!/usr/bin/python

import sys
import csv

# make sure we have 3 arguments
if len(sys.argv) < 3:
    print ("format: get_blank_captures <in_data_file> <out_data_file>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

# set of unique zooniverse IDs that retired with 'blank' or 'blank_consensus'
blanks = set()

# first go through and grab all the capture events that finished
# as 'blank' or 'blank_consensus'
with open(infilename, 'rb') as infile:

    # set up CSV reader
    filereader = csv.reader(infile, delimiter=',', quotechar='"')

    for line in filereader:
        if line[5] == "blank" or line[5] == "blank_consensus":
            blanks.add(line[2])

# keep statistics on each capture
stats = dict.fromkeys(blanks)

with open(infilename, 'rb') as infile:

    # set up CSV reader and writer
    filereader = csv.reader(infile, delimiter=',', quotechar='"')

    # header line
    filereader.next()

    # go through and do stats on all the classifications
    for line in filereader:
        zoonid = line[2]
        if zoonid in blanks:

            # create a new stats field if necessary
            if stats[zoonid] is None:
                stats[zoonid] = ["",0,0]

            # and add the stats
            stats[zoonid][1] = stats[zoonid][1] + 1
            if line[5] != "none":
                stats[zoonid][0] = line[5]
            if line[11] == "":
                stats[zoonid][2] = stats[zoonid][2] + 1         
                

# write results
with open(outfilename,'wb') as outfile:
                
    filewriter = csv.writer(outfile, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_NONE) 
    filewriter.writerow(["zooniverse_id","reason","num_class","num_blanks"])

    sorted_stats = sorted(stats.keys())
    for key in sorted_stats:
        value = stats[key]
        filewriter.writerow([key,value[0],value[1],value[2]])



