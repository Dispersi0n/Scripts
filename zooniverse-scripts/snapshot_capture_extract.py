#!/usr/bin/python

# this script takes as input the classifications data dump from Zooniverse
# typically named snapshot_SX.csv

# it creates a new file that lists all the "captures" uniquely, and sorted

import sys
import csv

if len(sys.argv) < 3:
    print ("format: snapshot_capture_extract.py <in_data_file> <out_data_file>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

infile = open(infilename,'rb')
filereader = csv.reader(infile, delimiter=',', quotechar='"')
outfile = open(outfilename,'w')

# write header for out file
outfile.write("Season,Site,Roll,Capture,ImageNum,ImageName,Zooniverse_ID\n")

# get rid of header line in infile
filereader.next()

# list of what we've already done
done = set()

# list of output lines
outlist = list()

# read each line
for line in filereader:

    # record each zooniverse_id and don't redo ones we've already done
    if line[2] not in done:
        done.update([line[2]])

        # how many images? count the semicolons
        images = line[9].split(';')
        
        ctr = 1
        for im in images:
            outline = line[6][1:],line[7],line[8][1:],line[3],str(ctr),im,line[2]
            outlist.append(outline)    
            ctr = ctr + 1

# now sort the output list
sorted_outlist = sorted(outlist, key=lambda x: (x[1],x[2],x[5]))

# and print to a file
filewriter = csv.writer(outfile) 
filewriter.writerows(sorted_outlist)

outfile.close()
infile.close()
