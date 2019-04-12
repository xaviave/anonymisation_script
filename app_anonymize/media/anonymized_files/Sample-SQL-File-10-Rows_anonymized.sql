--
-- Database: `samplevideo_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE IF NOT EXISTS `user_details` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `status` tinyint(10) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10001 ;

--
-- Dumping data for table `user_details`
--

INSERT INTO `user_details` (`user_id`, `username`, `first_name`, `last_name`, `gender`, `password`, `status`) VALUES
(1, 'Mathilde257', 'Clémence', 'Jacquot', 'Female', 'm3778pwzGRqAnebA7i6XHZEw8GNw5S77r779RZ4LD0oBu8iVvb', 7519315371),
(2, 'Marcel903', 'Arthur', 'Bernier', 'Male', 'kXwIXPTqvIEOTZVBIIQ8vAcstHj6KlRZDGTrONQiN4OYHomYTM', 981889895),
(3, 'Philippe79', 'Raymond', 'Chevallier', 'Male', 'zZrqdquEkBOD2m6aqeW0t0cycJM5Dg1mouGJEkD44BNh1jq14V', 2680799172),
(4, 'William312', 'Henri', 'Leger', 'Male', '88adTIieGCtxN6RgkhWHfFvSboGS5AU3NqCh5JzU5lYuTBDSRd', 6272337326),
(5, 'Joséphine647', 'Renée', 'Cousin', 'Female', 'yCnoXxWJexb0s0X4mqZvzZd6OwOil00sBm7PASPLM4wACSjhqt', 3883721240),
(6, 'Monique433', 'Célina', 'Lemaitre', 'Female', 'IVNmuxasCvn3Xxn1TYD8ZN4w5LVD2VxGZ7Iu2G4JbALt1lJuv4', 8222058394),
(7, 'Nathalie942', 'Madeleine', 'Torres', 'Female', '5D8FbavFZe3I6YMvcmdz5WiGxA0dktJCL2OZWdHxiDOGhrvzGT', 5902665646),
(8, 'Thibaut967', 'Isaac', 'Hamel', 'Male', 'KwRCGGA29JlSLfF1GJcflcx3WgIUDvVayHb9byYagla1JKMdmg', 8339312257),
(9, 'Louise662', 'Aurore', 'Lemoine', 'Female', 'perhQBfppPpM9w5VaRSzOZJrmJat4YqNSu7v7YSJMt7007oh2Q', 2314745345),
(10, 'Aurore800', 'Audrey', 'Roger', 'Female', 'S8JL3CNvN8iUPR5yqOhJfVeotTLQOlS8GbwH0LdnRFpLOYTNQ5', 1560693145);
