#!/usr/bin/python

import MySQLdb
import sys
import snapshotDB
import datetime
import csv

# make sure we have 2 arguments
if len(sys.argv) < 3 :
    print ("format: transform-ZooniverseClassifications <infile> <outfile>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]
mysqlhost = sys.argv[3]
mysqluser = sys.argv[4]
mysqlpass = sys.argv[5]
mysqldb = sys.argv[6]

# create dictionary for species
# hard-coded for speed
speciesDict = dict([('blank',1),
                    ('aardvark',2),
                    ('aardwolf',3),
                    ('baboon',4),
                    ('batEaredFox',5),
                    ('buffalo',6),
                    ('bushbuck',7),
                    ('caracal',8),
                    ('cheetah',9),
                    ('civet',10),
                    ('dikDik',11),
                    ('eland',12),
                    ('elephant',13),
                    ('gazelleGrants',14),
                    ('gazelleThomsons',15),
                    ('genet',16),
                    ('giraffe',17),
                    ('guineaFowl',18),
                    ('hare',19),
                    ('hartebeest',20),
                    ('hippopotamus',21),
                    ('honeyBadger',22),
                    ('human',23),
                    ('hyenaSpotted',24),
                    ('hyenaStriped',25),
                    ('impala',26),
                    ('jackal',27),
                    ('koriBustard',28),
                    ('leopard',29),
                    ('lionFemale',30),
                    ('lionMale',31),
                    ('mongoose',32),
                    ('ostrich',33),
                    ('otherBird',34),
                    ('porcupine',35),
                    ('reedbuck',36),
                    ('reptiles',37),
                    ('rhinoceros',38),
                    ('rodents',39),
                    ('secretaryBird',40),
                    ('serval',41),
                    ('topi',42),
                    ('vervetMonkey',43),
                    ('warthog',44),
                    ('waterbuck',45),
                    ('wildcat',46),
                    ('wildebeest',47),
                    ('zebra',48),
                    ('zorilla',49),
                    ('duiker',50),
                    ('steenbok',51),
                    ('cattle',52),
                    ('bat',53),
                    ('insectSpider',54),
                    ('vulture',55)])

userDict = dict()

try:
    # connect to the database
    db = MySQLdb.connect(host=mysqlhost,
                         user=mysqluser,
                         passwd=mysqlpass,
                         db=mysqldb,
                         local_infile=1)

    # open up the file
    infile = open(infilename,'rb')
    filereader = csv.reader(infile, delimiter=',', quotechar='"')

    outfile = open(outfilename,'w')
    filewriter = csv.writer(outfile, delimiter=',', quotechar='"')

    # use the database
    with db:
        snapshotDB.cur = db.cursor()

        # remove header line
        filereader.next()

        # write header line
        filewriter.writerow(["zoon_id","class_id","userID","classDateTime",
                            "speciesID","speciesCountID","stand","rest",
                            "move","eat","interact","babies"])

        # go through each line in the file
        for line in filereader:
     
            classid = line[0]
            uname = line[1]
            zoonid = line[2]
            createdat = line[4]
            species = line[11]
            spcount = line[12]
            standing = line[13]
            resting = line[14]
            moving = line[15]
            eating = line[16]
            interacting = line[17]
            babies = line[18]

            # look up user
            # save a local table for speed
            if uname in userDict:
                userID = userDict[uname]
            # look up and add to table if not found
            else:
                userID = snapshotDB.getUser(uname)
                if userID is None:
                    snapshotDB.addUser(uname,"")
                    print "Warning: user " + uname + " not found in database"
                    userID = snapshotDB.getUser(uname)
                userDict[uname] = userID

            # trim date-time to get rid of " UTC"
            cdat = createdat[:19]

            # look up species
            if species=="":
                species = "blank"
            #speciesID = snapshotDB.getSpecies(species)
            speciesID = speciesDict[species]

            # look up species count
            #countID = snapshotDB.getSpeciesCount(spcount)
            if spcount=="":
                countID = 0
            elif spcount=="11-50":
                countID = 11
            elif spcount=="51+":
                countID = 12
            else:
                countID = int(spcount)

            # convert true/false to 1/0
            if standing == "true":
                stand = 1
            else:
                stand = 0
            if resting == "true":
                rest = 1
            else:
                rest = 0
            if moving == "true":
                move = 1
            else:
                move = 0
            if eating == "true":
                eat = 1
            else:
                eat = 0
            if interacting == "true":
                interact = 1
            else:
                interact = 0
            if babies == "true":
                baby = 1
            else:
                baby = 0

            # write to the new file
            filewriter.writerow([zoonid,classid,userID,cdat,speciesID,
                               countID,stand,rest,move,eat,interact,baby])
            
 
    # close the file
    infile.close()
    outfile.close()

# catch errors
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)


# close connection to the database
finally:
    if db:
        db.close()
            

