#!/usr/bin/python

import sys
import os.path
import os


# make sure we have 2 arguments
if len(sys.argv) < 2 :
    print ("format: count_files <dir>")
    exit(1)

#basedir = raw_input("What directory would you like to count?")
basedir = sys.argv[1]

## Season by season count of files. Run BEFORE AND AFTER renaming, and compare.
print "directory, allfiles, jpg_count, txt_count, vid_count"
for dirname, dirnames, filenames in os.walk(basedir):
  jpg_files = len([file for file in filenames if file.lower().endswith('.jpg')])
  vid_files = len([file for file in filenames if file.lower().endswith('.mp4')])
  text_files = len([file for file in filenames if file.lower().endswith('.txt')])
  if "_" in dirname:
    print dirname + "," + str(len(filenames)) + "," + str(jpg_files) + "," + str(text_files) + "," + str(vid_files)


#bad_sites = [site for site in site_list if re.match(site_regex, site) == None]
