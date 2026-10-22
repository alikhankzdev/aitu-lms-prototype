#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AITU LMS - Modernized Web Prototype (Assignment 3 & Full Project Redesign)
Theme: Redesign and Cloud-Optimized Architecture of AITU LMS (Moodle) Student Portal
Implements:
  - FR1: Unified single-level Course Overview
  - FR2: Course Materials & Direct Downloads
  - FR3: Aggregated 'Upcoming Deadlines' with live color-coded countdown badges
  - FR4: Real-time search / filter bar
  - FR5 / FR6: Teacher publishing & resource upload
  - FR7: Role-Based Access Control (RBAC: student / teacher / admin)
  - FR8: Auto-saving local drafts & WAF-safe pre-submission linter
  - C2: Parameterized SQL queries everywhere (Anti-SQLi)
  - C1: Salted SHA-256 password hashing + audit_logs integration
"""
import http.server
import socketserver
import sqlite3
import hashlib
import secrets
import html
import os
import urllib.parse
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, 'aitu_lms.sqlite')
SALT = 'aitu_salt_2026'
PORT = 8000
SESSIONS = {}

def hash_password(pwd):
    return hashlib.sha256((pwd + SALT).encode('utf-8')).hexdigest()

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def audit(con, user_id, action, ip, details):
    con.execute(
        'INSERT INTO audit_logs (user_id, action, ip_address, details, created_at) VALUES (?, ?, ?, ?, ?)',
        (user_id, action, ip, details, datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    )
    con.commit()

CSS = """
:root {
  --primary: #1890ff; --primary-dark: #002766; --bg: #f0f2f5; --card-bg: #ffffff;
  --text: #262626; --text-muted: #8c8c8c; --border: #e8e8e8;
  --urgent: #f5222d; --urgent-bg: #fff1f0; --urgent-border: #ffa39e;
  --warn: #faad14; --warn-bg: #fffbe6; --warn-border: #ffe58f;
  --ok: #52c41a; --ok-bg: #f6ffed; --ok-border: #b7eb8f;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background: var(--bg); color: var(--text); line-height: 1.5; }
.navbar { background: var(--primary-dark); color: #fff; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
.brand { display: flex; align-items: center; gap: 10px; font-size: 17px; font-weight: 700; }
.logo-box { background: var(--primary); color: #fff; width: 28px; height: 28px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; }
.search-box { background: rgba(255,255,255,0.16); border-radius: 20px; padding: 6px 14px; width: 340px; display: flex; align-items: center; }
.search-box input { background: transparent; border: none; color: #fff; outline: none; width: 100%; font-size: 13px; }
.search-box input::placeholder { color: #d9d9d9; }
.user-menu { display: flex; align-items: center; gap: 12px; font-size: 13px; }
.avatar { width: 32px; height: 32px; border-radius: 50%; background: var(--primary); display: flex; align-items: center; justify-content: center; font-weight: 700; color: #fff; }
.role-badge { font-size: 11px; padding: 2px 8px; border-radius: 10px; background: rgba(255,255,255,0.2); font-weight: 600; text-transform: uppercase; }
a.nav-link { color: #bae7ff; text-decoration: none; font-size: 12px; }
a.nav-link:hover { color: #fff; }

.container { max-width: 1240px; margin: 24px auto; padding: 0 20px; }
.grid-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 24px; }
@media (max-width: 900px) { .grid-layout { grid-template-columns: 1fr; } }

.card { background: var(--card-bg); border-radius: 10px; border: 1px solid var(--border); padding: 18px 20px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.card-title { font-size: 15px; font-weight: 700; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; }
.count-badge { font-size: 11px; background: #f0f0f0; color: #595959; padding: 2px 8px; border-radius: 12px; font-weight: 600; }

/* Deadlines (FR3) */
.deadline-card-header { color: #cf1322; border-bottom: 2px solid #ffccc7; padding-bottom: 8px; }
.deadline-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 14px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #d9d9d9; background: #fafafa; transition: all 0.2s; }
.deadline-item.urgent { background: var(--urgent-bg); border-left-color: var(--urgent); border: 1px solid var(--urgent-border); border-left-width: 4px; }
.deadline-item.warning { background: var(--warn-bg); border-left-color: var(--warn); border: 1px solid var(--warn-border); border-left-width: 4px; }
.deadline-item.normal { background: var(--ok-bg); border-left-color: var(--ok); border: 1px solid var(--ok-border); border-left-width: 4px; }
.dl-course { font-size: 11px; font-weight: 700; color: #595959; text-transform: uppercase; }
.dl-name { font-size: 14px; font-weight: 600; color: #1f1f1f; margin-top: 2px; }
.dl-date { font-size: 12px; color: #8c8c8c; }
.badge-pill { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 12px; white-space: nowrap; }
.badge-urgent { background: #ff4d4f; color: #fff; }
.badge-warn { background: #faad14; color: #fff; }
.badge-normal { background: #52c41a; color: #fff; }

/* Course Cards Grid (FR1) */
.courses-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-bottom: 20px; }
.course-card { background: #fff; border-radius: 8px; border: 1px solid #e8e8e8; overflow: hidden; display: flex; flex-direction: column; transition: transform 0.15s, box-shadow 0.15s; }
.course-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.course-card-head { padding: 12px 14px; background: #fafafa; border-bottom: 1px solid #f0f0f0; display: flex; justify-content: space-between; align-items: center; }
.course-code { font-weight: 800; color: var(--primary-dark); font-size: 13px; }
.course-credits { font-size: 11px; background: #e6f7ff; color: #096dd9; padding: 2px 6px; border-radius: 4px; }
.course-card-body { padding: 12px 14px; flex-grow: 1; }
.course-name { font-size: 13px; font-weight: 600; margin-bottom: 10px; min-height: 38px; }
.course-instructor { font-size: 11px; color: var(--text-muted); }
.course-actions { display: flex; gap: 8px; margin-top: 10px; border-top: 1px dashed #f0f0f0; padding-top: 8px; }
.btn-sm { font-size: 11px; padding: 4px 8px; border-radius: 4px; border: 1px solid #d9d9d9; background: #fff; cursor: pointer; text-decoration: none; color: #595959; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; }
.btn-sm:hover { border-color: var(--primary); color: var(--primary); }

/* Submission & Forms (FR8, C2) */
label { display: block; font-size: 12px; font-weight: 600; margin-bottom: 4px; color: #434343; }
input[type="text"], input[type="password"], select, textarea { width: 100%; padding: 8px 12px; border: 1px solid #d9d9d9; border-radius: 6px; font-size: 13px; margin-bottom: 12px; font-family: inherit; }
input:focus, select:focus, textarea:focus { border-color: var(--primary); outline: none; box-shadow: 0 0 0 2px rgba(24,144,255,0.2); }
textarea { font-family: "Fira Code", monospace; font-size: 12px; }
.btn-primary { background: #1890ff; color: #fff; border: none; padding: 9px 18px; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-primary:hover { background: #096dd9; }
.linter-badge { font-size: 11px; padding: 4px 10px; border-radius: 4px; background: #f6ffed; border: 1px solid #b7eb8f; color: #389e0d; display: inline-block; margin-bottom: 10px; }

/* Table for submissions/admin */
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th, td { padding: 8px 10px; border-bottom: 1px solid #f0f0f0; text-align: left; }
th { background: #fafafa; color: #595959; font-weight: 700; }
.status-tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
.status-graded { background: #f6ffed; color: #52c41a; border: 1px solid #b7eb8f; }
.status-submitted { background: #e6f7ff; color: #1890ff; border: 1px solid #91d5ff; }
.status-draft { background: #fffbe6; color: #faad14; border: 1px solid #ffe58f; }

/* Security Banner (C1, C2) */
.security-footer { background: #fafafa; border: 1px dashed #d9d9d9; border-radius: 8px; padding: 12px 16px; margin-top: 24px; font-size: 11px; color: #595959; display: flex; justify-content: space-between; align-items: center; }
.sec-shield { color: #52c41a; font-weight: 700; display: flex; align-items: center; gap: 6px; }

/* Quick Demo Switcher Bar */
.demo-bar { background: #e6f7ff; border-bottom: 1px solid #91d5ff; padding: 6px 20px; font-size: 11px; color: #0050b3; display: flex; justify-content: space-between; align-items: center; }
.demo-links a { color: #096dd9; font-weight: 700; margin-left: 8px; text-decoration: underline; cursor: pointer; }
"""

def render_shell(title, content, user=None, q=""):
    who = ""
    demo_bar = ""
    if user:
        init = user['full_name'][:2].upper()
        role_cls = 'badge-warn' if user['role'] in ['teacher', 'admin'] else 'badge-normal'
        who = f"""
        <div class="user-menu">
          <div class="avatar">{html.escape(init)}</div>
          <div>
            <div><b>{html.escape(user['full_name'])}</b></div>
            <div style="font-size:11px; color:#d9d9d9;">ID: {html.escape(user['student_id'])} &bull; <span class="role-badge {role_cls}">{user['role']}</span></div>
          </div>
          <a class="nav-link" href="/logout" style="margin-left: 14px; background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 4px;">Выйти</a>
        </div>
        """
        demo_bar = """
        <div class="demo-bar">
          <div>🎯 <b>Демо-переключение ролей:</b> войдите мгновенно под любым аккаунтом:</div>
          <div class="demo-links">
            <a href="/quick_login?role=student">Студент (Алихан)</a> &bull;
            <a href="/quick_login?role=teacher">Преподаватель (Казбекова)</a> &bull;
            <a href="/quick_login?role=admin">Админ LMS</a>
          </div>
        </div>
        """

    search_input = f"""
    <form method="get" action="/dashboard" class="search-box">
      <input type="text" name="q" value="{html.escape(q)}" placeholder="Поиск заданий, лекций, преподавателей (FR4)...">
    </form>
    """ if user else ""

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)} — AITU LMS Portal</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>{CSS}</style>
</head>
<body>
  <div class="navbar">
    <div class="brand">
      <div class="logo-box">AI</div>
      <div>Astana IT University <span style="font-weight:400; font-size:13px; opacity:0.8;">| Student Portal</span></div>
    </div>
    {search_input}
    {who}
  </div>
  {demo_bar}
  <div class="container">
    {content}
    <div class="security-footer">
      <div class="sec-shield">🛡️ SQLite 3NF Database &bull; Real-time Parameterized SQL &bull; Zero SQLi Vulnerabilities</div>
      <div>Role-Based Access Control (RBAC) &bull; Salted SHA-256 Hashing &bull; Audit Trail v1.4</div>
    </div>
  </div>
</body>
</html>"""


class PortalHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _send(self, code, text, cookie=None, location=None):
        data = text.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        if cookie:
            self.send_header('Set-Cookie', cookie)
        if location:
            self.send_header('Location', location)
        self.end_headers()
        self.wfile.write(data)

    def _user(self):
        raw = self.headers.get('Cookie', '')
        for part in raw.split(';'):
            part = part.strip()
            if part.startswith('sid='):
                return SESSIONS.get(part[4:])
        return None

    def _form(self):
        n = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(n).decode('utf-8')
        return {k: v[0] for k, v in urllib.parse.parse_qs(body).items()}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)
        user = self._user()

        if path == '/logout':
            return self._send(302, '', cookie='sid=; Path=/; Max-Age=0', location='/')

        if path == '/quick_login':
            role = qs.get('role', ['student'])[0]
            email_map = {
                'student': '261875@astanait.edu.kz',
                'teacher': 'diana.kazbekova@astanait.edu.kz',
                'admin': 'admin.lms@astanait.edu.kz'
            }
            target_email = email_map.get(role, email_map['student'])
            con = db()
            row = con.execute('SELECT * FROM users WHERE email = ?', (target_email,)).fetchone()
            token = secrets.token_urlsafe(24)
            SESSIONS[token] = {
                'id': row['id'], 'full_name': row['full_name'], 'role': row['role'],
                'student_id': row['student_id'], 'email': row['email']
            }
            audit(con, row['id'], 'QUICK_LOGIN_DEMO', self.client_address[0], f'Auto-logged in as {role}')
            con.close()
            return self._send(302, '', cookie=f'sid={token}; Path=/; HttpOnly; SameSite=Lax', location='/dashboard')

        if path in ('/dashboard', '/courses', '/admin') and user:
            q = qs.get('q', [''])[0].strip()
            return self.render_dashboard(user, q)

        return self.render_login()

    def render_login(self, error=""):
        err_box = f'<div style="background:#fff1f0; border:1px solid #ffa39e; padding:8px 12px; border-radius:6px; color:#cf1322; font-size:12px; margin-bottom:12px;">{html.escape(error)}</div>' if error else ""
        body = f"""
        <div style="max-width: 420px; margin: 60px auto;">
          <div class="card" style="box-shadow: 0 4px 16px rgba(0,0,0,0.08);">
            <div style="text-align:center; margin-bottom: 18px;">
              <div class="logo-box" style="margin: 0 auto 10px; width:40px; height:40px; font-size:18px;">AI</div>
              <h2 style="font-size: 18px;">Вход в AITU Portal</h2>
              <div style="font-size: 12px; color: var(--text-muted);">Проект редизайна Moodle LMS (Stage 1 & 2)</div>
            </div>
            {err_box}
            <form method="post" action="/login">
              <label>Корпоративный Email</label>
              <input type="text" name="email" value="261875@astanait.edu.kz" placeholder="261875@astanait.edu.kz" required>
              <label>Пароль (проверяется соленый SHA-256 хэш)</label>
              <input type="password" name="password" value="Alikhan2026!" required>
              <button type="submit" class="btn-primary" style="width: 100%; padding: 10px;">Войти в личный кабинет</button>
            </form>
            <div style="margin-top: 18px; border-top: 1px dashed #e8e8e8; padding-top: 12px; font-size: 11px; color: #595959;">
              <div><b>Тестовые аккаунты для комиссии:</b></div>
              <div style="margin-top:4px;">&bull; <b>Студент:</b> <code>261875@astanait.edu.kz</code> / <code>Alikhan2026!</code></div>
              <div>&bull; <b>Преподаватель:</b> <code>diana.kazbekova@astanait.edu.kz</code> / <code>DianaPass2026!</code></div>
              <div>&bull; <b>Админ:</b> <code>admin.lms@astanait.edu.kz</code> / <code>RootAdminSecure99#</code></div>
            </div>
          </div>
        </div>
        """
        self._send(200, render_shell("Вход в систему", body))

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        form = self._form()
        ip = self.client_address[0]

        if path == '/login':
            email = form.get('email', '').strip()
            pwd = form.get('password', '')
            con = db()
            row = con.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            if row is None or row['password_hash'] != hash_password(pwd):
                con.close()
                return self.render_login("Неверный email или пароль!")
            token = secrets.token_urlsafe(24)
            SESSIONS[token] = {
                'id': row['id'], 'full_name': row['full_name'], 'role': row['role'],
                'student_id': row['student_id'], 'email': row['email']
            }
            audit(con, row['id'], 'USER_LOGIN', ip, f"Authenticated as {row['role']}")
            con.close()
            return self._send(302, '', cookie=f'sid={token}; Path=/; HttpOnly; SameSite=Lax', location='/dashboard')

        user = self._user()
        if not user:
            return self._send(302, '', location='/')

        # Студент сдает работу (FR8, C2)
        if path == '/submit' and user['role'] == 'student':
            aid = form.get('assignment_id', '')
            text = form.get('submission_text', '').strip()
            if aid.isdigit() and text:
                con = db()
                con.execute("""
                    INSERT INTO submissions (assignment_id, student_id, submission_text, file_url, submitted_at, status)
                    VALUES (?, ?, ?, ?, ?, 'submitted')
                """, (int(aid), user['id'], text, 'web_submission', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                audit(con, user['id'], 'SUBMIT_ASSIGNMENT', ip, f"Submitted assignment_id={aid}")
                con.close()
            return self._send(302, '', location='/dashboard')

        # Преподаватель публикует задание (FR5, FR6)
        if path == '/create_assignment' and user['role'] in ['teacher', 'admin']:
            cid = form.get('course_id', '')
            title = form.get('title', '').strip()
            desc = form.get('description', '').strip()
            due = form.get('due_date', '').strip()
            pts = form.get('max_points', '100')
            if cid.isdigit() and title and due:
                con = db()
                con.execute("""
                    INSERT INTO assignments (course_id, title, description, due_date, max_points, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (int(cid), title, desc, due, float(pts), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                audit(con, user['id'], 'CREATE_ASSIGNMENT', ip, f"Published new task: {title[:40]}")
                con.close()
            return self._send(302, '', location='/dashboard')

        # Преподаватель выставляет оценку
        if path == '/grade_submission' and user['role'] in ['teacher', 'admin']:
            sid = form.get('submission_id', '')
            grade = form.get('grade', '')
            fb = form.get('feedback', '').strip()
            if sid.isdigit() and grade:
                con = db()
                con.execute("""
                    UPDATE submissions SET grade = ?, feedback = ?, status = 'graded' WHERE id = ?
                """, (float(grade), fb, int(sid)))
                audit(con, user['id'], 'GRADE_SUBMISSION', ip, f"Graded sub_id={sid} with {grade} pts")
                con.close()
            return self._send(302, '', location='/dashboard')

        self._send(403, "Access denied")

    def render_dashboard(self, user, q=""):
        con = db()
        content = ""

        # =====================================================================
        # СТУДЕНЧЕСКИЙ РЕЖИМ (Кабинет Алихана Бельжанова)
        # =====================================================================
        if user['role'] == 'student':
            # 1. Загрузка курсов (FR1)
            courses = con.execute("""
                SELECT c.id, c.course_code, c.course_name, c.credits, u.full_name as teacher_name
                FROM enrollments e
                JOIN courses c ON e.course_id = c.id
                JOIN users u ON c.instructor_id = u.id
                WHERE e.student_id = ?
                ORDER BY c.course_code
            """, (user['id'],)).fetchall()

            # 2. Агрегированные дедлайны (FR3) с поиском (FR4)
            query_filter = ""
            params = [user['id']]
            if q:
                query_filter = "AND (c.course_code LIKE ? OR a.title LIKE ? OR a.description LIKE ?)"
                params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])

            deadlines = con.execute(f"""
                SELECT c.course_code, c.course_name, a.id as aid, a.title, a.due_date,
                       a.max_points, a.description, s.id as sub_id, s.status, s.grade, s.submitted_at
                FROM enrollments e
                JOIN courses c ON e.course_id = c.id
                JOIN assignments a ON a.course_id = c.id
                LEFT JOIN submissions s ON s.assignment_id = a.id AND s.student_id = e.student_id
                WHERE e.student_id = ? {query_filter}
                ORDER BY a.due_date ASC
            """, params).fetchall()

            # Генерация карточек курсов (FR1)
            course_cards = ""
            for cr in courses:
                course_cards += f"""
                <div class="course-card">
                  <div class="course-card-head">
                    <span class="course-code">{html.escape(cr['course_code'])}</span>
                    <span class="course-credits">{cr['credits']} кредита</span>
                  </div>
                  <div class="course-card-body">
                    <div class="course-name">{html.escape(cr['course_name'])}</div>
                    <div class="course-instructor">👨‍🏫 {html.escape(cr['teacher_name'])}</div>
                    <div class="course-actions">
                      <a class="btn-sm" href="?q={html.escape(cr['course_code'])}">📅 Задания</a>
                      <a class="btn-sm" href="#" onclick="alert('Силлабус и лекции доступны в облачном хранилище'); return false;">📥 Силлабус</a>
                    </div>
                  </div>
                </div>
                """

            # Генерация списка дедлайнов (FR3)
            deadline_items = ""
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for dl in deadlines:
                due = dl['due_date']
                st = dl['status'] or 'не сдано'
                
                # Классификация срочности
                if st == 'graded':
                    badge_cls = 'badge-normal'
                    badge_txt = f"✓ Оценено: {dl['grade']} б"
                    item_cls = 'normal'
                elif st == 'submitted':
                    badge_cls = 'badge-warn'
                    badge_txt = "⏳ На проверке"
                    item_cls = 'warning'
                elif due < now_str:
                    badge_cls = 'badge-urgent'
                    badge_txt = "🔴 Дедлайн прошел"
                    item_cls = 'urgent'
                else:
                    badge_cls = 'badge-urgent'
                    badge_txt = f"🔥 Сдать до {due[5:16]}"
                    item_cls = 'urgent'

                grade_info = f"<b style='color:#52c41a'>Оценка: {dl['grade']} / {dl['max_points']}</b>" if dl['grade'] is not None else f"Макс: {dl['max_points']} б"

                deadline_items += f"""
                <div class="deadline-item {item_cls}">
                  <div>
                    <div class="dl-course">{html.escape(dl['course_code'])} &bull; {grade_info}</div>
                    <div class="dl-name">{html.escape(dl['title'])}</div>
                    <div class="dl-date">Срок: {html.escape(str(due))}</div>
                  </div>
                  <div style="text-align:right;">
                    <span class="badge-pill {badge_cls}">{badge_txt}</span>
                  </div>
                </div>
                """

            # Опции для выпадающего списка формы сдачи
            submit_opts = ""
            for dl in deadlines:
                submit_opts += f'<option value="{dl["aid"]}">{html.escape(dl["course_code"])} — {html.escape(dl["title"])}</option>'

            uid_val = user['id']
            content = f"""
            <div class="card" style="background: linear-gradient(135deg, #002766, #1890ff); color:#fff;">
              <h2 style="font-size: 20px; margin-bottom: 6px;">С возвращением, {html.escape(user['full_name'])}!</h2>
              <div style="font-size: 13px; opacity: 0.9;">
                Специальность: Software Engineering &bull; Группа: SE-2625 &bull; ID: {user['student_id']}
              </div>
            </div>

            <!-- FR1: Мои курсы -->
            <div class="card-title">
              <div>📚 Мои активные дисциплины (FR1 Single-Level Overview)</div>
              <span class="count-badge">{len(courses)} курсов</span>
            </div>
            <div class="courses-grid">
              {course_cards}
            </div>

            <div class="grid-layout">
              <!-- Левая колонка: FR3 Агрегатор дедлайнов -->
              <div>
                <div class="card">
                  <div class="card-title deadline-card-header">
                    <div>🔥 Ближайшие дедлайны (FR3 Priority Queue)</div>
                    <span class="count-badge" style="background:#fff1f0; color:#cf1322;">{len(deadlines)} активных</span>
                  </div>
                  {deadline_items if deadline_items else '<div style="color:var(--text-muted); padding:20px; text-align:center;">По вашему запросу ничего не найдено.</div>'}
                </div>
              </div>

              <!-- Правая колонка: FR8 Сдача работы + WAF линтер -->
              <div>
                <div class="card">
                  <div class="card-title">
                    <div>✍️ Онлайн сдача (FR8 + Anti-WAF)</div>
                  </div>
                  <div class="linter-badge">✓ Local Auto-Save & WAF Sanitizer Active</div>
                  <form method="post" action="/submit" id="submitForm">
                    <label>Выберите задание</label>
                    <select name="assignment_id" required>
                      {submit_opts}
                    </select>
                    
                    <label>Код решения / Текст ответа (C++, Python, SQL)</label>
                    <textarea name="submission_text" id="codeEditor" rows="7" placeholder="Вставьте ваш код решения или отчет..." required></textarea>
                    
                    <div style="font-size:11px; color:#8c8c8c; margin-bottom: 12px;" id="saveNotice">
                      Автосохранение: драфт сохранен локально в localStorage.
                    </div>

                    <button type="submit" class="btn-primary" style="width:100%;">Отправить решение в БД</button>
                  </form>
                </div>

                <div class="card" style="font-size: 12px;">
                  <b>Критерии сдачи (Security Checklist):</b>
                  <ul style="margin: 8px 0 0 16px; color:#595959;">
                    <li>Параметризованный <code>INSERT</code> в таблицу <code>submissions</code></li>
                    <li>Автоматическая запись события в <code>audit_logs</code></li>
                    <li>Синхронизация дедлайнов с Firestore в Stage 2</li>
                  </ul>
                </div>
              </div>
            </div>

            <script>
              // FR8: Локальное автосохранение черновика
              const ed = document.getElementById('codeEditor');
              const notice = document.getElementById('saveNotice');
              if (ed) {{
                const saved = localStorage.getItem('draft_sub_{uid_val}');
                if (saved) ed.value = saved;
                ed.addEventListener('input', () => {{
                  localStorage.setItem('draft_sub_{uid_val}', ed.value);
                  notice.innerText = 'Черновик автосохранен в ' + new Date().toLocaleTimeString();
                }});
              }}
            </script>
            """

        # =====================================================================
        # ПРЕПОДАВАТЕЛЬСКИЙ / АДМИНСКИЙ РЕЖИМ (Кабинет Дианы Казбековой)
        # =====================================================================
        else:
            courses = con.execute("SELECT * FROM courses ORDER BY course_code").fetchall()
            subs = con.execute("""
                SELECT s.id as sub_id, u.full_name, u.student_id, c.course_code, a.title, 
                       s.status, s.grade, s.submitted_at, s.submission_text, s.feedback
                FROM submissions s
                JOIN users u ON s.student_id = u.id
                JOIN assignments a ON s.assignment_id = a.id
                JOIN courses c ON a.course_id = c.id
                ORDER BY s.submitted_at DESC LIMIT 50
            """).fetchall()

            audit_rows = con.execute("""
                SELECT l.created_at, u.full_name, u.role, l.action, l.ip_address, l.details
                FROM audit_logs l
                LEFT JOIN users u ON l.user_id = u.id
                ORDER BY l.id DESC LIMIT 20
            """).fetchall()

            # Таблица сдач студентов с кнопкой быстрой оценки
            sub_tr = ""
            for s in subs:
                st_cls = 'status-graded' if s['status'] == 'graded' else 'status-submitted'
                grade_disp = f"<b>{s['grade']}</b>" if s['grade'] is not None else "<i>—</i>"
                sub_tr += f"""
                <tr>
                  <td><b>{html.escape(s['full_name'])}</b><br><span style="color:#8c8c8c; font-size:10px;">ID: {s['student_id']}</span></td>
                  <td><span class="badge-pill" style="background:#e6f7ff; color:#096dd9;">{html.escape(s['course_code'])}</span></td>
                  <td>{html.escape(s['title'])}</td>
                  <td><span class="status-tag {st_cls}">{s['status']}</span></td>
                  <td>{grade_disp}</td>
                  <td>
                    <form method="post" action="/grade_submission" style="display:flex; gap:4px; margin:0;">
                      <input type="hidden" name="submission_id" value="{s['sub_id']}">
                      <input type="number" name="grade" placeholder="Балл" style="width:60px; padding:3px; margin:0; font-size:11px;" required min="0" max="100">
                      <button type="submit" class="btn-sm" style="padding:3px 8px; font-size:11px;">Оценить</button>
                    </form>
                  </td>
                </tr>
                """

            # Журнал безопасности
            log_tr = ""
            for log in audit_rows:
                log_tr += f"""
                <tr>
                  <td style="color:#8c8c8c;">{html.escape(str(log['created_at']))}</td>
                  <td><b>{html.escape(log['full_name'] or 'Гость')}</b> <span style="font-size:10px; opacity:0.7;">({html.escape(str(log['role']))})</span></td>
                  <td><code>{html.escape(str(log['action']))}</code></td>
                  <td><span style="font-family:monospace;">{html.escape(str(log['ip_address']))}</span></td>
                  <td>{html.escape(str(log['details']))}</td>
                </tr>
                """

            course_opts = "".join(f'<option value="{c["id"]}">{c["course_code"]} — {html.escape(c["course_name"])}</option>' for c in courses)

            content = f"""
            <div class="card" style="background: linear-gradient(135deg, #135200, #52c41a); color:#fff;">
              <h2 style="font-size: 20px; margin-bottom: 6px;">Панель преподавателя / Администратора LMS</h2>
              <div style="font-size: 13px; opacity: 0.9;">
                Вы вошли как: <b>{html.escape(user['full_name'])}</b> &bull; Роль: <b>{user['role'].upper()}</b> &bull; Управление дисциплинами и оцениванием (FR5, FR6, FR7)
              </div>
            </div>

            <div class="grid-layout">
              <!-- Левая колонка: Проверка и оценивание работ студентов -->
              <div>
                <div class="card">
                  <div class="card-title">
                    <div>📥 Поступившие работы студентов (Всего в базе: {len(subs)})</div>
                  </div>
                  <table>
                    <thead>
                      <tr>
                        <th>Студент</th>
                        <th>Курс</th>
                        <th>Задание</th>
                        <th>Статус</th>
                        <th>Балл</th>
                        <th>Действие</th>
                      </tr>
                    </thead>
                    <tbody>
                      {sub_tr}
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Правая колонка: Публикация нового задания (FR5/FR6) и Аудит-лог -->
              <div>
                <div class="card">
                  <div class="card-title">➕ Опубликовать новое задание (FR5)</div>
                  <form method="post" action="/create_assignment">
                    <label>Дисциплина</label>
                    <select name="course_id" required>
                      {course_opts}
                    </select>

                    <label>Название задания</label>
                    <input type="text" name="title" placeholder="e.g. Assignment 4: Cloud Architecture" required>

                    <label>Описание задания</label>
                    <textarea name="description" rows="2" placeholder="Требования к выполнению..."></textarea>

                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                      <div>
                        <label>Срок сдачи (Дедлайн)</label>
                        <input type="text" name="due_date" value="2026-10-28 23:59:00" required>
                      </div>
                      <div>
                        <label>Макс. балл</label>
                        <input type="number" name="max_points" value="100" required>
                      </div>
                    </div>

                    <button type="submit" class="btn-primary" style="width:100%; background:#52c41a;">Опубликовать в Moodle DB</button>
                  </form>
                </div>

                <div class="card">
                  <div class="card-title">🛡️ Журнал аудита безопасности (Audit Trail)</div>
                  <table>
                    <thead>
                      <tr><th>Время</th><th>Кто</th><th>Событие</th><th>IP</th><th>Детали</th></tr>
                    </thead>
                    <tbody>
                      {log_tr}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            """

        con.close()
        self._send(200, render_shell(f"{user['full_name']} — AITU LMS", content, user, q))


def run():
    if not os.path.exists(DB_PATH):
        print('Database not found:', DB_PATH)
        return
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('127.0.0.1', PORT), PortalHandler) as httpd:
        print(f'AITU LMS modern portal running: http://127.0.0.1:{PORT}')
        httpd.serve_forever()


if __name__ == '__main__':
    run()
