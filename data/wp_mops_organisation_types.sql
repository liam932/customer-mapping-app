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
-- Table structure for table `wp_mops_organisation_types`
--

CREATE TABLE `wp_mops_organisation_types` (
  `id` mediumint NOT NULL,
  `title` varchar(191) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

--
-- Dumping data for table `wp_mops_organisation_types`
--

INSERT INTO `wp_mops_organisation_types` (`id`, `title`, `created_at`) VALUES
(1, 'School - Catholic', '2020-01-21 05:03:43'),
(2, 'University', '2020-01-21 05:03:43'),
(3, 'Industry', '2020-01-21 05:03:43'),
(4, 'School - Government', '2020-01-21 05:03:43'),
(5, 'School - Private', '2020-01-21 05:03:43'),
(6, 'Supplier', '2021-04-07 01:29:51');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `wp_mops_organisation_types`
--
ALTER TABLE `wp_mops_organisation_types`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `wp_mops_organisation_types`
--
ALTER TABLE `wp_mops_organisation_types`
  MODIFY `id` mediumint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
