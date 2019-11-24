CREATE TABLE `Wonder`.`restaurant_data` ( 
    `restaurant_id` VARCHAR(25) NOT NULL ,
    `restaurant_name` VARCHAR(50) NOT NULL ,
    `restaurant_address` TEXT NOT NULL ,
    `latitude` TEXT NULL DEFAULT NULL , 
    `longitude` TEXT NULL DEFAULT NULL , 
    `yelp_rating` INT(1) NOT NULL 
) 
    ENGINE = InnoDB;
