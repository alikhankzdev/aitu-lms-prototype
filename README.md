# AITU LMS — Modernized Prototype & Relational Database (Assignment 3)

**Project:** Redesign and Cloud-Optimized Architecture of AITU LMS (Moodle) Student Portal  
**Course:** Information and Communication Technologies (ICT101) &bull; **Instructor:** Diana Kazbekova  
**Department:** Computer Science & Software Engineering, Astana IT University (2026)  

### Team Members (Group SE-2625):
- **Maratuly Adilkhan (261173)** — Lead Analyst, Presenter (`users`, `audit_logs`, STRIDE Threat Model C1, Privacy C3)
- **Belzhanov Alikhan (261875)** — System & Database Architect (`assignments`, `submissions`, 3NF Normalization A2, Parameterized SQL C2, Backup B3)
- **Khamidolla Sanzhar (260345)** — UI/UX & Frontend Developer (`courses`, `enrollments`, DBMS Comparative Analysis B1, 3-Tier Architecture D2)

---

## 🚀 Key Functional Capabilities (Requirements Met)
- **FR1 (Unified Course Overview):** Clean single-level dashboard showing all 6 active university courses without deep Moodle directory nesting.
- **FR3 (Aggregated Deadlines):** Real-time priority queue sorting impending deliverables chronologically with color-coded urgency countdown badges.
- **FR4 (Omnibox Search):** Real-time filtering across course codes, titles, and task descriptions.
- **FR5 / FR6 (Teacher Task Publishing):** Role-based interface enabling instructors to publish new assignments and live-grade submissions directly into the relational core.
- **FR8 (Local Auto-Save):** Client-side `localStorage` caching preventing submission draft loss during network dropouts.

---

## 🛡️ Security Architecture (Assignment 3 Part C)
1. **Zero SQL Injection Vulnerabilities (Requirement C2):**  
   Every dynamic database interaction strictly utilizes **parameterized prepared statements** (`?` positional parameters). User input is isolated as bound data, never concatenated into raw SQL syntax.
2. **Cryptographic Credential Protection (Requirement C1):**  
   Passwords are never stored in plaintext. Passwords utilize salted SHA-256 cryptographic hashing (`hashlib.sha256(password + salt)`).
3. **Role-Based Access Control (RBAC):**  
   Role separation between `student`, `teacher`, and `admin` enforced server-side.
4. **Audit Trail (Non-Repudiation):**  
   Every critical system event (`USER_LOGIN`, `SUBMIT_ASSIGNMENT`, `GRADE_SUBMISSION`) generates an immutable record in `audit_logs` storing user ID, action, client IP, and UTC timestamp.
5. **Data Minimization (Kazakhstan Law No. 94-V):**  
   Pruned National Identification Numbers (IIN) and personal phone numbers from database schemas.

---

## 💻 Quick Start & Live Demonstration

### 1. Launch Web Portal Prototype:
Double-click `Run_Web_Prototype.bat` or run:
```bash
python web_prototype.py
```
Open **`http://127.0.0.1:8000`** in any web browser.

**Demo Credentials:**
- **Student:** `261875@astanait.edu.kz` / `Alikhan2026!`
- **Teacher:** `diana.kazbekova@astanait.edu.kz` / `DianaPass2026!`
- **Admin:** `admin.lms@astanait.edu.kz` / `RootAdminSecure99#`

### 2. Inspect SQLite Database:
Double-click `Open_Database.bat` to launch **DB Browser for SQLite** pointing to `aitu_lms.sqlite`.

### 3. Verify Disaster Recovery:
```bash
sqlite3 restored.sqlite < backup_aitu_lms.sql
```
Restores the full 3NF database state in under 60 seconds.
