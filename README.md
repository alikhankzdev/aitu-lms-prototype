# AITU LMS Prototype

A lightweight learning management system built for AITU academic workflows — courses, assignments, submissions, grading, analytics and administration in a single Flask application with a SQLite (3NF) database.

**Team SE-2625:**
- Alikhan Belzhanov — System & Database Architecture (schema, submissions, parameterized SQL, backup/restore)
- Adilkhan Maratuly — Product analysis, requirements, presentation and documentation
- Sanzhar Khamidolla — Frontend engineering, UI/UX, accessibility, design system

## Stack

- **Backend:** Python 3, Flask 3 (application factory)
- **Database:** SQLite, third normal form, foreign keys, parameterized queries only
- **Frontend:** Jinja2 templates, hand-written CSS/JS, no external frameworks
- **Security:** CSRF tokens, salted password hashing (PBKDF2-style, `hashlib`/`hmac`), role-based access control (student / teacher / admin), login rate limiting, audit log
- **PWA:** service worker, offline shell, installable manifest

## Features

- Three role dashboards (student, teacher, administrator)
- Course catalogue, materials and announcements
- Assignment lifecycle: draft auto-save, submission, grading, feedback, revision history
- Review queue with filters and pagination
- Analytics: average grades by course, submission volume, grading backlog
- Calendar, notifications, profile and language switch (EN / RU / KK)
- Administration: users, enrollments, courses, semesters, archive, backup download
- WCAG 2.1 AA-oriented markup: skip links, focus styles, ARIA labels, keyboard support

## Project structure

```
app.py               application factory, auth, dashboards, submissions, grading
portal_features.py   calendar, analytics, drafts, announcements, recovery, semesters
i18n.py              EN / RU / KK translations
templates/           Jinja2 templates (one per screen)
static/              CSS, JS, images, course artwork, captions
schema.sql           database schema (3NF)
aitu_lms.sqlite      seeded demo database
tests_backend.py     backend test suite
tests_pwa.py         PWA / offline tests
docs/                requirement matrix, architecture notes, reports
```

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:8002

## Deploy

The repository ships with a `Procfile` for gunicorn-based platforms (Render, Railway, Fly.io, PythonAnywhere):

```
web: gunicorn -w 1 --threads 4 -b 0.0.0.0:$PORT "app:create_app()"
```

The application binds `HOST` / `PORT` from the environment.

## Demo accounts

| Role | Email | Password |
|------|-------|----------|
| Student | 261875@astanait.edu.kz | Alikhan2026! |
| Teacher | diana.kazbekova@astanait.edu.kz | DianaPass2026! |
| Admin | admin.lms@astanait.edu.kz | RootAdminSecure99# |

## Database snapshot

25 users · 6 courses · 46 assignments · 108 enrollments · 200 submissions

## Security notes

- All SQL statements use bound parameters; no string interpolation into queries
- Passwords stored as salted hashes, never plaintext
- Every state-changing form carries a CSRF token
- Authorization is enforced server-side per role and per resource
- Demo data is synthetic; this prototype is not intended for production use without TLS, a hardened WSGI server and a managed database

## Documentation

- `docs/` — requirement matrix (FR/NFR coverage), grading and analytics artefacts
- `PWA.md` — offline / installability notes
