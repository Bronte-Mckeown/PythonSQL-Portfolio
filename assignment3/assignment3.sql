-- This university database contains 7 tables.
CREATE DATABASE university;

USE university;

-- The departments table contains department ID and name.
-- The ID must start with a 2 and be 4 characters.
CREATE TABLE departments(
	department_id CHAR(4) PRIMARY KEY,
    department_name VARCHAR(200) UNIQUE NOT NULL,
    CHECK (department_id LIKE '2%')
);

-- DROP TABLE departments; 

--  Insert departments into table.
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

-- Return all department names, ordered by name
SELECT department_name 
FROM departments
ORDER BY department_name;

-- Return all department names that begin with P
-- ordered by name 
SELECT department_name
FROM departments
WHERE department_name LIKE 'P%'
ORDER BY department_name;

-- Count how many departments there are in table.
SELECT COUNT(department_id) 
AS total_departments 
FROM departments;

-- Create school table 
CREATE TABLE schools(
	school_id CHAR(4) PRIMARY KEY,
    school_name VARCHAR(100) UNIQUE NOT NULL,
    CHECK (school_id LIKE '6%')
);

INSERT INTO schools(school_id, school_name)
VALUES
('6000', 'STEM'),
('6001', 'Social Science'),
('6002', 'Humanities');

-- Create table linking departments to schools 
CREATE TABLE department_affiliation(
	department_name VARCHAR(200) PRIMARY KEY,
    school_name VARCHAR(100),
    INDEX dep_name (department_name),
    FOREIGN KEY (department_name) 
		REFERENCES departments(department_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	INDEX sch_name (school_name),
    FOREIGN KEY (school_name) 
		REFERENCES schools(school_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- DROP TABLE department_affiliation;

INSERT INTO department_affiliation(department_name, school_name)
VALUES
('Psychology', 'Social Science'),
('Sociology', 'Social Science'),
('Biology', 'STEM'),
('Chemistry', 'STEM'),
('Physics', 'STEM'),
('Mathematics', 'STEM'),
('History', 'Humanities'),
('Political Science', 'Social Science'),
('Economics', 'Social Science'),
('Philosophy', 'Humanities');

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

-- DROP TABLE students;

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

-- Check how many students there are overall
SELECT COUNT(student_id) 
AS total_students 
FROM students;

-- Return how many students are in each department
-- Use inner join to return department name
-- This will ignore students with no department
SELECT d.department_name, COUNT(student_id)
AS department_students
FROM students s
INNER JOIN departments d 
ON s.department = d.department_id
GROUP BY d.department_name;

-- Add two students with no department affiliation 
INSERT INTO students(student_id, first_name, last_name, dob, email_address)
VALUES
('4972', 'lucy', 'walmes', '1992-12-01', 'lucy.walmes@gmail.com'),
('4973', 'jack', 'daniels', '1995-11-23', 'jack.daniels@gmail.com');

-- Return how many students are in each department
-- Use LEFT join to return department name
-- This will also count students with no department (null)
SELECT d.department_name, COUNT(student_id)
AS department_students
FROM students s
LEFT JOIN departments d 
ON s.department = d.department_id
GROUP BY d.department_name;

-- Return how many students are in each department within STEM school


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

-- DROP TABLE staff;

-- Again, gave CHAT-GPT the first 2 rows and asked for 27 more
INSERT INTO staff(staff_id, first_name, last_name, dob, email_address, date_joined, department)
VALUES
('7789', 'Tony', 'Morland', '1965-11-02', 'tony.morland@york.ac.uk', '1997-05-04', '2478'),
('7790', 'Emily', 'Brown', '1972-06-14', 'emily.brown@york.ac.uk', '2001-09-12', '2478'),
('7791', 'John', 'Smith', '1980-08-25', 'john.smith@york.ac.uk', '2005-03-15', '2479'),
('7792', 'Jane', 'Doe', '1985-12-17', 'jane.doe@york.ac.uk', '2008-06-20', '2479'),
('7793', 'Michael', 'Johnson', '1978-01-03', 'michael.johnson@york.ac.uk', '2003-07-25', '2480'),
('7794', 'Sarah', 'Taylor', '1983-04-11', 'sarah.taylor@york.ac.uk', '2007-09-30', '2480'),
('7795', 'David', 'Lee', '1975-10-09', 'david.lee@york.ac.uk', '2000-05-22', '2481'),
('7796', 'Laura', 'White', '1981-03-23', 'laura.white@york.ac.uk', '2006-11-17', '2481'),
('7797', 'James', 'Martin', '1969-09-07', 'james.martin@york.ac.uk', '1995-02-10', '2482'),
('7798', 'Karen', 'Anderson', '1974-05-29', 'karen.anderson@york.ac.uk', '1999-08-05', '2482'),
('7799', 'Robert', 'Garcia', '1986-02-19', 'robert.garcia@york.ac.uk', '2010-04-12', '2483'),
('7800', 'Patricia', 'Martinez', '1982-11-30', 'patricia.martinez@york.ac.uk', '2009-06-28', '2483'),
('7801', 'Charles', 'Clark', '1970-07-16', 'charles.clark@york.ac.uk', '1996-01-18', '2484'),
('7802', 'Linda', 'Lewis', '1979-03-05', 'linda.lewis@york.ac.uk', '2002-10-09', '2484'),
('7803', 'Steven', 'Walker', '1981-08-27', 'steven.walker@york.ac.uk', '2006-12-14', '2485'),
('7804', 'Jessica', 'Hall', '1987-05-12', 'jessica.hall@york.ac.uk', '2011-03-21', '2485'),
('7805', 'George', 'Allen', '1968-01-22', 'george.allen@york.ac.uk', '1994-07-16', '2486'),
('7806', 'Nancy', 'Young', '1973-09-13', 'nancy.young@york.ac.uk', '1998-08-24', '2486'),
('7807', 'Brian', 'King', '1976-04-03', 'brian.king@york.ac.uk', '2001-11-13', '2487'),
('7808', 'Sandra', 'Hernandez', '1984-06-21', 'sandra.hernandez@york.ac.uk', '2008-05-08', '2487'),
('7809', 'Donald', 'Hill', '1971-10-14', 'donald.hill@york.ac.uk', '1997-02-11', '2478'),
('7810', 'Lisa', 'Scott', '1980-07-17', 'lisa.scott@york.ac.uk', '2004-05-30', '2479'),
('7811', 'Edward', 'Green', '1966-12-19', 'edward.green@york.ac.uk', '1993-04-03', '2480'),
('7812', 'Barbara', 'Adams', '1974-03-08', 'barbara.adams@york.ac.uk', '1998-09-14', '2481'),
('7813', 'Daniel', 'Nelson', '1977-05-26', 'daniel.nelson@york.ac.uk', '2000-07-22', '2482'),
('7814', 'Susan', 'Baker', '1985-11-04', 'susan.baker@york.ac.uk', '2012-02-28', '2483'),
('7815', 'Kenneth', 'Carter', '1982-06-14', 'kenneth.carter@york.ac.uk', '2009-04-12', '2484'),
('7816', 'Betty', 'Mitchell', '1970-09-19', 'betty.mitchell@york.ac.uk', '1996-03-16', '2485'),
('7817', 'Paul', 'Roberts', '1988-11-22', 'paul.roberts@york.ac.uk', '2014-08-20', '2486');

SELECT COUNT(*) AS total_staff FROM staff;

CREATE TABLE courses(
	course_id CHAR(4) PRIMARY KEY,
    course_name VARCHAR(200) UNIQUE NOT NULL,
    capacity INT DEFAULT 5, 
    enrol_deadline DATETIME DEFAULT '2024-08-01',
    CHECK (course_id LIKE '9%')
);

-- DROP TABLE courses; 

INSERT INTO courses(course_id, course_name, capacity, enrol_deadline)
VALUES
('9111', 'Introduction to Cognitive Neuroscience', 10, '2024-08-01 23:59:59'),
('9151', 'Introduction to Research Methods', 5, '2024-08-01 23:59:59'),
('9221', 'BioTech Applications', 10, '2024-08-01 23:59:59'),
('9131', 'Advanced Data Analysis', 15, '2024-08-01 23:59:59'),
('9141', 'Genetics and Genomics', 12, '2024-08-01 23:59:59'),
('9161', 'Machine Learning', 20, '2024-08-01 23:59:59'),
('9171', 'Artificial Intelligence', 20, '2024-08-01 23:59:59'),
('9181', 'Ethics in Technology', 8, '2024-08-01 23:59:59'),
('9191', 'Introduction to Philosophy', 15, '2024-08-01 23:59:59'),
('9201', 'Modern Political Theory', 10, '2024-08-01 23:59:59'),
('9211', 'Economic Principles', 25, '2024-08-01 23:59:59'),
('9231', 'History of Modern Art', 12, '2024-08-01 23:59:59'),
('9241', 'Environmental Science', 18, '2024-08-01 23:59:59'),
('9251', 'Organic Chemistry', 20, '2024-08-01 23:59:59'),
('9261', 'Quantum Physics', 15, '2024-08-01 23:59:59'),
('9271', 'English Literature through history', 30, '2024-08-01 23:59:59'),
('9281', 'Introduction to Sociology', 25, '2024-08-01 23:59:59'),
('9291', 'Cultural Anthropology', 10, '2024-08-01 23:59:59'),
('9301', 'International Relations', 20, '2024-08-01 23:59:59'),
('9311', 'Fundamentals of Marketing', 22, '2024-08-01 23:59:59'),
('9321', 'Business Management', 25, '2024-08-01 23:59:59'),
('9331', 'Introduction to Psychology', 30, '2024-08-01 23:59:59'),
('9341', 'Educational Psychology', 18, '2024-08-01 23:59:59'),
('9351', 'Developmental Biology', 15, '2024-08-01 23:59:59'),
('9361', 'Public Health', 20, '2024-08-01 23:59:59'),
('9371', 'Human Anatomy', 25, '2024-08-01 23:59:59'),
('9381', 'History of Ancient Civilizations', 12, '2024-07-01 23:59:59'),
('9391', 'Creative Writing', 10, '2024-07-01 23:59:59'),
('9401', 'Introduction to Robotics', 15, '2024-07-01 23:59:59'),
('9411', 'Digital Media and Society', 20, '2024-07-01 23:59:59'),
('9421', 'Neuropsychology', 8, '2024-08-01 23:59:59');

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

-- Asked Chat GPT to fill in course details based on data in other tables above
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

-- Student enrolment
-- Trigger: Can't add row if after enrolment deadline
-- Trigger: Can’t add row if course is full

CREATE TABLE enrolment(
	course_id CHAR(4),
    student_id CHAR(4),
    date_enrolled DATETIME,
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

-- Asked CHAT-GPT to enrol each student in a course within their department, starting with example insert
INSERT INTO enrolment(course_id, student_id, date_enrolled)
VALUES
('9111', '4240', '2024-08-01 23:52:59'),
('9181', '4598', '2024-08-01 23:52:59'),
('9221', '4594', '2024-08-01 23:52:59'),
('9141', '4812', '2024-08-01 23:52:59'),
('9161', '4981', '2024-08-01 23:52:59'),
('9251', '4623', '2024-08-01 23:52:59'),
('9231', '4234', '2024-08-01 23:52:59'),
('9271', '4345', '2024-08-01 23:52:59'),
('9201', '4267', '2024-08-01 23:52:59'),
('9291', '4854', '2024-08-01 23:52:59'),
('9331', '4643', '2024-08-01 23:52:59'),
('9341', '4901', '2024-08-01 23:52:59'),
('9321', '4378', '2024-08-01 23:52:59'),
('9351', '4922', '2024-08-01 23:52:59'),
('9361', '4955', '2024-08-01 23:52:59'),
('9371', '4883', '2024-08-01 23:52:59'),
('9381', '4477', '2024-08-01 23:52:59'),
('9391', '4419', '2024-08-01 23:52:59'),
('9401', '4828', '2024-08-01 23:52:59'),
('9411', '4390', '2024-08-01 23:52:59'),
('9421', '4735', '2024-08-01 23:52:59'),
('9151', '4866', '2024-08-01 23:52:59'),
('9221', '4917', '2024-08-01 23:52:59'),
('9141', '4508', '2024-08-01 23:52:59'),
('9161', '4661', '2024-08-01 23:52:59'),
('9251', '4722', '2024-08-01 23:52:59'),
('9231', '4766', '2024-08-01 23:52:59'),
('9271', '4600', '2024-08-01 23:52:59'),
('9201', '4789', '2024-08-01 23:52:59'),
('9291', '4532', '2024-08-01 23:52:59'),
('9331', '4993', '2024-08-01 23:52:59'),
('9341', '4511', '2024-08-01 23:52:59'),
('9321', '4512', '2024-08-01 23:52:59');

CREATE TABLE grades(
	student_id CHAR(4),
    course_id CHAR(4),
    grade INT,
    INDEX st_id (student_id),
    FOREIGN KEY (student_id)
		REFERENCES students(student_id)
        -- so module leaders can still calculate metrics if student record deleted.
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (course_id) 
		REFERENCES courses(course_id)
        -- keeps student grade even if course is deleted
        -- updates course id 
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    PRIMARY KEY (student_id, course_id)
);
