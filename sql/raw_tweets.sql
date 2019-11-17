-- phpMyAdmin SQL Dump
-- version 4.4.15.10
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 17, 2019 at 04:42 AM
-- Server version: 5.5.60-MariaDB
-- PHP Version: 5.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Wonder`
--

-- --------------------------------------------------------

--
-- Table structure for table `raw_tweets`
--

CREATE TABLE IF NOT EXISTS `raw_tweets` (
  `tweet_id` bigint(20) NOT NULL,
  `tweet_text` text NOT NULL,
  `retweet_count` int(11) NOT NULL,
  `favorite_count` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  `quoted_tweet_id` bigint(20) DEFAULT NULL,
  `retweeted_tweet_id` bigint(20) DEFAULT NULL,
  `reply_to_tweet_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  `twitter_query` text NOT NULL,
  `restaurant_id` int(11) NOT NULL,
  `twitter_client` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `raw_tweets`
--
ALTER TABLE `raw_tweets`
  ADD PRIMARY KEY (`tweet_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
