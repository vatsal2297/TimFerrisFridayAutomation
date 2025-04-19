--===========================================--
--== Main TFF Friday Email SCHEMA SQL ==--

create database nlarchive;
use nlarchive;

CREATE TABLE `tff_5bullet_emails` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email_message_id` varchar(255) NOT NULL,
  `email_date` datetime NOT NULL,
  `email_title` varchar(255) NOT NULL,
  PRIMARY KEY (`id`,`email_message_id`),
  UNIQUE KEY `email_message_id` (`email_message_id`)
) 

CREATE TABLE `tff_bullets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tff_email_id` int NOT NULL,
  `bullet_heading` varchar(255) NOT NULL,
  `bullet_content` mediumtext NOT NULL,
  `searchable_bullet_content` mediumtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tff_email_id` (`tff_email_id`),
  FULLTEXT KEY `search_bullet_content_indx` (`searchable_bullet_content`),
  CONSTRAINT `tff_bullets_ibfk_1` FOREIGN KEY (`tff_email_id`) REFERENCES `tff_5bullet_emails` (`id`)
)


--===========================================--
--== INFORMATION_SCHEMA SQL ==--

SELECT VERSION();

USE INFORMATION_SCHEMA;

SHOW Tables;

SELECT *
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = "nlarchive" AND TABLE_NAME = "tff_bullets";

SELECT *
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'nlarchive';

SELECT * FROM INFORMATION_SCHEMA.COLUMNS;

SELECT table_schema, SUM((data_length+index_length)/1024/1024) AS "Size occupied in MB", SUM(data_free)/1024/1024 AS "free space in MB" 
FROM information_schema.tables GROUP BY table_schema;

SELECT table_schema AS "Database",
       ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)"
FROM information_schema.tables
GROUP BY table_schema;

SELECT table_schema AS "Database",
       table_name AS "Table",
       ROUND((data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)"
FROM information_schema.tables
WHERE table_schema = 'nlarchive';


--===========================================--
--== Main TFF Friday Email SELECT SQL ==--

SHOW INDEXES FROM tff_bullets;

--Check the Number of bullets for each email inserted
SELECT e.id, e.email_date, e.email_title, COUNT(b.tff_email_id) AS 'Number of Bullets'
FROM nlarchive.tff_5bullet_emails e JOIN nlarchive.tff_bullets b
ON e.id = b.tff_email_id
GROUP BY e.id, es.email_date, e.email_title
ORDER BY e.id;

--Check last inserted Friday Email
SELECT email_message_id, email_date, email_title
FROM nlarchive.tff_5bullet_emails 
WHERE email_date = (
	SELECT MAX(email_date) 
    FROM nlarchive.tff_5bullet_emails
);

--Check the latest time the email has arrived regardless of date
SELECT * FROM nlarchive.tff_5bullet_emails
ORDER BY CONVERT(email_date, TIME) DESC;


--===========================================--
--== Main TFF Friday Email UPDATE SQL ==--

ALTER TABLE nlarchive.tff_5bullet_emails AUTO_INCREMENT = 1;
ALTER TABLE nlarchive.tff_bullets AUTO_INCREMENT = 1;


--===========================================--
--== Main TFF Friday Email DELETE SQL ==--

TRUNCATE TABLE nlarchive.tff_bullets;
TRUNCATE TABLE nlarchive.tff_5bullet_emails;

DELETE FROM nlarchive.tff_bullets;
DELETE FROM nlarchive.tff_5bullet_emails;

--Resetting Tables for old emails (deleting old format emails and resetting auto_increment)
DELETE FROM nlarchive.tff_bullets WHERE tff_email_id > 143;
DELETE FROM nlarchive.tff_5bullet_emails WHERE id > 143;

ALTER TABLE nlarchive.tff_bullets AUTO_INCREMENT = 144;
ALTER TABLE nlarchive.tff_5bullet_emails AUTO_INCREMENT = 144;