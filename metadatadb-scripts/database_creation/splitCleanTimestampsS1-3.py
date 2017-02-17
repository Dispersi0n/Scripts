#!/usr/bin/python

import sys

infilename = "./S1-3_cleaned.csv"
ofname1 = "./S1_cleaned.csv"
ofname2 = "./S2_cleaned.csv"
ofname3 = "./S3_cleaned.csv"

infile = open(infilename)
ofile1 = open(ofname1,'w')
ofile2 = open(ofname2,'w')
ofile3 = open(ofname3,'w')

header = infile.readline()
ofile1.write(header)
ofile2.write(header)
ofile3.write(header)

for line in infile:

    tokens = line.split(',')

    if tokens[1]=="1":
        ofile1.write(line)
    elif tokens[1]=="2":
        ofile2.write(line)
    elif tokens[1]=="3":
        ofile3.write(line)
    else:
        print("Nonconforming line:\n")
        print(line)

infile.close()
ofile1.close()
ofile2.close()
ofile3.close()
