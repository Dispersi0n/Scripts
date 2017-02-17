#!/usr/bin/python

import sys
import csv

# make sure we have 2 arguments
if len(sys.argv) < 2 :
    print ("format: check_captures <dir>")
    exit(1)

filename = sys.argv[1]

with open(filename,'rb') as fh:
    reader = csv.reader(fh,delimiter=',')
    reader.next()
    for row in reader:
       if row[1] != row[5][3:6]:
            print row

        
