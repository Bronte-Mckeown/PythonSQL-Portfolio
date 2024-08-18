-- Create and use nails data base. 
CREATE DATABASE nails;
USE nails;

-- Create nail_bookings table with nail technician name column, a column for each time slot, a column for each time slot's client
-- , each time slot's contact number and the booking date. Each time slot will only accept 4 types of nail appointment.
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

-- Use filldates procedure to add blank rows for bronte, finn, and max for the next three months 
CALL `nails`.`filldates`(20240702, 20241002, 'bronte');
CALL `nails`.`filldates`(20240702, 20241002, 'finn');
CALL `nails`.`filldates`(20240702, 20241002, 'max');

-- See all rows and columns in nail_bookings table 
SELECT * FROM nail_bookings;

-- Run the following to see your user name and host name
SELECT user(); 