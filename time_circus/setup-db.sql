DROP TABLE IF EXISTS performance_performer_assignment;

DROP TABLE IF EXISTS performance;

DROP TABLE IF EXISTS venue;

DROP TABLE IF EXISTS performer;

DROP TABLE IF EXISTS specialty;

CREATE TABLE specialty (
    specialty_id BIGINT PRIMARY KEY,
    specialty_name VARCHAR(100)
);

CREATE TABLE performer (
    performer_id BIGINT PRIMARY KEY,
    performer_stagename VARCHAR(50),
    performer_dob DATE,
    specialty_id BIGINT,
    FOREIGN KEY (specialty_id) REFERENCES specialty(specialty_id)
);

CREATE TABLE venue (
    venue_id BIGINT PRIMARY KEY,
    venue_name VARCHAR(100)
);

CREATE TABLE performance (
    performance_id BIGINT PRIMARY KEY,
    venue_id BIGINT,
    performance_date DATE,
    review_score SMALLINT,
    FOREIGN KEY (venue_id) REFERENCES venue(venue_id)
);

CREATE TABLE performance_performer_assignment (
    performance_performer_assignment_id BIGINT PRIMARY KEY,
    performer_id BIGINT,
    performance_id BIGINT,
    FOREIGN KEY (performer_id) REFERENCES performer(performer_id),
    FOREIGN KEY (performance_id) REFERENCES performance(performance_id)
);

INSERT INTO specialty (specialty_id, specialty_name) VALUES
(1, 'Fire Breathing'),
(2, 'Juggling'),
(3, 'Acrobatics'),
(4, 'Mind Reading'),
(5, 'Clowning'),
(6, 'Trapeze'),
(7, 'Magic'),
(8, 'Animal Training'),
(9, 'Sword Swallowing'),
(10, 'Contortionism'),
(11, 'Tightrope Walking'),
(12, 'Strongman'),
(13, 'Unicycling'),
(14, 'Escapology'),
(15, 'Knife Throwing'),
(16, 'Water Dancing'),
(17, 'Shadow Puppetry'),
(18, 'Gravity Defying Acts'),
(19, 'Quantum Jumps'),
(20, 'Illusions')
;

INSERT INTO performer (performer_id, performer_stagename, performer_dob, specialty_id) VALUES
(1, 'Orac the Oracle', '0123-05-12', 4),
(2, 'Julius the Juggler', '0100-03-15', 2),
(3, 'Zephyra the Zesty', '0095-08-07', 3),
(4, 'Atlas the Strongman', '0150-03-21', 12),
(5, 'Merlin the Marvelous', '1100-01-23', 7),
(6, 'Knight Knave', '1250-12-30', 15),
(7, 'Arthur the Acrobatic', '1300-04-17', 3),
(8, 'Gerald the Great', '1400-11-10', 1),
(9, 'Future Fiona', '2085-09-18', 20),
(10, 'Digital Dazzler', '2090-07-25', 18),
(11, 'Cosmic Chris', '2100-12-25', 19),
(12, 'Galactic Gina', '2200-02-03', 6),
(13, 'Infinite Ian', '3000-11-13', 8),
(14, 'Time Turner', '4000-01-07', 5),
(15, 'Dimension Dan', '1500-10-05', 9),
(16, 'Time-Travelling Tom', '1950-05-02', 16),
(17, 'Eccentric Eloise', '2025-08-27', 17),
(18, 'Bursting Barry', '1982-09-14', 10),
(19, 'Gritty Greta', '1994-02-25', 14),
(20, 'Nimble Nick', '1800-12-04', 13),
(21, 'Chronos the Unseen', '5000-12-12', 11),
(22, 'Cascadia', '6000-02-14', 7),
(23, 'Siren Sara', '2750-07-08', 16),
(24, 'Echo Enigma', '3200-05-05', 18),
(25, 'Paradox Percy', '4100-01-01', 20),
(26, 'Pyro Petra', '0920-11-23', 1),
(27, 'Holographic Hedley', '2180-08-29', 6),
(28, 'Temporal Tanya', '2400-03-13', 15),
(29, 'Psyche the Psychic', '2000-07-24', 4),
(30, 'Quantum Quentin', '2950-11-30', 19),
(31, 'Whispering Willow', '2900-10-10', 8),
(32, 'Elastic Ethan', '2050-05-18', 10),
(33, 'Kaleidoscope Kelly', '2850-09-09', 17),
(34, 'Cinematic Callie', '2750-12-13', 13),
(35, 'Stuntman Stan', '3010-04-16', 18),
(36, 'Dream Dancer', '3020-01-01', 16),
(37, 'Aether Aiden', '3025-07-01', 14),
(38, 'Vertigo Victor', '1200-12-25', 3),
(39, 'Master Max', '2055-09-09', 2),
(40, 'Warp Wayne', '2500-06-16', 19),
(41, 'Psychic Phil', '1850-06-20', 4),
(42, 'Flexi Felix', '2140-02-18', 10),
(43, 'Plasma Percy', '2210-08-08', 1),
(44, 'Spectacular Sienna', '2320-01-19', 7),
(45, 'Tidal Tilly', '2450-11-28', 11),
(46, 'Gadget Greg', '2600-03-03', 14),
(47, 'Mystery Mo', '2700-08-20', 4),
(48, 'Electric Ella', '2332-09-15', 16),
(49, 'Astro Ashley', '2605-04-11', 6),
(50, 'Clover Clown', '3050-06-24', 5)
;

INSERT INTO venue (venue_id, venue_name) VALUES
(1, 'Grand Circus'),
(2, 'Roman Colosseum'),
(3, 'Egyptian Pyramid'),
(4, 'Grand Central Terminal'),
(5, 'Ancient Greece Amphitheatre'),
(6, 'Medieval Castle Grounds'),
(7, 'Victorian Exhibition Hall'),
(8, 'Renaissance Festival'),
(9, 'Futuristic Dome'),
(10, 'Space Station Arena'),
(11, 'Underwater Stage'),
(12, 'Jungle Clearing'),
(13, 'Desert Oasis'),
(14, 'Mountain Top'),
(15, 'Beachfront Pavilion'),
(16, 'Mars Amphitheatre'),
(17, 'Venus Sky Dome'),
(18, 'Atlantis Arena'),
(19, 'Galactic Theater'),
(20, 'Time Travel Hub')
;

INSERT INTO performance (performance_id, venue_id, performance_date, review_score) VALUES
(1, 1, '2024-01-01', 95),
(2, 2, '2023-12-25', 90),
(3, 3, '2023-11-30', 85),
(4, 4, '2023-10-15', 92),
(5, 5, '2024-02-14', 88),
(6, 6, '2024-03-17', 91),
(7, 7, '2024-04-01', 87),
(8, 8, '2024-05-05', 93),
(9, 9, '2024-06-21', 89),
(10, 10, '2024-07-04', 97),
(11, 11, '3000-01-01', 100),
(12, 12, '1500-05-15', 92),
(13, 13, '2500-07-11', 90),
(14, 14, '1800-10-20', 88),
(15, 15, '5000-12-31', 85),
(16, 16, '6000-03-03', 94),
(17, 17, '5500-08-08', 97),
(18, 18, '2000-09-09', 91),
(19, 19, '3000-03-03', 86),
(20, 20, '4000-09-09', 88),
(21, 1, '1000-01-01', 82),
(22, 2, '4500-06-17', 91),
(23, 3, '3500-03-21', 93),
(24, 4, '1200-09-15', 87),
(25, 5, '1450-08-08', 84),
(26, 6, '2300-04-22', 90),
(27, 7, '2999-11-30', 98),
(28, 8, '2750-02-14', 85),
(29, 9, '3899-12-19', 91),
(30, 10, '2899-07-08', 79),
(31, 11, '3999-06-18', 86),
(32, 12, '4832-09-25', 96),
(33, 13, '3230-03-11', 88),
(34, 14, '2323-11-27', 90),
(35, 15, '2100-01-23', 89),
(36, 16, '1111-07-07', 83),
(37, 17, '1212-08-12', 92),
(38, 18, '1313-10-10', 87),
(39, 19, '1414-04-04', 85),
(40, 20, '1515-05-05', 93),
(41, 1, '1800-02-02', 82),
(42, 2, '1900-03-03', 86),
(43, 3, '2000-04-04', 90),
(44, 4, '2100-05-05', 87),
(45, 5, '2200-06-06', 89),
(46, 6, '2300-07-07', 94),
(47, 7, '2400-08-08', 91),
(48, 8, '2500-09-09', 88),
(49, 9, '2600-10-10', 90),
(50, 10, '2700-11-11', 95),
(51, 11, '2800-12-12', 97),
(52, 12, '2900-01-01', 84),
(53, 13, '3000-02-02', 93),
(54, 14, '3100-03-03', 92),
(55, 15, '3200-04-04', 89),
(56, 16, '3300-05-05', 96),
(57, 17, '3400-06-06', 90),
(58, 18, '3500-07-07', 85),
(59, 19, '3600-08-08', 88),
(60, 20, '3700-09-09', 91),
(61, 1, '3777-10-10', 87),
(62, 2, '3888-11-11', 82),
(63, 3, '3999-12-12', 95),
(64, 4, '4100-01-01', 86),
(65, 5, '4200-02-02', 94),
(66, 6, '4300-03-03', 90),
(67, 7, '4400-04-04', 96),
(68, 8, '4500-05-05', 89),
(69, 9, '4600-06-06', 92),
(70, 10, '4700-07-07', 84),
(71, 11, '4800-08-08', 93),
(72, 12, '4900-09-09', 97),
(73, 13, '5000-10-10', 91),
(74, 14, '5100-11-11', 88),
(75, 15, '5200-12-12', 90),
(76, 16, '5300-01-01', 95),
(77, 17, '5400-02-02', 89),
(78, 18, '5500-03-03', 93),
(79, 19, '5600-04-04', 90),
(80, 20, '5700-05-05', 86),
(81, 1, '5800-06-06', 92),
(82, 2, '5900-07-07', 83),
(83, 3, '6000-08-08', 89),
(84, 4, '6100-09-09', 96),
(85, 5, '6200-10-10', 91),
(86, 6, '6300-11-11', 87),
(87, 7, '6400-12-12', 94),
(88, 8, '6500-01-01', 85),
(89, 9, '6600-02-02', 92),
(90, 10, '6700-03-03', 88),
(91, 11, '6800-04-04', 90),
(92, 12, '6900-05-05', 94),
(93, 13, '7000-06-06', 87),
(94, 14, '7100-07-07', 89),
(95, 15, '7200-08-08', 95),
(96, 16, '7300-09-09', 96),
(97, 17, '7400-10-10', 93),
(98, 18, '7500-11-11', 88),
(99, 19, '7600-12-12', 91),
(100, 20, '7700-01-01', 94)
;

INSERT INTO performance_performer_assignment (performance_performer_assignment_id, performer_id, performance_id) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 4),
(5, 1, 5),
(6, 2, 6),
(7, 5, 7),
(8, 6, 8),
(9, 7, 9),
(10, 8, 10),
(11, 9, 11),
(12, 10, 12),
(13, 11, 13),
(14, 12, 14),
(15, 13, 15),
(16, 14, 16),
(17, 15, 17),
(18, 16, 18),
(19, 17, 19),
(20, 18, 20),
(21, 19, 11),
(22, 20, 12),
(23, 1, 13),
(24, 3, 14),
(25, 5, 15),
(26, 21, 16),
(27, 22, 17),
(28, 23, 18),
(29, 24, 19),
(30, 25, 20),
(31, 26, 21),
(32, 27, 22),
(33, 28, 23),
(34, 29, 24),
(35, 30, 25),
(36, 31, 26),
(37, 32, 27),
(38, 33, 28),
(39, 34, 29),
(40, 35, 30),
(41, 36, 31),
(42, 37, 32),
(43, 38, 33),
(44, 39, 34),
(45, 40, 35),
(46, 41, 36),
(47, 42, 37),
(48, 43, 38),
(49, 44, 39),
(50, 45, 40),
(51, 46, 21),
(52, 47, 22),
(53, 48, 23),
(54, 49, 24),
(55, 50, 25)
;