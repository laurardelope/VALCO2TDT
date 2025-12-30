-- --------------------------------------------------------
-- Host:                         10.10.0.71
-- Versión del servidor:         8.0.43-0ubuntu0.22.04.2 - (Ubuntu)
-- SO del servidor:              Linux
-- HeidiSQL Versión:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para valco2t
CREATE DATABASE IF NOT EXISTS `valco2t` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `valco2t`;

CREATE TABLE IF NOT EXISTS `ejecucionesDT` (
  `datetime` datetime NOT NULL,
  `datetimeServer` datetime DEFAULT NULL,
  `id_experimento` int DEFAULT NULL,
  `tiempo_medida` int DEFAULT NULL,
  `intensidad_corriente` float DEFAULT '0',
  `densidad_corriente` float DEFAULT '0',
  `caudal_co2` float DEFAULT '0',
  `concentracion_co2` float DEFAULT '0',
  `humedad_co2` float DEFAULT '0',
  `caudal_anolito` float DEFAULT '0',
  `caudal_catolito` float DEFAULT '0',
  `concentracion_anolito` float DEFAULT NULL,
  `concentracion_catolito` float DEFAULT NULL,
  `caudal_central` float DEFAULT '0',
  `concentracion_hcoo` float DEFAULT '0',
  `caudal_hcoo` float DEFAULT '0',
  `potencial_celda` float DEFAULT '0',
  `produccion_hcoo_gmin` float DEFAULT '0',
  `produccion_hcoo_molmin` float DEFAULT '0',
  `FE` float DEFAULT '0',
  `consumo_energetico` float DEFAULT '0',
  `potencia` float DEFAULT '0',
  `caudal_co2_out` float DEFAULT NULL,
  `concentracion_co2_out` float DEFAULT NULL,
  `presion_in` float DEFAULT NULL,
  `presion_out` float DEFAULT NULL,
  `temperatura_in` float DEFAULT NULL,
  `temperatura_out` float DEFAULT NULL,
  `concentracion_h2o_in` float DEFAULT NULL,
  `concentracion_h2o_out` float DEFAULT NULL,
  `pH` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

CREATE TABLE IF NOT EXISTS `electrodos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` char(50) NOT NULL DEFAULT '',
  `Catalizador` char(50) DEFAULT NULL,
  `n_compartimentos` int NOT NULL DEFAULT '0',
  `area` int NOT NULL DEFAULT '0',
  `Catolito` char(50) DEFAULT '0',
  `Anolito` char(50) DEFAULT '0',
  `Membrana` char(50) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `experimentos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_electrodo` int NOT NULL DEFAULT '0',
  `carga_catalizador` float NOT NULL DEFAULT '0',
  `densidad_corriente` float NOT NULL DEFAULT '0',
  `intensidad` float NOT NULL DEFAULT '0',
  `caudal_co2` float NOT NULL DEFAULT '0',
  `concentracion_co2` float NOT NULL DEFAULT '0',
  `humedad_co2` float NOT NULL DEFAULT '0',
  `caudal anolito` float NOT NULL DEFAULT '0',
  `caudal_catolito` float NOT NULL DEFAULT '0',
  `caudal_central` float NOT NULL DEFAULT '0',
  `concentracion_h2_in` float NOT NULL DEFAULT '0',
  `concentracion_anolito` float NOT NULL DEFAULT '0',
  `concentracion_catolito` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE IF NOT EXISTS `experimentosDT` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_experimento` int NOT NULL DEFAULT '0',
  `id_electrodo` int NOT NULL DEFAULT '0',
  `carga_catalizador` float NOT NULL DEFAULT '0',
  `densidad_corriente` float NOT NULL DEFAULT '0',
  `intensidad` float NOT NULL DEFAULT '0',
  `caudal_co2` float NOT NULL DEFAULT '0',
  `concentracion_co2` float NOT NULL DEFAULT '0',
  `humedad_co2` float NOT NULL DEFAULT '0',
  `caudal anolito` float NOT NULL DEFAULT '0',
  `caudal_catolito` float NOT NULL DEFAULT '0',
  `caudal_central` float NOT NULL DEFAULT '0',
  `concentracion_h2_in` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=247 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;




/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
