--
-- Database: `samplevideo_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE IF NOT EXISTS `user_details` (
  `user_id` int(11) NOT NULL KEY AUTO_INCREMENT,
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
(0          , 'Jacques220', 'Vincent', 'Bruneau', 'Male', '41f6rCu5WC4dTf737L2sxXlcP3oO6PHHF0Lmkafcw6ToHleGPT', 837812421),
(1          , 'Marianne578', 'Hortense', 'Humbert', 'Male', 'CpqaWPaRpaMb9dd7zjqshDTwLCeIWzsN6WVrby7tg8eNrugXT5', 5832499378),
(2          , 'Frédéric463', 'Thibaut', 'Charles', 'Male', 'vclK9B0eZq0ttdOju7c7AcTN4KJhbrBfkZDIeYPlKl4JCUNKk5', 9842023677),
(3          , 'Tristan581', 'Arnaude', 'Fleury', 'Male', 'MAponJ81K4unyb1oPqbvHkXqjzkoAdW2k1XwBD5kBPANhEB9q2', 8835549200),
(4          , 'Colette558', 'Isaac', 'Renault', 'Female', 'lSrSUXMEVd9WaqFKsCfaMRfR2AZ1uKDEOrVdBWxXi9JhWLDrck', 5226189717),
(5          , 'Isabelle730', 'Josette', 'Alves', 'Female', 'OecHcp0GCxfEHxCFKirPxNYoLT5oPwvbumPDDX0dcYbWhHTcWu', 3406748613),
(6          , 'Constance731', 'Lorraine', 'Leleu', 'Male', 'DgqSKLLJ5SsB3Gzig1C3gF4nkusMhlcDR2Vr9ty8SgBnKQ6q4Z', 9097397128),
(7          , 'Adrien126', 'Alphonse', 'Lemoine', 'Female', 'dDsmwwaJLRTWGZA8guhr7YzMS4WahBUKGZALthhpDyT8HY4nB7', 8757726375),
(8          , 'Adrien745', 'Alexandre', 'Prevost', 'Male', 'AhCWXBFsnwYZWZ9aqknnySjHcfqkfNlWJbErkfSxxx2xlwrGjq', 7971755672),
(9          , 'Michel465', 'Marianne', 'Lacombe', 'Female', '3ubRTKVoGDL5f9WQgN7lzRAAfF98lsBVrD7bmgNNMkzUZPntGD', 4709614424);
