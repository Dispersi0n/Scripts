#!/usr/bin/python

# This script takes as input 2 files:
# 1. a dump from the database for a season using export-season.py
# 2. the zooniverse unique capture file for a season
#
# Its job is to compare the two files and match up Zooniverse IDs
# to idCaptureEvents. The output is a file that can be directly
# imported to the CaptureEventsToZooniverseIDs table.
#
# The script expects the two input files to be sorted by
# site, roll, capture number, image name

import sys
import csv

def line_match(crow,zrow):

    # extract the image name from the path
    im = crow[6].split('/')[-1]

    # compare
    match = False
    if (crow[1]==zrow[0] and
        crow[2]==zrow[1] and
        crow[3]==zrow[2] and
        crow[4]==zrow[3] and
        crow[5]==zrow[4] and
        im==zrow[5]):
        match = True
    
    return match


def why_no_match(crow,zrow):

    # default return value
    to_ret = [0,""]
    
    if crow[1] < zrow[0]:
        to_ret[1] = "Capture from the wrong season here: "+str(crow)
        to_ret[0] = 2
    elif crow[1] > zrow[0]:
        to_ret[1] = "Zoon capture from the wrong season here: "+str(zrow)
        to_ret[0] = 1
    elif crow[2] < zrow[1]:
        to_ret[1] = "Site "+crow[2]+" has more images in DB than at Zooniverse"
        to_ret[0] = 2
    elif crow[2] > zrow[1]:
        to_ret[1] = "Site "+zrow[1]+" has fewer images in DB than at Zooniverse"
        to_ret[0] = 1
    elif crow[3] < zrow[2]:
        to_ret[1] = "Roll "+crow[2]+"_R"+crow[3]+" has more images in DB than at Zooniverse"
        to_ret[0] = 2
    elif crow[3] > zrow[2]:
        to_ret[1] = "Roll "+zrow[1]+"_R"+zrow[2]+" has fewer images in DB than at Zooniverse"
        to_ret[0] = 1
    elif crow[4] < zrow[3]:
        to_ret[1] = "Mismatch in captures. DB: "+str(crow)+". Zoon: "+str(zrow)
        to_ret[0] = 2
    elif crow[4] > zrow[3]:
        to_ret[1] = "Mismatch in captures. DB: "+str(crow)+". Zoon: "+str(zrow)
        to_ret[0] = 1
    elif crow[5] < zrow[4]:
        to_ret[1] = "Mismatch in images. DB: "+str(crow)+". Zoon: "+str(zrow)
        to_ret[0] = 2
    elif crow[5] > zrow[4]:
        to_ret[1] = "Mismatch in images. DB: "+str(crow)+". Zoon: "+str(zrow)
        to_ret[0] = 1
    elif crow[6].split('/')[-1] < zrow[5]:
        to_ret[1] = "Mismatch in image name. DB: "+str(crow)+". Zoon: "+str(zrow)
        to_ret[0] = 2
    elif crow[6].split('/')[-1] > zrow[5]:
        to_ret[1] = "Mismatch in image name. DB: "+str(crow)+". Zoon: "+str(zrow)
        to_ret[0] = 1

    return to_ret


        

#### MAIN ####

if len(sys.argv) < 4:
    print ("format: compare_captures.py <database_file> <zooniverse_unique_capture_file> <out_file>")
    exit(1)

capture_infilename = sys.argv[1]
zooniverse_infilename = sys.argv[2]
outfilename = sys.argv[3]
errfilename = outfilename + "_err.txt"

# store initial results in a big array
iresults = []
# store errors in array, too
errors = []

# read in the files and match them up
with open(capture_infilename,'rb') as capture_infile:
    with open(zooniverse_infilename,'rb') as zooniverse_infile:

        creader = csv.reader(capture_infile)
        zreader = csv.reader(zooniverse_infile)

        # ignore headers
        creader.next()
        zreader.next()

        # do the lines match?
        crow = creader.next()
        zrow = zreader.next()

        keepgoing = True

        while keepgoing:

            try:
        
                # yes! record the match
                if line_match(crow,zrow):
                    iresults.append((crow[0],zrow[6]))

                    crow = creader.next()
                    zrow = zreader.next()
                 
                # no. oh dear.
                else:
                    problem = why_no_match(crow,zrow)
                    todo = problem[0]
                    errors.append(problem[1])

                    # advance        
                    if todo==1:
                        zrow = zreader.next()
                    elif todo==2:
                        crow = creader.next()
                    else:
                        crow = creader.next()
                        zrow = zreader.next()

            # end of file
            except StopIteration:
                keepgoing = False
    
# now look at resulting array and see if there are any problems
# dedupe
deduped_results = list(set(iresults))

# sort by capture event
capture_sort = sorted(deduped_results, key=lambda tup: tup[0])

# is there every more than one?
prev = ""
for tup in capture_sort:
    if tup[0]==prev:
        errors.append("Capture event "+prev+" has multiple Zoon IDs")
    prev = tup[0]

# sort by zoon id
zoon_sort = sorted(deduped_results, key=lambda tup: tup[1])

# is there every more than one?
prev = ""
for tup in zoon_sort:
    if tup[0]==prev:
        errors.append("Zooniverse ID "+prev+" has multiple Capture IDs")
    prev = tup[0]

# write output file 
with open(outfilename,'wb') as outfile:
    owriter = csv.writer(outfile)
    owriter.writerow(["idCaptureEvent","Zooniverse_ID"])
    for tup in capture_sort:
        owriter.writerow(tup)

# write error file
with open(errfilename,'wb') as errfile:
    for line in errors:
        errfile.write(line+"\n")




