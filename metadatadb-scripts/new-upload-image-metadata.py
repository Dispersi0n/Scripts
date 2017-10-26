#!/usr/bin/python

import os
import datetime

# Get information about the season
seasonNbr = raw_input("\n"+"Please enter the season number: ")
msiUserName = raw_input("\n"+"Please enter your MSI user name (should match your authentication file): ")

#authfile_path = '/home/packerc/shared/metadata_db/scripts/logfiles'
log_path = '/Users/Axl/shared/metadata_db/scripts/logfiles'
scripts_path = '/Users/Axl/shared/metadata_db/scripts'
new_path = '/Users/Axl/shared/metadata_db/scripts/logfiles/S'+seasonNbr+"_meta_upload"

# Change to the metadata directory
os.chdir(log_path)
os.mkdir(new_path)

os.chdir(scripts_path)

os.system("./import_clean_season_metadata_into_database.py ./auth_files/auth-"+msiUserName+".txt ../metadata/seasons_files/season"+seasonNbr+"meta.csv ../../TimeStampCleaning/CleanedCaptures/S"+seasonNbr+"_cleaned.csv ./logfiles/S"+seasonNbr+"_meta_upload/ > ./logfiles/S"+seasonNbr+"_meta_upload/import_S"+seasonNbr+"_log.txt &")
