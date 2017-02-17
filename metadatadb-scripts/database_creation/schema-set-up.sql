SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `snapshot_meta` DEFAULT CHARACTER SET latin1 COLLATE latin1_general_ci ;
USE `snapshot_meta` ;

-- -----------------------------------------------------
-- Table `snapshot_meta`.`Seasons`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`Seasons` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`Seasons` (
  `idSeason` INT NOT NULL ,
  `StartDate` DATE NOT NULL ,
  `EndDate` DATE NOT NULL ,
  `Comments` VARCHAR(500) NULL ,
  PRIMARY KEY (`idSeason`) ,
  UNIQUE INDEX `idSeason_UNIQUE` (`idSeason` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`GridCells`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`GridCells` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`GridCells` (
  `idGridCell` VARCHAR(3) NOT NULL ,
  `CoordinateX` INT NOT NULL ,
  `CoordinateY` INT NOT NULL ,
  `Comments` VARCHAR(500) NULL ,
  PRIMARY KEY (`idGridCell`) ,
  UNIQUE INDEX `idGridCell_UNIQUE` (`idGridCell` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`Sites`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`Sites` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`Sites` (
  `idSite` INT NOT NULL AUTO_INCREMENT ,
  `GridCell` VARCHAR(3) NOT NULL ,
  `Current` TINYINT(1) NOT NULL ,
  `CoordinateX` INT NOT NULL ,
  `CoordinateY` INT NOT NULL ,
  `Facing` VARCHAR(3) NOT NULL ,
  `EstablishmentDate` DATE NULL ,
  `Altitude` INT NULL ,
  `Shade` INT NULL ,
  `Grass` INT NULL ,
  `Trees` INT NULL ,
  `Poles` INT NULL ,
  `TrailDistance` INT NULL ,
  `TrailQuality` INT NULL ,
  `NumImages` INT NULL ,
  `Comments` VARCHAR(500) NULL ,
  PRIMARY KEY (`idSite`) ,
  UNIQUE INDEX `idSite_UNIQUE` (`idSite` ASC) ,
  INDEX `SiteToGridCell` (`GridCell` ASC) ,
  CONSTRAINT `SiteToGridCell`
    FOREIGN KEY (`GridCell` )
    REFERENCES `snapshot_meta`.`GridCells` (`idGridCell` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`People`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`People` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`People` (
  `idPeople` INT NOT NULL AUTO_INCREMENT ,
  `Name` VARCHAR(45) NOT NULL ,
  `Initials` VARCHAR(3) NOT NULL ,
  PRIMARY KEY (`idPeople`) ,
  UNIQUE INDEX `idPeople_UNIQUE` (`idPeople` ASC) ,
  UNIQUE INDEX `Name_UNIQUE` (`Name` ASC) ,
  UNIQUE INDEX `Initials_UNIQUE` (`Initials` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`SiteChecks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`SiteChecks` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`SiteChecks` (
  `idChecks` INT NOT NULL AUTO_INCREMENT ,
  `AccessID` INT NULL ,
  `Site` INT NOT NULL ,
  `Season` INT NOT NULL ,
  `AssociatedRoll` TINYINT(1) NOT NULL DEFAULT 0 ,
  `Researcher` INT NULL ,
  `DateChecked` DATE NULL ,
  `DateUploaded` DATE NULL ,
  `ActionNeeded` VARCHAR(30) NULL ,
  `UploadComments` VARCHAR(20) NULL ,
  `TimeChange` TINYINT(1) NULL ,
  `TimeDisplayedOnCheck` DATETIME NULL ,
  `TimeActualOnCheck` DATETIME NULL ,
  `Comments` VARCHAR(512) NULL ,
  PRIMARY KEY (`idChecks`) ,
  UNIQUE INDEX `idChecks_UNIQUE` (`idChecks` ASC) ,
  INDEX `SiteCheckToSite` (`Site` ASC) ,
  INDEX `SiteCheckToSeason` (`Season` ASC) ,
  INDEX `SiteCheckToPeople` (`Researcher` ASC) ,
  CONSTRAINT `SiteCheckToSite`
    FOREIGN KEY (`Site` )
    REFERENCES `snapshot_meta`.`Sites` (`idSite` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `SiteCheckToSeason`
    FOREIGN KEY (`Season` )
    REFERENCES `snapshot_meta`.`Seasons` (`idSeason` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `SiteCheckToPeople`
    FOREIGN KEY (`Researcher` )
    REFERENCES `snapshot_meta`.`People` (`idPeople` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`Rolls`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`Rolls` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`Rolls` (
  `idRoll` INT NOT NULL AUTO_INCREMENT ,
  `Season` INT NOT NULL ,
  `Site` INT NOT NULL ,
  `RollNumber` INT NOT NULL ,
  `SwitchToVideoTime` DATETIME NULL ,
  `SiteCheck` INT NULL ,
  `Comments` VARCHAR(100) NULL ,
  PRIMARY KEY (`idRoll`) ,
  UNIQUE INDEX `idRoll_UNIQUE` (`idRoll` ASC) ,
  INDEX `RollsToSiteCheck` (`SiteCheck` ASC) ,
  INDEX `RollsToSeason` (`Season` ASC) ,
  INDEX `RollsToSite` (`Site` ASC) ,
  CONSTRAINT `RollsToSiteCheck`
    FOREIGN KEY (`SiteCheck` )
    REFERENCES `snapshot_meta`.`SiteChecks` (`idChecks` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `RollsToSeason`
    FOREIGN KEY (`Season` )
    REFERENCES `snapshot_meta`.`Seasons` (`idSeason` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `RollsToSite`
    FOREIGN KEY (`Site` )
    REFERENCES `snapshot_meta`.`Sites` (`idSite` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`ZooniverseStatuses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`ZooniverseStatuses` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`ZooniverseStatuses` (
  `idZooniverseStatuses` INT NOT NULL ,
  `StatusDescription` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`idZooniverseStatuses`) ,
  UNIQUE INDEX `idZooniverseStatus_UNIQUE` (`idZooniverseStatuses` ASC) ,
  UNIQUE INDEX `StatusDescription_UNIQUE` (`StatusDescription` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`TimestampStatuses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`TimestampStatuses` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`TimestampStatuses` (
  `idTimestampStatuses` INT NOT NULL ,
  `StatusDescription` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`idTimestampStatuses`) ,
  UNIQUE INDEX `idTimestampStatuses_UNIQUE` (`idTimestampStatuses` ASC) ,
  UNIQUE INDEX `StatusDescription_UNIQUE` (`StatusDescription` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`CaptureEvents`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`CaptureEvents` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`CaptureEvents` (
  `idCaptureEvent` INT NOT NULL AUTO_INCREMENT ,
  `Roll` INT NOT NULL ,
  `CaptureEventNum` INT NOT NULL ,
  `Invalid` INT NOT NULL DEFAULT 999 ,
  `ZooniverseStatus` INT NOT NULL DEFAULT 0 ,
  `CaptureTimestamp` DATETIME NULL ,
  PRIMARY KEY (`idCaptureEvent`) ,
  UNIQUE INDEX `idCaptureEvent_UNIQUE` (`idCaptureEvent` ASC) ,
  INDEX `CaptureEventToRoll` (`Roll` ASC) ,
  INDEX `CEtoRollStatusDescript` (`ZooniverseStatus` ASC) ,
  INDEX `CEToTimestampStatus` (`Invalid` ASC) ,
  CONSTRAINT `CaptureEventToRoll`
    FOREIGN KEY (`Roll` )
    REFERENCES `snapshot_meta`.`Rolls` (`idRoll` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `CEtoRollStatusDescript`
    FOREIGN KEY (`ZooniverseStatus` )
    REFERENCES `snapshot_meta`.`ZooniverseStatuses` (`idZooniverseStatuses` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `CEToTimestampStatus`
    FOREIGN KEY (`Invalid` )
    REFERENCES `snapshot_meta`.`TimestampStatuses` (`idTimestampStatuses` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`Images`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`Images` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`Images` (
  `idImage` INT NOT NULL AUTO_INCREMENT ,
  `CaptureEvent` INT NOT NULL ,
  `SequenceNum` INT NOT NULL ,
  `PathFilename` VARCHAR(200) NOT NULL ,
  `TimestampAccepted` DATETIME NULL ,
  `TimestampAcceptedNote` VARCHAR(45) NULL ,
  `TimestampJPG` DATETIME NULL ,
  `TimestampFile` DATETIME NULL ,
  `ZooniverseImageURL` VARCHAR(120) NULL ,
  PRIMARY KEY (`idImage`) ,
  UNIQUE INDEX `idImage_UNIQUE` (`idImage` ASC) ,
  INDEX `ImageToCaptureEvent` (`CaptureEvent` ASC) ,
  CONSTRAINT `ImageToCaptureEvent`
    FOREIGN KEY (`CaptureEvent` )
    REFERENCES `snapshot_meta`.`CaptureEvents` (`idCaptureEvent` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`Log`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`Log` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`Log` (
  `idLog` INT NOT NULL AUTO_INCREMENT ,
  `Person` INT NOT NULL ,
  `Time` DATETIME NOT NULL ,
  `Notes` VARCHAR(2056) NOT NULL ,
  PRIMARY KEY (`idLog`) ,
  UNIQUE INDEX `idLog_UNIQUE` (`idLog` ASC) ,
  INDEX `LogPerson` (`Person` ASC) ,
  CONSTRAINT `LogPerson`
    FOREIGN KEY (`Person` )
    REFERENCES `snapshot_meta`.`People` (`idPeople` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`ConsensusClassifications`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`ConsensusClassifications` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`ConsensusClassifications` (
  `idClassifications` INT NOT NULL AUTO_INCREMENT ,
  `Capture` INT NOT NULL ,
  `RetireReason` VARCHAR(16) NOT NULL ,
  `NumberOfClassifications` INT NOT NULL ,
  `NumberOfVotes` INT NOT NULL ,
  `NumberOfBlanks` INT NOT NULL ,
  `PielouEvenness` DOUBLE NOT NULL ,
  `NumberOfSpecies` INT NULL ,
  `ConsensusAlgorithm` VARCHAR(24) NULL ,
  PRIMARY KEY (`idClassifications`) ,
  UNIQUE INDEX `idClassifications_UNIQUE` (`idClassifications` ASC) ,
  INDEX `CaptureFromConClass` (`Capture` ASC) ,
  CONSTRAINT `CaptureFromConClass`
    FOREIGN KEY (`Capture` )
    REFERENCES `snapshot_meta`.`CaptureEvents` (`idCaptureEvent` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`Species`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`Species` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`Species` (
  `idSpecies` INT NOT NULL AUTO_INCREMENT ,
  `SpeciesName` VARCHAR(24) NOT NULL ,
  PRIMARY KEY (`idSpecies`) ,
  UNIQUE INDEX `idSpecies_UNIQUE` (`idSpecies` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`ConsensusVotes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`ConsensusVotes` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`ConsensusVotes` (
  `idConsensusVotes` INT NOT NULL AUTO_INCREMENT ,
  `ConsensusClassification` INT NOT NULL ,
  `VoteIndex` INT NOT NULL ,
  `Species` INT NOT NULL ,
  `NumberOfVotes` INT NOT NULL ,
  `CountMin` VARCHAR(5) NOT NULL ,
  `CountMedian` VARCHAR(5) NOT NULL ,
  `CountMax` VARCHAR(5) NOT NULL ,
  `Standing` DOUBLE NOT NULL ,
  `Resting` DOUBLE NOT NULL ,
  `Moving` DOUBLE NOT NULL ,
  `Eating` DOUBLE NOT NULL ,
  `Interacting` DOUBLE NOT NULL ,
  `Babies` DOUBLE NOT NULL ,
  PRIMARY KEY (`idConsensusVotes`) ,
  UNIQUE INDEX `idConsensusVotes_UNIQUE` (`idConsensusVotes` ASC) ,
  INDEX `ConClassFromConVotes` (`ConsensusClassification` ASC) ,
  INDEX `SpeciesFromConVotes` (`Species` ASC) ,
  CONSTRAINT `ConClassFromConVotes`
    FOREIGN KEY (`ConsensusClassification` )
    REFERENCES `snapshot_meta`.`ConsensusClassifications` (`idClassifications` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `SpeciesFromConVotes`
    FOREIGN KEY (`Species` )
    REFERENCES `snapshot_meta`.`Species` (`idSpecies` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`CaptureEventsAndZooniverseIDs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`CaptureEventsAndZooniverseIDs` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`CaptureEventsAndZooniverseIDs` (
  `ZooniverseIdentifier` VARCHAR(10) NOT NULL ,
  `Capture` INT NOT NULL ,
  PRIMARY KEY (`ZooniverseIdentifier`) ,
  UNIQUE INDEX `ZooniverseIdentifier_UNIQUE` (`ZooniverseIdentifier` ASC) ,
  INDEX `CEtoZIDcapture` (`Capture` ASC) ,
  CONSTRAINT `CEtoZIDcapture`
    FOREIGN KEY (`Capture` )
    REFERENCES `snapshot_meta`.`CaptureEvents` (`idCaptureEvent` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`Users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`Users` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`Users` (
  `idUsers` INT NOT NULL AUTO_INCREMENT ,
  `UserName` VARCHAR(46) NOT NULL ,
  `UserHash` VARCHAR(64) NULL ,
  PRIMARY KEY (`idUsers`) ,
  UNIQUE INDEX `idUsers_UNIQUE` (`idUsers` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`SpeciesCounts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`SpeciesCounts` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`SpeciesCounts` (
  `idSpeciesCounts` INT NOT NULL ,
  `CountDescription` VARCHAR(5) NULL ,
  PRIMARY KEY (`idSpeciesCounts`) ,
  UNIQUE INDEX `idSpeciesCount_UNIQUE` (`idSpeciesCounts` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `snapshot_meta`.`ZooniverseClassifications`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `snapshot_meta`.`ZooniverseClassifications` ;

CREATE  TABLE IF NOT EXISTS `snapshot_meta`.`ZooniverseClassifications` (
  `idZooniverseClassifications` INT NOT NULL AUTO_INCREMENT ,
  `ZooniverseIdentifier` VARCHAR(10) NOT NULL ,
  `ClassificationID` VARCHAR(24) NOT NULL ,
  `User` INT NOT NULL ,
  `ClassificationDateTime` DATETIME NOT NULL ,
  `Species` INT NOT NULL ,
  `SpeciesCount` INT NOT NULL ,
  `Standing` TINYINT NOT NULL ,
  `Resting` TINYINT NOT NULL ,
  `Moving` TINYINT NOT NULL ,
  `Eating` TINYINT NOT NULL ,
  `Interacting` TINYINT NOT NULL ,
  `Babies` TINYINT NOT NULL ,
  PRIMARY KEY (`idZooniverseClassifications`) ,
  UNIQUE INDEX `idZooniverseClassifications_UNIQUE` (`idZooniverseClassifications` ASC) ,
  INDEX `ZClassToUser` (`User` ASC) ,
  INDEX `ZClassToSpecies` (`Species` ASC) ,
  INDEX `ZClassToSpeciesCount` (`SpeciesCount` ASC) ,
  CONSTRAINT `ZClassToUser`
    FOREIGN KEY (`User` )
    REFERENCES `snapshot_meta`.`Users` (`idUsers` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ZClassToSpecies`
    FOREIGN KEY (`Species` )
    REFERENCES `snapshot_meta`.`Species` (`idSpecies` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ZClassToSpeciesCount`
    FOREIGN KEY (`SpeciesCount` )
    REFERENCES `snapshot_meta`.`SpeciesCounts` (`idSpeciesCounts` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;