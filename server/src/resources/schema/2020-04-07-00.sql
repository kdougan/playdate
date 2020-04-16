-- Create syntax for TABLE 'calendar'
CREATE TABLE `calendar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner_id` int(11) DEFAULT NULL,
  `private` tinyint(1) NOT NULL DEFAULT '0',
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_modified` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `calendar_fk0` (`owner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create syntax for TABLE 'event'
CREATE TABLE `event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `description` varchar(512) DEFAULT NULL,
  `calendar_id` int(11) DEFAULT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `duration` int(11) NOT NULL,
  `private` tinyint(1) NOT NULL DEFAULT '1',
  `asset` longblob,
  `meta` blob,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_modified` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `event_fk0` (`calendar_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create syntax for TABLE 'group'
CREATE TABLE `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  `open` tinyint(1) NOT NULL DEFAULT '0',
  `slot_count` int(11) NOT NULL DEFAULT '1',
  `meta` blob,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_modified` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `group_fk0` (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create syntax for TABLE 'person'
CREATE TABLE `person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `handle` varchar(16) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password` varchar(256) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `public` tinyint(1) NOT NULL DEFAULT '1',
  `role` varchar(12) NOT NULL DEFAULT 'user',
  `asset` longblob,
  `meta` blob,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `handle` (`handle`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Create syntax for TABLE 'person_event_queue'
CREATE TABLE `person_event_queue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `person_event_queue_uix0` (`person_id`,`event_id`),
  KEY `person_event_queue_fk0` (`person_id`),
  KEY `person_event_queue_fk1` (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create syntax for TABLE 'person_event_sub'
CREATE TABLE `person_event_sub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `meta` blob,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `person_event_sub_uix0` (`person_id`,`event_id`),
  KEY `person_event_sub_fk0` (`person_id`),
  KEY `person_event_sub_fk1` (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create syntax for TABLE 'person_group'
CREATE TABLE `person_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `person_group_uix0` (`person_id`,`group_id`),
  KEY `person_group_fk0` (`person_id`),
  KEY `person_group_fk1` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create syntax for TABLE 'person_calendar_sub'
CREATE TABLE `person_calendar_sub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `calendar_id` int(11) NOT NULL,
  `meta` blob,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `person_calendar_sub_uix0` (`person_id`,`calendar_id`),
  KEY `person_calendar_sub_fk0` (`person_id`),
  KEY `person_calendar_sub_fk1` (`calendar_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `calendar` ADD CONSTRAINT `calendar_fk0` FOREIGN KEY (`owner_id`) REFERENCES `person` (`id`);

ALTER TABLE `event` ADD CONSTRAINT `event_fk0` FOREIGN KEY (`calendar_id`) REFERENCES `calendar` (`id`);

ALTER TABLE `group` ADD CONSTRAINT `group_fk0` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`);

ALTER TABLE `person_event_queue` ADD CONSTRAINT `person_event_queue_fk0` FOREIGN KEY (`person_id`) REFERENCES `person` (`id`);

ALTER TABLE `person_event_queue` ADD CONSTRAINT `person_event_queue_fk1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`);

ALTER TABLE `person_event_sub` ADD CONSTRAINT `person_event_sub_fk0` FOREIGN KEY (`person_id`) REFERENCES `person` (`id`);

ALTER TABLE `person_event_sub` ADD CONSTRAINT `person_event_sub_fk1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`);

ALTER TABLE `person_group` ADD CONSTRAINT `person_group_fk0` FOREIGN KEY (`person_id`) REFERENCES `person` (`id`);

ALTER TABLE `person_group` ADD CONSTRAINT `person_group_fk1` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`);

ALTER TABLE `person_calendar_sub` ADD CONSTRAINT `person_calendar_sub_fk0` FOREIGN KEY (`person_id`) REFERENCES `person` (`id`);

ALTER TABLE `person_calendar_sub` ADD CONSTRAINT `person_calendar_sub_fk1` FOREIGN KEY (`calendar_id`) REFERENCES `calendar` (`id`);