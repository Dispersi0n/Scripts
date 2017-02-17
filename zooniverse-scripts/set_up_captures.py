#!/usr/bin/python

import sys
from datetime import datetime

# subroutines for processing rolls
def process_capture(season,outfile,roll,capturenum,capture):
    
    imgnum = 0
    rootpath = ("S" + str(season) + "/" + capture[0][0] + "/" +
                capture[0][0] + "_R" + str(roll) + "/")
                
    for tokens in capture:
        imgnum = imgnum + 1
        imgpath = rootpath + tokens[2]
        outfile.write(str(season) + "," + tokens[0] + "," + str(roll) +
                      "," + str(capturenum) + "," + str(imgnum) + "," +
                      imgpath + "," + tokens[3] + "\n")
               
def compare_by_filename(a,b):
    return cmp(a[2],b[2])  # compare by filename

def get_total_seconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

# we pass in a bunch of parsed lines that are all in the same roll
def process_roll(season,outfile,errfile,rolldata):

    # turn roll identifier into an integer
    roll = int((rolldata[0][1])[1:3])

    # sort the data by filename
    rolldata.sort(compare_by_filename)

    # go through and group capture events by whether they are within 5 secs
    # of the first one
    capture = list()
    firstdtobj = datetime.strptime(rolldata[0][3],'%Y:%m:%d %H:%M:%S')
    counter = 1
    for tokens in rolldata:

        #print "   tokens[3] = " + tokens[3] + "\n"

        dtobj = datetime.strptime(tokens[3],'%Y:%m:%d %H:%M:%S')
        # check to see if it's part of same capture
        totsec = get_total_seconds(dtobj - firstdtobj)
        if (totsec < 5 and totsec >= 0):
            capture.append(tokens)
        # otherwise, process the old capture and start a new one
        else:
            process_capture(season,outfile,roll,counter,capture)

            # error if this image comes before the previous one
            if totsec < 0:
                errfile.write("Chronologic error in Image " + tokens[0] +
                              ", " + tokens[1] + ", " + tokens[2] +
                              ": " + str(dtobj) + " is before " +
                              str(firstdtobj) + "\n")
              
            # start new capture
            capture = list()
            capture.append(tokens)
            firstdtobj = datetime.strptime(tokens[3],'%Y:%m:%d %H:%M:%S')
            counter = counter + 1
            
            
    # process the last capture
    process_capture(season,outfile,roll,counter,capture)
    return


# ----
# MAIN
# ----

# make sure we have 4 arguments
# season should just be a number, without the 'S'
if len(sys.argv) < 4:
    print ("format: set_up_captures <season> <in_data_file> <out_data_file>")
    exit(1)

season = sys.argv[1]
infilename = sys.argv[2]
outfilename = sys.argv[3]

infile = open(infilename,'r')
outfile = open(outfilename,'w')
errfile = open(outfilename+"_err.txt",'w')

# write header line in the out file
outfile.write("Season, Site, Roll, Capture, Image, PathFilename, TimestampJPG\n")

# get rid of header line in the in file
infile.readline()

oldsite = ""
oldroll = ""
rolldata = list()

# read lines in the file
for line in infile:

    #print line

    # chomp and parse
    line = line.rstrip()
    tokens = line.split(',')

    site = tokens[0]
    roll = tokens[1]

    # check to see if we're in the same roll
    if (site == oldsite and roll == oldroll):
        # add to list
        rolldata.append(tokens)

    # new roll
    else:
        # process the last roll
        if (oldsite != ""):
            process_roll(season,outfile,errfile,rolldata)
        
        # clear out the roll data and set old vars
        rolldata = list()
        oldsite = site
        oldroll = roll

        # and add this line as the first one of this roll
        rolldata.append(tokens)

# at the very end, process the last roll
process_roll(season,outfile,errfile,rolldata)


outfile.close()
infile.close()
errfile.close()
