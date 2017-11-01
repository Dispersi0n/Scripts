-- This procedure takes a table that contains invalid capture_event_id and pieces together what the value should be
-- The procedure then replaces all values with the correct value.
-- Designed for season9 and snapshot_s9.csv, may require tweaking for future seasons.

CREATE PROCEDURE update_captures()
BEGIN

-- Variable Declaration
DECLARE temp_idCaptureEvent varchar(20);
DECLARE temp_idCaptureEvent_db varchar(20);
DECLARE temp_Season varchar(10);
DECLARE temp_Season_db varchar(5);
DECLARE temp_idRoll varchar(10);
DECLARE temp_idRoll_db varchar(20);
DECLARE temp_RollNumber varchar(10);
DECLARE temp_RollNumber_db varchar(20);
DECLARE temp_GridCell varchar(10);
DECLARE temp_GridCell_db varchar(20);
DECLARE temp_TimeStampAccepted datetime;
DECLARE temp_TimeStampAccepted_db datetime;
DECLARE rowCount int;
DECLARE i int;

SELECT COUNT(*) FROM temp_mapping3 INTO rowCount;
--SET rowCount = 1;
SET i = 0;

WHILE i < rowCount DO
	SET temp_TimeStampAccepted = (select distinct timestamps from temp_mapping3 where Done = "No" limit 1);
	SET temp_Season = (select distinct season from temp_mapping3 where Done = "No" limit 1);
	SET temp_RollNumber = (select distinct roll from temp_mapping3 where Done = "No" limit 1);
	SET temp_GridCell = (select distinct site from temp_mapping3 where Done = "No" limit 1);
	SELECT DISTINCT CONCAT('S',a.Season),a.RollNumber,c.GridCell,b.TimeStampAccepted,d.idCaptureEvent from CaptureEvents d join Rolls a on a.idRoll = d.Roll join Images b on d.idCaptureEvent = b.CaptureEvent join Sites c on a.Site = c.idSite where a.Season=(select substring(temp_Season FROM 2 FOR LENGTH(temp_Season))) and c.GridCell = temp_GridCell and a.RollNumber=temp_RollNumber and b.TimeStampAccepted = temp_TimeStampAccepted
	INTO temp_Season_db, temp_RollNumber_db, temp_GridCell_db, temp_TimeStampAccepted_db, temp_idCaptureEvent_db;
	UPDATE temp_mapping3 SET capture_event_id = temp_idCaptureEvent_db, Done = "Yes" WHERE season = temp_Season_db AND site = temp_GridCell_db AND roll = temp_RollNumber_db AND timestamps = temp_TimeStampAccepted_db;
	SET i = i + 1;
END WHILE;
End;
;;