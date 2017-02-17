#! /usr/bin/env python

import sys
import os
import tarfile

# get the season directory name from standard in
if len(sys.argv)!=2:
    print ("useage: tar-season.py <directory>")
    sys.exit(0)
else:

    # change to season path and get files and directories
    os.chdir("./"+sys.argv[1])
    
    dircontents = os.listdir(".")

    # for each thing in the directory, tar it if it's a directory
    for item in dircontents:

        if os.path.isdir("./"+item):

            tar = tarfile.open(item+".tar","w")
            tar.add("./"+item)
            tar.close()
