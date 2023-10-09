-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema crypto
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema crypto
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `crypto` DEFAULT CHARACTER SET utf8 ;
USE `crypto` ;

-- -----------------------------------------------------
-- Table `crypto`.`coins`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `crypto`.`coins` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(25) NOT NULL,
  `price` DECIMAL(9,2) NOT NULL,
  `capacity` BIGINT NOT NULL,
  `volume` BIGINT NOT NULL,
  `history_hour` DECIMAL(4,2) NOT NULL,
  `history_day` DECIMAL(4,2) NOT NULL,
  `history_week` DECIMAL(4,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
