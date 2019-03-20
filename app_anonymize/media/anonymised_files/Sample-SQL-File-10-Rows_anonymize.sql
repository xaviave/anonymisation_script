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
(1          , 'Capucine741', 'Alexandria', 'Rey', 'Female', 'mllDma996W1Kdx6ChBLmXySMG5heQCsoOLyIOllP2j47S6bf6b', 8483204620),
(2          , 'Émile407', 'André', 'Jacquet', 'Male', 'ZSJRu67k7W7Wc7RRyRkGNLzcR3z9lezXK0b7eLdPwibPonZvb5', 4930851980),
(3          , 'Véronique869', 'Simone', 'Poulain', 'Female', 'rfOrIhmJ90meCwzxBQ8lAQf5h1sEmUBP0YnO0LRcIOjR1axZGB', 4738771979),
(4          , 'Frédéric575', 'Louis', 'Dos Santos', 'Male', 'ChNARdxxsThHmLFhOJUDbABo0G2kqMZwhXWn8jtWwKJ7Ax614Y', 8478845497),
(5          , 'Isaac891', 'Michel', 'Nicolas', 'Male', 'AK8nCx1OjQEkr6tI7jPQYI9HC3wPCeuO8aPRpXnjFdwJ9j90kf', 5302943401),
(6          , 'William515', 'Augustin', 'Merle', 'Male', 'igRl8q5TqYgBUymvJRYP8MiRGqWb6XyCT2PALHRInlGyJ0URmw', 8450019091),
(7          , 'Jacqueline449', 'Margaux', 'Charpentier', 'Female', 'IN0G0CHgVtlA1hcd0a1iTjTsY1msPQIcYjfij3dAwKpzSPzeug', 710457089),
(8          , 'Rémy438', 'Honoré', 'Neveu', 'Male', 'p4NCGXCM07SmqrAwyqt0Sxzi8xopTVq1nhge8CaH5N0qBByHZN', 7186689293),
(9          , 'Édouard748', 'Denis', 'Duhamel', 'Male', 'IEcqC10DH1WWkKCSaVD6qteEGvUH4kNaCXzHUVVWvZTbrggup3', 926036517),
(10         , 'Guy793', 'Thibault', 'Grenier', 'Male', 'WYgzc7t3u7TAVAMDb20w301AlLqIe4SUC1PnNe0ATQ5xDEWlYo', 5378191460);
