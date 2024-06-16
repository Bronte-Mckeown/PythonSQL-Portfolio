-- This assignment creates a university database.
-- It shows how it would be used by university admin for a range
-- of tasks including: enrolling students to the university and specific courses,
-- retrieving student numbers in departments and courses, keeping staff records,
-- and contacting staff via email to be mentors of junior staff members.

-- Create university database. 
CREATE DATABASE university;

-- Use database.
USE university;

-- Create 'departments' table.
-- Contains department ID (primary key) and department name.
-- The department ID must (1) start with a 2 and (2) be 4 characters.
-- The department name must be unique and not null.
CREATE TABLE departments(
	department_id CHAR(4) PRIMARY KEY,
    department_name VARCHAR(200) UNIQUE NOT NULL,
    CHECK (department_id LIKE '2%')
);

--  Insert departments into departments table.
INSERT INTO departments(department_id, department_name)
VALUES
('2478', 'Psychology'),
('2479', 'Sociology'),
('2480', 'Biology'),
('2481', 'Chemistry'),
('2482', 'Physics'),
('2483', 'Mathematics'),
('2484', 'History'),
('2485', 'Political Science'),
('2486', 'Economics'),
('2487', 'Philosophy');

-- Select all to see all departments (IDs and names) in university, ordered by name.
SELECT * 
FROM departments
ORDER BY department_name;

-- Select just department_name to only see department names, ordered by name.
SELECT department_name
AS 'Department'
FROM departments
ORDER BY department_name;

-- Return all department names that begin with P.
SELECT department_name
FROM departments
WHERE department_name LIKE 'P%'
ORDER BY department_name;

-- Count how many departments there are in the university.
SELECT COUNT(department_id) 
AS 'Total Departments'
FROM departments;

-- Create 'schools' table.
-- Contains school ID (primary key) and school name.
-- School ID must start with 6 and be 4 characters.
--  School name must be unique and not null.
CREATE TABLE schools(
	school_id CHAR(4) PRIMARY KEY,
    school_name VARCHAR(100) UNIQUE NOT NULL,
    CHECK (school_id LIKE '6%')
);

-- Insert data into schools table. 
INSERT INTO schools(school_id, school_name)
VALUES
('6000', 'STEM'),
('6001', 'Social Science'),
('6002', 'Humanities');

-- Create 'department_affiliation' table that links
-- department IDs and school IDs (both foreign keys). 
-- Make them both a composite primary key.
CREATE TABLE department_affiliation(
	department_id CHAR(4),
    school_id CHAR(4),
    INDEX dep_id (department_id),
    FOREIGN KEY (department_id) 
		REFERENCES departments(department_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	INDEX sch_id (school_id),
    FOREIGN KEY (school_id) 
		REFERENCES schools(school_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	PRIMARY KEY (department_id, school_id)
);

-- Insert IDs into department_affiliation table. 
INSERT INTO department_affiliation(department_id, school_id)
VALUES
('2478', '6001'), 
('2479', '6001'),
('2480', '6000'),
('2481', '6000'),
('2482', '6000'),
('2483', '6000'),
('2484', '6002'),
('2485', '6001'),
('2486', '6001'),
('2487', '6002');

-- Create 'students' table. 
-- The students table contains student ID, first and last names,
-- DOB, email address, and which department they belong in.
-- Student ID must start with 4 and be 4 characters long.
-- Names,  DOB (date) and emails cannot be null.
-- Email address must be unique.
-- If department ID is deleted in parent table, set to null here.
-- If department ID is updated in parent table, updated here.
CREATE TABLE students(
	student_id CHAR(4) PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	dob DATE NOT NULL,
	email_address VARCHAR(50) UNIQUE NOT NULL,
	CHECK (student_id LIKE '4%'),
    department CHAR(4),
    INDEX dep_id (department),
    FOREIGN KEY (department) 
		REFERENCES departments(department_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

--  Insert students into table.
-- Note: For time saving, gave CHAT-GPT the first three rows and asked it to generate 30 more.
-- Asked it to distribute students (approx) equally across departments.
INSERT INTO students(student_id, first_name, last_name, dob, email_address, department)
VALUES
('4240', 'bronte', 'mckeown', '1997-11-02', 'bronte.mckeown@gmail.com', '2478'),
('4598', 'dolly', 'parton', '1946-01-19', 'dolly.parton@gmail.com', '2479'),
('4594', 'finn', 'tonry', '1997-02-13', 'finntonry@gmail.com', '2480'),
('4812', 'harper', 'collins', '2001-05-22', 'harper.collins@gmail.com', '2481'),
('4981', 'mason', 'wright', '1995-07-30', 'mason.wright@gmail.com', '2482'),
('4623', 'olivia', 'james', '1999-09-18', 'olivia.james@gmail.com', '2483'),
('4234', 'liam', 'smith', '2000-12-25', 'liam.smith@gmail.com', '2484'),
('4345', 'sophia', 'johnson', '1998-03-03', 'sophia.johnson@gmail.com', '2485'),
('4267', 'jackson', 'miller', '1996-11-12', 'jackson.miller@gmail.com', '2486'),
('4854', 'isabella', 'brown', '2002-04-04', 'isabella.brown@gmail.com', '2487'),
('4643', 'elijah', 'davis', '2001-06-14', 'elijah.davis@gmail.com', '2478'),
('4901', 'mia', 'martinez', '1999-09-09', 'mia.martinez@gmail.com', '2479'),
('4378', 'aiden', 'garcia', '1997-07-07', 'aiden.garcia@gmail.com', '2480'),
('4922', 'amelia', 'rodriguez', '1998-08-20', 'amelia.rodriguez@gmail.com', '2481'),
('4955', 'noah', 'wilson', '2001-02-02', 'noah.wilson@gmail.com', '2482'),
('4883', 'emma', 'anderson', '1996-01-11', 'emma.anderson@gmail.com', '2483'),
('4477', 'logan', 'thomas', '1997-12-16', 'logan.thomas@gmail.com', '2484'),
('4419', 'ava', 'taylor', '1998-07-05', 'ava.taylor@gmail.com', '2485'),
('4828', 'lucas', 'moore', '2000-03-09', 'lucas.moore@gmail.com', '2486'),
('4390', 'charlotte', 'jackson', '1996-11-23', 'charlotte.jackson@gmail.com', '2487'),
('4735', 'michael', 'harris', '1999-10-15', 'michael.harris@gmail.com', '2478'),
('4866', 'grace', 'martin', '1995-04-19', 'grace.martin@gmail.com', '2479'),
('4917', 'benjamin', 'lee', '1998-12-10', 'benjamin.lee@gmail.com', '2480'),
('4508', 'chloe', 'perez', '2000-06-27', 'chloe.perez@gmail.com', '2481'),
('4661', 'alexander', 'lopez', '1997-01-13', 'alexander.lopez@gmail.com', '2482'),
('4722', 'ella', 'gonzalez', '2001-08-07', 'ella.gonzalez@gmail.com', '2483'),
('4766', 'sebastian', 'evans', '1996-05-14', 'sebastian.evans@gmail.com', '2484'),
('4600', 'zoe', 'robinson', '1998-02-22', 'zoe.robinson@gmail.com', '2485'),
('4789', 'jacob', 'walker', '2000-09-18', 'jacob.walker@gmail.com', '2486'),
('4532', 'victoria', 'hall', '1999-11-30', 'victoria.hall@gmail.com', '2487'),
('4993', 'samuel', 'allen', '2002-04-15', 'samuel.allen@gmail.com', '2478'),
('4511', 'scarlett', 'young', '2001-01-05', 'scarlett.young@gmail.com', '2479'),
('4512', 'elliot', 'young', '2001-01-05', 'elliot.young@gmail.com', '2480');

-- Count how many students there are overall in university.
SELECT COUNT(student_id) 
AS 'Total Students'
FROM students;

-- Add two students with no department affiliation as they haven't decided yet.
INSERT INTO students(student_id, first_name, last_name, dob, email_address)
VALUES
('4972', 'lucy', 'walmes', '1992-12-01', 'lucy.walmes@gmail.com'),
('4973', 'jack', 'daniels', '1995-11-23', 'jack.daniels@gmail.com');

-- Count how many students are in each department.
-- Use INNER join to return department name.
-- This will ignore students with no department.
-- Store in a view to use later.
CREATE VIEW n_students_by_department
AS
	SELECT d.department_name
			AS 'Department',
			COUNT(student_id)
			AS 'N Students'
	FROM students s
	INNER JOIN departments d 
	ON s.department = d.department_id
	GROUP BY d.department_name
	ORDER BY d.department_name;

-- Select specific departments from view 
SELECT * 
FROM n_students_by_department
WHERE Department in ('Biology', 'Chemistry', 'Physics');

-- Count how many students are in each department.
-- But this time, use LEFT (outer) join to return department name.
-- This will also count students with no department (null).
CREATE VIEW n_students_by_department_with_null
AS
	SELECT d.department_name
			AS 'Department',
			COUNT(student_id)
			AS 'N Students'
	FROM students s
	LEFT JOIN departments d 
	ON s.department = d.department_id
	GROUP BY d.department_name
	ORDER BY d.department_name;
    
-- Select number of students that don't have a department
SELECT *
FROM n_students_by_department_with_null
WHERE Department IS NULL;
    
-- Return how many students are in each department within STEM school.
SELECT d.department_name
	AS 'Department',
	COUNT(student_id)
	AS 'N Students'
FROM students st
JOIN departments d 
ON st.department = d.department_id
JOIN department_affiliation dep_a
ON d.department_id = dep_a.department_id
WHERE dep_a.school_id = '6000'
GROUP BY d.department_name;

-- Insert department IDs for those 2 students into student table using UPDATE
UPDATE students
SET department = 2478
WHERE student_id = '4972';

UPDATE students
SET department = 2478
WHERE student_id = '4973';

-- Check updates.
SELECT department
FROM students
WHERE student_id IN ('4972', '4973');

-- Select number of students that don't have a department
-- This will now be no students!
SELECT *
FROM n_students_by_department_with_null
WHERE Department IS NULL;

-- Create 'staff' table with staff IDs (primary key), first and last names,
-- DOB, email address, date staff member joined, and their department. 
-- Names, dob, email address and date joined can't be null.
-- Staff ID has to start with 7 and be 4 characters.
-- Department ID is foreign key from departments.
-- On delete in parent table, set to null and cascade updates.  
CREATE TABLE staff(
	staff_id CHAR(4) PRIMARY KEY, 
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    dob DATE NOT NULL,
    email_address VARCHAR(50) UNIQUE NOT NULL,
    date_joined DATE NOT NULL,
    department CHAR(4),
    INDEX dep_id (department),
    FOREIGN KEY (department) 
		REFERENCES departments(department_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
	CHECK (staff_id LIKE '7%')
);

-- Insert data into staff table.
-- Again, gave CHAT-GPT the first 2 rows and asked for 27 more to have more data to play with.
INSERT INTO staff(staff_id, first_name, last_name, dob, email_address, date_joined, department)
VALUES
('7789', 'Tony', 'Morland', '1965-11-02', 'tony.morland@york.ac.uk', '1997-05-04', '2478'),
('7790', 'Emily', 'Brown', '1972-06-14', 'emily.brown@york.ac.uk', '2023-09-12', '2478'),
('7791', 'John', 'Smith', '1980-08-25', 'john.smith@york.ac.uk', '2005-03-15', '2479'),
('7792', 'Jane', 'Doe', '1985-12-17', 'jane.doe@york.ac.uk', '2008-06-20', '2479'),
('7793', 'Michael', 'Johnson', '1978-01-03', 'michael.johnson@york.ac.uk', '2003-07-25', '2480'),
('7794', 'Sarah', 'Taylor', '1983-04-11', 'sarah.taylor@york.ac.uk', '2007-09-30', '2480'),
('7795', 'David', 'Lee', '1975-10-09', 'david.lee@york.ac.uk', '2023-05-22', '2481'),
('7796', 'Laura', 'White', '1981-03-23', 'laura.white@york.ac.uk', '2006-11-17', '2481'),
('7797', 'James', 'Martin', '1969-09-07', 'james.martin@york.ac.uk', '1995-02-10', '2482'),
('7798', 'Karen', 'Anderson', '1974-05-29', 'karen.anderson@york.ac.uk', '1999-08-05', NULL),
('7799', 'Robert', 'Garcia', '1986-02-19', 'robert.garcia@york.ac.uk', '2010-04-12', '2483'),
('7800', 'Patricia', 'Martinez', '1982-11-30', 'patricia.martinez@york.ac.uk', '2009-06-28', '2483'),
('7801', 'Charles', 'Clark', '1970-07-16', 'charles.clark@york.ac.uk', '1996-01-18', '2484'),
('7802', 'Linda', 'Lewis', '1979-03-05', 'linda.lewis@york.ac.uk', '2023-10-09', '2484'),
('7803', 'Steven', 'Walker', '1981-08-27', 'steven.walker@york.ac.uk', '2006-12-14', '2485'),
('7804', 'Jessica', 'Hall', '1987-05-12', 'jessica.hall@york.ac.uk', '2011-03-21', '2485'),
('7805', 'George', 'Allen', '1968-01-22', 'george.allen@york.ac.uk', '1994-07-16', '2486'),
('7806', 'Nancy', 'Young', '1973-09-13', 'nancy.young@york.ac.uk', '2022-08-24', '2486'),
('7807', 'Brian', 'King', '1976-04-03', 'brian.king@york.ac.uk', '2001-11-13', '2487'),
('7808', 'Sandra', 'Hernandez', '1984-06-21', 'sandra.hernandez@york.ac.uk', '2008-05-08', '2487'),
('7809', 'Donald', 'Hill', '1971-10-14', 'donald.hill@york.ac.uk', '2023-02-11', '2478'),
('7810', 'Lisa', 'Scott', '1980-07-17', 'lisa.scott@york.ac.uk', '2014-05-30', '2479'),
('7811', 'Edward', 'Green', '1966-12-19', 'edward.green@york.ac.uk', '1993-04-03', '2480'),
('7812', 'Barbara', 'Adams', '1974-03-08', 'barbara.adams@york.ac.uk', '2022-09-14', '2481'),
('7813', 'Daniel', 'Nelson', '1977-05-26', 'daniel.nelson@york.ac.uk', '2000-07-22', '2482'),
('7814', 'Susan', 'Baker', '1985-11-04', 'susan.baker@york.ac.uk', '2012-02-28', '2483'),
('7815', 'Kenneth', 'Carter', '1982-06-14', 'kenneth.carter@york.ac.uk', '2015-04-12', '2484'),
('7816', 'Betty', 'Mitchell', '1970-09-19', 'betty.mitchell@york.ac.uk', '1996-03-16', '2485'),
('7817', 'Paul', 'Roberts', '1988-11-22', 'paul.roberts@york.ac.uk', '2014-08-20', '2486');

-- Insert department ID for staff member with missing value. 
UPDATE staff
SET department = '2483'
WHERE staff_id = '7798';

-- Count all staff members in each department and school.
-- Need staff, departments, department_affiliation, and schools tables.
CREATE VIEW n_staff_by_department_school
AS
	SELECT d.department_name
		  AS 'Department',
		  sch.school_name
		  AS 'School',
		  COUNT(st.staff_id)
		  AS 'N Staff'
	FROM staff st
	JOIN departments d
		ON d.department_id = st.department
	JOIN department_affiliation dep_a
		ON d.department_id = dep_a.department_id
	JOIN schools sch
		ON dep_a.school_id = sch.school_id
	GROUP BY d.department_name, sch.school_name 
	ORDER BY sch.school_name, d.department_name;

-- Look at view. 
SELECT * 
FROM n_staff_by_department_school;

-- Use view to only select departments within Social Science.
SELECT *
FROM n_staff_by_department_school
WHERE School = 'Social Science';
    
-- Use view to now calculate total staff within each school.
SELECT School,
	SUM(`N Staff`)
	AS 'Total'
    FROM n_staff_by_department_school
    GROUP BY School;

-- Figure out which staff are mentees and potential mentors based on years experience.
CREATE VIEW mentor_mentees
AS
	SELECT 
		s.staff_id,
		s.first_name,
		s.last_name,
        s.email_address,
		d.department_name,
		-- If years experience is less than 5, they are a mentee, otherwise, a potential mentor.
		IF(YEAR(NOW()) - YEAR(date_joined) < 5, 'Mentee', 'Mentor') 
		AS `Mentor Status`
	FROM 
		staff s
	JOIN departments d
	ON d.department_id = s.department
	ORDER BY
		d.department_name, `Mentor Status`;

-- Look at all data in view. 
SELECT *
FROM mentor_mentees;
    
-- Get email addresses of each mentor in each department to contact.
SELECT email_address, department_name
FROM mentor_mentees
WHERE `Mentor Status` = 'Mentor';

-- Get average number of years teaching for staff in each department, ordered by number of years.
-- Involves calculating current date using NOW()
SELECT d.department_name
	   AS 'Department',
	   ROUND(AVG(YEAR(NOW()) - YEAR(s.date_joined)))
	   AS `Avg Years Experience`
FROM staff s
JOIN departments d
	ON d.department_id = s.department
GROUP BY d.department_id
ORDER BY `Avg Years Experience`;

-- Create a 'courses' table.
-- Course ID is the primary key (must start with 9 and be 4 characters long)
-- Course name must be unique and not null.  
-- Capacity indicates max capacity of course (default = 5)
-- Enrol deadline indicates deadline for enrolment (default = 1st Aug 2024) 
CREATE TABLE courses(
	course_id CHAR(4) PRIMARY KEY,
    course_name VARCHAR(200) UNIQUE NOT NULL,
    capacity INT DEFAULT 5, 
    enrol_deadline DATETIME DEFAULT '2024-08-01',
    CHECK (course_id LIKE '9%')
);

-- Insert data values into courses table (used CHAT-GPT again to generate more data (gave first two rows). 
INSERT INTO courses(course_id, course_name, capacity, enrol_deadline)
VALUES
('9111', 'Introduction to Cognitive Neuroscience', 5, '2024-08-01 23:59:59'),
('9151', 'Introduction to Research Methods', 5, '2024-08-01 23:59:59'),
('9221', 'BioTech Applications', 3, '2024-08-01 23:59:59'),
('9131', 'Advanced Data Analysis', 2, '2024-08-01 23:59:59'),
('9141', 'Genetics and Genomics', 1, '2024-08-01 23:59:59'),
('9161', 'Machine Learning', 2, '2024-08-01 23:59:59'),
('9171', 'Artificial Intelligence', 2, '2024-08-01 23:59:59'),
('9181', 'Ethics in Technology', 5, '2024-08-01 23:59:59'),
('9191', 'Introduction to Philosophy', 5, '2024-08-01 23:59:59'),
('9201', 'Modern Political Theory', 2, '2024-08-01 23:59:59'),
('9211', 'Economic Principles', 3, '2024-08-01 23:59:59'),
('9231', 'History of Modern Art', 2, '2024-08-01 23:59:59'),
('9241', 'Environmental Science', 8, '2024-08-01 23:59:59'),
('9251', 'Organic Chemistry', 1, '2024-08-01 23:59:59'),
('9261', 'Quantum Physics', 2, '2024-08-01 23:59:59'),
('9271', 'English Literature through history', 3, '2024-08-01 23:59:59'),
('9281', 'Introduction to Sociology', 2, '2024-08-01 23:59:59'),
('9291', 'Cultural Anthropology', 2, '2024-08-01 23:59:59'),
('9301', 'International Relations', 2, '2024-08-01 23:59:59'),
('9311', 'Fundamentals of Marketing', 2, '2024-08-01 23:59:59'),
('9321', 'Business Management', 5, '2024-08-01 23:59:59'),
('9331', 'Introduction to Psychology', 3, '2024-08-01 23:59:59'),
('9341', 'Educational Psychology', 1, '2024-08-01 23:59:59'),
('9351', 'Developmental Biology', 5, '2024-08-01 23:59:59'),
('9361', 'Public Health', 2, '2024-08-01 23:59:59'),
('9371', 'Human Anatomy', 5, '2024-08-01 23:59:59'),
('9381', 'History of Ancient Civilizations', 2, '2024-07-01 23:59:59'),
('9391', 'Creative Writing', 1, '2024-07-01 23:59:59'),
('9401', 'Introduction to Robotics', 5, '2024-07-01 23:59:59'),
('9411', 'Digital Media and Society', 2, '2024-07-01 23:59:59'),
('9421', 'Neuropsychology', 5, '2024-08-01 23:59:59');

-- Update course enrolment deadline for Neuropsychology course.
UPDATE courses
SET enrol_deadline = '2023-06-16 20:00:00'
WHERE course_name = 'Neuropsychology';

-- Create a course details table.
-- Primary key is course_id which is a foreign key, linked to courses.
-- Other fields include module leader (foreign key = staff id from staff table)
-- and department (foreign key = department id from department table).    
CREATE TABLE course_details(
	course_id CHAR(4),
	module_leader CHAR(4),
    department CHAR(4),
    INDEX crs_id (course_id),
    FOREIGN KEY (course_id) 
		REFERENCES courses(course_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX mod_id (module_leader),
    FOREIGN KEY (module_leader) 
		REFERENCES staff(staff_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
	INDEX dep_id (department),
    FOREIGN KEY (department) 
		REFERENCES departments(department_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	PRIMARY KEY (course_id) 
);

-- Asked Chat GPT to fill in course details based on data in other tables above.
INSERT INTO course_details(course_id, module_leader, department)
VALUES
('9111', '7789', '2478'),
('9151', '7790', '2478'),
('9221', '7793', '2480'),
('9131', '7794', '2480'),
('9141', '7795', '2481'),
('9161', '7797', '2482'),
('9171', '7798', '2482'),
('9181', '7791', '2479'),
('9191', '7792', '2479'),
('9201', '7805', '2486'),
('9211', '7806', '2486'),
('9231', '7801', '2484'),
('9241', '7802', '2484'),
('9251', '7799', '2483'),
('9261', '7800', '2483'),
('9271', '7803', '2485'),
('9281', '7804', '2485'),
('9291', '7807', '2487'),
('9301', '7808', '2487'),
('9311', '7810', '2479'),
('9321', '7811', '2480'),
('9331', '7789', '2478'),
('9341', '7790', '2478'),
('9351', '7795', '2481'),
('9361', '7796', '2481'),
('9371', '7812', '2481'),
('9381', '7813', '2482'),
('9391', '7814', '2483'),
('9401', '7815', '2484'),
('9411', '7816', '2485'),
('9421', '7817', '2486');

-- Create a Student enrolment table.
-- Course ID and student ID are composite primary keys (both foreign keys).
-- Will have 2 triggers to prevent student records being added that shouldn't be.
-- Trigger 1: Can't add row if time being added is after enrolment deadline.
-- Trigger 2: Can’t add row if course is full (past capacity).
CREATE TABLE enrolment(
	course_id CHAR(4),
    student_id CHAR(4),
    INDEX crs_id (course_id),
    FOREIGN KEY (course_id) 
		REFERENCES courses(course_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	INDEX st_id (student_id),
    FOREIGN KEY (student_id) 
		REFERENCES students(student_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY (course_id, student_id )
);

-- Asked CHAT-GPT to enrol each student in a course within their department, starting with example insert.
INSERT INTO enrolment(course_id, student_id)
VALUES
('9111', '4240'),
('9181', '4598'),
('9221', '4594'),
('9141', '4812'),
('9161', '4981'),
('9251', '4623'),
('9231', '4234'),
('9271', '4345'),
('9201', '4267'),
('9291', '4854'),
('9331', '4643'),
('9341', '4901'),
('9321', '4378'),
('9351', '4922'),
('9361', '4955'),
('9371', '4883'),
('9381', '4477'),
('9391', '4419'),
('9401', '4828'),
('9411', '4390'),
('9421', '4735'),
('9151', '4866'),
('9221', '4917'),
('9141', '4508'),
('9161', '4661'),
('9251', '4722'),
('9231', '4766'),
('9271', '4600'),
('9201', '4789'),
('9291', '4532'),
('9331', '4993'),
('9341', '4511'),
('9321', '4512');

-- Trigger to stop rows being added to enrolment when course is full. 
-- First change delimiter so that code doesn't stop prematurely in block. 
DELIMITER $$ 

-- Use 'Before Insert' so that this happens BEFORE row insert happens in enrolment table
CREATE TRIGGER check_capacity BEFORE INSERT ON enrolment 
FOR EACH ROW
BEGIN
	-- Declare variables to add to using queries below.
    DECLARE current_count INT;
    DECLARE capacity_count INT;

    -- Get the current count of the course (add to variable)
    SELECT COUNT(*) INTO current_count
    FROM enrolment
    WHERE course_id = NEW.course_id;

    -- Get the capacity of the course from the courses table (add to variable)
    SELECT capacity INTO capacity_count
    FROM courses
    WHERE course_id = NEW.course_id;

    -- Check if the current_count is greater than or equal to capicity
    IF current_count >= capacity_count THEN
    -- If it is, throw error using SQLSTATE '4500' (which is generate value for user-defined exception)
        SIGNAL SQLSTATE '45000' 
	-- Set message to display to user to explain error.
        SET MESSAGE_TEXT = 'Course capacity reached. Cannot add student record.';
    END IF;
END$$
-- Change delimiter back to normal. 
DELIMITER ;

-- Trigger to stop rows being added to enrolment when enrolment deadline has passed.
-- Change delimiter so that code doesn't stop prematurely in block.
DELIMITER $$ 

-- Use 'Before Insert' so that this happens BEFORE row insert happens in enrolment table
CREATE TRIGGER check_deadline BEFORE INSERT ON enrolment
FOR EACH ROW
BEGIN
	-- Declare variables to add to using queries below. 
    DECLARE deadline DATETIME;

    -- Get the capacity of the course from the courses table
    SELECT enrol_deadline INTO deadline
    FROM courses
    WHERE course_id = NEW.course_id;

    -- Check if the current time is after deadline
    IF  NOW() > deadline THEN
    -- If it does, throw error using SQLSTATE '4500' (which is generate value for user-defined exception)
        SIGNAL SQLSTATE '45000' 
	-- Set message to display to user. 
        SET MESSAGE_TEXT = 'Course enrolment deadline passed. Cannot add student record.';
    END IF;
END$$
-- Change delimiter back to normal. 
DELIMITER ;

-- Add more students into students table.
INSERT INTO students(student_id, first_name, last_name, dob, email_address, department)
VALUES
('4300', 'bronty', 'mckeowne', '1997-12-03', 'bronty.mckeowne@gmail.com', '2478'),
('4301', 'bron', 'delali', '1997-11-03', 'bron.delali@gmail.com', '2478'),
('4302', 'meliaa', 'smith', '1997-03-03', 'meliaa.smith@gmail.com', '2478');

-- Try to add student to course that is already at capacity.
INSERT INTO enrolment(course_id, student_id)
VALUES
('9141', '4300');

-- Add student to course that isn't at capaciy.
INSERT INTO enrolment(course_id, student_id)
VALUES
('9111', '4301');

-- Add student to course where deadline has passed.
INSERT INTO enrolment(course_id, student_id)
VALUES
('9421', '4301');

-- Add student to course where deadline hasn't passed.
INSERT INTO enrolment(course_id, student_id)
VALUES
('9361', '4301');

-- Last task: Philosophy department has shut down, update records.
-- DELETE Philosophy FROM departments table
DELETE FROM departments
WHERE department_name ='Philosophy';

-- Check deletion.
SELECT * 
FROM departments;

-- There are now 9 departments, instead of 10.
SELECT COUNT(department_name)
FROM departments;

-- Check effect on child tables.
SELECT * 
FROM students
ORDER BY first_name;

SELECT * 
FROM department_affiliation
ORDER BY school_id;
