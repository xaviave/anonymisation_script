-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 08, 2014 at 06:53 AM
-- Server version: 5.1.36
-- PHP Version: 5.3.0

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `sample`
--

-- --------------------------------------------------------

--
-- Table structure for table `agents`
--

CREATE TABLE IF NOT EXISTS `agents` (
  `AGENT_CODE` varchar(6) NOT NULL DEFAULT '',
  `AGENT_NAME` varchar(40) DEFAULT NULL,
  `WORKING_AREA` varchar(35) DEFAULT NULL,
  `COMMISSION` decimal(10,2) DEFAULT NULL,
  `PHONE_NO` varchar(15) DEFAULT NULL,
  `COUNTRY` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`AGENT_CODE`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `agents`
--

INSERT INTO `agents` (`AGENT_CODE`, `AGENT_NAME`, `WORKING_AREA`, `COMMISSION`, `PHONE_NO`, `COUNTRY`) VALUES
('Moi.  ', 'avec', 'Jordanie', 5939397370.26, '+33 1 90 78 34 ', 'Svalbard et Jan Mayen (Îl'),
('Ordre.', 'fidèle', 'Brunei', 1677689027.40, '+33 5 13 72 76 ', 'Guinée-Bissau'),
('Côte. ', 'souvenir', 'Palau', 3109129455.55, '02 24 47 86 88', 'Turkménistan'),
('Peu.  ', 'rapporter', 'São Tomé et Príncipe (Rép.)', 6377338952.84, '+33 (0)6 85 45 ', 'Bahamas'),
('Durer.', 'égal', 'Costa Rica', 5371571659.30, '05 91 27 03 10', 'Inde'),
('Bord. ', 'parler', 'Paraguay', 9834272791.33, '0304749685', 'Zimbabwe'),
('Idée. ', 'malheur', 'Ouganda', 4518056618.91, '+33 (0)1 18 74 ', 'Kiribati'),
('Dans. ', 'tache', 'Turkménistan', 9974753640.10, '06 56 24 59 64', 'Hong Kong'),
('Avoir.', 'pauvre', 'Lettonie', 3970821339.5, '+33 (0)5 18 92 ', 'Finlande'),
('Mais. ', 'disparaître', 'Guatemala', 4449108029.20, '+33 (0)8 76 14 ', 'Tchad'),
('Eau.  ', 'dangereux', 'Guatemala', 3490898855.70, '01 20 34 93 28', 'Inde'),
('Haut. ', 'surprendre', 'Sierra Leone', 2807228575.43, '+33 (0)6 41 56 ', 'Liban');

-- --------------------------------------------------------

--
-- Table structure for table `company`
--

CREATE TABLE IF NOT EXISTS `company` (
  `COMPANY_ID` varchar(6) NOT NULL DEFAULT '',
  `COMPANY_NAME` varchar(25) DEFAULT NULL,
  `COMPANY_CITY` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`COMPANY_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `company`
--

INSERT INTO `company` (`COMPANY_ID`, `COMPANY_NAME`, `COMPANY_CITY`) VALUES
(962200, 'sein', 'Ollivier-sur-Courtois'),
(667563, 'plusieurs', 'Sainte Stéphanie'),
(586656, 'subir', 'Leconte'),
(930396, 'politique', 'Renard'),
(508171, 'sûr', 'Pascal');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE IF NOT EXISTS `customer` (
  `CUST_CODE` varchar(6) NOT NULL,
  `CUST_NAME` varchar(40) NOT NULL,
  `CUST_CITY` varchar(35) DEFAULT NULL,
  `WORKING_AREA` varchar(35) NOT NULL,
  `CUST_COUNTRY` varchar(20) NOT NULL,
  `GRADE` decimal(10,0) DEFAULT NULL,
  `OPENING_AMT` decimal(12,2) NOT NULL,
  `RECEIVE_AMT` decimal(12,2) NOT NULL,
  `PAYMENT_AMT` decimal(12,2) NOT NULL,
  `OUTSTANDING_AMT` decimal(12,2) NOT NULL,
  `PHONE_NO` varchar(17) NOT NULL,
  `AGENT_CODE` varchar(6) DEFAULT NULL,
  KEY `CUSTCITY` (`CUST_CITY`),
  KEY `CUSTCITY_COUNTRY` (`CUST_CITY`,`CUST_COUNTRY`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`CUST_CODE`, `CUST_NAME`, `CUST_CITY`, `WORKING_AREA`, `CUST_COUNTRY`, `GRADE`, `OPENING_AMT`, `RECEIVE_AMT`, `PAYMENT_AMT`, `OUTSTANDING_AMT`, `PHONE_NO`, `AGENT_CODE`) VALUES
('Obéir.', 'environ                                 ', 'Jean', 'Bosnie-Herzégovine                 ', 'Gambie              ', 1249380463, 994713111654.51, 963404799152.14, 74831999833.81, 285185094246.21, '+33 (0)1 31 79 57', 'Passé.'),
('Côte. ', 'roman                                   ', 'Dupont', 'Costa Rica                         ', 'Maurice             ', 1068175584, 748842150123.75, 600465460631.9, 351679588883.59, 453770303242.59, '+33 (0)2 33 82 63', 'Lors.'),
('Seuil.', 'cinq                                    ', 'Jourdandan', 'Finlande                           ', 'Canada              ', 1181600126, 707080810592.24, 82481401310.18, 896495640231.62, 896495640231.62, '04 06 17 24 90   ', 'Fusil.'),
('Voir. ', 'je                                      ', 'Samson', 'Tanzanie                           ', 'Lettonie            ', 8926381639, 841567478993.49, 942398341555.59, 534588008604.29, 242331437276.3, '+33 3 60 95 65 04', 'Chose.'),
('Peur. ', 'beaucoup                                ', 'Samson', 'Kiribati                           ', 'Soudan              ', 5322230844, 822265087547.21, 778316986045.91, 173910850993.54, 513469515763.59, '+33 (0)3 12 56 33', 'Ton.'),
('Forme.', 'faible                                  ', 'Le Gall', 'Turks et Caïques (Îles)            ', 'Turquie             ', 6748855490, 542408628683.18, 872988892766.79, 607092666468.97, 697233647749.9, '+33 4 02 98 03 23', 'Épais.'),
('Mien. ', 'habiter                                 ', 'Hardy', 'Mariannes du Nord (Îles)           ', 'Lithuanie           ', 8637372362, 376063231827.92, 266075233401.34, 670635687117.85, 587422341832.19, '0684604028       ', 'Sorte.'),
('Tu.   ', 'anglais                                 ', 'Sainte Stéphanie', 'Bermudes (Les)                     ', 'Rép. Dém. du Congo  ', 7211960881, 159896632312.51, 159896632312.51, 984337380242.53, 868482482657.20, '04 13 12 26 99   ', 'Enfin.'),
('Désir.', 'secret                                  ', 'Mace', 'Fidji (République des)             ', 'Svalbard et Jan Maye', 8904349249, 710604450482.5, 710604450482.5, 710604450482.5, 710604450482.5, '0465507955       ', 'Trace.'),
('Carte.', 'ailleurs                                ', 'Sainte Élisabeth', 'Jamaïque                           ', 'Territoire britanniq', 5418059507, 750094026631.92, 712035221107.12, 712035221107.12, 750094026631.92, '05 94 78 33 14   ', 'Poche.'),
('Bas.  ', 'séparer                                 ', 'Torres', 'Indonésie                          ', 'Bhoutan             ', 6434682114, 391877823025.89, 300402289943.27, 391877823025.89, 300402289943.27, '+33 3 65 93 32 97', 'Âme.'),
('Plus. ', 'pierre                                  ', 'Pascal', 'Russie                             ', 'Gibraltar           ', 3784921006, 631231217338.93, 472042970387.22, 372536688822.10, 372536688822.10, '+33 (0)8 17 05 69', 'Ton.'),
('Cinq. ', 'français                                ', 'Pinto', 'Porto Rico                         ', 'Équateur            ', 2598330810, 513914702570.51, 343178959008.35, 397277038150.50, 397277038150.50, '+33 6 45 99 16 78', 'Sans.'),
('Peur. ', 'bout                                    ', 'Schmitt-les-Bains', 'Martinique                         ', 'Mozambique          ', 7759001543, 191427685837.18, 847522832663.29, 486083046879.92, 177504549280.96, '04 54 07 77 10   ', 'Aucun.'),
('Nez.  ', 'autour                                  ', 'Gimenezdan', 'Libéria                            ', 'Portugal            ', 398446198, 509254204993.31, 854531267395.81, 172851532062.81, 229728155837.47, '+33 8 92 67 38 10', 'Yeux.'),
('Train.', 'désir                                   ', 'Morel-les-Bains', 'Équateur                           ', 'Somalie             ', 4226834932, 109276419263.2, 607043730846.6, 290456297626.72, 518166237978.16, '0228532761       ', 'Peine.'),
('Haute.', 'plaisir                                 ', 'Hubert', 'Mali                               ', 'Nauru               ', 9076450881, 277284041999.1, 137402263391.78, 291507837189.99, 291507837189.99, '+33 5 63 90 60 27', 'Venir.'),
('Oh.   ', 'état                                    ', 'MathieuVille', 'Macédoine                          ', 'Côte d'Ivoire       ', 8585785074, 538731662981.95, 344917732866.18, 201940103236.93, 550011223137.88, '03 00 73 69 99   ', 'Abri.'),
('Fixer.', 'poète                                   ', 'Saint Tristannec', 'Soudan                             ', 'Tanzanie            ', 2823144675, 481639194256.89, 917808374367.30, 893526822215.37, 741805238444.96, '0646078414       ', 'Éclat.'),
('Fois. ', 'présent                                 ', 'Barbe', 'Svalbard et Jan Mayen (Îles)       ', 'Singapour           ', 3568091031, 961068447328.28, 961068447328.28, 587789331169.32, 681091997720.88, '02 38 43 65 86   ', 'Vingt.'),
('Eau.  ', 'curieux                                 ', 'Rogerdan', 'Émirats arabes unis                ', 'Samoa               ', 2827012635, 185108180974.15, 783142802849.37, 783142802849.37, 185108180974.15, '+33 (0)5 53 47 44', 'Te.'),
('Juge. ', 'sens                                    ', 'Maillardnec', 'Tadjikistan                        ', 'Gibraltar           ', 5383121721, 12758765407.97, 530028814475.50, 121020270450.99, 258348266502.84, '0819487548       ', 'Fait.'),
('Frère.', 'agir                                    ', 'Hebert', 'Grèce                              ', 'Papouasie-Nouvelle-G', 517831226, 755585114131.88, 922678263018.58, 530919825279.99, 960928828114.84, '01 39 92 97 78   ', 'Mine.'),
('Doute.', 'fait                                    ', 'Davidnec', 'Corée du Nord                      ', 'Ghana               ', 662386048, 791676067187.79, 774619131884.93, 191857531972.96, 988553870746.48, '08 87 16 46 05   ', 'Vin.'),
('Lui.  ', 'oublier                                 ', 'Saint Virginie', 'Corée du Nord                      ', 'Haïti               ', 600096933, 554088158129.68, 807538565786.57, 554088158129.68, 807538565786.57, '+33 6 10 32 38 47', 'Petit.');

-- --------------------------------------------------------

--
-- Table structure for table `daysorder`
--

CREATE TABLE IF NOT EXISTS `daysorder` (
  `ORD_NUM` decimal(6,0) NOT NULL,
  `ORD_AMOUNT` decimal(12,2) NOT NULL,
  `ADVANCE_AMOUNT` decimal(12,2) NOT NULL,
  `ORD_DATE` date NOT NULL,
  `CUST_CODE` varchar(6) NOT NULL,
  `AGENT_CODE` varchar(6) NOT NULL,
  `ORD_DESCRIPTION` varchar(60) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `daysorder`
--

INSERT INTO `daysorder` (`ORD_NUM`, `ORD_AMOUNT`, `ADVANCE_AMOUNT`, `ORD_DATE`, `CUST_CODE`, `AGENT_CODE`, `ORD_DESCRIPTION`) VALUES
(950158, 383383055953.59, 392573971922.58, '2010-08-18', 'Bon.  ', 'Vous. ', 'Beau permettre élever cou instant profiter.                 '),
(748259, 314427599284.99, 98271741811.18, '1975-03-25', 'Rose. ', 'Près. ', 'Geste ci souvent enfoncer moins palais chambre visible.     '),
(409062, 620569370867.34, 255444089761.52, '1997-06-11', 'Eaux. ', 'Avant.', 'Expliquer remercier ton non calme sourire.                  '),
(570748, 713100802441.24, 134206875346.34, '1997-07-30', 'Joie. ', 'Voler.', 'Oublier approcher peu père comment.                         '),
(8837  , 245920961465.13, 644088918939.42, '1972-03-19', 'Déjà. ', 'Mort. ', 'Papier connaissance homme endormir serrer.                  '),
(34583 , 126705438870.4, 54750093917.4, '2017-08-11', 'Mari. ', 'Leur. ', 'Sortir prière courant.                                      '),
(433846, 425511399142.41, 513353578802.58, '1974-11-10', 'Larme.', 'Forêt.', 'Certain droite moment contre groupe conduire eaux danger.   ');

-- --------------------------------------------------------

--
-- Table structure for table `despatch`
--

CREATE TABLE IF NOT EXISTS `despatch` (
  `DES_NUM` varchar(6) NOT NULL DEFAULT '',
  `DES_DATE` date DEFAULT NULL,
  `DES_AMOUNT` decimal(12,2) DEFAULT NULL,
  `ORD_NUM` decimal(6,0) DEFAULT NULL,
  `ORD_DATE` date DEFAULT NULL,
  `ORD_AMOUNT` decimal(12,2) DEFAULT NULL,
  `AGENT_CODE` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`DES_NUM`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `despatch`
--


-- --------------------------------------------------------

--
-- Table structure for table `foods`
--

CREATE TABLE IF NOT EXISTS `foods` (
  `ITEM_ID` varchar(6) NOT NULL DEFAULT '',
  `ITEM_NAME` varchar(25) DEFAULT NULL,
  `ITEM_UNIT` varchar(5) DEFAULT NULL,
  `COMPANY_ID` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`ITEM_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `foods`
--

INSERT INTO `foods` (`ITEM_ID`, `ITEM_NAME`, `ITEM_UNIT`, `COMPANY_ID`) VALUES
(809479, 'puis', 'ramen', 299582),
(103376, 'cercle', 'le', 410213),
(485586, 'habitant', 'cesse', 323312),
(71793 , 'ligne', 'publi', 412762),
(330949, 'partager', 'événe', 855748),
(378385, 'ruine', 'froid', 918947),
(161410, 'abandonner', 'cherc', 258668);

-- --------------------------------------------------------

--
-- Table structure for table `listofitem`
--

CREATE TABLE IF NOT EXISTS `listofitem` (
  `ITEMCODE` varchar(6) NOT NULL,
  `ITEMNAME` varchar(25) NOT NULL,
  `BATCHCODE` varchar(35) NOT NULL,
  `CONAME` varchar(35) DEFAULT NULL,
  UNIQUE KEY `ITEMCODE` (`ITEMCODE`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `listofitem`
--

INSERT INTO `listofitem` (`ITEMCODE`, `ITEMNAME`, `BATCHCODE`, `CONAME`) VALUES
('Rire. ', 'port                     ', 'Personnage entrée maladie.         ', 'établir'),
('Mort. ', 'encore                   ', 'Paysan de éviter.                  ', 'avant'),
('Jambe.', 'être                     ', 'Corde abri vivre dieu.             ', 'courir');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE IF NOT EXISTS `orders` (
  `ORD_NUM` decimal(6,0) NOT NULL,
  `ORD_AMOUNT` decimal(12,2) NOT NULL,
  `ADVANCE_AMOUNT` decimal(12,2) NOT NULL,
  `ORD_DATE` date NOT NULL,
  `CUST_CODE` varchar(6) NOT NULL,
  `AGENT_CODE` varchar(6) NOT NULL,
  `ORD_DESCRIPTION` varchar(60) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`ORD_NUM`, `ORD_AMOUNT`, `ADVANCE_AMOUNT`, `ORD_DATE`, `CUST_CODE`, `AGENT_CODE`, `ORD_DESCRIPTION`) VALUES
(904112, 62626443930.67, 354474778177.89, '1999-01-06', 'Page. ', 'Cri.  ', 'Voici lit leur même humain répéter si.                      '),
(482405, 765694845505.76, 888962149611.28, '2016-06-29', 'Comme.', 'L'un. ', 'Sec tapis garde poids importer parler armer gloire.         '),
(333105, 941759945117.77, 658156466437.57, '2001-05-05', 'Tard. ', 'Joie. ', 'Baisser devenir vous groupe étudier vue.                    '),
(392235, 637241047642.21, 163840698457.76, '2008-05-17', 'Vingt.', 'Rêver.', 'Afin De siècle loup eau.                                    '),
(395633, 309113320068.87, 691108604495.37, '1985-02-25', 'Scène.', 'Sept. ', 'Peur servir autant personnage bataille eaux.                '),
(242500, 627484112055.90, 863212804334.73, '1978-01-01', 'Trois.', 'Noir. ', 'Regretter nouveau rencontrer inquiéter.                     '),
(489154, 981376416021.9, 694306849743.74, '2013-08-14', 'Avant.', 'Mot.  ', 'Soi dégager front classe extraordinaire nation fier.        '),
(996831, 148687471863.74, 556492743309.62, '1978-07-10', 'Sept. ', 'Vieux.', 'Composer bientôt deviner inviter intéresser fortune.        '),
(362208, 751447695831.68, 252364583088.82, '1971-12-18', 'Tenir.', 'Vieux.', 'Oeuvre inviter représenter chaque impossible feuille.       '),
(215015, 115457495436.89, 506316451401.79, '1985-04-08', 'Port. ', 'Nez.  ', 'Considérer rêve monde haine. Haïr ligne professeur.         '),
(971141, 117489345474.50, 255917429819.30, '2006-03-09', 'Beaux.', 'Saint.', 'Ressembler lien alors croiser bon faux glisser.             '),
(286127, 808477768212.24, 180458943975.1, '2009-07-21', 'Grave.', 'Aller.', 'Secours abri police contraire.                              '),
(412189, 645336857211.32, 144910639702.8, '1977-01-10', 'Chat. ', 'Image.', 'Chemise terrain digne tel cours trace chasser.              '),
(725400, 620393091816.79, 560824657599.59, '2011-01-06', 'Clair.', 'Sol.  ', 'Appartenir chien souvenir être.                             '),
(699357, 456047134587.18, 493567691046.52, '1990-06-07', 'Tant. ', 'Seul. ', 'Droite fonder révolution déchirer train port non.           '),
(462080, 109560944097.56, 13161592809.83, '1984-07-15', 'Crise.', 'Jeter.', 'Joindre bon vieux fidèle occasion. Moi obtenir très.        '),
(99155 , 754107733673.64, 290949935411.69, '1978-07-05', 'Salle.', 'Matin.', 'Cri sentir faute perte aile rôle saint lueur.               '),
(579360, 108199861742.13, 918262098700.26, '1970-01-20', 'Fond. ', 'Froid.', 'Image écraser situation remplir.                            '),
(640922, 555923740049.65, 997171397498.43, '1983-11-21', 'Foi.  ', 'Fuir. ', 'Personnage objet soumettre.                                 '),
(487322, 399826676871.1, 689647491934.8, '2000-08-22', 'Image.', 'Roman.', 'Sueur tracer émotion ouvrage trace.                         '),
(856806, 889478825115.79, 388786066314.90, '1992-01-15', 'Long. ', 'Y.    ', 'Circonstance ci seuil dernier.                              '),
(743147, 380271305382.83, 596237626616.85, '2015-04-05', 'Forme.', 'But.  ', 'Quelque inquiéter exemple fleur nuage cri avoir.            '),
(176570, 167437995334.52, 796185098015.11, '1973-07-29', 'Coin. ', 'Repas.', 'Crier vague ton nommer détacher verre remarquer.            '),
(416596, 390267669002.65, 211658751483.85, '2010-05-12', 'Muet. ', 'Grain.', 'Instant partie que monter.                                  '),
(832414, 518879650195.49, 123112304874.72, '1992-04-23', 'Avant.', 'Rêve. ', 'Chaud éclat théâtre sac douceur.                            '),
(930120, 284596847071.19, 150325304473.80, '1987-10-07', 'Se.   ', 'Peser.', 'Finir preuve phrase livrer.                                 '),
(827195, 667849305589.59, 841240195004.46, '1995-12-10', 'Midi. ', 'Avant.', 'Passer prince titre ruine malgré acheter cent.              '),
(778380, 771742100860.86, 263614771245.85, '2014-05-04', 'Eaux. ', 'Coup. ', 'Paysage silencieux as payer danser.                         '),
(348019, 752324542218.86, 586625985718.15, '2002-03-30', 'Sien. ', 'Roman.', 'Entraîner eaux céder drôle page autant marchand.            '),
(454749, 846311215730.16, 939062401870.36, '2005-07-07', 'Rôle. ', 'Ou.   ', 'Part corde nourrir appartenir.                              '),
(644541, 667093815453.30, 413714058404.30, '1991-01-09', 'Moi.  ', 'Du.   ', 'Deviner dormir saint cependant écrire meilleur.             '),
(755229, 368689552612.42, 544999464498.4, '2010-09-08', 'Dont. ', 'Clef. ', 'Fixe détacher oncle celui. Planche rond mien cri comment.   '),
(581300, 649235524598.33, 815579624009.88, '1982-12-07', 'En.   ', 'Jour. ', 'Devenir faim tenir rapporter rapport.                       '),
(926845, 535776634916.1, 600720308510.94, '1989-08-16', 'Point.', 'Plus. ', 'Parti prochain main. Ceci habitant bas demande.             '),
(375273, 783900134248.96, 780778512369.93, '2001-10-27', 'Comme.', 'Salut.', 'Signer naître semaine assister vieillard pour dame maladie. '),
(410357, 387381252568.12, 910469710797.27, '1988-03-12', 'Matin.', 'Barbe.', 'Trésor prière amour solitude ciel.                          ');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE IF NOT EXISTS `student` (
  `NAME` varchar(30) NOT NULL,
  `TITLE` varchar(25) NOT NULL,
  `CLASS` varchar(5) NOT NULL,
  `SECTION` varchar(1) NOT NULL,
  `ROLLID` decimal(3,0) NOT NULL,
  PRIMARY KEY (`CLASS`,`SECTION`,`ROLLID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`NAME`, `TITLE`, `CLASS`, `SECTION`, `ROLLID`) VALUES
('recevoir                      ', 'Ouvert après rire titre. ', 'répon', 'b', 386),
('passage                       ', 'Tendre possible rouge.   ', 'saint', 'v', 630),
('fruit                         ', 'Ce seul résoudre.        ', 'dos  ', 'g', 897);

-- --------------------------------------------------------

--
-- Table structure for table `studentreport`
--

CREATE TABLE IF NOT EXISTS `studentreport` (
  `CLASS` varchar(5) NOT NULL,
  `SECTION` varchar(1) NOT NULL,
  `ROLLID` decimal(3,0) NOT NULL,
  `GRADE` varchar(5) NOT NULL,
  `SEMISTER` varchar(5) DEFAULT NULL,
  `CLASS_ATTENDED` decimal(25,0) DEFAULT NULL,
  KEY `FK_CSR` (`CLASS`,`SECTION`,`ROLLID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `studentreport`
--

INSERT INTO `studentreport` (`CLASS`, `SECTION`, `ROLLID`, `GRADE`, `SEMISTER`, `CLASS_ATTENDED`) VALUES
('effac', 'h', 589, 'page ', 'recon', 9330434441354910417422412),
('cerve', 'p', 533, 'demi ', 'suiva', 2633249988410773332725539),
('vieux', 'l', 577, 'colon', 'tout', 437480787981775879423051),
('prése', 'l', 237, 'ramen', 'oser', 4134608169843979694374811),
('beau ', 'b', 516, 'étoil', 'besoi', 7323209547753259745754919);
