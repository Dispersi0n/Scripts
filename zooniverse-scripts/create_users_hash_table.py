#!/usr/bin/python

import sys
import csv
import hashlib

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:38:13 2016

@author: User
"""

# input should be an exported Zooniverse file

# get file names from command prompt
if len(sys.argv) < 3 :
    print ("format: create_users_hash_table.py <infile> <outfile>")
    exit(1)

infilename = sys.argv[1]
hashfilename = sys.argv[2]

# a list of all users (unique)
userset = set()

with open(infilename, 'r') as infile:
    
    filereader = csv.reader(infile, delimiter=',', quotechar='"')

    # discard header
    filereader.next()
    
    # go through file and collect the users
    for row in filereader:
        userset.add(row[1])

# sort, hash, and print out
userlist = sorted(list(userset))

with open(hashfilename,'w') as hashfile:
    hashwriter = csv.writer(hashfile, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL)

    # header
    hashwriter.writerow(["user_name","user_hash"])

    for username in userlist:
        thehash = username
        if username[0:13] != "not-logged-in":
            thehash = hashlib.sha224(username[0:39]).hexdigest()
        
        hashwriter.writerow([username,thehash])

