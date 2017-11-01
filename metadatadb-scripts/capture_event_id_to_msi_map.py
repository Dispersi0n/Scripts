import os
import csv
import pandas as pd
import sys
import MySQLdb

# This script takes a snapshot file from Zooniverse and maps the capture events in MSI to the correct spots in the csv.
# This script was needed after season 9 had every row in the "capture_event_id" column at Zooniverse listed as "tutorial"

if sys.argv < 2:
	print("Usage: capture_event_id_to_msi_map.py <snapshotFile>")
	exit(1)

snapshotFile = sys.argv[1]

# Get database credentials
mySqlHost = "localhost"
mySqlSchema = "packerc_snapshot_serengeti"
msiUserName = "alexrose"
dbPasswd = "Y260xCbl2RAQ"

# Read in csv file
df = pd.read_csv(snapshotFile)

def execute(command):
 	#print(command)
 	cur.execute(command)
 	return

try:
    # connect to the database
	db = MySQLdb.connect(host=mySqlHost,
						user=msiUserName,
						passwd=dbPasswd,
						db=mySqlSchema)

    # use the database
	with db:
		for i,row in enumerate(df.itertuples(),0):
			# Gather some housekeeping for finding accepted timestamp for capture event inside csv
			TimeStampsTemp = str(row.timestamps)
			TimeStampAcceptedArray = TimeStampsTemp.split(";")
			
			# Set variables to get capture event ID from database
			event_id = str(row.capture_event_id)
			GridCell = str(row.site)
			RollNumber = str(row.roll)
			TimeStampAccepted = str(TimeStampAcceptedArray[0])
			cur=db.cursor()
			command = ("select distinct d.idCaptureEvent "+
						"from CaptureEvents d "+
						"join Rolls a on a.idRoll = d.Roll "+
						"join Images b on d.idCaptureEvent = b.CaptureEvent "+
						"join Sites c on a.Site = c.idSite "+
						"where a.Season=9 "
						"and c.GridCell = \""+str(GridCell)+"\""+
	 					"and a.RollNumber= \""+str(RollNumber)+"\""+
	 					"and b.TimeStampAccepted = \""+str(TimeStampAccepted)+"\"")
			execute(command)
			result = cur.fetchall()
			for resultRow in result:
				print str(i)+","+str(resultRow[0])
				#df.at[row,'capture_event_id'] = str(resultRow[0])
				df.set_value(i,'capture_event_id',str(resultRow[0]))
		df.to_csv(snapshotFile,index=False)


except Exception as e:
	print(e)
