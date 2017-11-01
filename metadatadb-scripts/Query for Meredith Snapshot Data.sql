select idCaptureEvent as "CaptureEventID",
		TimeStampAccepted as "DateTime",
		GridCell as "SiteID",
		CoordinateX as "LocationX",
		CoordinateY as "LocationY",
		Species,
		SpeciesCount,
		Standing,
		Resting,
		Moving,
		Eating,
		Interacting,
		Babies,
		PielouEvenness,
		NumberOfSpecies,
		Season
from CaptureEvents,Images,ConsensusClassifications,ConsensusVotes,Rolls,Sites--,ZooniverseClassifications


captureevents + images on Images.CaptureEvent = CaptureEvents.idCaptureEvent
+ ConsensusClassifications on 



select a.idCaptureEvent as "CaptureEventID",
		g.ZooniverseIdentifier,
		b.TimeStampAccepted as "DateTime",
		f.GridCell as "SiteID",
		f.CoordinateX as "LocationX",
		f.CoordinateY as "LocationY",
		d.Species,
		d.Standing,
		d.Resting,
		d.Moving,
		d.Eating,
		d.Interacting,
		d.Babies,
		c.PielouEvenness,
		c.NumberOfSpecies,
		CONCAT("S",e.Season)
from CaptureEvents a
JOIN Images b
	on a.idCaptureEvent = b.CaptureEvent 
JOIN ConsensusClassifications c
	on a.idCaptureEvent = c.Capture 
JOIN ConsensusVotes d
	on c.idClassifications = d.idConsensusVotes
JOIN Rolls e
	on a.Roll = e.idRoll
JOIN Sites f
	on e.Site = f.idSite
JOIN CaptureEventsAndZooniverseIDs g
	on a.idCaptureEvent = g.Capture
limit 10;

----------- Final Working below -------------------

SELECT DISTINCT g.ZooniverseIdentifier as "CaptureEventID"
		, DATE_FORMAT(b.TimeStampAccepted,"%m/%d/%y %H:%i") as "DateTime"
		, f.GridCell as "SiteID"
		, f.CoordinateX as "LocationX"
		, f.CoordinateY as "LocationY"
		, d.Species
		, d.CountMedian as "Count"
		, d.Standing
		, d.Resting
		, d.Moving
		, d.Eating
		, d.Interacting
		, d.Babies
		, c.PielouEvenness
		, c.NumberOfSpecies
		, CONCAT("S",e.Season) as "Season" 
FROM CaptureEvents a 
	JOIN Images b on a.idCaptureEvent = b.CaptureEvent 
	JOIN ConsensusClassifications c on a.idCaptureEvent = c.Capture 
	JOIN ConsensusVotes d on c.idClassifications = d.idConsensusVotes 
	JOIN Rolls e on a.Roll = e.idRoll 
	JOIN Sites f on e.Site = f.idSite 
	JOIN CaptureEventsAndZooniverseIDs g on a.idCaptureEvent = g.Capture
WHERE e.Season = "4" 
LIMIT 10;

