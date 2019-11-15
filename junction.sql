-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema junction
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema junction
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `junction` DEFAULT CHARACTER SET utf8 ;
USE `junction` ;

-- -----------------------------------------------------
-- Table `junction`.`wishilist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `junction`.`wishilist` (
  `idwishilist` INT NOT NULL AUTO_INCREMENT,
  `iduser` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idwishilist`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `junction`.`fund`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `junction`.`fund` (
  `idfund` INT NOT NULL AUTO_INCREMENT,
  `idwish` INT NOT NULL,
  `idproduct` INT NOT NULL,
  `amount` FLOAT NOT NULL,
  `already` FLOAT NOT NULL DEFAULT 0,
  `willbe` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`idfund`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `junction`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `junction`.`categories` (
  `idcategories` INT NOT NULL,
  `iduser` VARCHAR(45) NOT NULL,
  `dislikes` INT NULL DEFAULT 0,
  PRIMARY KEY (`idcategories`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `junction`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `junction`.`product` (
  `idproduct` INT NOT NULL,
  `idwishlist` INT NOT NULL,
  `willbe` VARCHAR(45) NOT NULL DEFAULT 'no',
  PRIMARY KEY (`idproduct`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `junction`.`celebrations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `junction`.`celebrations` (
  `name` INT NOT NULL,
  `start` DATE NOT NULL,
  `finish` DATE NOT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
