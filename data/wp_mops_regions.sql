-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: pod-216963.pod-216963.svc.cluster.local:3306:13306
-- Generation Time: Aug 21, 2025 at 03:36 AM
-- Server version: 8.0.41-32
-- PHP Version: 8.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wp_mopsedu`
--

-- --------------------------------------------------------

--
-- Table structure for table `wp_mops_regions`
--

CREATE TABLE `wp_mops_regions` (
  `id` mediumint NOT NULL,
  `title` varchar(191) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

--
-- Dumping data for table `wp_mops_regions`
--

INSERT INTO `wp_mops_regions` (`id`, `title`, `created_at`) VALUES
(1, 'ACT', '2020-01-21 05:03:34'),
(2, 'Albury Wagga', '2020-01-21 05:03:34'),
(3, 'Ballarat', '2020-01-21 05:03:34'),
(4, 'Bendigo', '2020-01-21 05:03:34'),
(5, 'NSW Central West South', '2020-01-21 05:03:34'),
(6, 'NSW Central Coast', '2020-01-21 05:03:34'),
(7, 'Central Vic', '2020-01-21 05:03:34'),
(8, 'FNQ', '2020-01-21 05:03:34'),
(9, 'Geelong', '2020-01-21 05:03:34'),
(10, 'Gippsland', '2020-01-21 05:03:34'),
(11, 'Gold Coast', '2020-01-21 05:03:34'),
(12, 'Mackay and Townsville', '2020-01-21 05:03:34'),
(13, 'Melbourne', '2020-01-21 05:03:34'),
(14, 'Mildura', '2020-01-21 05:03:34'),
(15, 'NSW Mid North Coast', '2020-01-21 05:03:34'),
(16, 'Brisbane', '2020-01-21 05:03:34'),
(17, 'Northern Territory', '2020-01-21 05:03:34'),
(18, 'NSW Central West North', '2020-01-21 05:03:34'),
(19, 'Sunshine Coast', '2020-01-21 05:03:34'),
(20, 'Sydney', '2020-01-21 05:03:34'),
(21, 'Toowoomba', '2020-01-21 05:03:34'),
(22, 'Western Australia', '2020-01-21 05:03:34'),
(23, 'Zone 3', '2020-01-21 05:03:34'),
(39, 'NSW South Coast', '2020-01-21 05:03:34'),
(40, 'South Australia', '2020-08-26 03:47:07'),
(41, 'Suppliers', '2021-04-07 01:30:37'),
(42, 'Adelaide', '2021-07-01 23:06:01'),
(43, 'Uni Leads', '2021-07-07 05:27:28'),
(44, 'South Adelaide', '2021-07-23 02:03:24'),
(45, 'North Adelaide', '2021-07-23 02:03:34'),
(46, 'NSW Far North Coast', '2020-01-21 05:03:34');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `wp_mops_regions`
--
ALTER TABLE `wp_mops_regions`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `wp_mops_regions`
--
ALTER TABLE `wp_mops_regions`
  MODIFY `id` mediumint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
