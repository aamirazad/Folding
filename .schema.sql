CREATE TABLE `user` (
	`id` int NOT NULL AUTO_INCREMENT,
	`date` timestamp NOT NULL DEFAULT current_timestamp(),
	`score` bigint NOT NULL,
	`user_id` int NOT NULL,
    `day` BIT,
	PRIMARY KEY (`id`)
);