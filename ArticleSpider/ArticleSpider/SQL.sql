CREATE TABLE IF NOT EXISTS `ArticleInfo`(
   `title` VARCHAR(100) NOT NULL,
   `date` DATE,
   `url` VARCHAR(300) NOT NULL,
   `url_object_id` VARCHAR(50) NOT NULL,
   `front_image_url` VARCHAR(300),
   `front_image_path` VARCHAR(200),
   `praise_num` INT UNSIGNED,
   `fav_num` INT UNSIGNED,
   `comment_num` INT UNSIGNED,
   `tag` VARCHAR(200),
   PRIMARY KEY ( `url_object_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
