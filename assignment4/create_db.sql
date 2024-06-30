CREATE DATABASE nails;
USE nails;

CREATE TABLE `nail_bookings` (
  `nailTech` varchar(45) DEFAULT NULL,
  `12-13` varchar(15) DEFAULT NULL CHECK (`12-13` IN ('regular manicure', 'gel manicure', 'regular pedicure', 'gel pedicure')),
  `12-13-client` varchar(20) DEFAULT NULL,
  `12-13-contact` char(11) DEFAULT NULL,
  `13-14` varchar(15) DEFAULT NULL CHECK (`13-14` IN ('regular manicure', 'gel manicure', 'regular pedicure', 'gel pedicure')),
  `13-14-client` varchar(20) DEFAULT NULL,
  `13-14-contact` char(11)  DEFAULT NULL,
  `14-15` varchar(15) DEFAULT NULL CHECK (`14-15` IN ('regular manicure', 'gel manicure', 'regular pedicure', 'gel pedicure')),
  `14-15-client` varchar(20) DEFAULT NULL,
  `14-15-contact` char(11)  DEFAULT NULL,
  `15-16` varchar(15) DEFAULT NULL CHECK (`15-16` IN ('regular manicure', 'gel manicure', 'regular pedicure', 'gel pedicure')),
  `15-16-client` varchar(20) DEFAULT NULL,
  `15-16-contact` char(11)  DEFAULT NULL,
  `16-17` varchar(15) DEFAULT NULL CHECK (`16-17` IN ('regular manicure', 'gel manicure', 'regular pedicure', 'gel pedicure')),
  `16-17-client` varchar(20) DEFAULT NULL,
  `16-17-contact` char(11)  DEFAULT NULL,
  `17-18` varchar(15) DEFAULT NULL CHECK (`17-18` IN ('regular manicure', 'gel manicure', 'regular pedicure', 'gel pedicure')),
  `17-18-client` varchar(20) DEFAULT NULL,
  `17-18-contact` char(11)  DEFAULT NULL,
  `bookingDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Stored procedure to insert rows into nail bookings table.
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `filldates`(dateStart DATE, dateEnd DATE, nailTech VARCHAR(45))
BEGIN
-- While date start is less than date end, perform loop to insert empty rows.
  WHILE dateStart <= dateEnd DO
	-- Insert new record into booking table.
    INSERT INTO nail_bookings (nailTech, bookingDate) VALUES (nailTech, dateStart);
    -- Adds 1 day to datestart before start of next loop.
    SET dateStart = date_add(dateStart, INTERVAL 1 DAY);
-- End loop. 
  END WHILE;
-- End procedure. 
END$$
DELIMITER ;

CALL `nails`.`filldates`(20240629, 20240930, 'Bronte');
CALL `nails`.`filldates`(20240629, 20240930, 'Finn');
CALL `nails`.`filldates`(20240629, 20240930, 'Max');

SELECT * FROM nail_bookings;

