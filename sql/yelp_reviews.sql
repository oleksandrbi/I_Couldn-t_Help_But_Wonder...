CREATE TABLE `Wonder`.`yelp_reviews` ( 
    `restaurant_id` VARCHAR(25) NOT NULL , 
    `restaurant_name` VARCHAR(50) NOT NULL ,
    `user_id` VARCHAR(25) NOT NULL , 
    `user_name` VARCHAR(25) NOT NULL , 
    `review_time` TIMESTAMP NOT NULL , 
    `review_text` LONGTEXT NOT NULL ,
    `review_url` LONGTEXT NULL DEFAULT NULL 
) 
ENGINE = InnoDB;
