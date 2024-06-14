-- create database university;

USE university;

-- CREATE TABLE students(
-- 	student_id CHAR(4) PRIMARY KEY,
--     first_name VARCHAR(50) NOT NULL,
--     last_name VARCHAR(50) NOT NULL,
--     dob DATE NOT NULL,
--     email_address VARCHAR(50) UNIQUE NOT NULL
-- );

-- DROP students;

-- INSERT INTO students(student_id, first_name, last_name, dob, email_address)
-- VALUES
-- ('2240', 'bronte', 'mckeown', STR_TO_DATE('02/11/1997','%d/%m/%Y'), 'bronte.mckeown@gmail.com'),
-- ('4598', 'dolly', 'parton', STR_TO_DATE('19/01/1946','%d/%m/%Y'), 'dolly.parton@gmail.com'),
-- ('6598', 'finn', 'tonry', STR_TO_DATE('13/02/1997','%d/%m/%Y'), 'finntonry@gmail.com'),
-- ('7812', 'harper', 'collins', STR_TO_DATE('22/05/2001','%d/%m/%Y'), 'harper.collins@gmail.com'),
-- ('3981', 'mason', 'wright', STR_TO_DATE('30/07/1995','%d/%m/%Y'), 'mason.wright@gmail.com'),
-- ('5623', 'olivia', 'james', STR_TO_DATE('18/09/1999','%d/%m/%Y'), 'olivia.james@gmail.com'),
-- ('9234', 'liam', 'smith', STR_TO_DATE('25/12/2000','%d/%m/%Y'), 'liam.smith@gmail.com'),
-- ('3345', 'sophia', 'johnson', STR_TO_DATE('03/03/1998','%d/%m/%Y'), 'sophia.johnson@gmail.com'),
-- ('1267', 'jackson', 'miller', STR_TO_DATE('12/11/1996','%d/%m/%Y'), 'jackson.miller@gmail.com'),
-- ('7854', 'isabella', 'brown', STR_TO_DATE('04/04/2002','%d/%m/%Y'), 'isabella.brown@gmail.com'),
-- ('5643', 'elijah', 'davis', STR_TO_DATE('14/06/2001','%d/%m/%Y'), 'elijah.davis@gmail.com'),
-- ('8901', 'mia', 'martinez', STR_TO_DATE('09/09/1999','%d/%m/%Y'), 'mia.martinez@gmail.com'),
-- ('2378', 'aiden', 'garcia', STR_TO_DATE('07/07/1997','%d/%m/%Y'), 'aiden.garcia@gmail.com');

CREATE TABLE departments(
	department_id CHAR(4) PRIMARY KEY,
    department_name VARCHAR(200) UNIQUE NOT NULL
);

-- To add: Deparment Head ID as foreign key (from staff table)
 
CREATE TABLE courses(
	course_id CHAR(4) PRIMARY KEY,
    course_name VARCHAR(200) UNIQUE NOT NULL,
    capacity INT DEFAULT 5, 
    enrol_deadline DATETIME
);

-- To add: Department ID (from department table) and Staff ID (staff table) as foreign keys
