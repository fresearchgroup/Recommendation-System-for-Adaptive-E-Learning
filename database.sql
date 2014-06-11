-- MySQL dump 10.13  Distrib 5.5.37, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: django_db
-- ------------------------------------------------------
-- Server version	5.5.37-0ubuntu0.14.04.1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add feedback',7,'add_feedback'),(20,'Can change feedback',7,'change_feedback'),(21,'Can delete feedback',7,'delete_feedback'),(22,'Can add course',8,'add_course'),(23,'Can change course',8,'change_course'),(24,'Can delete course',8,'delete_course'),(25,'Can add student',9,'add_student'),(26,'Can change student',9,'change_student'),(27,'Can delete student',9,'delete_student'),(28,'Can add student state',10,'add_studentstate'),(29,'Can change student state',10,'change_studentstate'),(30,'Can delete student state',10,'delete_studentstate'),(31,'Can add course dependency',11,'add_coursedependency'),(32,'Can change course dependency',11,'change_coursedependency'),(33,'Can delete course dependency',11,'delete_coursedependency'),(34,'Can add question',12,'add_question'),(35,'Can change question',12,'change_question'),(36,'Can delete question',12,'delete_question'),(37,'Can add question_ concept',13,'add_question_concept'),(38,'Can change question_ concept',13,'change_question_concept'),(39,'Can delete question_ concept',13,'delete_question_concept'),(40,'Can add question_ concept_new',14,'add_question_concept_new'),(41,'Can change question_ concept_new',14,'change_question_concept_new'),(42,'Can delete question_ concept_new',14,'delete_question_concept_new'),(43,'Can add grade',15,'add_grade'),(44,'Can change grade',15,'change_grade'),(45,'Can delete grade',15,'delete_grade'),(46,'Can add confidence rto r',16,'add_confidencertor'),(47,'Can change confidence rto r',16,'change_confidencertor'),(48,'Can delete confidence rto r',16,'delete_confidencertor'),(49,'Can add confidence wto w',17,'add_confidencewtow'),(50,'Can change confidence wto w',17,'change_confidencewtow'),(51,'Can delete confidence wto w',17,'delete_confidencewtow'),(52,'Can add q1 q2 right wrong',18,'add_q1q2rightwrong'),(53,'Can change q1 q2 right wrong',18,'change_q1q2rightwrong'),(54,'Can delete q1 q2 right wrong',18,'delete_q1q2rightwrong'),(55,'Can add ratings',19,'add_ratings'),(56,'Can change ratings',19,'change_ratings'),(57,'Can delete ratings',19,'delete_ratings'),(58,'Can add task state',20,'add_taskmeta'),(59,'Can change task state',20,'change_taskmeta'),(60,'Can delete task state',20,'delete_taskmeta'),(61,'Can add saved group result',21,'add_tasksetmeta'),(62,'Can change saved group result',21,'change_tasksetmeta'),(63,'Can delete saved group result',21,'delete_tasksetmeta'),(64,'Can add interval',22,'add_intervalschedule'),(65,'Can change interval',22,'change_intervalschedule'),(66,'Can delete interval',22,'delete_intervalschedule'),(67,'Can add crontab',23,'add_crontabschedule'),(68,'Can change crontab',23,'change_crontabschedule'),(69,'Can delete crontab',23,'delete_crontabschedule'),(70,'Can add periodic tasks',24,'add_periodictasks'),(71,'Can change periodic tasks',24,'change_periodictasks'),(72,'Can delete periodic tasks',24,'delete_periodictasks'),(73,'Can add periodic task',25,'add_periodictask'),(74,'Can change periodic task',25,'change_periodictask'),(75,'Can delete periodic task',25,'delete_periodictask'),(76,'Can add worker',26,'add_workerstate'),(77,'Can change worker',26,'change_workerstate'),(78,'Can delete worker',26,'delete_workerstate'),(79,'Can add task',27,'add_taskstate'),(80,'Can change task',27,'change_taskstate'),(81,'Can delete task',27,'delete_taskstate');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$12000$z12kclo3wRfv$sDVmZNi+CPLYDZCO5DS3mqpozbfCsekf0DtOFW+3Smc=','2014-06-10 11:22:13',1,'devanshu','','','devanshu.jain919@gmail.com',1,1,'2014-06-06 12:05:38'),(22,'pbkdf2_sha256$12000$YgqgzWOR41rc$lzS3+0/MAr3C+Eu/0yXV7sQGideoH3UsCIc5DltgiG0=','2014-06-06 18:05:03',0,'student1','','','student1@gmail.com',0,1,'2014-06-06 18:05:03'),(23,'pbkdf2_sha256$12000$0QfoV4oTrHzF$4qlbhMZfkTc3Vv7EL3AJRq4TubgHfbRU7IypFkhLb5o=','2014-06-06 18:35:17',0,'student2','','','student2@gmail.com',0,1,'2014-06-06 18:35:17');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_taskmeta`
--

DROP TABLE IF EXISTS `celery_taskmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celery_taskmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `result` longtext,
  `date_done` datetime NOT NULL,
  `traceback` longtext,
  `hidden` tinyint(1) NOT NULL,
  `meta` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `celery_taskmeta_2ff6b945` (`hidden`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_taskmeta`
--

LOCK TABLES `celery_taskmeta` WRITE;
/*!40000 ALTER TABLE `celery_taskmeta` DISABLE KEYS */;
INSERT INTO `celery_taskmeta` VALUES (1,'13c1cca1-e0d7-4533-947a-35ecc6aadd65','FAILURE','gAJjZXhjZXB0aW9ucwpBdHRyaWJ1dGVFcnJvcgpxAVUnJ2ludCcgb2JqZWN0IGhhcyBubyBhdHRyaWJ1dGUgJ3Nlc3Npb24ncQKFcQNScQQu','2014-06-10 09:42:35','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 40, in concept_map\n    questionList_attempted = Question.objects.filter(course_id = course_id)\nAttributeError: \'int\' object has no attribute \'session\'\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(2,'007c62c9-333c-42a9-9c0c-4c8e4a74e0ca','FAILURE','gAJjZXhjZXB0aW9ucwpBdHRyaWJ1dGVFcnJvcgpxAVUnJ2ludCcgb2JqZWN0IGhhcyBubyBhdHRyaWJ1dGUgJ3Nlc3Npb24ncQKFcQNScQQu','2014-06-10 09:43:49','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 40, in concept_map\n    questionList_attempted = Question.objects.filter(course_id = int(course_id))\nAttributeError: \'int\' object has no attribute \'session\'\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(3,'2681d8e7-f3e2-400c-b80a-83ce2fcc82a5','FAILURE','gAJjZXhjZXB0aW9ucwpBdHRyaWJ1dGVFcnJvcgpxAVUnJ2ludCcgb2JqZWN0IGhhcyBubyBhdHRyaWJ1dGUgJ3Nlc3Npb24ncQKFcQNScQQu','2014-06-10 09:44:28','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 40, in concept_map\n    print \"course_id = \" + course_id\nAttributeError: \'int\' object has no attribute \'session\'\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(4,'97581f9c-3878-4816-abe7-435093b00878','FAILURE','gAJjZXhjZXB0aW9ucwpBdHRyaWJ1dGVFcnJvcgpxAVUnJ2ludCcgb2JqZWN0IGhhcyBubyBhdHRyaWJ1dGUgJ3Nlc3Npb24ncQKFcQNScQQu','2014-06-10 09:45:23','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 40, in concept_map\n    print \"course_id = \" + course_id\nAttributeError: \'int\' object has no attribute \'session\'\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(5,'3329c327-3b66-4bbd-a8a6-0c7faf4cd9e5','FAILURE','gAJjZXhjZXB0aW9ucwpBdHRyaWJ1dGVFcnJvcgpxAVUnJ2ludCcgb2JqZWN0IGhhcyBubyBhdHRyaWJ1dGUgJ3Nlc3Npb24ncQKFcQNScQQu','2014-06-10 09:47:22','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 40, in concept_map\n    print \"course_id = \" + course_id\nAttributeError: \'int\' object has no attribute \'session\'\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(6,'af3aa6a9-25a1-42f6-8740-6c88b566a616','FAILURE','gAJjZXhjZXB0aW9ucwpUeXBlRXJyb3IKcQFVKmNhbm5vdCBjb25jYXRlbmF0ZSAnc3RyJyBhbmQgJ2ludCcgb2JqZWN0c3EChXEDUnEELg==','2014-06-10 09:48:06','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 40, in concept_map\n    print \"course_id = \" + course_id\nTypeError: cannot concatenate \'str\' and \'int\' objects\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(7,'a3d40bfe-fb81-415d-a9ff-6c634b954ffe','FAILURE','gAJjZXhjZXB0aW9ucwpUeXBlRXJyb3IKcQFVKmNhbm5vdCBjb25jYXRlbmF0ZSAnc3RyJyBhbmQgJ2ludCcgb2JqZWN0c3EChXEDUnEELg==','2014-06-10 09:48:29','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 40, in concept_map\n    print \"course_id = \" + course_id\nTypeError: cannot concatenate \'str\' and \'int\' objects\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(8,'573d0557-3ae5-42dd-bcb5-a53dabd8ecdf','FAILURE','gAJjZXhjZXB0aW9ucwpOYW1lRXJyb3IKcQFVJGdsb2JhbCBuYW1lICdzdHVkZW50JyBpcyBub3QgZGVmaW5lZHEChXEDUnEELg==','2014-06-10 09:48:47','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 53, in concept_map\n    object1 = Grade.objects.get(questionID=question1,studentID=student)\nNameError: global name \'student\' is not defined\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(9,'ae877831-c96c-416a-a257-ae39f4d67e97','FAILURE','gAJjZXhjZXB0aW9ucwpUeXBlRXJyb3IKcQFVMGNvbmNlcHRfbWFwKCkgdGFrZXMgZXhhY3RseSAxIGFyZ3VtZW50ICgyIGdpdmVuKXEChXEDUnEELg==','2014-06-10 09:49:39','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\nTypeError: concept_map() takes exactly 1 argument (2 given)\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(10,'8ae30312-ebe2-4009-8c46-7a7be65a5562','FAILURE','gAJjZXhjZXB0aW9ucwpUeXBlRXJyb3IKcQFVMGNvbmNlcHRfbWFwKCkgdGFrZXMgZXhhY3RseSAxIGFyZ3VtZW50ICgyIGdpdmVuKXEChXEDUnEELg==','2014-06-10 09:49:53','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\nTypeError: concept_map() takes exactly 1 argument (2 given)\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(11,'35e568e0-7293-4de4-87bb-1092479ca704','SUCCESS',NULL,'2014-06-10 09:50:21',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(12,'117addfa-9865-476b-bd8b-ada201d547b7','SUCCESS',NULL,'2014-06-10 09:51:18',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(13,'f4bc85b8-574e-4f72-aae7-58dec6fc46cc','SUCCESS',NULL,'2014-06-10 09:52:32',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(14,'4f932ee9-b0d5-409c-84dc-48565f1ca961','FAILURE','gAJjZXhjZXB0aW9ucwpaZXJvRGl2aXNpb25FcnJvcgpxAVUWZmxvYXQgZGl2aXNpb24gYnkgemVyb3EChXEDUnEELg==','2014-06-10 09:53:47','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 206, in concept_map\n    value2 = float(scoreRight)/float(scoreTargetRight)\nZeroDivisionError: float division by zero\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(15,'dcfedcaf-b0bb-4a0f-bafb-7e215f2b7f36','FAILURE','gAJjZXhjZXB0aW9ucwpaZXJvRGl2aXNpb25FcnJvcgpxAVUWZmxvYXQgZGl2aXNpb24gYnkgemVyb3EChXEDUnEELg==','2014-06-10 09:54:17','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 206, in concept_map\n    value2 = float(scoreRight)/float(scoreTargetRight)\nZeroDivisionError: float division by zero\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(16,'bc4b7df4-5615-4291-a93d-b4fde80901b4','FAILURE','gAJjZXhjZXB0aW9ucwpaZXJvRGl2aXNpb25FcnJvcgpxAVUWZmxvYXQgZGl2aXNpb24gYnkgemVyb3EChXEDUnEELg==','2014-06-10 09:54:35','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 206, in concept_map\n    value2 = float(scoreRight)/float(scoreTargetRight)\nZeroDivisionError: float division by zero\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(17,'e49d2fc0-9758-4512-96f5-3c1b1c8eaa63','FAILURE','gAJjZXhjZXB0aW9ucwpaZXJvRGl2aXNpb25FcnJvcgpxAVUWZmxvYXQgZGl2aXNpb24gYnkgemVyb3EChXEDUnEELg==','2014-06-10 11:14:41','Traceback (most recent call last):\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 240, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"/usr/local/lib/python2.7/dist-packages/celery/app/trace.py\", line 437, in __protected_call__\n    return self.run(*args, **kwargs)\n  File \"/home/devanshu/summer_django_iitb/mysite/firstapp/tasks.py\", line 206, in concept_map\n    value2 = float(scoreRight)/float(scoreTargetRight)\nZeroDivisionError: float division by zero\n',0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(18,'2c132048-54b3-4564-bcd2-0f37450b80f6','SUCCESS',NULL,'2014-06-10 11:21:42',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(19,'1b32cc21-910f-4292-ab67-6cfff15e699a','SUCCESS',NULL,'2014-06-10 11:23:20',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(20,'5ec6b7fb-a4b9-4ced-a78b-322029b8154c','SUCCESS',NULL,'2014-06-10 11:28:34',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(21,'e0b6e7f9-d625-4ad2-90e7-c798947f3644','SUCCESS',NULL,'2014-06-10 11:29:35',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(22,'da6199f9-94f4-4654-bda8-c23c5d722322','SUCCESS',NULL,'2014-06-10 11:29:47',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(23,'044b7b1c-bcfc-4df5-940a-7d7695a28034','SUCCESS',NULL,'2014-06-10 11:30:08',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(24,'9c29f550-4212-4ce4-978c-4cf5cbe115cb','SUCCESS',NULL,'2014-06-10 11:31:39',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(25,'fb053091-ca2c-4a0c-a4b0-8249cff1d3cb','SUCCESS',NULL,'2014-06-10 11:32:12',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(26,'1d083033-a30a-47ea-a69f-8b30286856c6','SUCCESS',NULL,'2014-06-11 06:26:21',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(27,'71aaadfc-7f61-46f6-a671-2c573340eb78','SUCCESS',NULL,'2014-06-11 06:26:21',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(28,'26aa90e3-8ab4-4e74-bdaa-8eac96c1962f','SUCCESS',NULL,'2014-06-11 06:26:22',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA'),(29,'367832eb-fcd7-47d6-ad7b-5a18d032d67b','SUCCESS',NULL,'2014-06-11 06:26:38',NULL,0,'eJxrYKotZIzgYGBgSM7IzEkpSs0rZIotZC7WAwBWuwcA');
/*!40000 ALTER TABLE `celery_taskmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_tasksetmeta`
--

DROP TABLE IF EXISTS `celery_tasksetmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celery_tasksetmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskset_id` varchar(255) NOT NULL,
  `result` longtext NOT NULL,
  `date_done` datetime NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taskset_id` (`taskset_id`),
  KEY `celery_tasksetmeta_2ff6b945` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_tasksetmeta`
--

LOCK TABLES `celery_tasksetmeta` WRITE;
/*!40000 ALTER TABLE `celery_tasksetmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_tasksetmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2014-06-06 12:07:15',1,8,'1','foundation',1,''),(2,'2014-06-06 12:07:48',1,8,'2','Basics of C Programming',1,''),(3,'2014-06-06 12:08:09',1,8,'3','Decision making',1,''),(4,'2014-06-06 12:08:19',1,8,'4','Iterations',1,''),(5,'2014-06-06 12:08:30',1,8,'5','Arrays and Structures',1,''),(6,'2014-06-06 12:16:10',1,4,'2','student1',3,''),(7,'2014-06-06 12:23:15',1,8,'5','Arrays and Structures',3,''),(8,'2014-06-06 12:23:15',1,8,'4','Iterations',3,''),(9,'2014-06-06 12:23:15',1,8,'3','Decision making',3,''),(10,'2014-06-06 12:23:15',1,8,'2','Basics of C Programming',3,''),(11,'2014-06-06 12:23:15',1,8,'1','foundation',3,''),(12,'2014-06-06 12:23:53',1,8,'6','foundation',1,''),(13,'2014-06-06 12:24:01',1,8,'7','Basics of C Programming',1,''),(14,'2014-06-06 12:24:09',1,8,'8','Decision making',1,''),(15,'2014-06-06 12:24:16',1,8,'9','Iterations',1,''),(16,'2014-06-06 12:24:23',1,8,'10','Arrays and Structures',1,''),(17,'2014-06-06 12:24:51',1,4,'4','student1',3,''),(18,'2014-06-06 12:48:28',1,9,'2','student1',3,''),(19,'2014-06-06 12:48:36',1,4,'5','student1',3,''),(20,'2014-06-06 14:31:30',1,8,'10','Arrays and Structures',3,''),(21,'2014-06-06 14:31:30',1,8,'9','Iterations',3,''),(22,'2014-06-06 14:31:30',1,8,'8','Decision making',3,''),(23,'2014-06-06 14:31:30',1,8,'7','Basics of C Programming',3,''),(24,'2014-06-06 14:31:30',1,8,'6','foundation',3,''),(25,'2014-06-06 14:31:48',1,4,'6','student1',3,''),(26,'2014-06-06 14:31:48',1,4,'7','student2',3,''),(27,'2014-06-06 14:32:39',1,8,'11','foundation',1,''),(28,'2014-06-06 14:32:49',1,8,'12','Basics of C Programming',1,''),(29,'2014-06-06 14:32:57',1,8,'13','Decision making',1,''),(30,'2014-06-06 14:33:04',1,8,'14','Iterations',1,''),(31,'2014-06-06 14:33:11',1,8,'15','Arrays and Structures',1,''),(32,'2014-06-06 14:34:19',1,4,'8','student1',3,''),(33,'2014-06-06 14:35:23',1,4,'10','student1',3,''),(34,'2014-06-06 14:36:24',1,4,'13','student1',3,''),(35,'2014-06-06 17:46:43',1,4,'15','student1',3,''),(36,'2014-06-06 17:46:43',1,4,'16','student2',3,''),(37,'2014-06-06 17:46:44',1,4,'17','student3',3,''),(38,'2014-06-06 17:46:44',1,4,'18','student4',3,''),(39,'2014-06-06 17:49:23',1,4,'19','student1',3,''),(40,'2014-06-06 18:03:27',1,4,'20','student1',3,''),(41,'2014-06-06 18:04:50',1,4,'21','student1',3,''),(42,'2014-06-10 11:22:29',1,4,'24','student3',3,''),(43,'2014-06-10 11:22:30',1,4,'25','student4',3,''),(44,'2014-06-10 11:22:30',1,4,'26','student5',3,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'feedback','firstapp','feedback'),(8,'course','firstapp','course'),(9,'student','firstapp','student'),(10,'student state','firstapp','studentstate'),(11,'course dependency','firstapp','coursedependency'),(12,'question','firstapp','question'),(13,'question_ concept','firstapp','question_concept'),(14,'question_ concept_new','firstapp','question_concept_new'),(15,'grade','firstapp','grade'),(16,'confidence rto r','firstapp','confidencertor'),(17,'confidence wto w','firstapp','confidencewtow'),(18,'q1 q2 right wrong','firstapp','q1q2rightwrong'),(19,'ratings','firstapp','ratings'),(20,'task state','djcelery','taskmeta'),(21,'saved group result','djcelery','tasksetmeta'),(22,'interval','djcelery','intervalschedule'),(23,'crontab','djcelery','crontabschedule'),(24,'periodic tasks','djcelery','periodictasks'),(25,'periodic task','djcelery','periodictask'),(26,'worker','djcelery','workerstate'),(27,'task','djcelery','taskstate');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0yerkqr5yi4ycr51qnampx0djbzqoe25','NzNlMjE5ZDU1ZTQ5YzRkOTY4NDFkNDI3YThlZDUxNjkyM2M1MjMwZTp7Il9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2014-06-21 05:53:17'),('81cws5b9c30u3it3kzkh18toje9184rn','NzNlMjE5ZDU1ZTQ5YzRkOTY4NDFkNDI3YThlZDUxNjkyM2M1MjMwZTp7Il9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2014-06-25 06:28:32');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_crontabschedule`
--

DROP TABLE IF EXISTS `djcelery_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(64) NOT NULL,
  `hour` varchar(64) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(64) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_crontabschedule`
--

LOCK TABLES `djcelery_crontabschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_intervalschedule`
--

DROP TABLE IF EXISTS `djcelery_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_intervalschedule`
--

LOCK TABLES `djcelery_intervalschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictask`
--

DROP TABLE IF EXISTS `djcelery_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `interval_id` int(11) DEFAULT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `djcelery_periodictask_8905f60d` (`interval_id`),
  KEY `djcelery_periodictask_7280124f` (`crontab_id`),
  CONSTRAINT `crontab_id_refs_id_286da0d1` FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`),
  CONSTRAINT `interval_id_refs_id_1829f358` FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictask`
--

LOCK TABLES `djcelery_periodictask` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictask` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictasks`
--

DROP TABLE IF EXISTS `djcelery_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictasks`
--

LOCK TABLES `djcelery_periodictasks` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_taskstate`
--

DROP TABLE IF EXISTS `djcelery_taskstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_taskstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(64) NOT NULL,
  `task_id` varchar(36) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `tstamp` datetime NOT NULL,
  `args` longtext,
  `kwargs` longtext,
  `eta` datetime DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  `result` longtext,
  `traceback` longtext,
  `runtime` double DEFAULT NULL,
  `retries` int(11) NOT NULL,
  `worker_id` int(11) DEFAULT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `djcelery_taskstate_5654bf12` (`state`),
  KEY `djcelery_taskstate_4da47e07` (`name`),
  KEY `djcelery_taskstate_abaacd02` (`tstamp`),
  KEY `djcelery_taskstate_cac6a03d` (`worker_id`),
  KEY `djcelery_taskstate_2ff6b945` (`hidden`),
  CONSTRAINT `worker_id_refs_id_6fd8ce95` FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_taskstate`
--

LOCK TABLES `djcelery_taskstate` WRITE;
/*!40000 ALTER TABLE `djcelery_taskstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_taskstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_workerstate`
--

DROP TABLE IF EXISTS `djcelery_workerstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_workerstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(255) NOT NULL,
  `last_heartbeat` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  KEY `djcelery_workerstate_11e400ef` (`last_heartbeat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_workerstate`
--

LOCK TABLES `djcelery_workerstate` WRITE;
/*!40000 ALTER TABLE `djcelery_workerstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_workerstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_confidencertor`
--

DROP TABLE IF EXISTS `firstapp_confidencertor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_confidencertor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `questionSource_id` int(11) NOT NULL,
  `questionTarget_id` int(11) NOT NULL,
  `confidenceValue` decimal(3,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `firstapp_confidencertor_998e91e6` (`questionSource_id`),
  KEY `firstapp_confidencertor_08697b3c` (`questionTarget_id`),
  CONSTRAINT `questionSource_id_refs_id_5beb6ff1` FOREIGN KEY (`questionSource_id`) REFERENCES `firstapp_question` (`id`),
  CONSTRAINT `questionTarget_id_refs_id_5beb6ff1` FOREIGN KEY (`questionTarget_id`) REFERENCES `firstapp_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_confidencertor`
--

LOCK TABLES `firstapp_confidencertor` WRITE;
/*!40000 ALTER TABLE `firstapp_confidencertor` DISABLE KEYS */;
INSERT INTO `firstapp_confidencertor` VALUES (116,403,404,1.00),(117,404,403,1.00),(118,403,405,1.00),(119,405,403,1.00),(120,404,405,1.00),(121,405,404,1.00),(122,407,408,1.00),(123,408,407,1.00),(124,406,407,1.00),(125,407,406,1.00),(126,406,408,1.00),(127,408,406,1.00);
/*!40000 ALTER TABLE `firstapp_confidencertor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_confidencewtow`
--

DROP TABLE IF EXISTS `firstapp_confidencewtow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_confidencewtow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `questionSource_id` int(11) NOT NULL,
  `questionTarget_id` int(11) NOT NULL,
  `confidenceValue` decimal(3,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `firstapp_confidencewtow_998e91e6` (`questionSource_id`),
  KEY `firstapp_confidencewtow_08697b3c` (`questionTarget_id`),
  CONSTRAINT `questionSource_id_refs_id_37f5b57b` FOREIGN KEY (`questionSource_id`) REFERENCES `firstapp_question` (`id`),
  CONSTRAINT `questionTarget_id_refs_id_37f5b57b` FOREIGN KEY (`questionTarget_id`) REFERENCES `firstapp_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=572 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_confidencewtow`
--

LOCK TABLES `firstapp_confidencewtow` WRITE;
/*!40000 ALTER TABLE `firstapp_confidencewtow` DISABLE KEYS */;
INSERT INTO `firstapp_confidencewtow` VALUES (517,403,404,1.00),(518,404,403,1.00),(519,403,405,1.00),(520,405,403,1.00),(521,403,406,1.00),(522,403,407,1.00),(523,403,408,1.00),(524,404,405,1.00),(525,405,404,1.00),(526,404,406,1.00),(527,404,407,1.00),(528,404,408,1.00),(529,405,406,1.00),(530,405,407,1.00),(531,405,408,1.00),(532,406,407,1.00),(533,407,406,1.00),(534,406,408,1.00),(535,408,406,1.00),(536,404,403,1.00),(537,405,403,1.00),(538,405,404,1.00),(539,407,406,1.00),(540,408,406,1.00),(541,404,403,1.00),(542,405,403,1.00),(543,405,404,1.00),(544,407,406,1.00),(545,408,406,1.00),(546,404,403,1.00),(547,405,403,1.00),(548,405,404,1.00),(549,407,406,1.00),(550,408,406,1.00),(551,407,408,1.00),(552,408,407,1.00),(553,408,407,1.00),(554,408,407,1.00),(555,408,407,1.00),(556,404,403,1.00),(557,405,403,1.00),(558,406,403,1.00),(559,405,404,1.00),(560,406,404,1.00),(561,406,405,1.00),(562,407,406,1.00),(563,408,406,1.00),(564,404,403,1.00),(565,405,403,1.00),(566,406,403,1.00),(567,405,404,1.00),(568,406,404,1.00),(569,406,405,1.00),(570,407,406,1.00),(571,408,406,1.00);
/*!40000 ALTER TABLE `firstapp_confidencewtow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_course`
--

DROP TABLE IF EXISTS `firstapp_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `content` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_course`
--

LOCK TABLES `firstapp_course` WRITE;
/*!40000 ALTER TABLE `firstapp_course` DISABLE KEYS */;
INSERT INTO `firstapp_course` VALUES (11,'foundation','documents/dummy_1'),(12,'Basics of C Programming','documents/part_1_1.pdf'),(13,'Decision making','documents/part_2_1.pdf'),(14,'Iterations','documents/part_3_1.pdf'),(15,'Arrays and Structures','documents/part_4_1.pdf');
/*!40000 ALTER TABLE `firstapp_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_coursedependency`
--

DROP TABLE IF EXISTS `firstapp_coursedependency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_coursedependency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_source_id` int(11) NOT NULL,
  `course_target_id` int(11) NOT NULL,
  `value` decimal(3,2) NOT NULL,
  `total_stu` int(11) NOT NULL,
  `average_change` decimal(3,2) NOT NULL,
  `similarity` decimal(10,5) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `firstapp_coursedependency_710ddea0` (`course_source_id`),
  KEY `firstapp_coursedependency_3a69002a` (`course_target_id`),
  CONSTRAINT `course_source_id_refs_id_83e6a737` FOREIGN KEY (`course_source_id`) REFERENCES `firstapp_course` (`id`),
  CONSTRAINT `course_target_id_refs_id_83e6a737` FOREIGN KEY (`course_target_id`) REFERENCES `firstapp_course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_coursedependency`
--

LOCK TABLES `firstapp_coursedependency` WRITE;
/*!40000 ALTER TABLE `firstapp_coursedependency` DISABLE KEYS */;
INSERT INTO `firstapp_coursedependency` VALUES (41,11,12,0.25,6,0.31,0.99326),(42,12,11,0.25,0,0.00,0.99326),(43,11,13,0.25,4,0.35,-0.22486),(44,13,11,0.25,0,0.00,-0.22486),(45,12,13,0.25,3,-0.05,-0.11043),(46,13,12,0.25,3,0.10,-0.11043),(47,11,14,0.25,1,0.21,-0.99027),(48,14,11,0.25,0,0.00,-0.99027),(49,12,14,0.25,2,0.34,-0.53464),(50,14,12,0.25,2,-0.05,-0.53464),(51,13,14,0.25,0,0.00,-0.78087),(52,14,13,0.25,0,0.00,-0.78087),(53,11,15,0.25,1,0.44,-0.35088),(54,15,11,0.25,0,0.00,-0.35088),(55,12,15,0.25,3,0.00,-0.68274),(56,15,12,0.25,5,0.07,-0.68274),(57,13,15,0.25,0,0.00,-0.65079),(58,15,13,0.25,0,0.00,-0.65079),(59,14,15,0.25,1,0.36,0.99876),(60,15,14,0.25,3,-0.11,0.99876);
/*!40000 ALTER TABLE `firstapp_coursedependency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_feedback`
--

DROP TABLE IF EXISTS `firstapp_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `q1` varchar(1) NOT NULL,
  `q2` varchar(1) NOT NULL,
  `q3` varchar(1) NOT NULL,
  `q4` varchar(1) NOT NULL,
  `q5` varchar(1) NOT NULL,
  `q6` varchar(1) NOT NULL,
  `q7` varchar(1) NOT NULL,
  `q8` varchar(1) NOT NULL,
  `q9` varchar(1) NOT NULL,
  `q10` varchar(1) NOT NULL,
  `q11` varchar(1) NOT NULL,
  `q12` varchar(1) NOT NULL,
  `q13` varchar(1) NOT NULL,
  `q14` varchar(1) NOT NULL,
  `q15` varchar(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_feedback`
--

LOCK TABLES `firstapp_feedback` WRITE;
/*!40000 ALTER TABLE `firstapp_feedback` DISABLE KEYS */;
INSERT INTO `firstapp_feedback` VALUES (1,'2','5','5','5','','','','','','','','','','',''),(2,'2','5','5','5','','','','','','','','','','',''),(3,'','','','','4','5','5','5','','','','','','','');
/*!40000 ALTER TABLE `firstapp_feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_grade`
--

DROP TABLE IF EXISTS `firstapp_grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_grade` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `questionID_id` int(11) NOT NULL,
  `studentID_id` int(11) NOT NULL,
  `value` int(11) NOT NULL,
  `prev` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `firstapp_grade_18d8447d` (`questionID_id`),
  KEY `firstapp_grade_69772cfd` (`studentID_id`),
  CONSTRAINT `questionID_id_refs_id_3f6d1800` FOREIGN KEY (`questionID_id`) REFERENCES `firstapp_question` (`id`),
  CONSTRAINT `studentID_id_refs_id_827896f8` FOREIGN KEY (`studentID_id`) REFERENCES `firstapp_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=662 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_grade`
--

LOCK TABLES `firstapp_grade` WRITE;
/*!40000 ALTER TABLE `firstapp_grade` DISABLE KEYS */;
INSERT INTO `firstapp_grade` VALUES (645,403,12,1,1),(646,403,13,0,0),(648,404,12,1,1),(649,404,13,0,0),(651,405,12,1,1),(652,405,13,0,0),(654,406,12,1,1),(655,406,13,0,0),(657,407,12,1,1),(658,407,13,1,1),(660,408,12,1,1),(661,408,13,1,1);
/*!40000 ALTER TABLE `firstapp_grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_q1q2rightwrong`
--

DROP TABLE IF EXISTS `firstapp_q1q2rightwrong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_q1q2rightwrong` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_x_id` int(11) NOT NULL,
  `question_y_id` int(11) NOT NULL,
  `right` int(11) NOT NULL,
  `wrong` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `firstapp_q1q2rightwrong_82dbb2ad` (`question_x_id`),
  KEY `firstapp_q1q2rightwrong_7adbd77e` (`question_y_id`),
  CONSTRAINT `question_x_id_refs_id_2854a7dd` FOREIGN KEY (`question_x_id`) REFERENCES `firstapp_question` (`id`),
  CONSTRAINT `question_y_id_refs_id_2854a7dd` FOREIGN KEY (`question_y_id`) REFERENCES `firstapp_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2970 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_q1q2rightwrong`
--

LOCK TABLES `firstapp_q1q2rightwrong` WRITE;
/*!40000 ALTER TABLE `firstapp_q1q2rightwrong` DISABLE KEYS */;
INSERT INTO `firstapp_q1q2rightwrong` VALUES (2949,403,404,1,1),(2950,403,405,1,1),(2951,403,406,0,1),(2952,403,407,0,0),(2953,403,408,0,0),(2954,404,405,1,1),(2955,404,406,0,1),(2956,404,407,0,0),(2957,404,408,0,0),(2958,405,406,0,1),(2959,405,407,0,0),(2960,405,408,0,0),(2961,406,407,1,1),(2962,406,408,1,1),(2963,407,408,1,1),(2964,403,403,1,1),(2965,404,404,1,1),(2966,405,405,1,1),(2967,406,406,1,1),(2968,407,407,1,1),(2969,408,408,1,1);
/*!40000 ALTER TABLE `firstapp_q1q2rightwrong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_question`
--

DROP TABLE IF EXISTS `firstapp_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `question` varchar(600) NOT NULL,
  `option1` varchar(40) NOT NULL,
  `option2` varchar(40) NOT NULL,
  `option3` varchar(40) NOT NULL,
  `option4` varchar(40) NOT NULL,
  `answer` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `firstapp_question_6234103b` (`course_id`),
  CONSTRAINT `course_id_refs_id_cddb6a70` FOREIGN KEY (`course_id`) REFERENCES `firstapp_course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=409 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_question`
--

LOCK TABLES `firstapp_question` WRITE;
/*!40000 ALTER TABLE `firstapp_question` DISABLE KEYS */;
INSERT INTO `firstapp_question` VALUES (403,12,'C programs are converted \ninto machine language with the help of ','Editor','Compiler','OS','None of the above',2),(404,12,'A character variable can at a time store','1 character','8 characters','256 characters','None of the above',1),(405,12,'The maximum value that an integer constant can have is','-32767','32767','1.7014e+38','depends on the machine',4),(406,12,'Which of the following is not a keyword in C ?','for','char','print','case',3),(407,13,'What would be the output of the following program:  main( ) \n		{ \n			int a = 300, b = 0, c = 10 ; \n			if ( a >= 400 ) \n			b = 300 ; \n			c = 200 ; \n			printf ( \"\n%d %d\", b, c ) ; 		\n		}','0 10','10 0','0 200','200 300',3),(408,13,'What would be the output of the following program:\n main( ) \n			{ \n			int   x = 10, y = 20 ; \n			x == 20 && y != 10 ? printf( \"True\" ) : printf( \"False\" ) ; \n			} ','true','flase','compilation error','none of the above',2);
/*!40000 ALTER TABLE `firstapp_question` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER after_question_insert AFTER INSERT ON firstapp_question FOR EACH ROW BEGIN INSERT INTO firstapp_grade(questionID_id,studentID_id,value) SELECT NEW.id,firstapp_student.id,0 FROM firstapp_student; END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `firstapp_question_concept`
--

DROP TABLE IF EXISTS `firstapp_question_concept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_question_concept` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `concept_id` int(11) NOT NULL,
  `value` decimal(3,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `firstapp_question_concept_25110688` (`question_id`),
  KEY `firstapp_question_concept_8a386586` (`concept_id`),
  CONSTRAINT `concept_id_refs_id_7e1a5fdf` FOREIGN KEY (`concept_id`) REFERENCES `firstapp_course` (`id`),
  CONSTRAINT `question_id_refs_id_ad4bc767` FOREIGN KEY (`question_id`) REFERENCES `firstapp_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1381 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_question_concept`
--

LOCK TABLES `firstapp_question_concept` WRITE;
/*!40000 ALTER TABLE `firstapp_question_concept` DISABLE KEYS */;
INSERT INTO `firstapp_question_concept` VALUES (1351,403,11,0.00),(1352,403,12,0.50),(1353,403,13,0.00),(1354,403,14,0.50),(1355,403,15,0.00),(1356,404,11,0.50),(1357,404,12,0.00),(1358,404,13,0.50),(1359,404,14,0.00),(1360,404,15,0.50),(1361,405,11,0.00),(1362,405,12,0.50),(1363,405,13,0.00),(1364,405,14,0.50),(1365,405,15,0.00),(1366,406,11,0.50),(1367,406,12,0.00),(1368,406,13,0.50),(1369,406,14,0.00),(1370,406,15,0.50),(1371,407,11,0.00),(1372,407,12,0.50),(1373,407,13,0.00),(1374,407,14,0.50),(1375,407,15,0.00),(1376,408,11,0.50),(1377,408,12,0.00),(1378,408,13,0.50),(1379,408,14,0.00),(1380,408,15,0.50);
/*!40000 ALTER TABLE `firstapp_question_concept` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_question_concept_new`
--

DROP TABLE IF EXISTS `firstapp_question_concept_new`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_question_concept_new` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `concept_id` int(11) NOT NULL,
  `value` decimal(3,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `firstapp_question_concept_new_25110688` (`question_id`),
  KEY `firstapp_question_concept_new_8a386586` (`concept_id`),
  CONSTRAINT `concept_id_refs_id_bd9c5434` FOREIGN KEY (`concept_id`) REFERENCES `firstapp_course` (`id`),
  CONSTRAINT `question_id_refs_id_52c160e2` FOREIGN KEY (`question_id`) REFERENCES `firstapp_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1341 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_question_concept_new`
--

LOCK TABLES `firstapp_question_concept_new` WRITE;
/*!40000 ALTER TABLE `firstapp_question_concept_new` DISABLE KEYS */;
INSERT INTO `firstapp_question_concept_new` VALUES (1311,403,11,0.00),(1312,403,12,0.33),(1313,403,13,0.00),(1314,403,14,0.33),(1315,403,15,0.00),(1316,404,11,0.33),(1317,404,12,0.00),(1318,404,13,0.33),(1319,404,14,0.00),(1320,404,15,0.33),(1321,405,11,0.00),(1322,405,12,0.33),(1323,405,13,0.00),(1324,405,14,0.33),(1325,405,15,0.00),(1326,406,11,0.33),(1327,406,12,0.00),(1328,406,13,0.33),(1329,406,14,0.00),(1330,406,15,0.33),(1331,407,11,0.00),(1332,407,12,0.33),(1333,407,13,0.00),(1334,407,14,0.33),(1335,407,15,0.00),(1336,408,11,0.33),(1337,408,12,0.00),(1338,408,13,0.33),(1339,408,14,0.00),(1340,408,15,0.33);
/*!40000 ALTER TABLE `firstapp_question_concept_new` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_ratings`
--

DROP TABLE IF EXISTS `firstapp_ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_ratings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `firstapp_ratings_94741166` (`student_id`),
  KEY `firstapp_ratings_0a47aae8` (`item_id`),
  CONSTRAINT `item_id_refs_id_dd5c3946` FOREIGN KEY (`item_id`) REFERENCES `firstapp_course` (`id`),
  CONSTRAINT `student_id_refs_id_b5bdaaca` FOREIGN KEY (`student_id`) REFERENCES `firstapp_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_ratings`
--

LOCK TABLES `firstapp_ratings` WRITE;
/*!40000 ALTER TABLE `firstapp_ratings` DISABLE KEYS */;
INSERT INTO `firstapp_ratings` VALUES (51,12,11,0),(52,12,12,1),(53,12,13,1),(54,12,14,7),(55,12,15,9),(56,13,11,0),(57,13,12,1),(58,13,13,10),(59,13,14,0),(60,13,15,0);
/*!40000 ALTER TABLE `firstapp_ratings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_student`
--

DROP TABLE IF EXISTS `firstapp_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_preference` varchar(30) NOT NULL,
  `prev_course_id` int(11) NOT NULL,
  `rating_sum` int(11) NOT NULL,
  `rated_concepts` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `firstapp_student_6340c63c` (`user_id`),
  KEY `firstapp_student_184354bc` (`prev_course_id`),
  CONSTRAINT `prev_course_id_refs_id_f1b7f63e` FOREIGN KEY (`prev_course_id`) REFERENCES `firstapp_course` (`id`),
  CONSTRAINT `user_id_refs_id_6e7e9b09` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_student`
--

LOCK TABLES `firstapp_student` WRITE;
/*!40000 ALTER TABLE `firstapp_student` DISABLE KEYS */;
INSERT INTO `firstapp_student` VALUES (12,'student1',22,'pdf',12,18,5),(13,'student2',23,'pdf',13,11,5);
/*!40000 ALTER TABLE `firstapp_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firstapp_studentstate`
--

DROP TABLE IF EXISTS `firstapp_studentstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstapp_studentstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `KL` decimal(3,2) NOT NULL,
  `unknown` decimal(3,2) NOT NULL,
  `unsat_known` decimal(3,2) NOT NULL,
  `known` decimal(3,2) NOT NULL,
  `learned` decimal(3,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `firstapp_studentstate_94741166` (`student_id`),
  KEY `firstapp_studentstate_6234103b` (`course_id`),
  CONSTRAINT `course_id_refs_id_804c357c` FOREIGN KEY (`course_id`) REFERENCES `firstapp_course` (`id`),
  CONSTRAINT `student_id_refs_id_5a407441` FOREIGN KEY (`student_id`) REFERENCES `firstapp_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstapp_studentstate`
--

LOCK TABLES `firstapp_studentstate` WRITE;
/*!40000 ALTER TABLE `firstapp_studentstate` DISABLE KEYS */;
INSERT INTO `firstapp_studentstate` VALUES (56,12,11,1.00,0.00,0.00,0.00,1.00),(57,12,12,1.00,0.00,0.00,0.00,1.00),(58,12,13,1.00,0.00,0.00,0.00,1.00),(59,12,14,1.00,0.00,0.00,0.00,1.00),(60,12,15,0.64,0.00,1.00,0.00,0.00),(61,13,11,1.00,0.00,0.00,0.00,1.00),(62,13,12,1.00,0.00,0.00,0.00,1.00),(63,13,13,1.00,0.00,0.00,0.00,1.00),(64,13,14,0.31,1.00,0.00,0.00,0.00),(65,13,15,0.31,1.00,0.00,0.00,0.00);
/*!40000 ALTER TABLE `firstapp_studentstate` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-06-11 14:09:50
