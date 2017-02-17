#!/usr/bin/python

import sys
import csv

# get file names from command prompt
if len(sys.argv) < 2 :
    print ("format: file_divide_1_to_6.py <infile>")
    exit(1)

infilename = sys.argv[1]

infile = open(infilename, 'rb')
filereader = csv.reader(infile, delimiter=',', quotechar='"')

outfile1 = open("snapshot_S1.csv",'wb')
outfile2 = open("snapshot_S2.csv",'wb')
outfile3 = open("snapshot_S3.csv",'wb')
outfile4 = open("snapshot_S4.csv",'wb')
outfile5 = open("snapshot_S5.csv",'wb')
outfile6 = open("snapshot_S6.csv",'wb')
filewriter1 = csv.writer(outfile1, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_ALL)
filewriter2 = csv.writer(outfile2, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_ALL)
filewriter3 = csv.writer(outfile3, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_ALL)
filewriter4 = csv.writer(outfile4, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_ALL)
filewriter5 = csv.writer(outfile5, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_ALL)
filewriter6 = csv.writer(outfile6, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_ALL)

# header line
line = filereader.next()
filewriter1.writerow(line)
filewriter2.writerow(line)
filewriter3.writerow(line)
filewriter4.writerow(line)
filewriter5.writerow(line)
filewriter6.writerow(line)
    
for line in filereader:
    if line[6] == "S1":
        filewriter1.writerow(line)
    elif line[6] == "S2":
        filewriter2.writerow(line)
    elif line[6] == "S3":
        filewriter3.writerow(line)
    elif line[6] == "S4":
        filewriter4.writerow(line)
    elif line[6] == "S5":
        filewriter5.writerow(line)
    elif line[6] == "S6":
        filewriter6.writerow(line)
    elif line[6] != "tutorial":
        print line
        
infile.close()

outfile1.close()
outfile2.close()
outfile3.close()
outfile4.close()
outfile5.close()
outfile6.close()
