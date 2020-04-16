CREATE INDEX `event_idx0` ON event(`start_time`, `end_time`);

ALTER TABLE `calendar` ADD COLUMN `meta` blob;