-- phpMyAdmin SQL Dump
-- version 4.4.15.10
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 26, 2019 at 05:40 AM
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
-- Table structure for table `yelp_reviews`
--

CREATE TABLE IF NOT EXISTS `yelp_reviews` (
  `review_id` varchar(25) NOT NULL,
  `restaurant_id` varchar(25) NOT NULL,
  `user_id` varchar(25) NOT NULL,
  `rating` varchar(5) NOT NULL,
  `review_text` longtext NOT NULL,
  `timestamp` datetime NOT NULL,
  `useful` int(11) NOT NULL,
  `funny` int(11) NOT NULL,
  `cool` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `yelp_reviews`
--
ALTER TABLE `yelp_reviews`
  ADD PRIMARY KEY (`review_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

