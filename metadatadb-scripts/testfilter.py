import os,sys,csv

def filterSnapshot(snapshotFilePath,outFilePath,seasonNbr):
	with open(snapshotFilePath,'r') as fin, open (outFilePath,'w') as fout:
		writer = csv.writer(fout, delimiter=',')
		for row in csv.reader(fin, delimiter=','):
			if row[6] == 'S'+seasonNbr or row[6] == 'season':
				print row[6]
				writer.writerow(row)

filterSnapshot(sys.argv[1],sys.argv[2],sys.argv[3])