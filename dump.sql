-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: fsd
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `salt` varchar(150) NOT NULL,
  `hashed` varchar(150) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `authenticated` bit Default 1 NOT NULL,
  `activate` bit Default 1 NOT NULL,
  `anonymous` bit Default 0 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--
--
LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (id, username, email, salt, hashed) VALUES (1,"giraffefrogs","giraffefrogs@gmail.com","Fclzfn+H5aLP8aTl5NFOVvlwWEY=","195fee5e7671ed08afb96748607d3d0e454476928818c94ff116bdbc46b8f5b31b960240de9ba7d4090f2946ee64784e7bc11a1edd810edeee0dff8b71f5eb3e");
INSERT INTO `users` (id, username, email, salt, hashed) VALUES (2,"apebanana","apebanana@gmail.com","RQDPHXXAhA+ESsDXDyw1Zv92QEA=","016fd9796d4d36bd4f5f166cb30f7676d0dc193647a764e95496d82e4b3bd58ded98e34720a7eeabe9c422f5cc62ed9ef3b2c4752ab65b6367c1ccc58cb420dc");
INSERT INTO `users` (id, username, email, salt, hashed) VALUES (3,"monkeychicken","monkeychicken@gmail.com","CF1EByLjx0ekz2hOi5QafOVAQAE=","2ba9afb23624a0c50c2e0e61d42dd7307925e04cd26f641406471ad217bd9cb3429e93bc64dd360bda2411c440251a85537f89cce96f51d9a540d1a40f9ffaeb");
INSERT INTO `users` (id, username, email, salt, hashed) VALUES (4,"catmince","catmince@gmail.com","9PzdxmTZ0VZWN115m8I3UweN468=","e7fb4d84577293a1f28b75bf394a28f56fe87288c98d29c38eea4d0c4fcbf1971043e419019a12f88f829aa323b3a9fce04730a3fe8656cea7ffed3f881bbc8a");
INSERT INTO `users` (id, username, email, salt, hashed) VALUES (5,"donkeymince","donkeymince@gmail.com","dgOlPVt8Ax53MiHtUyvYz0Fh7FU=","6fa82a46901918a45b8a1f8410fbe3c1a6b710174f4e947d90cbe85946fc4c7dd73cad708e57b8f6b12cdeeba3b89af5309bd641fe458e2fa4cd7442168734d6");
INSERT INTO `users` (id, username, email, salt, hashed) VALUES (6,"kangarooegg","kangarooegg@gmail.com","mq/lTTdaaVlngSdPPeJVs2r1sV0=","49e0dbd76e06e190c1a99e20ec50196df1c79e14a3cfa9865ec01f8863507b85b54015c9c986309d2eca13b485cdb853421d71152a7d617d5dc43e38890e8a76");
INSERT INTO `users` (id, username, email, salt, hashed) VALUES (7,"birdbroccoli","birdbroccoli@gmail.com","qOKc94GUa7WczcgialZ7+1wC32w=","462da44de5f3e12a3cda0285655b35bc81ae640e269f65f3d1fe8f425f45f8dfe3df038ca2742c7ea9fc6c27faf8ce89d7b6f4fa7bc4ddac036e20221e9c2a87");
INSERT INTO `users` (id, username, email, salt, hashed) VALUES (8,"trollcarrot","trollcarrot@gmail.com","5Kc/e6cW5JO0nsJPNLUDgsvlmEo=","fa6d89591fd400e382424756ba831cd40e0f073144d9526abf4fabb9d8b46479a244c545dc44657a623b650bb4060cc375d6012ca54590af4a32b107a012ff19");
INSERT INTO `users` (id, username, email, salt, hashed) VALUES (9,"octopusice","octopusice@gmail.com","IeeIDuko1ICEdwm6C4oU8DmyOs4=","1be2d129a8ad1a9f5d1344697c57aa469801cd1cd98e61ba0a1c70988b386acefddaea4f69dfa1bfeacfcf855bad37fd290d859775b3461419e88533dff5117d");
INSERT INTO `users` (id, username, email, salt, hashed) VALUES (10,"catpie","catpie@gmail.com","tth8jhenlnnBRBTJReC9BeE1Mpw=","84c6eb93b5f98732ef9b39958dab54596db607de6d324c8c5b88f7a6f15dfaf2dcd0fcbb21dbd27a1b2f32e8b35078badfafa0a5223b34dba796ef4359a11f92");
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meals`
--

DROP TABLE IF EXISTS `meals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(400) DEFAULT NULL,
  `postcode` varchar(20) NOT NULL,
  `image` TEXT,
  `guest_num` int(3) DEFAULT 1 NOT NULL,
  `date` DATE NOT NULL,
  `time` TIME NOT NULL,
  `price` float NOT Null DEFAULT 0,
  `lat` float NOT Null,
  `lng` float NOT Null,
  `user_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `id` (`id`),
  CONSTRAINT `meals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meals`
--

LOCK TABLES `meals` WRITE;
/*!40000 ALTER TABLE `meals` DISABLE KEYS */;
INSERT INTO `meals` (id, name, description, postcode, guest_num, date, time, price, lat, lng, user_id) VALUES (1, "end of exams party", "Celebrate end of the exams and let's have party all night long!!!", "SE15 6TU", 21, "2018-11-03", "13:20:00", 20, 51.481507, -0.066121, 1);
INSERT INTO `meals` (id, name, description, postcode, guest_num, date, time, price, lat, lng, user_id) VALUES (2, "Chocolate deal", "Shut up and eat chotolate.", "SE13 7GE", 5, "2018-07-06", "12:30:00", 5, 51.462089, -0.015908, 4);
INSERT INTO `meals` (id, name, description, postcode, guest_num, date, time, price, lat, lng, user_id) VALUES (3, "beer time", "Drink Drink Drink", "SE16 6NA", 12, "2018-06-06", "19:30:00", 10, 51.504943, -0.038054, 1);
INSERT INTO `meals` (id, name, description, postcode, guest_num, date, time, price, lat, lng, user_id) VALUES (4, "Chinese food festival", "Everyone is welcome to try out our Chinese food.", "SE6 4NJ", 30, "2018-06-06", "19:30:00", 10, 51.440606, -0.031977, 1);
INSERT INTO `meals` (id, name, description, postcode, guest_num, date, time, price, lat, lng, user_id) VALUES (5, "Meat Time!!!", "Even if we enjoy the meat a lot but vegan food is served as well.", "SE15 3JW", 4, "2018-5-16", "20:30:00", 30, 51.463672, -0.0589, 7);
INSERT INTO `meals` (id, name, description, postcode, guest_num, date, time, price, lat, lng, user_id) VALUES (6, "Bring your own food", "Please bring and share your own food with us.", "SE20 8RW", 10, "2018-05-06", "12:30:00", 0, 51.414256, -0.052869, 5);
INSERT INTO `meals` (id, name, description, postcode, guest_num, date, time, price, lat, lng, user_id) VALUES (7, "Italy night", "Lets make our own pizza night.", "SE16 4QA", 4, "2018-06-06", "19:30:00", 15, 51.499046, -0.062541, 9);
INSERT INTO `meals` (id, name, description, postcode, guest_num, date, time, price, lat, lng, user_id) VALUES (8, "Japanese zen time", "Sushi is the best.", "SE20 7HJ", 5, "2018-06-06", "19:30:00", 30, 51.417882, -0.058942, 7);
INSERT INTO `meals` (id, name, description, postcode, guest_num, date, time, price, lat, lng, user_id) VALUES (9, "Come and meat up", ":)", "SE5 9DB", 30, "2018-06-06", "19:30:00", 5, 51.469824, -0.099602, 3);
INSERT INTO `meals` (id, name, description, postcode, guest_num, date, time, price, lat, lng, user_id) VALUES (10, "Weekly meetup", "Time to meet new friends!", "SE22 0PJ", 10, "2018-06-06", "19:30:00", 12, 51.446569, -0.068246, 2);
/*!40000 ALTER TABLE `meals` ENABLE KEYS */;
UNLOCK TABLES;


/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

--
-- Table structure for table `reservations`
--

DROP TABLE IF EXISTS `reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `meal_id` int(11) NOT NULL,
  `guest_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`meal_id`) REFERENCES `meals` (`id`),
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`guest_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Dumping data for table `reservations`
--

LOCK TABLES `reservations` WRITE;
/*!40000 ALTER TABLE `reservations` DISABLE KEYS */;
INSERT INTO `reservations` (meal_id,guest_id) VALUES(5,9);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(7,3);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(1,3);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(6,6);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(5,6);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(7,7);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(3,7);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(8,5);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(4,9);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(5,5);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(3,3);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(6,7);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(8,1);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(3,10);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(4,4);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(6,10);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(8,10);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(7,6);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(6,3);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(10,4);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(8,2);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(1,4);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(7,5);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(10,10);
INSERT INTO `reservations` (meal_id,guest_id) VALUES(6,1);
/*!40000 ALTER TABLE `reservations` ENABLE KEYS */;
UNLOCK TABLES;
