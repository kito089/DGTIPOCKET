-- MySQL Script generated by MySQL Workbench
-- sáb 18 nov 2023 21:05:55
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema prototipos
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema prototipos
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `prototipos` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
-- -----------------------------------------------------
USE `prototipos` ;

-- -----------------------------------------------------
-- Table `especialidad`
-- -----------------------------------------------------

ALTER DATABASE `prototipos` CHARACTER SET = latin1 COLLATE latin1_swedish_ci;

CREATE TABLE IF NOT EXISTS `especialidad` (
  `idespecialidad` INT NOT NULL,
  `nombre` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`idespecialidad`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1 COLLATE latin1_swedish_ci;

-- -----------------------------------------------------
-- Table `grupo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grupo` (
  `idgrupo` INT(11) NOT NULL AUTO_INCREMENT,
  `letra` VARCHAR(1) NOT NULL,
  `turno` TINYINT(4) NOT NULL,
  `especialidad_idespecialidad` INT NOT NULL,
  PRIMARY KEY (`idgrupo`, `especialidad_idespecialidad`),
  INDEX `fk_grupo_especialidad1_idx` (`especialidad_idespecialidad`),
  CONSTRAINT `fk_grupo_especialidad1`
    FOREIGN KEY (`especialidad_idespecialidad`)
    REFERENCES `especialidad` (`idespecialidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = latin1 COLLATE latin1_swedish_ci;


-- -----------------------------------------------------
-- Table `alumnos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alumnos` (
  `idalumnos` INT(11) NOT NULL AUTO_INCREMENT,
  `no_control` VARCHAR(14) NOT NULL,
  `curp` VARCHAR(18) NOT NULL,
  `grado` VARCHAR(1) NOT NULL,
  `grupo_idgrupo` INT(11) NOT NULL,
  PRIMARY KEY (`idalumnos`, `no_control`, `curp`, `grupo_idgrupo`),
  INDEX `fk_alumnos_grupo_idx` (`grupo_idgrupo`),
  CONSTRAINT `fk_alumnos_grupo`
    FOREIGN KEY (`grupo_idgrupo`)
    REFERENCES `grupo` (`idgrupo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1 COLLATE latin1_swedish_ci;


-- -----------------------------------------------------
-- Table `avisos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `avisos` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(255) NOT NULL,
  `descripcion` TEXT NULL DEFAULT NULL,
  `fecha` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1 COLLATE latin1_swedish_ci;


-- -----------------------------------------------------
-- Table `concursos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `concursos` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(255) NOT NULL,
  `descripcion` TEXT NULL DEFAULT NULL,
  `url_imagen` VARCHAR(255) NULL DEFAULT NULL,
  `fecha` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1 COLLATE latin1_swedish_ci;


-- -----------------------------------------------------
-- Table `modulos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `modulos` (
  `idmodulos` INT(11) NOT NULL AUTO_INCREMENT,
  `uac` VARCHAR(20) NOT NULL,
  `nombre` VARCHAR(400) NOT NULL,
  `horas` INT(11) NOT NULL,
  `semestre` INT(11) NOT NULL,
  `especialidad_idespecialidad` INT NOT NULL,
  PRIMARY KEY (`idmodulos`, `uac`, `especialidad_idespecialidad`),
  INDEX `fk_modulos_especialidad1_idx` (`especialidad_idespecialidad`),
  CONSTRAINT `fk_modulos_especialidad1`
    FOREIGN KEY (`especialidad_idespecialidad`)
    REFERENCES `especialidad` (`idespecialidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1 COLLATE latin1_swedish_ci;


-- -----------------------------------------------------
-- Table `submodulos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `submodulos` (
  `idsubmodulos` INT(11) NOT NULL AUTO_INCREMENT,
  `uac` VARCHAR(20) NOT NULL,
  `nombre` VARCHAR(400) NOT NULL,
  `horas` INT(11) NOT NULL,
  `modulos_idmodulos` INT(11) NOT NULL,
  PRIMARY KEY (`idsubmodulos`, `modulos_idmodulos`),
  INDEX `fk_submodulos_modulos1_idx` (`modulos_idmodulos`),
  CONSTRAINT `fk_submodulos_modulos1`
    FOREIGN KEY (`modulos_idmodulos`)
    REFERENCES `modulos` (`idmodulos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1 COLLATE latin1_swedish_ci;


-- -----------------------------------------------------
-- Table `evaluacion_e`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `evaluacion_e` (
  `idevaluacion_e` INT(11) NOT NULL AUTO_INCREMENT,
  `parcial1` DECIMAL(2,2) NULL DEFAULT NULL,
  `parcial2` DECIMAL(2,2) NULL DEFAULT NULL,
  `parcial3` DECIMAL(2,2) NULL DEFAULT NULL,
  `asistencia1` INT(11) NULL DEFAULT NULL,
  `asistencia2` INT(11) NULL DEFAULT NULL,
  `asistencia3` INT(11) NULL DEFAULT NULL,
  `submodulos_idsubmodulos` INT(11) NOT NULL,
  `alumnos_idalumnos` INT(11) NOT NULL,
  PRIMARY KEY (`idevaluacion_e`, `submodulos_idsubmodulos`, `alumnos_idalumnos`),
  INDEX `fk_evaluacion_e_submodulos1_idx` (`submodulos_idsubmodulos`),
  INDEX `fk_evaluacion_e_alumnos1_idx` (`alumnos_idalumnos`),
  CONSTRAINT `fk_evaluacion_e_alumnos1`
    FOREIGN KEY (`alumnos_idalumnos`)
    REFERENCES `alumnos` (`idalumnos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evaluacion_e_submodulos1`
    FOREIGN KEY (`submodulos_idsubmodulos`)
    REFERENCES `submodulos` (`idsubmodulos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1 COLLATE latin1_swedish_ci;


-- -----------------------------------------------------
-- Table `materias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `materias` (
  `idmaterias` INT(11) NOT NULL AUTO_INCREMENT,
  `uac` VARCHAR(20) NOT NULL,
  `nombre` VARCHAR(400) NOT NULL,
  `horas` INT(11) NOT NULL,
  `semestre` INT(11) NOT NULL,
  PRIMARY KEY (`idmaterias`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1 COLLATE latin1_swedish_ci;


-- -----------------------------------------------------
-- Table `evaluacion_tc`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `evaluacion_tc` (
  `idevaluacion_tc` INT(11) NOT NULL AUTO_INCREMENT,
  `parcial1` DECIMAL(2,2) NULL DEFAULT NULL,
  `parcial2` DECIMAL(2,2) NULL DEFAULT NULL,
  `parcial3` DECIMAL(2,2) NULL DEFAULT NULL,
  `asistencia1` INT(11) NULL DEFAULT NULL,
  `asistencia2` INT(11) NULL DEFAULT NULL,
  `asistencia3` INT(11) NULL DEFAULT NULL,
  `materias_idmaterias` INT(11) NOT NULL,
  `alumnos_idalumnos` INT(11) NOT NULL,
  PRIMARY KEY (`idevaluacion_tc`, `materias_idmaterias`, `alumnos_idalumnos`),
  INDEX `fk_evaluacion_tc_materias1_idx` (`materias_idmaterias`),
  INDEX `fk_evaluacion_tc_alumnos1_idx` (`alumnos_idalumnos`),
  CONSTRAINT `fk_evaluacion_tc_alumnos1`
    FOREIGN KEY (`alumnos_idalumnos`)
    REFERENCES `alumnos` (`idalumnos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evaluacion_tc_materias1`
    FOREIGN KEY (`materias_idmaterias`)
    REFERENCES `materias` (`idmaterias`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1 COLLATE latin1_swedish_ci;


-- -----------------------------------------------------
-- Table `noticias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `noticias` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(45) NOT NULL,
  `descripcion` VARCHAR(255) NOT NULL,
  `img` VARCHAR(255) NULL DEFAULT NULL,
  `fecha` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = latin1 COLLATE latin1_swedish_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `especialidad`
-- -----------------------------------------------------
START TRANSACTION;
USE `prototipos`;
INSERT INTO `especialidad` (`idespecialidad`, `nombre`) VALUES (1, 'PROGRAMACIÓN');
INSERT INTO `especialidad` (`idespecialidad`, `nombre`) VALUES (2, 'SOPORTE Y MANTENIMIENTO A EQUIPO DE COMPUTO');
INSERT INTO `especialidad` (`idespecialidad`, `nombre`) VALUES (3, 'ADMINISTRACION DE RECURSOS HUMANOS');
INSERT INTO `especialidad` (`idespecialidad`, `nombre`) VALUES (4, 'MATENIMIENTO AUTOMOTRIZ');

COMMIT;


-- -----------------------------------------------------
-- Data for table `grupo`
-- -----------------------------------------------------
START TRANSACTION;
USE `prototipos`;
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (1, 'A', 0, 1);
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (2, 'B', 0, 2);
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (3, 'C', 0, 3);
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (4, 'D', 0, 3);
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (5, 'E', 0, 3);
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (6, 'F', 0, 4);
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (7, 'G', 1, 1);
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (8, 'H', 1, 2);
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (9, 'I', 1, 3);
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (10, 'J', 1, 3);
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (11, 'K', 1, 3);
INSERT INTO `grupo` (`idgrupo`, `letra`, `turno`, `especialidad_idespecialidad`) VALUES (12, 'L', 1, 4);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modulos`
-- -----------------------------------------------------
START TRANSACTION;
USE `prototipos`;
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (1, '3061300001-17M1', 'MÓDULO I. DESARROLLA SOFTWARE DE APLICACION CON PROGRAMACIÓN ESTRUCTURADA', 17, 2, 1);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (2, '3061300001-17M2', 'MÓDULO II. APLICA METODOLOGÍAS DE DESARROLLO DE SOFTWARE CON HERRAMIENTAS DE PROGRAMACIÓN VISUAL', 17, 3, 1);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (3, '3061300001-17M3', 'MÓDULO III. DESARROLLA APLICACIONES WEB', 17, 4, 1);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (4, '3061300001-17M4', 'MÓDULO IV. DESARROLLA SOFTWARE DE APLICACIÓN WEB CON ALMACENAMIENTO PERSISTENTE DE DATOS', 12, 5, 1);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (5, '3061300001-17M5', 'MÓDULO V. DESARROLLA APLICACIONES PARA DISPOSITIVOS MOVILES', 12, 6, 1);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (6, '3062300001-17M1', 'MÓDULO I. ENSAMBLA, CONFIGURA E INSTALA HARDWARE Y SOFTWARE EN EL EQUIPO DE CÓMPUTO', 17, 2, 2);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (7, '3062300001-17M2', 'MÓDULO II. MANTIENE HARDWARE Y SOFTWARE EN EL EQUIPO DE CÓMPUTO', 17, 3, 2);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (8, '3062300001-17M3', 'MÓDULO III. PROPORCIONA SOPORTE TÉCNICO PRESENCIAL O A DISTANCIA EN SOFTWARE DE APLICACIÓN Y HARDWARE', 17, 4, 2);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (9, '3062300001-17M4', 'MÓDULO IV. DISEÑA REDES DE COMPUTADORAS', 12, 5, 2);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (10, '3062300001-17M5', 'MÓDULO V. INSTALA Y OPERA REDES DE COMPUTADORAS', 12, 6, 2);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (11, '333502001-16M1', 'MÓDULO I. PLANTEA ACTIVIDADES DEL ÁREA DE RECURSOS HUMANOS EN FUNCIÓN A CADA ÁREA DE LA ORGANIZACIÓN', 17, 2, 3);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (12, '333502001-16M2', 'MÓDULO II. INTEGRA EL CAPITAL HUMANO A LA ORGANIZACIÓN', 17, 3, 3);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (13, '333502001-16M3', 'MÓDULO III. ASISTE EN EL CONTROL Y EVALUACIÓN DEL DESEMPEÑO DEL CAPITAL HUMANO DE LA ORGANIZACIÓN', 17, 4, 3);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (14, '333502001-16M4', 'MÓDULO IV. CONTROLA LOS PROCESOS Y SERVICIOS DE HIGIENE Y SEGURIDAD DEL CAPITAL HUMANO EN LA ORGANIZACIÓN', 12, 5, 3);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (15, '333502001-16M5', 'MÓDULO V. DETERMINA LAS REMUNERACIONES AL CAPITAL HUMANO DE LA ORGANIZACIÓN', 12, 6, 3);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (16, '351500002-16M1', 'MÓDULO I. MANTIENE LOS SISTEMAS ELÉCTRICOS Y ELECTRÓNICOS DEL AUTOMÓVIL', 17, 2, 4);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (17, '351500002-16M2', 'MÓDULO II. MANTIENE EL MOTOR DE COMBUSTIÓN INTERNA', 17, 3, 4);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (18, '351500002-16M3', 'MÓDULO III. MANTIENE LOS SISTEMAS DE CONTROL ELECTRÓNICO DEL MOTOR DE COMBUSTIÓN INTERNA', 17, 4, 4);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (19, '351500002-16M4', 'MÓDULO IV. MANTIENE EL SISTEMA DE TRANSMISIÓN DEL AUTOMÓVIL', 12, 5, 4);
INSERT INTO `modulos` (`idmodulos`, `uac`, `nombre`, `horas`, `semestre`, `especialidad_idespecialidad`) VALUES (20, '351500002-16M5', 'MÓDULO V. MANTIENE LOS SISTEMAS DE SUSPENSIÓN, DIRECCIÓN Y FRENOS DEL AUTOMÓVIL', 12, 6, 4);

COMMIT;


-- -----------------------------------------------------
-- Data for table `submodulos`
-- -----------------------------------------------------
START TRANSACTION;
USE `prototipos`;
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (1, '3061300001-17M1S1', 'CONSTRUYE ALGORITMOS PARA LA SOLUCIÓN DE PROBLEMAS', 5, 1);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (2, '3061300001-17M1S2', 'APLICA ESTRUCTURAS DE CONTROL CON UN LENGUAJE DE PROGRAMACIÓN', 7, 1);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (3, '3061300001-17M1S3', 'APLICA ESTRUCTURAS DE DATOS CON UN LENGUAJE DE PROGRAMACIÓN', 5, 1);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (4, '3061300001-17M2S1', 'APLICA LA METODOLOGÍA ESPIRAL CON PROGRAMACIÓN ORIENTADA A OBJETOS', 9, 2);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (5, '3061300001-17M2S2', 'APLICA LA METODOLOGÍA DE DESARROLLO RÁPIDO DE APLICACIONES CON PROGRAMACIÓN ORIENTADA A EVENTOS', 11, 2);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (6, '3061300001-17M3S1', 'CONSTRUYE PÁGINAS WEB', 4, 3);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (7, '3061300001-17M3S2', 'DESARROLLA APLICACIONES QUE SE EJECUTAN EN EL CLIENTE', 6, 3);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (8, '3061300001-17M3S3', 'DESARROLLA APLICACIONES QUE SE EJECUTAN EN EL SERVIDOR', 7, 3);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (9, '3061300001-17M4S1', 'CONSTRUYE BASES DE DATOS PARA APLICACIONES WEB', 6, 4);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (10, '3061300001-17M4S2', 'DESARROLLA APLICACIONES WEB CON CONEXIÓN A BASES DE DATOS', 6, 4);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (11, '3061300001-17M5S1', 'DESARROLLA APLICACIONES MÓVILES PARA ANDROID', 6, 5);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (12, '3061300001-17M5S2', 'DESARROLLA APLICACIONES MÓVILES PARA IOS', 6, 5);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (13, '3062300001-17M1S1', 'ENSAMBLA E INSTALA CONTROLADORES Y DISPOSITIVOS PERIFÉRICOS', 10, 6);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (14, '3062300001-17M1S2', 'INSTALA Y CONFIGURA SOFTWARE', 7, 6);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (15, '3062300001-17M2S1', 'REALIZA MANTENIMIENTO PREVENTIVO', 7, 7);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (16, '3062300001-17M2S2', 'REALIZA MANTENIMIENTO CORRECTIVO', 10, 7);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (17, '3062300001-17M3S1', 'BRINDA SOPORTE TÉCNICO DE MANERA PRESENCIAL', 6, 8);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (18, '3062300001-17M3S2', 'BRINDA SOPORTE TÉCNICO A DISTANCIA', 11, 8);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (19, '3062300001-17M4S1', 'CLASIFICA LOS ELEMENTOS BÁSICOS DE LA RED LAN', 5, 9);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (20, '3062300001-17M4S2', 'DISEÑA LA RED LAN', 7, 9);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (21, '3062300001-17M5S1', 'INSTALA UNA RED LAN', 6, 10);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (22, '3062300001-17M5S2', 'OPERA UNA RED LAN', 6, 10);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (23, '333502001-16M1S1', 'DISTINGUE LOS DIFERENTES TIPOS DE EMPRESA POR SU GIRO, ÁREAS FUNCIONALES, DOCUMENTACIÓN ADMINISTRATIVA Y RECURSOS', 10, 11);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (24, '333502001-16M1S2', 'ELABORA ESTRATEGIAS PARA REALIZAR LAS ACTIVIDADES DE SU ÁREA', 7, 11);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (25, '333502001-16M2S1', 'REALIZA EL PROCESO DE ADMISIÓN Y EMPLEO', 10, 12);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (26, '333502001-16M2S2', 'CONTRIBUYE A LA INTEGRACIÓN Y DESARROLLO DEL PERSONAL EN LA ORGANIZACIÓN', 7, 12);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (27, '333502001-16M3S1', 'ASISTE EN LAS ACTIVIDADES DE CAPACITACIÓN PARA EL DESARROLLO DEL CAPITAL HUMANO', 7, 13);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (28, '333502001-16M3S2', 'EVALÚA EL DESEMPEÑO DE LA ORGANIZACIÓN UTILIZANDO HERRAMIENTAS DE CALIDAD', 10, 13);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (29, '333502001-16M4S1', 'SUPERVISA EL CUMPLIMIENTO DE LAS MEDIDAS DE HIGIENE Y SEGURIDAD EN LA ORGANIZACIÓN', 6, 14);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (30, '333502001-16M4S2', 'SUPERVISA EL CUMPLIMIENTO DE TAREAS Y PROCESOS PARA EVALUAR LA PRODUCTIVIDAD EN LA ORGANIZACIÓN', 6, 14);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (31, '333502001-16M5S1', 'DETERMINA LA NÓMINA DEL PERSONAL DE LA ORGANIZACIÓN TOMANDO EN CUENTA LA NORMATIVIDAD LABORAL', 8, 15);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (32, '333502001-16M5S2', 'DETERMINA REMUNERACIONES DEL PERSONAL EN SITUACIONES EXTRAORDINARIAS', 4, 15);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (33, '351500002-16M1S1', 'MANTIENE EL SISTEMA ELÉCTRICO DEL AUTOMÓVIL', 6, 16);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (34, '351500002-16M1S2', 'MANTIENE EL SISTEMA ELECTRÓNICO DEL AUTOMÓVIL', 11, 16);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (35, '351500002-16M2S1', 'MANTIENE EL MOTOR DE GASOLINA Y DE DIÉSEL', 8, 17);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (36, '351500002-16M2S2', 'MANTIENE EL SISTEMA DE CALEFACCIÓN Y AIRE ACONDICIONADO DEL AUTOMÓVIL', 4, 17);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (37, '351500002-16M2S3', 'MANTIENE EL SISTEMA DE ENFRIAMIENTO Y LUBRICACIÓN DEL MOTOR', 5, 17);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (38, '351500002-16M3S1', 'MANTIENE EL SISTEMA DE INYECCIÓN ELECTRÓNICA DE LOS MOTORES DE GASOLINA Y DIÉSEL', 7, 18);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (39, '351500002-16M3S2', 'MANTIENE EL SISTEMA DE EMISIONES CONTAMINANTES DEL AUTOMÓVIL', 4, 18);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (40, '351500002-16M3S3', 'MANTIENE EL SISTEMAS DE ENCENDIDO ELECTRÓNICO Y COMPUTARIZADO DEL AUTOMÓVIL', 6, 18);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (41, '351500002-16M4S1', 'MANTIENE EL SISTEMA DE TRANSMISIÓN Y TRANSEJE MANUAL DEL AUTOMÓVIL', 6, 19);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (42, '351500002-16M4S2', 'MANTIENE EL SISTEMA DE TRANSMISIÓN Y TRANSEJE AUTOMÁTICO DEL AUTOMÓVIL', 6, 19);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (43, '351500002-16M5S1', 'MANTIENE LOS SISTEMAS DE SUSPENSIÓN Y DIRECCIÓN DEL AUTOMÓVIL', 5, 20);
INSERT INTO `submodulos` (`idsubmodulos`, `uac`, `nombre`, `horas`, `modulos_idmodulos`) VALUES (44, '351500002-16M5S2', 'MANTIENE EL SISTEMA DE FRENOS DEL AUTOMÓVIL', 7, 20);

COMMIT;


-- -----------------------------------------------------
-- Data for table `materias`
-- -----------------------------------------------------
START TRANSACTION;
USE `prototipos`;
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (1, '343101-17DB', 'ÁLGEBRA', 4, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (2, '322201-17DB', 'INGLÉS I', 3, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (3, '342201-17DB', 'QUÍMICA I', 4, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (4, '344101-17DB', 'TECNOLOGÍAS DE LA INFORMACIÓN Y LA COMUNICACIÓN', 3, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (5, '322501-17DB', 'LÓGICA', 4, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (6, '322301-17DB', 'LECTURA, EXPRESIÓN ORAL Y ESCRITA I', 4, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (7, '343102-17DB', 'GEOMETRÍA Y TRIGONOMETRÍA', 4, 2);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (8, '322202-17DB', 'INGLÉS II', 3, 2);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (9, '342202-17DB', 'QUÍMICA II', 4, 2);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (10, '322302-17DB', 'LECTURA, EXPRESIÓN ORAL Y ESCRITA II', 4, 2);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (11, '343103-17DB', 'GEOMETRÍA ANALÍTICA', 4, 3);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (12, '322203-17DB', 'INGLÉS III', 3, 3);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (13, '341101-17DB', 'BIOLOGÍA', 4, 3);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (14, '322502-17DB', 'ÉTICA', 4, 3);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (15, '343104-17DB', 'CÁLCULO DIFERENCIAL', 4, 4);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (16, '322204-17DB', 'INGLÉS IV', 3, 4);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (17, '342101-17DB', 'FÍSICA I', 4, 4);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (18, '341201-17DB', 'ECOLOGÍA', 4, 4);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (19, '342102-17DB', 'FISICA II', 4, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (20, '322503-17DB', 'CIENCIA, TECNOLOGÍA, SOCIEDAD Y VALORES', 4, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (21, '343105-17DE', 'CÁLCULO INTEGRAL', 5, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (22, '322205-17FPp', 'INGLÉS V', 5, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (23, '343201-17DE', 'PROBABILIDAD Y ESTADÍSTICA', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (24, '322504-17DE', 'TEMAS DE FILOSOFÍA', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (25, '321402-13-FPp', 'DIBUJO TÉCNICO', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (26, '371001-13-FPp', 'TEMAS DE CIENCIAS DE LA SALUD', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (27, '331002-13-FPp', 'TEMAS DE CIENCIAS SOCIALES', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (28, '322303-13-FPp', 'LITERATURA', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (29, '322401-13-FPp', 'HISTORIA', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (30, '341103-13-FPp', 'TEMAS DE BIOLOGÍA CONTEMPORÁNEA', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (31, '343106-13-FPp', 'MATEMÁTICAS APLICADAS', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (32, '333001-13-FPp', 'TEMAS DE ADMINISTRACIÓN', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (33, '342103-13-FPp', 'TEMAS DE FÍSICA', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (34, '331001-13-FPp', 'INTRODUCCIÓN A LA ECONOMÍA', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (35, '334101-13-FPp', 'INTRODUCCIÓN AL DERECHO', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (36, '341102-13-FPp', 'INTRODUCCIÓN A LA BIOQUÍMICA', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (37, 'P-611-2023-1-1', 'Lengua y comunicación I', 3, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (38, 'P-611-2023-1-2', 'Inglés I', 3, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (39, 'P-611-2023-1-3', 'Pensamiento matemático I', 4, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (40, 'P-611-2023-1-4', 'Cultura digital I', 3, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (41, 'P-611-2023-1-5', 'La materia y sus interacciones', 4, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (42, 'P-611-2023-1-6', 'Humanidades I', 4, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (43, 'P-611-2023-1-7', 'Ciencias sociales I', 2, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (44, 'P-611-2023-1-8', 'Recursos socioemocionales I', 3, 1);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (45, 'P-611-2023-2-1', 'Lengua y comunicación II', 3, 2);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (46, 'P-611-2023-2-2', 'Inglés II', 3, 2);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (47, 'P-611-2023-2-3', 'Pensamiento matemático II', 4, 2);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (48, 'P-611-2023-2-4', 'Cultura digital II', 2, 2);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (49, 'P-611-2023-2-5', 'Conservación de la energía y sus interacciones con la materia', 4, 2);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (50, 'P-611-2023-2-6', 'Ciencias sociales II', 2, 2);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (51, 'P-611-2023-2-8', 'Recursos socioemocionoales II', 3, 2);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (52, 'P-611-2023-3-1', 'Lengua y comunicación III', 3, 3);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (53, 'P-611-2023-3-2', 'Inglés III', 3, 3);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (54, 'P-611-2023-3-3', 'Pensamiento matemático III', 4, 3);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (55, 'P-611-2023-3-4', 'Ecosistemas: interacciones, energía y dinámica', 4, 3);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (56, 'P-611-2023-3-5', 'Humanidades II', 4, 3);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (57, 'P-611-2023-3-7', 'Recursos socioemocionales III', 3, 3);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (58, 'P-611-2023-4-1', 'Inglés IV', 3, 4);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (59, 'P-611-2023-4-2', 'Tenas selectos de matemáticas I', 4, 4);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (60, 'P-611-2023-4-3', 'Conciencia histórica 1: Perspectivas del México antiguo en los contextos globales', 3, 4);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (61, 'P-611-2023-4-4', 'Reacciones químicas: conservación de la materia en la formación de nuevas subtancias', 4, 4);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (62, 'P-611-2023-4-5', 'Ciencias sociales III', 2, 4);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (63, 'P-611-2023-4-7', 'Recursos socioemocionales IV', 3, 4);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (64, 'P-611-2023-5-1', 'Inglés V', 5, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (65, 'P-611-2023-5-10', 'Temas de administración ', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (66, 'P-611-2023-5-11', 'Introducción a la economía', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (67, 'P-611-2023-5-12', 'Introducción al Derecho', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (68, 'P-611-2023-5-13', 'Introducción a la bioquímica', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (69, 'P-611-2023-5-14', 'Temas de biología contemporánea', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (70, 'P-611-2023-5-15', 'Temas de Ciencias de la Salud', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (71, 'P-611-2023-5-16', 'Temas de Ciencias Sociales', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (72, 'P-611-2023-5-17', 'Literatura', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (73, 'P-611-2023-5-18', 'Historia', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (74, 'P-611-2023-5-2', 'Temas selectos de matemáticas II', 5, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (75, 'P-611-2023-5-3', 'Conciencia histórica II. México durante el expansionismo capitalista.', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (76, 'P-611-2023-5-4', 'La energía en los procesos de la vida diaria', 4, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (77, 'P-611-2023-5-6', 'Recursos socioemocionales V', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (78, 'P-611-2023-5-7', 'Temas de física', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (79, 'P-611-2023-5-8', 'Dibujo técnico', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (80, 'P-611-2023-5-9', 'Matemáticas', 3, 5);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (81, 'P-611-2023-6-1', 'Temas selectos de matemáticas III', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (82, 'P-611-2023-6-10', 'Temas de administración', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (83, 'P-611-2023-6-11', 'Introducción a la economía', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (84, 'P-611-2023-6-12', 'Introducción al Derecho', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (85, 'P-611-2023-6-13', 'Introducción a la bioquímica', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (86, 'P-611-2023-6-14', 'Temas de biología contemporánea', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (87, 'P-611-2023-6-15', 'Temas de Ciencias de la Salud', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (88, 'P-611-2023-6-16', 'Temas de Ciencias Sociales', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (89, 'P-611-2023-6-17', 'Literatura', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (90, 'P-611-2023-6-18', 'Historia', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (91, 'P-611-2023-6-2', 'Conciencia histórica III. La realidad actual en perspectiva histórica', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (92, 'P-611-2023-6-3', 'Organismos, estructuras y procesos. Herencia y evolución biológica', 4, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (93, 'P-611-2023-6-4', 'Humanidades III', 5, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (94, 'P-611-2023-6-6', 'Recursos socioemocionales VI', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (95, 'P-611-2023-6-7', 'Temas de física', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (96, 'P-611-2023-6-8', 'Dibujo técnico', 3, 6);
INSERT INTO `materias` (`idmaterias`, `uac`, `nombre`, `horas`, `semestre`) VALUES (97, 'P-611-2023-6-9', 'Matemáticas', 3, 6);

COMMIT;
