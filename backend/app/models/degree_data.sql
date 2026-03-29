INSERT INTO degree_types (id, name) VALUES
(1, 'Bachelors');

INSERT INTO fields (id, name) VALUES
(1, 'Engineering'),
(2, 'Science'),
(3, 'Commerce'),
(4, 'Arts');

INSERT INTO disciplines (id, name, field_id) VALUES

-- Engineering
(1, 'Computer Science', 1),
(2, 'Mechanical Engineering', 1),
(3, 'Electrical Engineering', 1),
(4, 'Civil Engineering', 1),
(5, 'Electronics (EXTC)', 1),

-- Science
(6, 'Physics', 2),
(7, 'Chemistry', 2),
(8, 'Biology', 2),
(9, 'Mathematics', 2),
(10, 'Data Science', 2),

-- Commerce
(11, 'Finance', 3),
(12, 'Accounting', 3),
(13, 'Business Administration', 3),
(14, 'Economics', 3),

-- Arts
(15, 'Psychology', 4),
(16, 'English', 4),
(17, 'Sociology', 4);

INSERT INTO degrees 
(name, type_id, field_id, discipline_id, math_weight, tech_weight, arts_weight, commerce_weight, science_weight)
VALUES

-- 🔹 ENGINEERING
('B.Tech Computer Science', 1, 1, 1, 0.9, 1.0, 0.1, 0.1, 0.8),
('B.Tech Mechanical Engineering', 1, 1, 2, 0.8, 0.7, 0.1, 0.1, 0.9),
('B.Tech Electrical Engineering', 1, 1, 3, 0.85, 0.7, 0.1, 0.1, 0.9),
('B.Tech Civil Engineering', 1, 1, 4, 0.8, 0.6, 0.1, 0.1, 0.85),
('B.Tech Electronics (EXTC)', 1, 1, 5, 0.9, 0.9, 0.1, 0.1, 0.8),

-- 🔹 SCIENCE
('B.Sc Physics', 1, 2, 6, 0.7, 0.4, 0.1, 0.1, 1.0),
('B.Sc Chemistry', 1, 2, 7, 0.6, 0.3, 0.1, 0.1, 1.0),
('B.Sc Biology', 1, 2, 8, 0.4, 0.2, 0.2, 0.1, 1.0),
('B.Sc Mathematics', 1, 2, 9, 1.0, 0.5, 0.1, 0.1, 0.7),
('B.Sc Data Science', 1, 2, 10, 0.9, 0.8, 0.1, 0.2, 0.7),

-- 🔹 COMMERCE
('B.Com Finance', 1, 3, 11, 0.5, 0.2, 0.2, 1.0, 0.2),
('B.Com Accounting', 1, 3, 12, 0.5, 0.2, 0.2, 1.0, 0.2),
('BBA Business Administration', 1, 3, 13, 0.4, 0.3, 0.2, 1.0, 0.2),
('BA Economics', 1, 3, 14, 0.6, 0.3, 0.2, 1.0, 0.3),

-- 🔹 ARTS
('BA Psychology', 1, 4, 15, 0.2, 0.1, 1.0, 0.2, 0.3),
('BA English', 1, 4, 16, 0.1, 0.1, 1.0, 0.1, 0.2),
('BA Sociology', 1, 4, 17, 0.2, 0.1, 1.0, 0.2, 0.3),

-- 🔹 HYBRID / POPULAR
('BCA (Computer Applications)', 1, 1, 1, 0.7, 1.0, 0.1, 0.2, 0.5);