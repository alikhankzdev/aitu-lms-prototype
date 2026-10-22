#!/usr/bin/env python3
# ====================================================================
# AITU LMS Prototype Integration Engine (Part D1)
# Demonstrates live READ and WRITE database operations with security
# Team: Maratuly Adilkhan (261173), Belzhanov Alikhan (261875), Khamidolla Sanzhar (260345)
# Group: SE-2625 | Course: Information and Communication Technologies
# ====================================================================

import sqlite3
import os
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aitu_lms.sqlite')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# --------------------------------------------------------------------
# 1. READ OPERATION: Student Deadline Priority Queue (FR3 & FR1)
# --------------------------------------------------------------------
def read_upcoming_deadlines(student_id_str):
    print("=" * 70)
    print(f"📖 LIVE READ OPERATION: Fetching Deadlines for Student [{student_id_str}]")
    print("=" * 70)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Secure Parameterized Query (prevents SQL Injection - Requirement C2)
    sql = """
        SELECT 
            c.course_code,
            c.course_name,
            a.title,
            a.due_date,
            COALESCE(s.status, 'not_submitted') AS submission_status,
            s.grade
        FROM users u
        JOIN enrollments e ON u.id = e.student_id
        JOIN courses c ON e.course_id = c.id
        JOIN assignments a ON c.id = a.course_id
        LEFT JOIN submissions s ON (a.id = s.assignment_id AND s.student_id = u.id)
        WHERE u.student_id = ?
        ORDER BY a.due_date ASC
        LIMIT 6;
    """
    
    cursor.execute(sql, (student_id_str,))
    rows = cursor.fetchall()
    
    print(f"{'Course':<10} | {'Assignment Title':<35} | {'Due Date':<19} | {'Status':<12}")
    print("-" * 85)
    for r in rows:
        code, cname, title, due, status, grade = r
        grade_str = f"({grade} pts)" if grade is not None else ""
        print(f"{code:<10} | {title[:35]:<35} | {due:<19} | {status:<10} {grade_str}")
        
    conn.close()
    print("-" * 85)
    print(f"✓ READ SUCCESSFUL: Retrieved {len(rows)} active records via parameterized SQL.")

# --------------------------------------------------------------------
# 2. WRITE OPERATION: Secure Assignment Submission (FR8 & C2)
# --------------------------------------------------------------------
def write_assignment_submission(student_id_str, assignment_id, submission_text, file_url):
    print("\n" + "=" * 70)
    print(f"✍️ LIVE WRITE OPERATION: Submitting Assignment #{assignment_id} for [{student_id_str}]")
    print("=" * 70)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Resolve internal user_id
    cursor.execute("SELECT id, full_name FROM users WHERE student_id = ?;", (student_id_str,))
    user = cursor.fetchone()
    if not user:
        print(f"Error: User {student_id_str} not found.")
        conn.close()
        return False
        
    uid, full_name = user
    print(f"Authenticated Student: {full_name} (Internal ID: {uid})")
    
    # 2. Secure Parameterized INSERT or REPLACE
    # Using parameterized query (?) strictly prevents SQL Injection attacks (Requirement C2)
    write_sql = """
        INSERT INTO submissions (assignment_id, student_id, submission_text, file_url, submitted_at, status)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, 'submitted');
    """
    
    cursor.execute(write_sql, (assignment_id, uid, submission_text, file_url))
    new_sub_id = cursor.lastrowid
    
    # 3. Log security audit event in audit_logs table (Requirement C2 Audit Logging)
    log_sql = """
        INSERT INTO audit_logs (user_id, action, ip_address, details)
        VALUES (?, 'SUBMIT_ASSIGNMENT', '192.168.1.105', ?);
    """
    audit_detail = f"Successfully submitted assignment_id={assignment_id}, submission_id={new_sub_id}, file={file_url}"
    cursor.execute(log_sql, (uid, audit_detail))
    
    conn.commit()
    conn.close()
    
    print(f"✓ WRITE SUCCESSFUL: Created submission record #{new_sub_id} with parameterized SQL.")
    print(f"✓ SECURITY AUDIT LOGGED: Created security audit trail for user {uid}.")
    return True

# --------------------------------------------------------------------
# 3. VERIFY OPERATION: Re-read to prove data was persistently stored
# --------------------------------------------------------------------
def verify_persistence(assignment_id, student_id_str):
    print("\n" + "=" * 70)
    print(f"🔍 VERIFICATION: Inspecting Persisted Database Record")
    print("=" * 70)
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = """
        SELECT s.id, u.full_name, a.title, s.submission_text, s.file_url, s.submitted_at, s.status
        FROM submissions s
        JOIN users u ON s.student_id = u.id
        JOIN assignments a ON s.assignment_id = a.id
        WHERE u.student_id = ? AND a.id = ?
        ORDER BY s.id DESC
        LIMIT 1;
    """
    cursor.execute(sql, (student_id_str, assignment_id))
    record = cursor.fetchone()
    if record:
        print(f"Record ID:       {record[0]}")
        print(f"Student:         {record[1]}")
        print(f"Assignment:      {record[2]}")
        print(f"Submitted At:    {record[5]}")
        print(f"Status:          {record[6]}")
        print(f"File URL:        {record[4]}")
        print(f"Content Preview: {record[3][:80]}...")
        print("✓ PERSISTENCE CONFIRMED: Data is permanently saved in SQLite engine.")
    conn.close()

if __name__ == '__main__':
    target_student = "261875"  # Alikhan Belzhanov
    
    # Step 1: Live Read
    read_upcoming_deadlines(target_student)
    
    # Step 2: Live Write
    sample_code = """-- AITU LMS Assignment 3 Solution
-- Team: Maratuly A., Belzhanov A., Khamidolla S.
-- Normalization to 3NF achieved with foreign key constraints.
SELECT * FROM users WHERE role = 'student';"""
    sample_file = "SE2625_Team_ICT_Assignment3.pdf"
    write_assignment_submission(target_student, 4, sample_code, sample_file)
    
    # Step 3: Verification
    verify_persistence(4, target_student)
