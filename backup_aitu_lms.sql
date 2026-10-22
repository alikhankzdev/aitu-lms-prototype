BEGIN TRANSACTION;
CREATE TABLE assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    due_date TIMESTAMP NOT NULL,
    max_points DECIMAL(5,2) DEFAULT 100.00 CHECK (max_points > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);
INSERT INTO "assignments" VALUES(1,1,'ICT Assignment 1: Hardware & OS Analysis','Analyze personal PC hardware and operating systems.','2026-09-18 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(2,1,'ICT Assignment 2: HCI & Computer Networks','Evaluate Nielsen usability heuristics and network architecture.','2026-09-27 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(3,1,'ICT Midterm Project Stage 1','Concept, requirements, and architecture of LMS redesign.','2026-10-09 23:00:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(4,1,'ICT Assignment 3: Databases & Security','Implement relational schema and cybersecurity threat model.','2026-10-12 23:00:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(5,1,'ICT Assignment 4: Smart Cloud Services','Cloud integration, data analytics, and mobile optimization.','2026-10-23 23:00:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(6,1,'ICT Endterm Project Stage 2','Final deployed prototype demonstration.','2026-10-25 23:00:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(7,2,'Linear Algebra HW 1: Systems of Linear Equations','David Lay Chapter 1: Row reduction and Gaussian elimination.','2026-09-13 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(8,2,'Linear Algebra HW 2: Vector Equations & Matrix Operations','David Lay Chapter 1.3-1.5 solutions.','2026-09-20 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(9,2,'Linear Algebra HW 3: Matrix Inverses & LU Decomposition','David Lay Chapter 2: Invertibility and factorizations.','2026-09-27 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(10,2,'Linear Algebra HW 4: Vector Subspaces & Linear Independence','David Lay Chapter 2.5-2.8 handwritten solutions.','2026-10-04 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(11,2,'Linear Algebra HW 5: Determinants & Cramer''s Rule','David Lay Chapter 3: Determinant expansions and volume.','2026-10-11 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(12,2,'Linear Algebra Midterm Exam','In-class written exam covering Chapters 1-3.','2026-10-15 15:00:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(13,3,'Programming 1 Assignment 1: Basic C++ Syntax','Arithmetic expressions, conditionals, and I/O streams.','2026-09-14 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(14,3,'Programming 1 Assignment 2: Loops and Nested Logic','24 algorithmic tasks on while, for, and do-while loops.','2026-09-21 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(15,3,'Programming 1 Assignment 3: 1D and 2D Arrays','20 tasks on array traversal, sorting, and matrix transformations.','2026-09-29 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(16,3,'Programming 1 Midterm Coding Exam','Live coding evaluation in Visual Studio on array algorithms.','2026-10-18 10:00:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(17,4,'English B2 Assignment 1: Research Article Analysis','Synthesize findings from a peer-reviewed engineering paper.','2026-09-22 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(18,4,'English B2 Case Study Presentation','Oral defense on platform moderation and digital media.','2026-10-07 00:00:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(19,4,'English B2 Midterm Vocabulary & Grammar','Lesson 4-5 assessment covering relative clauses and formal tone.','2026-10-13 07:47:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(20,5,'Cultural Studies Midterm Presentation: Sufism','Comparative analysis of Central Asian cultural heritage.','2026-09-20 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(21,5,'Cultural Studies Midterm Paper Quiz','In-class written quiz on philosophical traditions.','2026-10-10 23:59:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(22,6,'Calculus 1 Practice 1: Functions and Limits','Evaluation of indeterminate limits and continuous functions.','2026-09-23 15:00:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(23,6,'Calculus 1 Quiz 1: Limit Theorems','In-class test on epsilon-delta definitions and sequence convergence.','2026-09-27 15:00:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(24,6,'Calculus 1 Practice 2: Derivatives and Chain Rule','Differentiation techniques and rate of change.','2026-10-07 13:57:00',100,'2026-10-11 15:05:50');
INSERT INTO "assignments" VALUES(25,6,'Calculus 1 Quiz 2: Applications of Derivatives','Extrema finding, mean value theorem, and optimization.','2026-10-16 14:00:00',100,'2026-10-11 15:05:50');
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action VARCHAR(50) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);
INSERT INTO "audit_logs" VALUES(1,14,'WAF_CHECK_PASSED','192.168.1.159','Input sanitized; no SQL injection tokens detected.','2026-09-15 00:42:00');
INSERT INTO "audit_logs" VALUES(2,21,'BACKUP_CREATED','10.0.4.150','Automated SQLite snapshot exported to secure backup bucket.','2026-09-15 06:04:00');
INSERT INTO "audit_logs" VALUES(3,25,'SUBMIT_ASSIGNMENT','192.168.1.70','File uploaded and saved to draft area.','2026-09-15 12:00:00');
INSERT INTO "audit_logs" VALUES(4,4,'PASSWORD_VERIFIED','192.168.1.217','Bcrypt hash verified successfully.','2026-09-15 18:16:00');
INSERT INTO "audit_logs" VALUES(5,10,'LOGIN_SUCCESS','192.168.1.178','User authenticated via corporate Microsoft OIDC SSO.','2026-09-16 00:36:00');
INSERT INTO "audit_logs" VALUES(6,21,'WAF_CHECK_PASSED','192.168.1.78','Input sanitized; no SQL injection tokens detected.','2026-09-16 06:48:00');
INSERT INTO "audit_logs" VALUES(7,8,'LOGIN_SUCCESS','192.168.1.52','User authenticated via corporate Microsoft OIDC SSO.','2026-09-16 12:49:00');
INSERT INTO "audit_logs" VALUES(8,24,'WAF_CHECK_PASSED','10.0.4.99','Input sanitized; no SQL injection tokens detected.','2026-09-16 18:00:00');
INSERT INTO "audit_logs" VALUES(9,5,'PASSWORD_VERIFIED','192.168.1.209','Bcrypt hash verified successfully.','2026-09-17 00:04:00');
INSERT INTO "audit_logs" VALUES(10,5,'SUBMIT_ASSIGNMENT','192.168.1.198','File uploaded and saved to draft area.','2026-09-17 06:46:00');
INSERT INTO "audit_logs" VALUES(11,18,'LOGIN_SUCCESS','192.168.1.112','User authenticated via corporate Microsoft OIDC SSO.','2026-09-17 12:19:00');
INSERT INTO "audit_logs" VALUES(12,23,'PASSWORD_VERIFIED','192.168.1.66','Bcrypt hash verified successfully.','2026-09-17 18:41:00');
INSERT INTO "audit_logs" VALUES(13,4,'ACCESS_CONTROL_ENFORCED','192.168.1.51','Non-teacher account blocked from administrative endpoint.','2026-09-18 00:13:00');
INSERT INTO "audit_logs" VALUES(14,7,'LOGIN_SUCCESS','192.168.1.37','User authenticated via corporate Microsoft OIDC SSO.','2026-09-18 06:43:00');
INSERT INTO "audit_logs" VALUES(15,9,'SUBMIT_ASSIGNMENT','10.0.4.28','File uploaded and saved to draft area.','2026-09-18 12:39:00');
INSERT INTO "audit_logs" VALUES(16,1,'BACKUP_CREATED','192.168.1.194','Automated SQLite snapshot exported to secure backup bucket.','2026-09-18 18:30:00');
INSERT INTO "audit_logs" VALUES(17,5,'ACCESS_CONTROL_ENFORCED','192.168.1.154','Non-teacher account blocked from administrative endpoint.','2026-09-19 00:03:00');
INSERT INTO "audit_logs" VALUES(18,19,'ACCESS_CONTROL_ENFORCED','192.168.1.235','Non-teacher account blocked from administrative endpoint.','2026-09-19 06:38:00');
INSERT INTO "audit_logs" VALUES(19,4,'ACCESS_CONTROL_ENFORCED','192.168.1.204','Non-teacher account blocked from administrative endpoint.','2026-09-19 12:14:00');
INSERT INTO "audit_logs" VALUES(20,7,'LOGIN_SUCCESS','10.0.4.124','User authenticated via corporate Microsoft OIDC SSO.','2026-09-19 18:23:00');
INSERT INTO "audit_logs" VALUES(21,25,'ACCESS_CONTROL_ENFORCED','192.168.1.111','Non-teacher account blocked from administrative endpoint.','2026-09-20 00:38:00');
INSERT INTO "audit_logs" VALUES(22,23,'ACCESS_CONTROL_ENFORCED','192.168.1.23','Non-teacher account blocked from administrative endpoint.','2026-09-20 06:27:00');
INSERT INTO "audit_logs" VALUES(23,24,'LOGIN_SUCCESS','10.0.4.10','User authenticated via corporate Microsoft OIDC SSO.','2026-09-20 12:15:00');
INSERT INTO "audit_logs" VALUES(24,11,'LOGIN_SUCCESS','192.168.1.31','User authenticated via corporate Microsoft OIDC SSO.','2026-09-20 18:47:00');
INSERT INTO "audit_logs" VALUES(25,11,'ACCESS_CONTROL_ENFORCED','192.168.1.196','Non-teacher account blocked from administrative endpoint.','2026-09-21 00:19:00');
INSERT INTO "audit_logs" VALUES(26,8,'WAF_CHECK_PASSED','192.168.1.166','Input sanitized; no SQL injection tokens detected.','2026-09-21 06:40:00');
INSERT INTO "audit_logs" VALUES(27,2,'LOGIN_SUCCESS','10.0.4.111','User authenticated via corporate Microsoft OIDC SSO.','2026-09-21 12:23:00');
INSERT INTO "audit_logs" VALUES(28,12,'BACKUP_CREATED','192.168.1.125','Automated SQLite snapshot exported to secure backup bucket.','2026-09-21 18:56:00');
INSERT INTO "audit_logs" VALUES(29,12,'ACCESS_CONTROL_ENFORCED','192.168.1.94','Non-teacher account blocked from administrative endpoint.','2026-09-22 00:22:00');
INSERT INTO "audit_logs" VALUES(30,1,'SUBMIT_ASSIGNMENT','192.168.1.169','File uploaded and saved to draft area.','2026-09-22 06:35:00');
INSERT INTO "audit_logs" VALUES(31,5,'PASSWORD_VERIFIED','10.0.4.133','Bcrypt hash verified successfully.','2026-09-22 12:08:00');
INSERT INTO "audit_logs" VALUES(32,9,'LOGIN_SUCCESS','10.0.4.173','User authenticated via corporate Microsoft OIDC SSO.','2026-09-22 18:11:00');
INSERT INTO "audit_logs" VALUES(33,11,'ACCESS_CONTROL_ENFORCED','192.168.1.151','Non-teacher account blocked from administrative endpoint.','2026-09-23 00:42:00');
INSERT INTO "audit_logs" VALUES(34,9,'SUBMIT_ASSIGNMENT','192.168.1.208','File uploaded and saved to draft area.','2026-09-23 06:36:00');
INSERT INTO "audit_logs" VALUES(35,7,'LOGIN_SUCCESS','10.0.4.21','User authenticated via corporate Microsoft OIDC SSO.','2026-09-23 12:19:00');
INSERT INTO "audit_logs" VALUES(36,19,'LOGIN_SUCCESS','10.0.4.7','User authenticated via corporate Microsoft OIDC SSO.','2026-09-23 18:38:00');
INSERT INTO "audit_logs" VALUES(37,23,'SUBMIT_ASSIGNMENT','192.168.1.93','File uploaded and saved to draft area.','2026-09-24 00:07:00');
INSERT INTO "audit_logs" VALUES(38,3,'BACKUP_CREATED','192.168.1.87','Automated SQLite snapshot exported to secure backup bucket.','2026-09-24 06:31:00');
INSERT INTO "audit_logs" VALUES(39,1,'LOGIN_SUCCESS','192.168.1.29','User authenticated via corporate Microsoft OIDC SSO.','2026-09-24 12:36:00');
INSERT INTO "audit_logs" VALUES(40,13,'BACKUP_CREATED','10.0.4.223','Automated SQLite snapshot exported to secure backup bucket.','2026-09-24 18:15:00');
INSERT INTO "audit_logs" VALUES(41,4,'BACKUP_CREATED','192.168.1.122','Automated SQLite snapshot exported to secure backup bucket.','2026-09-25 00:26:00');
INSERT INTO "audit_logs" VALUES(42,17,'BACKUP_CREATED','192.168.1.41','Automated SQLite snapshot exported to secure backup bucket.','2026-09-25 06:52:00');
INSERT INTO "audit_logs" VALUES(43,22,'SUBMIT_ASSIGNMENT','192.168.1.135','File uploaded and saved to draft area.','2026-09-25 12:14:00');
INSERT INTO "audit_logs" VALUES(44,15,'SUBMIT_ASSIGNMENT','192.168.1.107','File uploaded and saved to draft area.','2026-09-25 18:33:00');
INSERT INTO "audit_logs" VALUES(45,16,'LOGIN_SUCCESS','192.168.1.183','User authenticated via corporate Microsoft OIDC SSO.','2026-09-26 00:44:00');
INSERT INTO "audit_logs" VALUES(46,10,'BACKUP_CREATED','10.0.4.234','Automated SQLite snapshot exported to secure backup bucket.','2026-09-26 06:33:00');
INSERT INTO "audit_logs" VALUES(47,11,'LOGIN_SUCCESS','192.168.1.128','User authenticated via corporate Microsoft OIDC SSO.','2026-09-26 12:17:00');
INSERT INTO "audit_logs" VALUES(48,10,'WAF_CHECK_PASSED','192.168.1.67','Input sanitized; no SQL injection tokens detected.','2026-09-26 18:13:00');
INSERT INTO "audit_logs" VALUES(49,3,'BACKUP_CREATED','192.168.1.40','Automated SQLite snapshot exported to secure backup bucket.','2026-09-27 00:34:00');
INSERT INTO "audit_logs" VALUES(50,23,'LOGIN_SUCCESS','10.0.4.69','User authenticated via corporate Microsoft OIDC SSO.','2026-09-27 06:17:00');
INSERT INTO "audit_logs" VALUES(51,23,'WAF_CHECK_PASSED','10.0.4.222','Input sanitized; no SQL injection tokens detected.','2026-09-27 12:00:00');
INSERT INTO "audit_logs" VALUES(52,20,'BACKUP_CREATED','192.168.1.106','Automated SQLite snapshot exported to secure backup bucket.','2026-09-27 18:04:00');
INSERT INTO "audit_logs" VALUES(53,15,'ACCESS_CONTROL_ENFORCED','10.0.4.117','Non-teacher account blocked from administrative endpoint.','2026-09-28 00:31:00');
INSERT INTO "audit_logs" VALUES(54,5,'SUBMIT_ASSIGNMENT','192.168.1.186','File uploaded and saved to draft area.','2026-09-28 06:26:00');
INSERT INTO "audit_logs" VALUES(55,17,'PASSWORD_VERIFIED','192.168.1.132','Bcrypt hash verified successfully.','2026-09-28 12:07:00');
INSERT INTO "audit_logs" VALUES(56,14,'PASSWORD_VERIFIED','192.168.1.185','Bcrypt hash verified successfully.','2026-09-28 18:50:00');
INSERT INTO "audit_logs" VALUES(57,16,'ACCESS_CONTROL_ENFORCED','192.168.1.75','Non-teacher account blocked from administrative endpoint.','2026-09-29 00:16:00');
INSERT INTO "audit_logs" VALUES(58,25,'PASSWORD_VERIFIED','10.0.4.81','Bcrypt hash verified successfully.','2026-09-29 06:06:00');
INSERT INTO "audit_logs" VALUES(59,10,'ACCESS_CONTROL_ENFORCED','192.168.1.99','Non-teacher account blocked from administrative endpoint.','2026-09-29 12:17:00');
INSERT INTO "audit_logs" VALUES(60,16,'BACKUP_CREATED','192.168.1.231','Automated SQLite snapshot exported to secure backup bucket.','2026-09-29 18:32:00');
INSERT INTO "audit_logs" VALUES(61,9,'PASSWORD_VERIFIED','192.168.1.41','Bcrypt hash verified successfully.','2026-09-30 00:58:00');
INSERT INTO "audit_logs" VALUES(62,24,'WAF_CHECK_PASSED','10.0.4.110','Input sanitized; no SQL injection tokens detected.','2026-09-30 06:30:00');
INSERT INTO "audit_logs" VALUES(63,8,'SUBMIT_ASSIGNMENT','192.168.1.165','File uploaded and saved to draft area.','2026-09-30 12:59:00');
INSERT INTO "audit_logs" VALUES(64,18,'BACKUP_CREATED','192.168.1.190','Automated SQLite snapshot exported to secure backup bucket.','2026-09-30 18:25:00');
INSERT INTO "audit_logs" VALUES(65,25,'SUBMIT_ASSIGNMENT','192.168.1.31','File uploaded and saved to draft area.','2026-10-01 00:41:00');
INSERT INTO "audit_logs" VALUES(66,18,'SUBMIT_ASSIGNMENT','192.168.1.37','File uploaded and saved to draft area.','2026-10-01 06:10:00');
INSERT INTO "audit_logs" VALUES(67,16,'SUBMIT_ASSIGNMENT','192.168.1.195','File uploaded and saved to draft area.','2026-10-01 12:38:00');
INSERT INTO "audit_logs" VALUES(68,11,'ACCESS_CONTROL_ENFORCED','10.0.4.58','Non-teacher account blocked from administrative endpoint.','2026-10-01 18:13:00');
INSERT INTO "audit_logs" VALUES(69,11,'SUBMIT_ASSIGNMENT','10.0.4.25','File uploaded and saved to draft area.','2026-10-02 00:13:00');
INSERT INTO "audit_logs" VALUES(70,20,'LOGIN_SUCCESS','192.168.1.34','User authenticated via corporate Microsoft OIDC SSO.','2026-10-02 06:39:00');
INSERT INTO "audit_logs" VALUES(71,4,'BACKUP_CREATED','192.168.1.161','Automated SQLite snapshot exported to secure backup bucket.','2026-10-02 12:23:00');
INSERT INTO "audit_logs" VALUES(72,16,'SUBMIT_ASSIGNMENT','10.0.4.163','File uploaded and saved to draft area.','2026-10-02 18:14:00');
INSERT INTO "audit_logs" VALUES(73,2,'ACCESS_CONTROL_ENFORCED','192.168.1.193','Non-teacher account blocked from administrative endpoint.','2026-10-03 00:12:00');
INSERT INTO "audit_logs" VALUES(74,13,'WAF_CHECK_PASSED','192.168.1.107','Input sanitized; no SQL injection tokens detected.','2026-10-03 06:46:00');
INSERT INTO "audit_logs" VALUES(75,5,'BACKUP_CREATED','192.168.1.166','Automated SQLite snapshot exported to secure backup bucket.','2026-10-03 12:20:00');
INSERT INTO "audit_logs" VALUES(76,18,'ACCESS_CONTROL_ENFORCED','192.168.1.131','Non-teacher account blocked from administrative endpoint.','2026-10-03 18:24:00');
INSERT INTO "audit_logs" VALUES(77,3,'PASSWORD_VERIFIED','192.168.1.214','Bcrypt hash verified successfully.','2026-10-04 00:35:00');
INSERT INTO "audit_logs" VALUES(78,17,'SUBMIT_ASSIGNMENT','10.0.4.183','File uploaded and saved to draft area.','2026-10-04 06:44:00');
INSERT INTO "audit_logs" VALUES(79,8,'SUBMIT_ASSIGNMENT','192.168.1.164','File uploaded and saved to draft area.','2026-10-04 12:27:00');
INSERT INTO "audit_logs" VALUES(80,6,'WAF_CHECK_PASSED','10.0.4.134','Input sanitized; no SQL injection tokens detected.','2026-10-04 18:24:00');
INSERT INTO "audit_logs" VALUES(81,17,'LOGIN_SUCCESS','192.168.1.19','User authenticated via corporate Microsoft OIDC SSO.','2026-10-05 00:23:00');
INSERT INTO "audit_logs" VALUES(82,2,'ACCESS_CONTROL_ENFORCED','10.0.4.236','Non-teacher account blocked from administrative endpoint.','2026-10-05 06:47:00');
INSERT INTO "audit_logs" VALUES(83,18,'WAF_CHECK_PASSED','192.168.1.73','Input sanitized; no SQL injection tokens detected.','2026-10-05 12:11:00');
INSERT INTO "audit_logs" VALUES(84,24,'BACKUP_CREATED','192.168.1.122','Automated SQLite snapshot exported to secure backup bucket.','2026-10-05 18:48:00');
INSERT INTO "audit_logs" VALUES(85,17,'SUBMIT_ASSIGNMENT','192.168.1.220','File uploaded and saved to draft area.','2026-10-06 00:47:00');
INSERT INTO "audit_logs" VALUES(86,17,'WAF_CHECK_PASSED','192.168.1.240','Input sanitized; no SQL injection tokens detected.','2026-10-06 06:45:00');
INSERT INTO "audit_logs" VALUES(87,25,'SUBMIT_ASSIGNMENT','192.168.1.28','File uploaded and saved to draft area.','2026-10-06 12:35:00');
INSERT INTO "audit_logs" VALUES(88,4,'BACKUP_CREATED','192.168.1.113','Automated SQLite snapshot exported to secure backup bucket.','2026-10-06 18:39:00');
INSERT INTO "audit_logs" VALUES(89,22,'SUBMIT_ASSIGNMENT','192.168.1.183','File uploaded and saved to draft area.','2026-10-07 00:02:00');
INSERT INTO "audit_logs" VALUES(90,6,'PASSWORD_VERIFIED','192.168.1.198','Bcrypt hash verified successfully.','2026-10-07 06:00:00');
INSERT INTO "audit_logs" VALUES(91,23,'SUBMIT_ASSIGNMENT','10.0.4.26','File uploaded and saved to draft area.','2026-10-07 12:25:00');
INSERT INTO "audit_logs" VALUES(92,16,'SUBMIT_ASSIGNMENT','192.168.1.227','File uploaded and saved to draft area.','2026-10-07 18:09:00');
INSERT INTO "audit_logs" VALUES(93,15,'LOGIN_SUCCESS','192.168.1.191','User authenticated via corporate Microsoft OIDC SSO.','2026-10-08 00:00:00');
INSERT INTO "audit_logs" VALUES(94,17,'LOGIN_SUCCESS','192.168.1.110','User authenticated via corporate Microsoft OIDC SSO.','2026-10-08 06:19:00');
INSERT INTO "audit_logs" VALUES(95,12,'SUBMIT_ASSIGNMENT','10.0.4.117','File uploaded and saved to draft area.','2026-10-08 12:20:00');
INSERT INTO "audit_logs" VALUES(96,13,'ACCESS_CONTROL_ENFORCED','192.168.1.221','Non-teacher account blocked from administrative endpoint.','2026-10-08 18:47:00');
INSERT INTO "audit_logs" VALUES(97,22,'SUBMIT_ASSIGNMENT','192.168.1.56','File uploaded and saved to draft area.','2026-10-09 00:15:00');
INSERT INTO "audit_logs" VALUES(98,15,'PASSWORD_VERIFIED','192.168.1.215','Bcrypt hash verified successfully.','2026-10-09 06:53:00');
INSERT INTO "audit_logs" VALUES(99,1,'BACKUP_CREATED','10.0.4.221','Automated SQLite snapshot exported to secure backup bucket.','2026-10-09 12:24:00');
INSERT INTO "audit_logs" VALUES(100,9,'BACKUP_CREATED','10.0.4.79','Automated SQLite snapshot exported to secure backup bucket.','2026-10-09 18:16:00');
INSERT INTO "audit_logs" VALUES(101,23,'LOGIN_SUCCESS','192.168.1.194','User authenticated via corporate Microsoft OIDC SSO.','2026-10-10 00:27:00');
INSERT INTO "audit_logs" VALUES(102,19,'WAF_CHECK_PASSED','192.168.1.72','Input sanitized; no SQL injection tokens detected.','2026-10-10 06:09:00');
INSERT INTO "audit_logs" VALUES(103,23,'WAF_CHECK_PASSED','192.168.1.36','Input sanitized; no SQL injection tokens detected.','2026-10-10 12:08:00');
INSERT INTO "audit_logs" VALUES(104,18,'LOGIN_SUCCESS','192.168.1.210','User authenticated via corporate Microsoft OIDC SSO.','2026-10-10 18:06:00');
INSERT INTO "audit_logs" VALUES(105,12,'ACCESS_CONTROL_ENFORCED','192.168.1.34','Non-teacher account blocked from administrative endpoint.','2026-10-11 00:38:00');
INSERT INTO "audit_logs" VALUES(106,1,'ACCESS_CONTROL_ENFORCED','10.0.4.46','Non-teacher account blocked from administrative endpoint.','2026-10-11 06:10:00');
INSERT INTO "audit_logs" VALUES(107,18,'ACCESS_CONTROL_ENFORCED','10.0.4.237','Non-teacher account blocked from administrative endpoint.','2026-10-11 12:49:00');
INSERT INTO "audit_logs" VALUES(108,16,'LOGIN_SUCCESS','192.168.1.221','User authenticated via corporate Microsoft OIDC SSO.','2026-10-11 18:07:00');
INSERT INTO "audit_logs" VALUES(109,13,'LOGIN_SUCCESS','192.168.1.195','User authenticated via corporate Microsoft OIDC SSO.','2026-10-12 00:39:00');
INSERT INTO "audit_logs" VALUES(110,10,'WAF_CHECK_PASSED','10.0.4.203','Input sanitized; no SQL injection tokens detected.','2026-10-12 06:05:00');
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    instructor_id INTEGER NOT NULL,
    credits INTEGER NOT NULL CHECK (credits BETWEEN 1 AND 10),
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE RESTRICT
);
INSERT INTO "courses" VALUES(1,'ICT101','Information and Communication Technologies',1,4);
INSERT INTO "courses" VALUES(2,'MATH101','Linear Algebra and Analytic Geometry',2,5);
INSERT INTO "courses" VALUES(3,'CS101','Introduction to Programming 1 (C++)',3,5);
INSERT INTO "courses" VALUES(4,'ENG101','Foreign Language 1 (Academic English B2)',4,3);
INSERT INTO "courses" VALUES(5,'CULT002','Cultural Studies',5,2);
INSERT INTO "courses" VALUES(6,'CALC101','Calculus 1 (Differential Calculus)',6,5);
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE (student_id, course_id)
);
INSERT INTO "enrollments" VALUES(1,8,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(2,8,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(3,8,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(4,8,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(5,8,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(6,8,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(7,9,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(8,9,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(9,9,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(10,9,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(11,9,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(12,9,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(13,10,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(14,10,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(15,10,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(16,10,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(17,10,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(18,10,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(19,11,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(20,11,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(21,11,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(22,11,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(23,11,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(24,11,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(25,12,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(26,12,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(27,12,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(28,12,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(29,12,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(30,12,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(31,13,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(32,13,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(33,13,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(34,13,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(35,13,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(36,13,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(37,14,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(38,14,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(39,14,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(40,14,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(41,14,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(42,14,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(43,15,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(44,15,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(45,15,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(46,15,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(47,15,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(48,15,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(49,16,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(50,16,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(51,16,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(52,16,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(53,16,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(54,16,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(55,17,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(56,17,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(57,17,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(58,17,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(59,17,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(60,17,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(61,18,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(62,18,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(63,18,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(64,18,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(65,18,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(66,18,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(67,19,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(68,19,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(69,19,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(70,19,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(71,19,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(72,19,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(73,20,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(74,20,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(75,20,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(76,20,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(77,20,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(78,20,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(79,21,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(80,21,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(81,21,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(82,21,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(83,21,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(84,21,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(85,22,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(86,22,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(87,22,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(88,22,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(89,22,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(90,22,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(91,23,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(92,23,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(93,23,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(94,23,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(95,23,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(96,23,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(97,24,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(98,24,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(99,24,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(100,24,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(101,24,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(102,24,6,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(103,25,1,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(104,25,2,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(105,25,3,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(106,25,4,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(107,25,5,'2026-10-11 15:05:50');
INSERT INTO "enrollments" VALUES(108,25,6,'2026-10-11 15:05:50');
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    submission_text TEXT,
    file_url VARCHAR(255),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) DEFAULT 'submitted' CHECK (status IN ('draft', 'submitted', 'graded')),
    grade DECIMAL(5,2) CHECK (grade >= 0.0 AND grade <= 100.0),
    feedback TEXT,
    FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
);
INSERT INTO "submissions" VALUES(1,1,8,'// Student ID: 261875 Submission for ICT Assignment 1: Hardware & OS Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_1_std_8.pdf','2026-09-18 09:59:00','graded',70,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(2,1,9,'// Student ID: 261173 Submission for ICT Assignment 1: Hardware & OS Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_1_std_9.pdf','2026-09-16 10:59:00','graded',80.8,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(3,1,10,'// Student ID: 260345 Submission for ICT Assignment 1: Hardware & OS Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_1_std_10.pdf','2026-09-16 05:59:00','graded',71.6,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(4,1,11,'// Student ID: 261001 Submission for ICT Assignment 1: Hardware & OS Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_1_std_11.pdf','2026-09-17 13:59:00','graded',75.8,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(5,1,12,'// Student ID: 261002 Submission for ICT Assignment 1: Hardware & OS Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_1_std_12.pdf','2026-09-16 08:59:00','graded',68,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(6,1,13,'// Student ID: 261003 Submission for ICT Assignment 1: Hardware & OS Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_1_std_13.pdf','2026-09-16 13:59:00','graded',80.3,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(7,1,14,'// Student ID: 261004 Submission for ICT Assignment 1: Hardware & OS Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_1_std_14.pdf','2026-09-17 20:59:00','graded',69.7,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(8,1,15,'// Student ID: 261005 Submission for ICT Assignment 1: Hardware & OS Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_1_std_15.pdf','2026-09-17 20:59:00','graded',88.8,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(9,2,8,'// Student ID: 261875 Submission for ICT Assignment 2: HCI & Computer Networks
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_2_std_8.pdf','2026-09-25 15:59:00','graded',65,'Report is great, live console demonstration had issues.');
INSERT INTO "submissions" VALUES(10,2,9,'// Student ID: 261173 Submission for ICT Assignment 2: HCI & Computer Networks
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_2_std_9.pdf','2026-09-26 08:59:00','graded',86.2,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(11,2,10,'// Student ID: 260345 Submission for ICT Assignment 2: HCI & Computer Networks
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_2_std_10.pdf','2026-09-27 18:59:00','graded',74.7,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(12,2,11,'// Student ID: 261001 Submission for ICT Assignment 2: HCI & Computer Networks
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_2_std_11.pdf','2026-09-27 12:59:00','graded',67.5,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(13,2,12,'// Student ID: 261002 Submission for ICT Assignment 2: HCI & Computer Networks
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_2_std_12.pdf','2026-09-26 20:59:00','graded',76.6,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(14,2,13,'// Student ID: 261003 Submission for ICT Assignment 2: HCI & Computer Networks
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_2_std_13.pdf','2026-09-25 20:59:00','graded',76.5,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(15,2,14,'// Student ID: 261004 Submission for ICT Assignment 2: HCI & Computer Networks
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_2_std_14.pdf','2026-09-25 08:59:00','graded',92.5,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(16,2,15,'// Student ID: 261005 Submission for ICT Assignment 2: HCI & Computer Networks
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_2_std_15.pdf','2026-09-26 15:59:00','graded',91.9,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(17,3,8,'// Student ID: 261875 Submission for ICT Midterm Project Stage 1
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_3_std_8.pdf','2026-10-07 16:00:00','graded',95,'Comprehensive 12-page report and clean architecture.');
INSERT INTO "submissions" VALUES(18,3,9,'// Student ID: 261173 Submission for ICT Midterm Project Stage 1
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_3_std_9.pdf','2026-10-09 13:00:00','graded',85,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(19,3,10,'// Student ID: 260345 Submission for ICT Midterm Project Stage 1
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_3_std_10.pdf','2026-10-08 10:00:00','graded',80.9,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(20,3,11,'// Student ID: 261001 Submission for ICT Midterm Project Stage 1
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_3_std_11.pdf','2026-10-09 03:00:00','graded',85.2,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(21,3,12,'// Student ID: 261002 Submission for ICT Midterm Project Stage 1
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_3_std_12.pdf','2026-10-07 22:00:00','graded',77.7,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(22,3,13,'// Student ID: 261003 Submission for ICT Midterm Project Stage 1
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_3_std_13.pdf','2026-10-08 02:00:00','graded',70.7,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(23,3,14,'// Student ID: 261004 Submission for ICT Midterm Project Stage 1
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_3_std_14.pdf','2026-10-08 19:00:00','graded',72.8,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(24,3,15,'// Student ID: 261005 Submission for ICT Midterm Project Stage 1
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_3_std_15.pdf','2026-10-08 05:00:00','graded',94.8,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(25,4,8,'// Student ID: 261875 Submission for ICT Assignment 3: Databases & Security
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_4_std_8.pdf','2026-10-10 08:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(26,4,9,'// Student ID: 261173 Submission for ICT Assignment 3: Databases & Security
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_4_std_9.pdf','2026-10-10 02:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(27,4,10,'// Student ID: 260345 Submission for ICT Assignment 3: Databases & Security
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_4_std_10.pdf','2026-10-11 16:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(28,4,11,'// Student ID: 261001 Submission for ICT Assignment 3: Databases & Security
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_4_std_11.pdf','2026-10-09 23:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(29,4,12,'// Student ID: 261002 Submission for ICT Assignment 3: Databases & Security
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_4_std_12.pdf','2026-10-12 04:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(30,4,13,'// Student ID: 261003 Submission for ICT Assignment 3: Databases & Security
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_4_std_13.pdf','2026-10-11 09:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(31,4,14,'// Student ID: 261004 Submission for ICT Assignment 3: Databases & Security
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_4_std_14.pdf','2026-10-12 04:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(32,4,15,'// Student ID: 261005 Submission for ICT Assignment 3: Databases & Security
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_4_std_15.pdf','2026-10-10 03:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(33,5,8,'// Student ID: 261875 Submission for ICT Assignment 4: Smart Cloud Services
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_5_std_8.pdf','2026-10-23 19:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(34,5,9,'// Student ID: 261173 Submission for ICT Assignment 4: Smart Cloud Services
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_5_std_9.pdf','2026-10-21 05:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(35,5,10,'// Student ID: 260345 Submission for ICT Assignment 4: Smart Cloud Services
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_5_std_10.pdf','2026-10-22 16:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(36,5,11,'// Student ID: 261001 Submission for ICT Assignment 4: Smart Cloud Services
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_5_std_11.pdf','2026-10-21 21:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(37,5,12,'// Student ID: 261002 Submission for ICT Assignment 4: Smart Cloud Services
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_5_std_12.pdf','2026-10-22 04:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(38,5,13,'// Student ID: 261003 Submission for ICT Assignment 4: Smart Cloud Services
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_5_std_13.pdf','2026-10-21 21:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(39,5,14,'// Student ID: 261004 Submission for ICT Assignment 4: Smart Cloud Services
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_5_std_14.pdf','2026-10-22 13:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(40,5,15,'// Student ID: 261005 Submission for ICT Assignment 4: Smart Cloud Services
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_5_std_15.pdf','2026-10-22 03:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(41,6,8,'// Student ID: 261875 Submission for ICT Endterm Project Stage 2
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_6_std_8.pdf','2026-10-24 03:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(42,6,9,'// Student ID: 261173 Submission for ICT Endterm Project Stage 2
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_6_std_9.pdf','2026-10-23 23:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(43,6,10,'// Student ID: 260345 Submission for ICT Endterm Project Stage 2
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_6_std_10.pdf','2026-10-25 10:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(44,6,11,'// Student ID: 261001 Submission for ICT Endterm Project Stage 2
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_6_std_11.pdf','2026-10-25 06:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(45,6,12,'// Student ID: 261002 Submission for ICT Endterm Project Stage 2
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_6_std_12.pdf','2026-10-24 00:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(46,6,13,'// Student ID: 261003 Submission for ICT Endterm Project Stage 2
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_6_std_13.pdf','2026-10-24 07:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(47,6,14,'// Student ID: 261004 Submission for ICT Endterm Project Stage 2
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_6_std_14.pdf','2026-10-25 15:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(48,6,15,'// Student ID: 261005 Submission for ICT Endterm Project Stage 2
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_1/assign_6_std_15.pdf','2026-10-24 18:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(49,7,8,'// Student ID: 261875 Submission for Linear Algebra HW 1: Systems of Linear Equations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_7_std_8.pdf','2026-09-12 19:59:00','graded',100,'Handwritten homework verified in 5mm notebook.');
INSERT INTO "submissions" VALUES(50,7,9,'// Student ID: 261173 Submission for Linear Algebra HW 1: Systems of Linear Equations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_7_std_9.pdf','2026-09-12 23:59:00','graded',82.2,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(51,7,10,'// Student ID: 260345 Submission for Linear Algebra HW 1: Systems of Linear Equations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_7_std_10.pdf','2026-09-11 09:59:00','graded',72.2,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(52,7,11,'// Student ID: 261001 Submission for Linear Algebra HW 1: Systems of Linear Equations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_7_std_11.pdf','2026-09-11 06:59:00','graded',76.5,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(53,7,12,'// Student ID: 261002 Submission for Linear Algebra HW 1: Systems of Linear Equations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_7_std_12.pdf','2026-09-11 20:59:00','graded',86.6,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(54,7,13,'// Student ID: 261003 Submission for Linear Algebra HW 1: Systems of Linear Equations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_7_std_13.pdf','2026-09-11 07:59:00','graded',75.1,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(55,7,14,'// Student ID: 261004 Submission for Linear Algebra HW 1: Systems of Linear Equations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_7_std_14.pdf','2026-09-11 19:59:00','graded',85.2,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(56,7,15,'// Student ID: 261005 Submission for Linear Algebra HW 1: Systems of Linear Equations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_7_std_15.pdf','2026-09-12 23:59:00','graded',88.6,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(57,8,8,'// Student ID: 261875 Submission for Linear Algebra HW 2: Vector Equations & Matrix Operations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_8_std_8.pdf','2026-09-19 08:59:00','graded',100,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(58,8,9,'// Student ID: 261173 Submission for Linear Algebra HW 2: Vector Equations & Matrix Operations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_8_std_9.pdf','2026-09-20 04:59:00','graded',71.4,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(59,8,10,'// Student ID: 260345 Submission for Linear Algebra HW 2: Vector Equations & Matrix Operations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_8_std_10.pdf','2026-09-20 03:59:00','graded',80.8,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(60,8,11,'// Student ID: 261001 Submission for Linear Algebra HW 2: Vector Equations & Matrix Operations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_8_std_11.pdf','2026-09-18 23:59:00','graded',95,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(61,8,12,'// Student ID: 261002 Submission for Linear Algebra HW 2: Vector Equations & Matrix Operations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_8_std_12.pdf','2026-09-19 19:59:00','graded',92,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(62,8,13,'// Student ID: 261003 Submission for Linear Algebra HW 2: Vector Equations & Matrix Operations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_8_std_13.pdf','2026-09-18 15:59:00','graded',83.2,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(63,8,14,'// Student ID: 261004 Submission for Linear Algebra HW 2: Vector Equations & Matrix Operations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_8_std_14.pdf','2026-09-18 00:59:00','graded',89.4,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(64,8,15,'// Student ID: 261005 Submission for Linear Algebra HW 2: Vector Equations & Matrix Operations
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_8_std_15.pdf','2026-09-19 23:59:00','graded',87,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(65,9,8,'// Student ID: 261875 Submission for Linear Algebra HW 3: Matrix Inverses & LU Decomposition
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_9_std_8.pdf','2026-09-27 17:59:00','graded',100,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(66,9,9,'// Student ID: 261173 Submission for Linear Algebra HW 3: Matrix Inverses & LU Decomposition
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_9_std_9.pdf','2026-09-24 23:59:00','graded',67.9,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(67,9,10,'// Student ID: 260345 Submission for Linear Algebra HW 3: Matrix Inverses & LU Decomposition
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_9_std_10.pdf','2026-09-25 05:59:00','graded',73.7,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(68,9,11,'// Student ID: 261001 Submission for Linear Algebra HW 3: Matrix Inverses & LU Decomposition
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_9_std_11.pdf','2026-09-27 10:59:00','graded',85.6,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(69,9,12,'// Student ID: 261002 Submission for Linear Algebra HW 3: Matrix Inverses & LU Decomposition
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_9_std_12.pdf','2026-09-27 15:59:00','graded',67.7,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(70,9,13,'// Student ID: 261003 Submission for Linear Algebra HW 3: Matrix Inverses & LU Decomposition
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_9_std_13.pdf','2026-09-27 01:59:00','graded',90.3,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(71,9,14,'// Student ID: 261004 Submission for Linear Algebra HW 3: Matrix Inverses & LU Decomposition
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_9_std_14.pdf','2026-09-27 07:59:00','graded',68.5,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(72,9,15,'// Student ID: 261005 Submission for Linear Algebra HW 3: Matrix Inverses & LU Decomposition
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_9_std_15.pdf','2026-09-27 09:59:00','graded',92.9,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(73,10,8,'// Student ID: 261875 Submission for Linear Algebra HW 4: Vector Subspaces & Linear Independence
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_10_std_8.pdf','2026-10-04 05:59:00','graded',100,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(74,10,9,'// Student ID: 261173 Submission for Linear Algebra HW 4: Vector Subspaces & Linear Independence
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_10_std_9.pdf','2026-10-04 14:59:00','graded',77,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(75,10,10,'// Student ID: 260345 Submission for Linear Algebra HW 4: Vector Subspaces & Linear Independence
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_10_std_10.pdf','2026-10-04 12:59:00','graded',84.2,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(76,10,11,'// Student ID: 261001 Submission for Linear Algebra HW 4: Vector Subspaces & Linear Independence
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_10_std_11.pdf','2026-10-02 22:59:00','graded',78.2,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(77,10,12,'// Student ID: 261002 Submission for Linear Algebra HW 4: Vector Subspaces & Linear Independence
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_10_std_12.pdf','2026-10-04 04:59:00','graded',91.2,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(78,10,13,'// Student ID: 261003 Submission for Linear Algebra HW 4: Vector Subspaces & Linear Independence
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_10_std_13.pdf','2026-10-04 14:59:00','graded',79.6,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(79,10,14,'// Student ID: 261004 Submission for Linear Algebra HW 4: Vector Subspaces & Linear Independence
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_10_std_14.pdf','2026-10-04 14:59:00','graded',89.7,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(80,10,15,'// Student ID: 261005 Submission for Linear Algebra HW 4: Vector Subspaces & Linear Independence
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_10_std_15.pdf','2026-10-02 17:59:00','graded',66.4,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(81,11,8,'// Student ID: 261875 Submission for Linear Algebra HW 5: Determinants & Cramer''s Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_11_std_8.pdf','2026-10-09 02:59:00','graded',100,'Submitted 4h early with authentic handwriting.');
INSERT INTO "submissions" VALUES(82,11,9,'// Student ID: 261173 Submission for Linear Algebra HW 5: Determinants & Cramer''s Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_11_std_9.pdf','2026-10-10 12:59:00','graded',81,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(83,11,10,'// Student ID: 260345 Submission for Linear Algebra HW 5: Determinants & Cramer''s Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_11_std_10.pdf','2026-10-10 00:59:00','graded',82.2,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(84,11,11,'// Student ID: 261001 Submission for Linear Algebra HW 5: Determinants & Cramer''s Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_11_std_11.pdf','2026-10-10 04:59:00','graded',83.2,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(85,11,12,'// Student ID: 261002 Submission for Linear Algebra HW 5: Determinants & Cramer''s Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_11_std_12.pdf','2026-10-10 03:59:00','graded',65.6,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(86,11,13,'// Student ID: 261003 Submission for Linear Algebra HW 5: Determinants & Cramer''s Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_11_std_13.pdf','2026-10-11 00:59:00','graded',82.1,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(87,11,14,'// Student ID: 261004 Submission for Linear Algebra HW 5: Determinants & Cramer''s Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_11_std_14.pdf','2026-10-09 03:59:00','graded',66.5,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(88,11,15,'// Student ID: 261005 Submission for Linear Algebra HW 5: Determinants & Cramer''s Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_11_std_15.pdf','2026-10-08 23:59:00','graded',79.6,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(89,12,8,'// Student ID: 261875 Submission for Linear Algebra Midterm Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_12_std_8.pdf','2026-10-15 08:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(90,12,9,'// Student ID: 261173 Submission for Linear Algebra Midterm Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_12_std_9.pdf','2026-10-13 23:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(91,12,10,'// Student ID: 260345 Submission for Linear Algebra Midterm Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_12_std_10.pdf','2026-10-15 10:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(92,12,11,'// Student ID: 261001 Submission for Linear Algebra Midterm Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_12_std_11.pdf','2026-10-14 07:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(93,12,12,'// Student ID: 261002 Submission for Linear Algebra Midterm Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_12_std_12.pdf','2026-10-13 01:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(94,12,13,'// Student ID: 261003 Submission for Linear Algebra Midterm Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_12_std_13.pdf','2026-10-13 22:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(95,12,14,'// Student ID: 261004 Submission for Linear Algebra Midterm Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_12_std_14.pdf','2026-10-12 15:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(96,12,15,'// Student ID: 261005 Submission for Linear Algebra Midterm Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_2/assign_12_std_15.pdf','2026-10-15 10:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(97,13,8,'// Student ID: 261875 Submission for Programming 1 Assignment 1: Basic C++ Syntax
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_13_std_8.pdf','2026-09-13 05:59:00','graded',80,'need write #include');
INSERT INTO "submissions" VALUES(98,13,9,'// Student ID: 261173 Submission for Programming 1 Assignment 1: Basic C++ Syntax
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_13_std_9.pdf','2026-09-13 15:59:00','graded',78.1,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(99,13,10,'// Student ID: 260345 Submission for Programming 1 Assignment 1: Basic C++ Syntax
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_13_std_10.pdf','2026-09-12 15:59:00','graded',78.1,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(100,13,11,'// Student ID: 261001 Submission for Programming 1 Assignment 1: Basic C++ Syntax
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_13_std_11.pdf','2026-09-14 11:59:00','graded',75.9,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(101,13,12,'// Student ID: 261002 Submission for Programming 1 Assignment 1: Basic C++ Syntax
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_13_std_12.pdf','2026-09-13 15:59:00','graded',88.4,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(102,13,13,'// Student ID: 261003 Submission for Programming 1 Assignment 1: Basic C++ Syntax
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_13_std_13.pdf','2026-09-12 08:59:00','graded',79,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(103,13,14,'// Student ID: 261004 Submission for Programming 1 Assignment 1: Basic C++ Syntax
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_13_std_14.pdf','2026-09-13 02:59:00','graded',66.1,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(104,13,15,'// Student ID: 261005 Submission for Programming 1 Assignment 1: Basic C++ Syntax
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_13_std_15.pdf','2026-09-12 10:59:00','graded',93.3,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(105,14,8,'// Student ID: 261875 Submission for Programming 1 Assignment 2: Loops and Nested Logic
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_14_std_8.pdf','2026-09-20 12:59:00','graded',90,'100');
INSERT INTO "submissions" VALUES(106,14,9,'// Student ID: 261173 Submission for Programming 1 Assignment 2: Loops and Nested Logic
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_14_std_9.pdf','2026-09-20 00:59:00','graded',74.4,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(107,14,10,'// Student ID: 260345 Submission for Programming 1 Assignment 2: Loops and Nested Logic
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_14_std_10.pdf','2026-09-21 06:59:00','graded',92.8,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(108,14,11,'// Student ID: 261001 Submission for Programming 1 Assignment 2: Loops and Nested Logic
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_14_std_11.pdf','2026-09-19 05:59:00','graded',80.6,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(109,14,12,'// Student ID: 261002 Submission for Programming 1 Assignment 2: Loops and Nested Logic
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_14_std_12.pdf','2026-09-19 15:59:00','graded',82.7,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(110,14,13,'// Student ID: 261003 Submission for Programming 1 Assignment 2: Loops and Nested Logic
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_14_std_13.pdf','2026-09-21 15:59:00','graded',85.6,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(111,14,14,'// Student ID: 261004 Submission for Programming 1 Assignment 2: Loops and Nested Logic
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_14_std_14.pdf','2026-09-20 22:59:00','graded',92.1,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(112,14,15,'// Student ID: 261005 Submission for Programming 1 Assignment 2: Loops and Nested Logic
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_14_std_15.pdf','2026-09-19 06:59:00','graded',75.3,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(113,15,8,'// Student ID: 261875 Submission for Programming 1 Assignment 3: 1D and 2D Arrays
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_15_std_8.pdf','2026-09-28 04:59:00','graded',100,'100');
INSERT INTO "submissions" VALUES(114,15,9,'// Student ID: 261173 Submission for Programming 1 Assignment 3: 1D and 2D Arrays
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_15_std_9.pdf','2026-09-28 23:59:00','graded',86.7,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(115,15,10,'// Student ID: 260345 Submission for Programming 1 Assignment 3: 1D and 2D Arrays
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_15_std_10.pdf','2026-09-27 14:59:00','graded',72.2,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(116,15,11,'// Student ID: 261001 Submission for Programming 1 Assignment 3: 1D and 2D Arrays
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_15_std_11.pdf','2026-09-27 22:59:00','graded',73.2,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(117,15,12,'// Student ID: 261002 Submission for Programming 1 Assignment 3: 1D and 2D Arrays
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_15_std_12.pdf','2026-09-28 11:59:00','graded',83.9,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(118,15,13,'// Student ID: 261003 Submission for Programming 1 Assignment 3: 1D and 2D Arrays
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_15_std_13.pdf','2026-09-28 11:59:00','graded',92.8,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(119,15,14,'// Student ID: 261004 Submission for Programming 1 Assignment 3: 1D and 2D Arrays
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_15_std_14.pdf','2026-09-27 15:59:00','graded',81.3,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(120,15,15,'// Student ID: 261005 Submission for Programming 1 Assignment 3: 1D and 2D Arrays
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_15_std_15.pdf','2026-09-27 08:59:00','graded',89.1,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(121,16,8,'// Student ID: 261875 Submission for Programming 1 Midterm Coding Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_16_std_8.pdf','2026-10-17 16:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(122,16,9,'// Student ID: 261173 Submission for Programming 1 Midterm Coding Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_16_std_9.pdf','2026-10-17 14:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(123,16,10,'// Student ID: 260345 Submission for Programming 1 Midterm Coding Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_16_std_10.pdf','2026-10-16 10:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(124,16,11,'// Student ID: 261001 Submission for Programming 1 Midterm Coding Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_16_std_11.pdf','2026-10-15 16:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(125,16,12,'// Student ID: 261002 Submission for Programming 1 Midterm Coding Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_16_std_12.pdf','2026-10-16 07:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(126,16,13,'// Student ID: 261003 Submission for Programming 1 Midterm Coding Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_16_std_13.pdf','2026-10-17 11:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(127,16,14,'// Student ID: 261004 Submission for Programming 1 Midterm Coding Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_16_std_14.pdf','2026-10-17 18:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(128,16,15,'// Student ID: 261005 Submission for Programming 1 Midterm Coding Exam
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_3/assign_16_std_15.pdf','2026-10-16 07:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(129,17,8,'// Student ID: 261875 Submission for English B2 Assignment 1: Research Article Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_17_std_8.pdf','2026-09-22 16:59:00','graded',80,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(130,17,9,'// Student ID: 261173 Submission for English B2 Assignment 1: Research Article Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_17_std_9.pdf','2026-09-21 18:59:00','graded',76.3,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(131,17,10,'// Student ID: 260345 Submission for English B2 Assignment 1: Research Article Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_17_std_10.pdf','2026-09-20 08:59:00','graded',87.8,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(132,17,11,'// Student ID: 261001 Submission for English B2 Assignment 1: Research Article Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_17_std_11.pdf','2026-09-21 04:59:00','graded',89,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(133,17,12,'// Student ID: 261002 Submission for English B2 Assignment 1: Research Article Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_17_std_12.pdf','2026-09-20 23:59:00','graded',75.5,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(134,17,13,'// Student ID: 261003 Submission for English B2 Assignment 1: Research Article Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_17_std_13.pdf','2026-09-22 09:59:00','graded',75.8,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(135,17,14,'// Student ID: 261004 Submission for English B2 Assignment 1: Research Article Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_17_std_14.pdf','2026-09-20 00:59:00','graded',83.5,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(136,17,15,'// Student ID: 261005 Submission for English B2 Assignment 1: Research Article Analysis
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_17_std_15.pdf','2026-09-20 01:59:00','graded',75.5,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(137,18,8,'// Student ID: 261875 Submission for English B2 Case Study Presentation
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_18_std_8.pdf','2026-10-04 00:00:00','graded',78,'Good presentation.');
INSERT INTO "submissions" VALUES(138,18,9,'// Student ID: 261173 Submission for English B2 Case Study Presentation
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_18_std_9.pdf','2026-10-05 06:00:00','graded',78.5,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(139,18,10,'// Student ID: 260345 Submission for English B2 Case Study Presentation
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_18_std_10.pdf','2026-10-04 05:00:00','graded',72.9,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(140,18,11,'// Student ID: 261001 Submission for English B2 Case Study Presentation
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_18_std_11.pdf','2026-10-04 14:00:00','graded',72.5,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(141,18,12,'// Student ID: 261002 Submission for English B2 Case Study Presentation
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_18_std_12.pdf','2026-10-05 18:00:00','graded',86.4,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(142,18,13,'// Student ID: 261003 Submission for English B2 Case Study Presentation
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_18_std_13.pdf','2026-10-06 14:00:00','graded',68.6,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(143,18,14,'// Student ID: 261004 Submission for English B2 Case Study Presentation
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_18_std_14.pdf','2026-10-04 10:00:00','graded',84.1,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(144,18,15,'// Student ID: 261005 Submission for English B2 Case Study Presentation
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_18_std_15.pdf','2026-10-06 14:00:00','graded',93.6,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(145,19,8,'// Student ID: 261875 Submission for English B2 Midterm Vocabulary & Grammar
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_19_std_8.pdf','2026-10-11 20:47:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(146,19,9,'// Student ID: 261173 Submission for English B2 Midterm Vocabulary & Grammar
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_19_std_9.pdf','2026-10-12 12:47:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(147,19,10,'// Student ID: 260345 Submission for English B2 Midterm Vocabulary & Grammar
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_19_std_10.pdf','2026-10-12 09:47:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(148,19,11,'// Student ID: 261001 Submission for English B2 Midterm Vocabulary & Grammar
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_19_std_11.pdf','2026-10-10 21:47:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(149,19,12,'// Student ID: 261002 Submission for English B2 Midterm Vocabulary & Grammar
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_19_std_12.pdf','2026-10-10 19:47:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(150,19,13,'// Student ID: 261003 Submission for English B2 Midterm Vocabulary & Grammar
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_19_std_13.pdf','2026-10-13 01:47:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(151,19,14,'// Student ID: 261004 Submission for English B2 Midterm Vocabulary & Grammar
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_19_std_14.pdf','2026-10-10 19:47:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(152,19,15,'// Student ID: 261005 Submission for English B2 Midterm Vocabulary & Grammar
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_4/assign_19_std_15.pdf','2026-10-10 18:47:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(153,20,8,'// Student ID: 261875 Submission for Cultural Studies Midterm Presentation: Sufism
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_20_std_8.pdf','2026-09-18 01:59:00','graded',89,'Well-structured Sufism presentation.');
INSERT INTO "submissions" VALUES(154,20,9,'// Student ID: 261173 Submission for Cultural Studies Midterm Presentation: Sufism
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_20_std_9.pdf','2026-09-18 10:59:00','graded',66,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(155,20,10,'// Student ID: 260345 Submission for Cultural Studies Midterm Presentation: Sufism
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_20_std_10.pdf','2026-09-20 08:59:00','graded',67.7,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(156,20,11,'// Student ID: 261001 Submission for Cultural Studies Midterm Presentation: Sufism
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_20_std_11.pdf','2026-09-19 21:59:00','graded',65.6,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(157,20,12,'// Student ID: 261002 Submission for Cultural Studies Midterm Presentation: Sufism
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_20_std_12.pdf','2026-09-19 13:59:00','graded',84.5,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(158,20,13,'// Student ID: 261003 Submission for Cultural Studies Midterm Presentation: Sufism
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_20_std_13.pdf','2026-09-20 02:59:00','graded',86.7,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(159,20,14,'// Student ID: 261004 Submission for Cultural Studies Midterm Presentation: Sufism
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_20_std_14.pdf','2026-09-18 05:59:00','graded',76.5,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(160,20,15,'// Student ID: 261005 Submission for Cultural Studies Midterm Presentation: Sufism
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_20_std_15.pdf','2026-09-18 09:59:00','graded',75.8,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(161,21,8,'// Student ID: 261875 Submission for Cultural Studies Midterm Paper Quiz
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_21_std_8.pdf','2026-10-09 01:59:00','graded',85,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(162,21,9,'// Student ID: 261173 Submission for Cultural Studies Midterm Paper Quiz
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_21_std_9.pdf','2026-10-09 01:59:00','graded',93.3,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(163,21,10,'// Student ID: 260345 Submission for Cultural Studies Midterm Paper Quiz
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_21_std_10.pdf','2026-10-09 03:59:00','graded',73.8,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(164,21,11,'// Student ID: 261001 Submission for Cultural Studies Midterm Paper Quiz
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_21_std_11.pdf','2026-10-09 08:59:00','graded',75.2,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(165,21,12,'// Student ID: 261002 Submission for Cultural Studies Midterm Paper Quiz
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_21_std_12.pdf','2026-10-10 04:59:00','graded',90.6,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(166,21,13,'// Student ID: 261003 Submission for Cultural Studies Midterm Paper Quiz
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_21_std_13.pdf','2026-10-08 19:59:00','graded',91.7,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(167,21,14,'// Student ID: 261004 Submission for Cultural Studies Midterm Paper Quiz
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_21_std_14.pdf','2026-10-08 21:59:00','graded',71.8,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(168,21,15,'// Student ID: 261005 Submission for Cultural Studies Midterm Paper Quiz
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_5/assign_21_std_15.pdf','2026-10-09 09:59:00','graded',84.5,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(169,22,8,'// Student ID: 261875 Submission for Calculus 1 Practice 1: Functions and Limits
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_22_std_8.pdf','2026-09-22 07:00:00','graded',60,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(170,22,9,'// Student ID: 261173 Submission for Calculus 1 Practice 1: Functions and Limits
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_22_std_9.pdf','2026-09-23 03:00:00','graded',79.7,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(171,22,10,'// Student ID: 260345 Submission for Calculus 1 Practice 1: Functions and Limits
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_22_std_10.pdf','2026-09-23 05:00:00','graded',77.9,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(172,22,11,'// Student ID: 261001 Submission for Calculus 1 Practice 1: Functions and Limits
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_22_std_11.pdf','2026-09-23 08:00:00','graded',85.5,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(173,22,12,'// Student ID: 261002 Submission for Calculus 1 Practice 1: Functions and Limits
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_22_std_12.pdf','2026-09-22 04:00:00','graded',72.3,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(174,22,13,'// Student ID: 261003 Submission for Calculus 1 Practice 1: Functions and Limits
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_22_std_13.pdf','2026-09-21 20:00:00','graded',83.9,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(175,22,14,'// Student ID: 261004 Submission for Calculus 1 Practice 1: Functions and Limits
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_22_std_14.pdf','2026-09-21 13:00:00','graded',71.6,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(176,22,15,'// Student ID: 261005 Submission for Calculus 1 Practice 1: Functions and Limits
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_22_std_15.pdf','2026-09-22 16:00:00','graded',73.4,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(177,23,8,'// Student ID: 261875 Submission for Calculus 1 Quiz 1: Limit Theorems
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_23_std_8.pdf','2026-09-27 09:00:00','graded',30,'Paper test score.');
INSERT INTO "submissions" VALUES(178,23,9,'// Student ID: 261173 Submission for Calculus 1 Quiz 1: Limit Theorems
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_23_std_9.pdf','2026-09-27 07:00:00','graded',77,'Very well done. All test cases passed with optimal complexity.');
INSERT INTO "submissions" VALUES(179,23,10,'// Student ID: 260345 Submission for Calculus 1 Quiz 1: Limit Theorems
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_23_std_10.pdf','2026-09-25 05:00:00','graded',78,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(180,23,11,'// Student ID: 261001 Submission for Calculus 1 Quiz 1: Limit Theorems
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_23_std_11.pdf','2026-09-27 00:00:00','graded',87.2,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(181,23,12,'// Student ID: 261002 Submission for Calculus 1 Quiz 1: Limit Theorems
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_23_std_12.pdf','2026-09-24 20:00:00','graded',71,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(182,23,13,'// Student ID: 261003 Submission for Calculus 1 Quiz 1: Limit Theorems
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_23_std_13.pdf','2026-09-25 22:00:00','graded',82.7,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(183,23,14,'// Student ID: 261004 Submission for Calculus 1 Quiz 1: Limit Theorems
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_23_std_14.pdf','2026-09-25 10:00:00','graded',77.6,'Well-structured report. Comprehensive analysis of the problem statement.');
INSERT INTO "submissions" VALUES(184,23,15,'// Student ID: 261005 Submission for Calculus 1 Quiz 1: Limit Theorems
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_23_std_15.pdf','2026-09-27 01:00:00','graded',87.2,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(185,24,8,'// Student ID: 261875 Submission for Calculus 1 Practice 2: Derivatives and Chain Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_24_std_8.pdf','2026-10-06 17:57:00','graded',65,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(186,24,9,'// Student ID: 261173 Submission for Calculus 1 Practice 2: Derivatives and Chain Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_24_std_9.pdf','2026-10-06 16:57:00','graded',89.6,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(187,24,10,'// Student ID: 260345 Submission for Calculus 1 Practice 2: Derivatives and Chain Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_24_std_10.pdf','2026-10-04 21:57:00','graded',74.2,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(188,24,11,'// Student ID: 261001 Submission for Calculus 1 Practice 2: Derivatives and Chain Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_24_std_11.pdf','2026-10-06 12:57:00','graded',74.8,'Solid mathematical reasoning. Accurate use of cofactor expansion.');
INSERT INTO "submissions" VALUES(189,24,12,'// Student ID: 261002 Submission for Calculus 1 Practice 2: Derivatives and Chain Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_24_std_12.pdf','2026-10-06 12:57:00','graded',86.7,'Good code structure. Please ensure header files are properly included.');
INSERT INTO "submissions" VALUES(190,24,13,'// Student ID: 261003 Submission for Calculus 1 Practice 2: Derivatives and Chain Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_24_std_13.pdf','2026-10-04 21:57:00','graded',76.5,'Excellent work! Accurate derivations and clean formatting.');
INSERT INTO "submissions" VALUES(191,24,14,'// Student ID: 261004 Submission for Calculus 1 Practice 2: Derivatives and Chain Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_24_std_14.pdf','2026-10-06 09:57:00','graded',69.5,'Great presentation and oral defense. Met all rubric requirements.');
INSERT INTO "submissions" VALUES(192,24,15,'// Student ID: 261005 Submission for Calculus 1 Practice 2: Derivatives and Chain Rule
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_24_std_15.pdf','2026-10-04 23:57:00','graded',81.5,'Good submission. Minor issues with formatting but calculations are correct.');
INSERT INTO "submissions" VALUES(193,25,8,'// Student ID: 261875 Submission for Calculus 1 Quiz 2: Applications of Derivatives
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_25_std_8.pdf','2026-10-14 04:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(194,25,9,'// Student ID: 261173 Submission for Calculus 1 Quiz 2: Applications of Derivatives
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_25_std_9.pdf','2026-10-14 06:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(195,25,10,'// Student ID: 260345 Submission for Calculus 1 Quiz 2: Applications of Derivatives
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_25_std_10.pdf','2026-10-15 00:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(196,25,11,'// Student ID: 261001 Submission for Calculus 1 Quiz 2: Applications of Derivatives
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_25_std_11.pdf','2026-10-13 22:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(197,25,12,'// Student ID: 261002 Submission for Calculus 1 Quiz 2: Applications of Derivatives
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_25_std_12.pdf','2026-10-15 12:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(198,25,13,'// Student ID: 261003 Submission for Calculus 1 Quiz 2: Applications of Derivatives
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_25_std_13.pdf','2026-10-15 15:00:00','submitted',NULL,NULL);
INSERT INTO "submissions" VALUES(199,25,14,'// Student ID: 261004 Submission for Calculus 1 Quiz 2: Applications of Derivatives
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_25_std_14.pdf','2026-10-14 20:00:00','draft',NULL,NULL);
INSERT INTO "submissions" VALUES(200,25,15,'// Student ID: 261005 Submission for Calculus 1 Quiz 2: Applications of Derivatives
// Completed all required parts according to syllabus instructions.','/uploads/2026/course_6/assign_25_std_15.pdf','2026-10-15 05:00:00','draft',NULL,NULL);
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id VARCHAR(10) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL CHECK (email LIKE '%@astanait.edu.kz'),
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO "users" VALUES(1,'T001','diana.kazbekova@astanait.edu.kz','caba5029f017b9b2174dbbdc207f8b0c34d0d3e4fce0e883c72a1b396ca73a7e','Diana Kazbekova','teacher','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(2,'T002','anara.mukhamedina@astanait.edu.kz','f9fea0f820987ded5c9dbc880246ac138c916094befc6efb21e41ba9a5b52924','Anara Mukhamedina','teacher','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(3,'T003','nurtas.nadirov@astanait.edu.kz','8b8800160cb677d749c5a75a533d81be1ddb3edd91c3b082f6772892c8404333','Nurtas Nadirov','teacher','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(4,'T004','aidyn.aldaberdikyzy@astanait.edu.kz','6e856885423562f48da97c36d8219ca7a167dadb3fa1dc959d4f802873a05196','Aidyn Aldaberdikyzy','teacher','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(5,'T005','gaukhar.alzhanova@astanait.edu.kz','f33c529f37873a912d8ad97f643277c798ce44cbae9811aba82c29edaef8d2a6','Gaukhar Alzhanova','teacher','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(6,'T006','aidana.azhikhan@astanait.edu.kz','5481661cdb96cb59d162d196785535026732f41d09250a2db76e8fa930e0a808','Aidana Azhikhan','teacher','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(7,'ADM1','admin.lms@astanait.edu.kz','c0629e849d311bd83ea57bf407f2917cb46778cf5ad0ec39e09e9bec7943e407','System Administrator','admin','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(8,'261875','261875@astanait.edu.kz','589bb33d3ce536e5561cdadb25be9a78cd20cb8090603deceb0ba48679ba4929','Belzhanov Alikhan','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(9,'261173','261173@astanait.edu.kz','766818d2747e92aea52dc8d59bd868730fcb483951e9cb4f01fb172eff36a5eb','Maratuly Adilkhan','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(10,'260345','260345@astanait.edu.kz','d4d220997a986b9f9280e4d203fc23e8ae582708eb4f2ec66fe5ab81a5c50f78','Khamidolla Sanzhar','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(11,'261001','261001@astanait.edu.kz','359f15b5a9d9cb1b50f8cfdbb0b4a3acbe5f735ff97ed4d297681528eca68208','Sovetov Muslim','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(12,'261002','261002@astanait.edu.kz','0e0a34c5e938bf9301d8d56ac4eee45910e7765048c06ee701c6e6291801c7de','Toleubaykyzy Aruzhan','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(13,'261003','261003@astanait.edu.kz','be303297e28a4265bc6877890be83bca2c8edbd79aaae960f83c985cfd7322e3','Orynbasar Aruzhan','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(14,'261004','261004@astanait.edu.kz','3ec5684e8961e9f6a74df4f87896e057142fabeccc990e2b58c11a18160b18c3','Kassymov Daniyal','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(15,'261005','261005@astanait.edu.kz','6c5376affbed7179379cb52a19518fc6bbf700b41446e1a598d6af8d5918e7c4','Zhaksylyk Dias','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(16,'261006','261006@astanait.edu.kz','23b3c325cbd44a5b3a481e0b75ec7d2a455382fe94245c48c923693c9522c9a0','Serikbayeva Madina','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(17,'261007','261007@astanait.edu.kz','de7bcd9f30fcbdef5098be9d2dfaec168be684c45fecc85d1b0f25b429ba4a3d','Bolatuly Arman','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(18,'261008','261008@astanait.edu.kz','b88503be224d6e047b89977f06a56592dc2f4adfe634f4217b52bcc10f9a4363','Nurgaliyev Timur','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(19,'261009','261009@astanait.edu.kz','8967d2414097f8e8bd6b08c2f496363a156369b887064af2a6ba728530fee2f5','Abisheva Kamila','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(20,'261010','261010@astanait.edu.kz','5600e252387881b054a95db85dcde7645a7e552d34338f8d2bfd4f94ccfad919','Bazarbayev Sultan','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(21,'261011','261011@astanait.edu.kz','e0c6abc434f947e7a4c801cae20b6e4da855d71ed204c5b6417b1e0e06f6826e','Rakhimzhanov Bekzat','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(22,'261012','261012@astanait.edu.kz','a5e05ce81a15ae78832f7a855547e59d099cd3b079e7e590c9af3215af3101fc','Utegenova Aida','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(23,'261013','261013@astanait.edu.kz','eae5c9fa7e9e0aa86ee4352e871ac9e902a0ca0cfaaf52a792fc70adf07130a8','Zhumabay Rustem','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(24,'261014','261014@astanait.edu.kz','b6aa85d58988a51a15c94ef7400ce4e0cdf6891640c4c1b56be1a05682736637','Altynbekova Dilnaz','student','2026-10-11 15:05:50');
INSERT INTO "users" VALUES(25,'261015','261015@astanait.edu.kz','31c83236f097e0d048efd73526ec1f7c7c958c14cfc7aa4a0fbdc037ea1feb74','Kenzhebayev Mansur','student','2026-10-11 15:05:50');
CREATE INDEX idx_assignments_due ON assignments(due_date);
CREATE INDEX idx_submissions_lookup ON submissions(assignment_id, student_id);
CREATE INDEX idx_enrollments_student ON enrollments(student_id);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('users',25);
INSERT INTO "sqlite_sequence" VALUES('courses',6);
INSERT INTO "sqlite_sequence" VALUES('enrollments',108);
INSERT INTO "sqlite_sequence" VALUES('assignments',25);
INSERT INTO "sqlite_sequence" VALUES('submissions',200);
INSERT INTO "sqlite_sequence" VALUES('audit_logs',110);
COMMIT;
