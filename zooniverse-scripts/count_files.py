#!/usr/bin/python

import sys
import os


# make sure we have 2 arguments
if len(sys.argv) < 2 :
    print ("format: count_files <dir>")
    exit(1)

basedir = sys.argv[1]

for dirname, dirnames, filenames in os.walk(basedir):

    if "_" in dirname:
        print dirname + "," + str(len(filenames))
        
