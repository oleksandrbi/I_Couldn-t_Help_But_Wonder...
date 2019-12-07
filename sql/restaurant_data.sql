CREATE TABLE `restaurant_data` (
  `restaurant_id` varchar(25) NOT NULL,
  `restaurant_name` text NOT NULL,
  `address` text NOT NULL,
  `city` text NOT NULL,
  `state` text NOT NULL,
  `postal_code` int(11) NOT NULL,
  `latitude` text,
  `longitude` text,
  `avg_yelp_rating` varchar(5) NOT NULL,
  `review_count` int(11) NOT NULL,
  `attributes` text,
  `categories` text NOT NULL,
  `hours` text,
  `queries_set` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`restaurant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SELECT * FROM Wonder.restaurant_data;