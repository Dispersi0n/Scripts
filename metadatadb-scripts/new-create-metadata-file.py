#!/usr/bin/python

import os
import datetime

#authfile_path = '/home/packerc/shared/metadata_db/metadata/seasons_files'
metadata_path = '/Users/Axl/shared/metadata_db/metadata/seasons_files'

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

# Get information about the season
seasonNbr = raw_input("\n"+"Please enter the season number: ")
seasonStartDate = raw_input("\n"+"Please enter the season's start date (format: yyyy-mm-dd): ")
validate(seasonStartDate)
seasonEndDate = raw_input("\n"+"Please enter the season's end date (format: yyyy-mm-dd): ")
validate(seasonEndDate)

while (seasonStartDate > seasonEndDate):
	print "ERROR: Season end date must be after season start date."
	seasonEndDate = raw_input("\n"+"Please enter the season's end date (format: yyyy-mm-dd): ")
	validate(seasonEndDate)


seasonComments = raw_input("Please enter your comments (500 characters max) about the season (ex. Retrieved by Alex): ")

# Change to the metadata directory
os.chdir(metadata_path)

# Set filename
fileName = "season" + seasonNbr + "meta.csv"

# Open authentication file and write header line
f = open(fileName,"w+")
f.write(seasonNbr+","+"\""+seasonStartDate+"\",\""+seasonEndDate+"\",\""+seasonComments+"\"")
f.close()

print "Season "+seasonNbr+" file created successfully."