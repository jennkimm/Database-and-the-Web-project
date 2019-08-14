-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: mytwits
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `twits`
--

DROP TABLE IF EXISTS `twits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `twits` (
  `twit_id` int(11) NOT NULL AUTO_INCREMENT,
  `twit` varchar(140) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`twit_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `twits_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `twits`
--

LOCK TABLES `twits` WRITE;
/*!40000 ALTER TABLE `twits` DISABLE KEYS */;
INSERT INTO `twits` VALUES (1,'i am not a bot',1,'2017-12-23 08:17:07'),(2,'nor me; i am also not a bot',2,'2017-12-23 08:17:38'),(3,'i am a bot that hunts bots - beware!!! editing!',3,'2017-12-23 08:18:37'),(4,'test user id = 1',1,'2018-02-04 16:42:23');
/*!40000 ALTER TABLE `twits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `salt` varchar(150) DEFAULT NULL,
  `hashed` varchar(150) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `image` BLOB DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'dan1','password1','salt','91851f8b157ca4053908b8d105a26c54b3cda24e8848e1479ebd22cd2fcac587feb89f4224fbcb1479d9fd0fd04b9f16047642538507bed252c73438dc46e230','skim037@gold.ac.uk'),(2,'dan2','password2','salty','b50a25014a978c2b2a5bfdcd6e723eed307531d35846803ccfa72e22d5d7f2f9d8d5ee23418a4b4fdd2ed1fd504c8df0673a33682aa985fe80ee58f60b5595bb','skim037@gold.ac.uk'),(3,'dan3','password3','salted','3289efc1e7d7e653014233453e5e660d7af9aa1ecf0339b3b9f03b80c2e450377220f7426e69d6735b6d6b47b38aea911312e13a9416c2e18d48fca31aa95ea9','skim037@gold.ac.uk');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-02-06 23:25:53
