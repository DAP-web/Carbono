-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: carbonodb
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `taskid` int NOT NULL AUTO_INCREMENT,
  `userid` int NOT NULL,
  `date` date NOT NULL,
  `task` text NOT NULL,
  `priority` varchar(5) NOT NULL,
  `estado` tinyint NOT NULL,
  `categoria` varchar(50) NOT NULL,
  PRIMARY KEY (`taskid`),
  KEY `FK_userid_idx` (`userid`),
  CONSTRAINT `FK_userid` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,1,'2021-07-09','Yonaguni','Alta',1,'Productividad'),(2,1,'2021-07-09','Te Mudaste','Alta',1,'Productividad'),(3,1,'2021-07-09','Shake that','Media',1,'Productividad'),(5,1,'2021-07-13','Vuelve (Remix)','Media',1,'Productividad'),(6,1,'2021-07-13','Te mudaste','Media',1,'Productividad'),(7,1,'2021-07-13','De Museo','Baja',0,'Productividad'),(8,1,'2021-07-10','Ver Modern Family','Media',1,'Descanso'),(9,2,'2021-07-10','Subir Macro','Alta',1,'Trabajo'),(10,2,'2021-07-13','Subir el volcan de Sta. Ana','Media',0,'Recreacion'),(11,2,'2021-08-03','Ir a la playa','Alta',0,'Recreacion'),(13,2,'2021-08-01','Entregar API Sofi','Alta',0,'Trabajo'),(15,3,'2021-08-03','Concierto London','Alta',0,'Productividad'),(16,3,'2021-08-06','Jet hacia Cartagena','Media',0,'Compras'),(17,2,'2021-08-04','Ir a la veterinaria','Alta',0,'Mascotas'),(18,3,'2021-08-04','Ir al Dolphin Mall','Baja',0,'Compras'),(19,2,'2021-08-05','Terminar filtros','Media',0,'Trabajo'),(20,1,'2021-08-05','Grabar video','Media',0,'Recreacion'),(21,2,'2021-07-10','Reunion con GoGreen','Alta',0,'Trabajo'),(22,1,'2021-08-05','Firmar autografos','Media',1,'Trabajo'),(23,1,'2021-08-05','Pasar a traer a Marron 5','Media',1,'Recreacion'),(24,2,'2021-08-09','Subir proyecto a heroku','Alta',0,'Trabajo'),(25,2,'2021-08-10','Mandar Progra','Alta',0,'Trabajo'),(26,2,'2021-08-10','Reservar vuelo a Costa Rica','Media',0,'Viajes'),(28,10,'2021-08-06','Terminar funcionalidad UPDATE Y DELETE','Alta',1,'Trabajo'),(29,10,'2021-08-08','Modificar registro html y CSS','Alta',1,'Trabajo'),(30,10,'2021-08-07','Organizar el CSS de toda la pagina','Alta',0,'Trabajo'),(31,10,'2021-08-07','Bañar a mi perro','Media',0,'Mascotas'),(32,10,'2021-08-08','Organizar Macro','Alta',0,'Trabajo'),(33,9,'2021-08-01','Estudiar Opti','Media',0,'Trabajo'),(34,9,'2021-07-13','Salir a la Costa','Baja',0,'Recreacion'),(35,9,'2021-07-13','Chequear maleta para ir a la costa','Media',0,'Recreacion'),(36,9,'2021-08-09','Sacar a pasear a Pipo y a Bruno','Media',0,'Descanso'),(37,5,'2021-07-10','Estudiar Macro','Media',1,'Productividad'),(38,5,'2021-07-10','Realizar tarea corta Macro','Media',0,'Productividad'),(39,5,'2021-08-05','Estudiar Infe','Baja',0,'Trabajo'),(40,5,'2021-08-05','Salir a pasear','Baja',1,'Descanso'),(41,7,'2021-08-05','Estudiar Fluidos','Alta',0,'Productividad'),(42,7,'2021-08-09','Salir al Tunco','Baja',1,'Descanso'),(43,7,'2021-08-06','Mandar login','Media',0,'Trabajo'),(44,7,'2021-08-07','Mandar actualizacion del CSS','Alta',0,'Trabajo'),(45,6,'2021-08-06','Consultar plantilla Index','Alta',0,'Trabajo'),(46,6,'2021-08-07','Terminar de modificar plantilla Index','Alta',0,'Trabajo'),(47,6,'2021-08-07','Mandar plantilla Index modificada','Media',0,'Trabajo'),(48,8,'2021-08-07','Terminar de modificar la plantilla de Index con imagenes','Alta',0,'Trabajo'),(49,8,'2021-08-07','Mandar plantilla modificada al 100% del index','Alta',0,'Trabajo');
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` text NOT NULL,
  `salt` text NOT NULL,
  `admin` tinyint NOT NULL,
  `creation` date NOT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'BadBunny','bad@bad.com','$2b$14$4iLz9Lh01YHtRwCMlx/dSO.zxpt6OIgwRIE57PEyD4tbVAVBbyICe','$2b$14$4iLz9Lh01YHtRwCMlx/dSO',0,'2021-06-13'),(2,'Diego','die@die.com','$2b$14$Z.izT9lzfAlN.NZ4Qc72M.0G7rYJ7tgq5O4n18untGeIQFfTl0P8.','$2b$14$Z.izT9lzfAlN.NZ4Qc72M.',1,'2021-06-13'),(3,'Taylor','tay@ts.com','$2b$14$jFulHI2Seh/HAphXTbvsY.GhplF9Csa.upGsSxFXbFYCIFq/s4TNu','$2b$14$jFulHI2Seh/HAphXTbvsY.',0,'2021-08-03'),(4,'Sierra Madre','bose@bose.com','$2b$14$hwOjRSRK7QD9HFPWXeVvHuXkNajeE2gHdjIddkABlaaALQVZFXWQe','$2b$14$hwOjRSRK7QD9HFPWXeVvHu',0,'2021-08-06'),(5,'Aaron','a@a.com','$2b$14$Kn/C3DQ13D0ZJWHg4sJyKuKleyfRF//K9i4TjCtov3uuh/jgz3T9S','$2b$14$Kn/C3DQ13D0ZJWHg4sJyKu',0,'2021-08-07'),(6,'Victoria','v@v.com','$2b$14$.ZQP93P8vhW4FWOjmKj2N.pjCwu1nUJ28aLsGP5DHlBEcKN/AnOHW','$2b$14$.ZQP93P8vhW4FWOjmKj2N.',0,'2021-08-07'),(7,'Keavy','ke@ke.com','$2b$14$38WDxZfNbfGgkqBUvh2laOdHwWHZy9kcDjoNywXXgi5PMiYErtiFu','$2b$14$38WDxZfNbfGgkqBUvh2laO',0,'2021-08-07'),(8,'Isela','i@i.com','$2b$14$dguQ5uy3UDOdd0UUU1k/C.PK8kNucydVm2OlWzm1SUXqUpdeV5W6u','$2b$14$dguQ5uy3UDOdd0UUU1k/C.',0,'2021-08-07'),(9,'Marcela','mar@mar.com','$2b$14$gOsTXFs8/RzPu3eec.n3DuxbMiXHHe0DiC0crBA.1Zs1vXrCmdRW.','$2b$14$gOsTXFs8/RzPu3eec.n3Du',1,'2021-08-07'),(10,'Angela','an@an.com','$2b$14$UsZQOhIot7vlpGsOgL70Cuem41aROHsWfebtYZ/RofrSnL/5Jqub.','$2b$14$UsZQOhIot7vlpGsOgL70Cu',1,'2021-08-07');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-07 15:28:49
