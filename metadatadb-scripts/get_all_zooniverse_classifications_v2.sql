# just do valids from one season at a time
CREATE TEMPORARY TABLE IF NOT EXISTS table0 AS 
select idCaptureEvent from CaptureEvents join Rolls
on CaptureEvents.Roll = Rolls.idRoll
where Invalid=0;

# first identify all the ZoonIDs we need to select
CREATE TEMPORARY TABLE IF NOT EXISTS table1 AS 
select idCaptureEvent,ZooniverseIdentifier
from table0 join (CaptureEventsAndZooniverseIDs,ConsensusClassifications)
on ConsensusClassifications.Capture=CaptureEventsAndZooniverseIDs.Capture 
and ConsensusClassifications.Capture=table0.idCaptureEvent;

# next grab what's needed from the Zooniverse table
CREATE TEMPORARY TABLE IF NOT EXISTS table2 AS 
select ZooniverseClassifications.ZooniverseIdentifier,
ClassificationID,User,Species,SpeciesCount,
Standing,Resting,Moving,Eating,Interacting,Babies
from table1 join ZooniverseClassifications
on table1.ZooniverseIdentifier=ZooniverseClassifications.ZooniverseIdentifier;

# get the users
CREATE TEMPORARY TABLE IF NOT EXISTS table3 AS 
select ZooniverseIdentifier,
ClassificationID,
if(UserHash="",UserName,UserHash) as UserString,
Species,SpeciesCount,
Standing,Resting,Moving,Eating,Interacting,Babies
from table2 join Users
on table2.User=Users.idUsers;

# get the species
CREATE TEMPORARY TABLE IF NOT EXISTS table4 AS 
select ZooniverseIdentifier,
ClassificationID,UserString,SpeciesName,SpeciesCount,
Standing,Resting,Moving,Eating,Interacting,Babies
from table3 join Species
on table3.Species=Species.idSpecies;

# convert to desired output format
CREATE TEMPORARY TABLE IF NOT EXISTS table5 AS 
select ZooniverseIdentifier as CaptureEventID,
ClassificationID,
if(substring(UserString,1,14)='not-logged-in-',UserString,substring(UserString,1,32)) as UserID,
SpeciesName as Species,
SpeciesCount as Count,
Standing,Resting,Moving,Eating,Interacting,Babies
from table4
order by CaptureEventID,ClassificationID;

select * from table5;