import datetime
import re

def execute(command):
    print(command)
    cur.execute(command)
    return

def log(name,comments):
    "Adds an entry to the log"
    now = datetime.datetime.utcnow()
    command = "SELECT idPeople FROM People WHERE Name=\"" + name + "\""
    execute(command)
    result = cur.fetchone()
    # if that person isn't in the table, add it
    if result == None:
        print ("Person: " + name + " is not in People table. Adding person.")
        addPerson(name)
        command = "SELECT idPeople FROM People WHERE Name=\"" + name + "\""
        execute(command)
        result = cur.fetchone()
    person = result[0]        
    command = ("INSERT INTO Log (Person,Time,Notes) " +
               "VALUES (" + str(person) + ",\"" + str(now) +
               "\",\"" + comments + "\")")
    execute(command)
    return

def addPerson(name,initials):
    "Adds a researcher name to the people table"
    command = ("INSERT INTO People (Name,Initials) " +
               "VALUES (\"" + name + "\",\"" + initials + "\")")
    execute(command)
    return

def addGridCell(name,x,y,comments=""):
    "Adds a grid cell to the grid cell table"
    command = ("INSERT INTO GridCells " +
               "(idGridCell,CoordinateX,CoordinateY,Comments) " +
               "VALUES (\"" + name + "\"," + str(x) + "," + str(y) +
               ",\"" + comments + "\")")
    execute(command)
    return

def addSite(cell,current,x,y,face,dateset,alt,
            shade,grass,trees,poles,traild,trailq,images,comments):
    "Adds a site to the site table"
    command = ("INSERT INTO Sites " +
               "(GridCell,Current,CoordinateX,CoordinateY,Facing," +
               "EstablishmentDate,Altitude,Shade,Grass,Trees,Poles," +
               "TrailDistance,TrailQuality,NumImages,Comments) " +
               "VALUES (\"" + cell + "\"," + str(current) + "," +
               str(x) + "," + str(y) + ",\"" + face + "\",\"" + dateset +
               "\"," + str(alt) + "," + str(shade) + "," + grass + "," +
               trees + "," + poles + "," + traild + "," + trailq + "," +
               images + ",\"" + comments + "\")")
    execute(command)
    return
               
def addSeason(season,start,end,comments):
    "Adds a season to the seasons table"
    command = ("INSERT INTO Seasons " +
               "(idSeason,StartDate,EndDate,Comments) " +
               "VALUES (" + str(season) + ",\"" + start + "\",\"" +
               end + "\",\"" + comments + "\")")
    execute(command)
    return

def addZooniverseStatus(index,meaning):
    "Adds a status to the ZooniverseStatuses table"
    command = ("INSERT INTO ZooniverseStatuses " +
               "(idZooniverseStatuses,StatusDescription) " +
               "VALUES (" + str(index) + ",\"" + meaning + "\")")
    execute(command)
    return

def addTimestampStatus(index,meaning):
    "Adds a status to the TimestampStatus table"
    command = ("INSERT INTO TimestampStatuses " +
               "(idTimestampStatuses,StatusDescription) " +
               "VALUES (" + str(index) + ",\"" + meaning + "\")")
    execute(command)
    return

def addSpecies(species):
    "Adds a species to the Species table"
    command = ("INSERT INTO Species " +
               "(SpeciesName) " +
               "VALUES (\"" + species + "\")")
    execute(command)
    return

def addSpeciesCounts(index,meaning):
    "Adds a species count to the SpeciesCounts table"
    command = ("INSERT INTO SpeciesCounts " +
               "(idSpeciesCounts,CountDescription) " +
               "VALUES (" + str(index) + ",\"" + meaning + "\")")
    execute(command)
    return

def getActionText(num):
    "Looks up the text associated with an action number"
    action = ""
    if   num == 2: action = "Camera"
    elif num == 3: action = "Case"
    elif num == 4: action = "Pole"
    elif num == 5: action = "Replacement b/c Damaged"
    elif num == 6: action = "OK"
    elif num == 7: action = "Other"  
    return action

def getUploadText(num):
    "Looks up the text associated with an upload number"

    print num
    upload = ""
    if   num == 1: upload = "Ok"
    elif num == 2: upload = "Misfires"
    elif num == 4: upload = "Flash Broken"
    elif num == 5: upload = "Other"
    elif num == 6: upload = "No Card to Upload"
    elif num == 7: upload = "Upload Error"
    return upload

def lookupInitials(initials):
    "Looks up the initials for a researcher and returns the id"

    if initials=="":
        initials="UNK"
    command = "SELECT idPeople FROM People WHERE Initials=\"" + initials + "\""
    execute(command)
    result = cur.fetchone()
    if result == None:      
        # if the intials aren't in the database, add the ititals as name
        addPerson(initials,initials)
        execute(command)
        result = cur.fetchone()
    idname = result[0]
        
    return idname

def addSiteCheck(accessID,season,site,initials,dateCheck,dateUpload,
                 actionNum,uploadNum,timeChange,timeFrom,timeTo,comments):
    "Adds a site check to the SiteCheck table"
    
    # do lookups
    action = getActionText(actionNum)
    upload = getUploadText(uploadNum)
    person = lookupInitials(initials)            

    # make sure the site is valid
    command = "SELECT idSite FROM Sites WHERE GridCell=\"" + site + "\""
    execute(command)
    result = cur.fetchone()
    if result == None:
        print ("ERROR: " + site + " is not in database.")
        command = "SELECT idSite FROM Sites WHERE GridCell=\"UNK\""
        execute(command)
        result = cur.fetchone()    
    siteID = result[0]

    if accessID=="":
        accessIDstr="NULL"
    else:
        accessIDstr=str(accessID)

    if dateCheck=="":
        dateCheckstr="NULL"
    else:
        dateCheckstr="\"" + dateCheck + "\""

    if dateUpload=="":
        dateUploadstr="NULL"
    else:
        dateUploadstr="\"" + dateUpload + "\""

    if action=="":
        actionstr="NULL"
    else:
        actionstr="\"" + action + "\""

    if upload=="":
        uploadstr="NULL"
    else:
        uploadstr="\"" + upload + "\""

    if timeChange=="":
        timeChange="NULL"

    if timeFrom=="":
        timeFromstr="NULL"
    else:
        timeFromstr="\"" + timeFrom + "\""

    if timeTo=="":
        timeTostr="NULL"
    else:
        timeTostr="\"" + timeTo + "\""

    if comments=="":
        commentstr="NULL"
    else:
        # if the comments have double-quotes, we'll need to strip them out
        comments = re.sub('"','=',comments)
        commentstr="\"" + comments + "\""

    command = ("INSERT INTO SiteChecks " +
               "(AccessID,Site,Season,Researcher,DateChecked,DateUploaded," +
               "ActionNeeded,UploadComments,TimeChange,TimeDisplayedOnCheck," +
               "TimeActualOnCheck,Comments) " +
               "VALUES (" + accessIDstr + "," + str(siteID) + "," +
               str(season) + "," + str(person) + "," + dateCheckstr + "," +
               dateUploadstr + "," + actionstr + "," + uploadstr + "," +
               timeChange + "," + timeFromstr + "," + timeTostr +
               "," + commentstr + ")")
    execute(command)
    return

def addRoll(season,site,roll):
    "Adds a roll to the rolls table, if it's not already there"
    # get the siteid
    command = ("SELECT idSite FROM Sites WHERE GridCell=\"" + site + "\"" +
               " AND Current=TRUE")
    execute(command)
    result = cur.fetchone()
    if result == None:
        print ("ERROR: " + site + " is not in database.")
    else:
        siteID = result[0]

    # see if this roll already exists
    command = ("SELECT idRoll FROM Rolls WHERE Season=" + str(season) +
               " AND Site=" + str(siteID) + " AND RollNumber=" + str(roll))
    execute(command)
    result = cur.fetchone()
    # if not, add the roll
    if result == None:
        command = ("INSERT INTO Rolls (Season,Site,RollNumber) " +
                   "VALUES (" + str(season) + "," + str(siteID) + "," +
                   str(roll) + ")")
        execute(command)
        command = ("SELECT idRoll FROM Rolls WHERE Season=" + str(season) +
                   " AND Site=" + str(siteID) + " AND RollNumber=" + str(roll))
        execute(command)
        result = cur.fetchone()    
    return result[0]

def addCapture(rollID,capnum):
    "Adds a capture to the CaptureEvents table and returns its ID"

    # see if this capture already exists
    command = ("SELECT idCaptureEvent FROM CaptureEvents WHERE " +
               "Roll=" + str(rollID) + " AND CaptureEventNum=" +
               str(capnum))
    execute(command)
    result = cur.fetchone()
    if result != None:
        print ("ERROR: Capture already exists; Roll " + str(rollID) +
               ", Capture " + str(capnum) + "\n")
        exit(1)
      
    # create the capture event
    command = ("INSERT INTO CaptureEvents (Roll,CaptureEventNum" +
               ") VALUES (" + str(rollID) + "," + str(capnum) + ")")
    execute(command)

    # get its ID number
    command = ("SELECT idCaptureEvent FROM CaptureEvents WHERE " +
               "Roll=" + str(rollID) + " AND CaptureEventNum=" +
               str(capnum))
    execute(command)
    result = cur.fetchone()
    return result[0]


def addImage(captureID,imagenum,path,timestampjpg):
    "Add an image to the Images table"

    # create the image
    command = ("INSERT INTO Images (CaptureEvent,SequenceNum,PathFilename," +
               "TimestampJPG) VALUES " +
               "(" + str(captureID) + "," + str(imagenum) + ",\"" + path + "\",\"" +
               timestampjpg + "\")")
    execute(command)
    return

def addCaptureEventAndZooniverseID(captureID,zoonID):
    "Link captures with Zooniverse IDs"

    command = ("INSERT INTO CaptureEventsAndZooniverseIDs " +
               "(Capture,ZooniverseIdentifier) VALUES (" + str(captureID) +
               ",\"" + zoonID + "\")")
    execute(command)
    return     

def addUser(uname,uhash):
    "Add a user to the Users table"

    command = ("INSERT INTO Users (UserName,UserHash) VALUES (\"" +
               uname + "\",\"" + uhash + "\")")
    execute(command)
    return

def addZooniverseClassification(capture,zoonid,classid,userID,createdat,
                                speciesID,countID,stand,rest,move,eat,
                                interact,baby):
    "Add a classification to the ZooniverseClassifications table"

    command = ("INSERT INTO ZooniverseClassifications (Capture," +
               "ZooniverseIdentifier,ClassificationID,User," +
               "ClassificationDateTime,Species,SpeciesCount,Standing," +
               "Resting,Moving,Eating,Interacting,Babies) VALUES (" +
               str(capture) + ",\"" + zoonid + "\",\"" + classid + "\"," +
               str(userID) + ",\"" + createdat + "\"," + str(speciesID) +
               "," + str(countID) + "," + str(stand) + "," + str(rest) +
               "," + str(move) + "," + str(eat) + "," + str(interact) +
               "," + str(baby) + ")")
    execute(command)
    return

def addUnlinkedZooniverseClassification(zoonid,classid,userID,createdat,
                                        speciesID,countID,stand,rest,move,
                                        eat,interact,baby):
    "Add an unlinked classification to the ZooniverseClassifications table"

    command = ("INSERT INTO ZooniverseClassifications (" +
               "ZooniverseIdentifier,ClassificationID,User," +
               "ClassificationDateTime,Species,SpeciesCount,Standing," +
               "Resting,Moving,Eating,Interacting,Babies) VALUES (" +
                "\"" + zoonid + "\",\"" + classid + "\"," +
               str(userID) + ",\"" + createdat + "\"," + str(speciesID) +
               "," + str(countID) + "," + str(stand) + "," + str(rest) +
               "," + str(move) + "," + str(eat) + "," + str(interact) +
               "," + str(baby) + ")")
    execute(command)
    return
 
def addManyUnlinkedZooniverseClassifications(file):
    "Add a file's worth of classificaitons to the ZooniverseClassifications table"

    command = ("LOAD DATA LOCAL INFILE \"" + file + "\" INTO TABLE "+
               "ZooniverseClassifications FIELDS TERMINATED BY ',' "+
               "ENCLOSED BY '' IGNORE 1 LINES " +
               "(ZooniverseIdentifier,ClassificationID,User,ClassificationDateTime," +
               "Species,SpeciesCount,Standing,Resting,Moving,Eating,Interacting,Babies)")

    execute(command)
    return

def addLinks(file):
    "Add a file's worth of links to the CaptureEventsAndZooniverseIDs table"

    command = ("LOAD DATA LOCAL INFILE \"" + file + "\" INTO TABLE "+
               "CaptureEventsAndZooniverseIDs FIELDS TERMINATED BY ',' "+
               "ENCLOSED BY '' IGNORE 1 LINES " +
               "(Capture,ZooniverseIdentifier)")

    execute(command)
    return

def addConsensusBlanks(file):
    "Add a file's worth of consensus blanks to the ConsensusClassification table"

    # create a temporary table
    command = ("CREATE TEMPORARY TABLE IF NOT EXISTS temptable (" +
               "`ZoonID` VARCHAR(10) NOT NULL," +
               "`Retire` VARCHAR(16) NOT NULL," +
               "`NumClass` INT NOT NULL," +
               "`NumBlanks` INT NOT NULL)" +
               "ENGINE = InnoDB;")
    execute(command)

    # load the file               
    command = ("LOAD DATA LOCAL INFILE \"" + file + "\" INTO TABLE "+
               "temptable FIELDS TERMINATED BY ',' "+
               "ENCLOSED BY '' IGNORE 1 LINES " +
               "(ZoonID,Retire,NumClass,NumBlanks)")
    execute(command)
    
    # join so we have capture numbers
    command = ("CREATE TEMPORARY TABLE IF NOT EXISTS temptable2 " +
               "SELECT * FROM temptable JOIN CaptureEventsAndZooniverseIDs " +
               "ON temptable.ZoonID = CaptureEventsAndZooniverseIDs.ZooniverseIdentifier")
    execute(command)

    # add the rows to the consensusclassification table
    command = ("INSERT INTO ConsensusClassifications " +
               "(Capture,RetireReason,NumberOfClassifications,NumberOfVotes,NumberOfBlanks," +
               "PielouEvenness,NumberOfSpecies,ConsensusAlgorithm) " +
               "SELECT Capture,Retire,NumClass,0,NumBlanks,0,0,'blanks' " +
               "FROM temptable2")
    execute(command)


def addConsensusClassifications(file):
    "Add a files's worth of consensus classifications to the ConsensusClassifications and ConsensusVotes tables"

    # create a temporary table
    command = ("CREATE TEMPORARY TABLE IF NOT EXISTS temptable (" +
               "`ZoonID` VARCHAR(10) NOT NULL," +
               "`Retire` VARCHAR(16) NOT NULL," +
               "`NumClass` INT NOT NULL," +
               "`NumVotes` INT NOT NULL," +
               "`NumBlanks` INT NOT NULL," +
               "`Pielou` DOUBLE NOT NULL," +
               "`NumSpp` INT NOT NULL," +
               "`SppIndex` INT NOT NULL," +
               "`Spp` VARCHAR(24) NOT NULL," +
               "`SppVotes` INT NOT NULL," +
               "`CountMin` INT NOT NULL," +
               "`CountMedian` INT NOT NULL," +
               "`CountMax` INT NOT NULL," +
               "`Stand` DOUBLE NOT NULL," +
               "`Rest` DOUBLE NOT NULL," +
               "`Move` DOUBLE NOT NULL," +
               "`Eat` DOUBLE NOT NULL," +
               "`Interact` DOUBLE NOT NULL," +
               "`Baby` DOUBLE NOT NULL) " +
               "ENGINE = InnoDB;")
    execute(command)

    # load the file               
    command = ("LOAD DATA LOCAL INFILE \"" + file + "\" INTO TABLE "+
               "temptable FIELDS TERMINATED BY ',' "+
               "ENCLOSED BY '' IGNORE 1 LINES " +
               "(ZoonID,@ignore,Retire,@ignore,@ignore,@ignore,@ignore," +
               "NumClass,NumVotes,NumBlanks,Pielou,NumSpp,SppIndex,Spp," +
               "SppVotes,@ignore,CountMin,CountMedian,CountMax,Stand," +
               "Rest,Move,Eat,Interact,Baby)")
    execute(command)

    # join so we have capture numbers
    command = ("CREATE TEMPORARY TABLE IF NOT EXISTS temptable2 " +
               "SELECT * FROM temptable JOIN CaptureEventsAndZooniverseIDs " +
               "ON temptable.ZoonID = CaptureEventsAndZooniverseIDs.ZooniverseIdentifier")
    execute(command)

    # add the rows to the consensusclassification table
    command = ("INSERT INTO ConsensusClassifications " +
               "(Capture,RetireReason,NumberOfClassifications,NumberOfVotes,NumberOfBlanks," +
               "PielouEvenness,NumberOfSpecies,ConsensusAlgorithm) " +
               "SELECT distinct(Capture),Retire,NumClass,NumVotes,NumBlanks,Pielou,NumSpp,'plurality' " +
               "FROM temptable2")
    execute(command)

    # change column name to keep MySQL happy
    command = ("ALTER TABLE temptable2 CHANGE Capture CaptureID INT")
    execute(command)

    # get the table ID number for the consensusclassifications
    command = ("CREATE TEMPORARY TABLE IF NOT EXISTS temptable3 " +
               "SELECT idClassifications,SppIndex,Spp,SppVotes,CountMin,CountMedian,CountMax," +
               "Stand,Rest,Move,Eat,Interact,Baby " +
               "FROM ConsensusClassifications JOIN temptable2 " +
               "ON ConsensusClassifications.Capture = temptable2.CaptureID")
    execute(command)

    # and add the rows to the consensusvotes table
    command = ("INSERT INTO ConsensusVotes " +
               "(ConsensusClassification,VoteIndex,Species,NumberOfVotes," +
               "CountMin,CountMedian,CountMax," +
               "Standing,Resting,Moving,Eating,Interacting,Babies) " +
               "SELECT idClassifications,SppIndex,idSpecies,SppVotes," +
               "CountMin,CountMedian,CountMax," +
               "Stand,Rest,Move,Eat,Interact,Baby " +
               "FROM temptable3 JOIN Species " +
               "ON temptable3.Spp = Species.SpeciesName")
    execute(command)

    return                   
    
def getSite(site):
    "Get site ID by site name"

    command = ("SELECT idSite FROM Sites WHERE GridCell=\"" + site +
               "\" AND Current=1")
    execute(command)
    result = cur.fetchone()
    return result[0]
             
def getRoll(seasonID,siteID,rollnum):
    "Get roll ID by season ID, site ID, and roll number"

    command = ("SELECT idRoll FROM Rolls WHERE Season=" + str(seasonID) +
               " AND Site=" + str(siteID) + " AND RollNumber=" +
               str(rollnum))
    execute(command)
    result = cur.fetchone()
    return result[0]

def getCaptureEvent(rollID,capturenum):
    "Get CaptureEvent ID by roll ID and capture number"

    command = ("SELECT idCaptureEvent FROM CaptureEvents WHERE Roll=" +
               str(rollID) + " AND CaptureEventNum=" + str(capturenum))
    execute(command)
    result = cur.fetchone()
    return result[0]

def getImage(captureID,imagenum):
    "Get Image ID by capture ID and image number"

    command = ("SELECT idImage FROM Images WHERE CaptureEvent=" +
               str(captureID) + " AND SequenceNum=" + str(imagenum))
    execute(command)
    result = cur.fetchone()
    return result[0]
    
def confirmImageTimestamp(imageID,ts):
    "Set TimeStampAccepted field in Images"

    command = ("UPDATE Images SET TimestampAccepted=\"" + ts +
               "\" WHERE idImage=" + str(imageID))
    execute(command)
    return

def correctImageTimestamp(imageID,ts,comments):
    "Set TimeStampAccepted field in Images and add a comment"
    
    command = ("UPDATE Images SET TimestampAccepted=\"" + ts +
               "\", TimestampAcceptedNote=\"" + comments + 
               "\" WHERE idImage=" + str(imageID))
    execute(command)
    return

def setCaptureTimestamp(captureID,ts,inv):
    "Set CaptureTimestamp field in CaptureEvents"

    command = ("UPDATE CaptureEvents SET CaptureTimestamp=\"" + ts +
               "\", Invalid=" + str(inv) + " WHERE idCaptureEvent=" +
               str(captureID))
    execute(command)
    return

def getImageFromImageName(path):
    command = ("SELECT idImage FROM Images WHERE PathFilename=\"" +
               path + "\"")
    execute(command)
    result = cur.fetchone()
    return result[0]

def getCaptureEventFromImage(imageID):
    command = ("SELECT CaptureEvent FROM Images WHERE idImage=" +
               str(imageID))
    execute(command)
    result = cur.fetchone()
    return result[0]

def getUser(uname):
    "Get a user's ID number from the Users table"

    command = ("SELECT idUsers FROM Users WHERE UserName=\"" + uname + "\"")
    execute(command)
    result = cur.fetchone()
    if result == None:
        return None
    
    return result[0]

def getSpecies(species):
    "Get a species ID by species name"

    command = ("SELECT idSpecies FROM Species WHERE SpeciesName=\"" +
               species + "\"")
    execute(command)
    result = cur.fetchone()
    return result[0]
    
def getSpeciesCount(spcount):
    "Get a species count ID by species count number"

    command = ("SELECT idSpeciesCounts FROM SpeciesCounts WHERE " +
               "CountDescription=\"" + spcount + "\"")
    execute(command)
    result = cur.fetchone()
    return result[0]

def getCaptureEventFromZooniverseID(zoonid):
    "Get the corresponding capture event from a Zooniverse ID"

    command = ("SELECT Capture FROM CaptureEventsAndZooniverseIDs WHERE " +
               "ZooniverseIdentifier=\"" + zoonid + "\"")
    execute(command)
    result = cur.fetchone()
    return result[0]

    
def addConsensus(captureID,retire_reason,num_of_classifications,
                 num_of_votes,num_of_blanks,pielou,num_of_species,algorithm):
    "Look up the consensus and return it if it exists, else create it"

    # see if a consensus already exists for this capture
    command = ("SELECT idClassifications FROM ConsensusClassifications WHERE " +
               "Capture=" + str(captureID))
    execute(command)
    result = cur.fetchone()
    # if not, add it
    if result == None:
        command = ("INSERT INTO ConsensusClassifications (Capture," +
                   "RetireReason,NumberOfClassifications,NumberOfVotes," +
                   "NumberOfBlanks,PielouEvenness,NumberOfSpecies," +
                   "ConsensusAlgorithm) VALUES (" + str(captureID) + ",\"" +
                   retire_reason + "\"," + num_of_classifications, + "," +
                   num_of_votes + "," + num_of_blanks + "," + pielou + "," +
                   num_of_species + ",\"" + algorithm + "\")")
        execute(command)
        command = ("SELECT idClassifications FROM ConsensusClassifications WHERE " +
                   "Capture=" + str(captureID))
        execute(command)
        result = cur.fetchone()

    return result[0]

def addVote(consensusID,vote_index,speciesID,species_votes,
            species_count_min,species_count_median,species_count_max,
            standing,resting,moving,eating,interacting,babies):
    "Add a partial (1-species) consensus vote"

    command = ("INSERT INTO ConsensusVotes (ConsensusClassification," +
               "VoteIndex,Species,NumberOfVotes,CountMin,CountMedian," +
               "CountMax,Standing,Resting,Moving,Eating,Interacting," +
               "Babies) VALUES (" + str(consensusID) + "," + str(vote_index) +
               "," + str(speciesID) + "," + species_votes + "," +
               species_count_min + "," + species_count_median + "," +
               species_count_max + "," + standing + "," + resting + "," +
               moving + "," + eating + "," + interacting + "," + babies + ")")
    execute(command)
    return

def setZooniverseStatus(captureID,num):
    "Set the Zooniverse Status for a Capture Event"

    command = ("UPDATE CaptureEvents SET ZooniverseStatus=" + str(num) +
               " WHERE idCaptureEvent=" + str(captureID))
    execute(command)
    return

def combineCaptures(captureID1,captureID2):
    "Combine two captures by moving the second into the first and deleting the second"

    # get last image in sequence
    command = ("SELECT SequenceNum from Images WHERE CaptureEvent=" + str(captureID1))
    execute(command)
    lastImage = 0
    for row in cur:
        if row[0]>lastImage:
            lastImage=row[0]
 
    imageCounter = lastImage + 1
    
    # get new images and update their sequence numbers and the captureID
    command = ("SELECT idImage from Images WHERE CaptureEvent=" + str(captureID2))
    execute(command)
    for row in cur:
        newcommand = ("UPDATE Images SET SequenceNum=" + str(imageCounter) +
                      ", CaptureEvent=" + str(captureID1) +
                      " WHERE idImage=" + str(row[0]))
        execute(newcommand)
        imageCounter = imageCounter + 1

    # invalidate the second one
    command = ("UPDATE CaptureEvents SET Invalid=1 WHERE idCaptureEvent=" +
               str(captureID2))
    execute(command)
    
    return

def setRollUptime(rollID):
    "Set the StartDate and StopDate for a roll"

    command = ("SELECT DATE(MIN(CaptureTimestamp)),DATE(MAX(CaptureTimestamp)) " +
               "FROM Rolls JOIN CaptureEvents " +
               "ON CaptureEvents.Roll = Rolls.idRoll " +
               "WHERE idRoll=" + str(rollID) + " AND Invalid=0")
    execute(command)
    result = cur.fetchone()

    command = ("UPDATE Rolls " +
               "SET StartDate=" + result[0] + ",StopDate=" + result[1] + " " +
               "WHERE idRoll=" + str(rollID))
    execute(command)

    return

def setUptimeForAllRollsNeedingIt():
    "Set the StartDate and StopDate for all rolls that have nulls in those places"

    command = ("CREATE TEMPORARY TABLE IF NOT EXISTS temptable " +
               "SELECT idRoll,DATE(MIN(CaptureTimestamp)) AS mindate," +
               "DATE(MAX(CaptureTimestamp)) AS maxdate " +
               "FROM Rolls JOIN CaptureEvents " +
               "ON CaptureEvents.Roll = Rolls.idRoll " +
               "WHERE StartDate IS NULL AND Invalid=0 " +
               "GROUP BY 1")
    execute(command)

    command = ("UPDATE Rolls JOIN temptable " +
               "ON Rolls.idRoll = temptable.idRoll " +
               "SET StartDate=mindate,StopDate=maxdate")
    execute(command)

    return
    


    

# error checking scripts:
# * go through person table and look for person without initials or initials
#   are the same as the name
# * go through sitecheck table and look for ones where the site is listed as
#   "UNK"
# * when a seaon is finished, need to update the seasons table; we don't
#   know the end date ahead of time, but well may be adding site check
#   data before all the data is gathered
# * check where no JPG timestamp or where Z-URL is blank
# * we will need to reassociate captures with their proper sites. Right now
#   everything's being added to the "current" site.

    
