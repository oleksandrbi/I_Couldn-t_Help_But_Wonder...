-- phpMyAdmin SQL Dump
-- version 4.4.15.10
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 17, 2019 at 04:40 AM
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
-- Table structure for table `tweet_entities`
--

CREATE TABLE IF NOT EXISTS `tweet_entities` (
  `entity_id` int(11) NOT NULL,
  `tweet_id` bigint(20) NOT NULL,
  `entity_type` set('HASHTAG','URL','USER_MENTION','') NOT NULL,
  `start_index` int(11) NOT NULL,
  `stop_index` int(11) NOT NULL,
  `text` text,
  `url` text,
  `display_url` text,
  `expanded_url` text,
  `user_id` bigint(20) DEFAULT NULL,
  `username` text,
  `full_name` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tweet_entities`
--
ALTER TABLE `tweet_entities`
  ADD PRIMARY KEY (`entity_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tweet_entities`
--
ALTER TABLE `tweet_entities`
  MODIFY `entity_id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
