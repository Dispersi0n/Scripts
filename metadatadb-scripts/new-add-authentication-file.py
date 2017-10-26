#!/usr/bin/python

#import MySQLdb
import os
import getpass

#authfile_path = '/home/packerc/shared/metadata_db/scripts/auth_files'
authfile_path = '/Users/Axl/shared/metadata_db/scripts/auth_files'

# server = 'mysql.msi.umn.edu'
msiUserName = raw_input("Please enter your MSI username (x500): ")
dbPasswd = getpass.getpass("Please enter your database password (may be different from your MSI password): ")
# schema = 'packerc_snapshot_serengeti'


# try:
#     db = MySQLdb.connect(server, msiUserName, 
#                          dbPasswd, schema)
#     cursor = db.cursor()        
#     cursor.execute("SELECT VERSION()")
#     results = cursor.fetchone()
#     # Check if anything at all is returned
#     if results:
#         print "Connection Successful."
#     else:
#         print "Connection Failed, please contact help@msi.umn.edu to ask for access to packerc_snapshot_serengeti MySQL database."
#         break
# except MySQLdb.Error:
#     print "Connection Failed, please contact help@msi.umn.edu to ask for access to packerc_snapshot_serengeti MySQL database."
#     break

os.chdir(authfile_path)

#shortName = raw_input("Please enter a short, one-word name for yourself (ex. packer): ")
fullName = raw_input ("Please enter your first and last name (ex. Craig Packer): ")
fileName = "auth-" + msiUserName + ".txt"

# Open authentication file and write 3 lines
# 1st line is MSI Username (ex. packer)
# 2nd line is database password
# 3rd line is the user's full name (ex. Craig Packer)
f = open(fileName,"w+")
f.write(msiUserName+"\n")
f.write(dbPasswd+"\n")
f.write(fullName)
f.close()

# Set authentication file to be read only
# File is only accessible to the person running this script
os.chmod(fileName,0600)

print "Authentication file created successfully."