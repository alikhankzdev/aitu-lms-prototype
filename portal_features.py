"""Additive portal capabilities; all private data stays behind existing authorization."""
from datetime import datetime, timedelta
import calendar as cal
import csv, io, secrets, hashlib, sqlite3
from pathlib import Path
from flask import g, request, session, render_template, redirect, url_for, abort, flash, jsonify

def register_features(app, db, require, course_access, assignment_access, course_rows, assignments_for_user, audit, notify, tr, password_hash, password_matches):
    with app.app_context():
        con=db()
        if not con.execute("SELECT 1 FROM sqlite_master WHERE name='assignment_drafts'").fetchone():
            folder=Path(app.config['DATABASE']).parent/'backups';folder.mkdir(exist_ok=True)
            backup=sqlite3.connect(folder/('before_features_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.sqlite'));con.backup(backup);backup.close()
        con.executescript('''
        CREATE TABLE IF NOT EXISTS profiles(user_id INTEGER PRIMARY KEY REFERENCES users(id), specialty TEXT DEFAULT '', group_name TEXT DEFAULT '', study_year INTEGER DEFAULT 1, phone TEXT DEFAULT '', bio TEXT DEFAULT '', avatar TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS assignment_drafts(user_id INTEGER REFERENCES users(id), assignment_id INTEGER REFERENCES assignments(id), body TEXT NOT NULL, revision INTEGER NOT NULL DEFAULT 1, updated_at TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(user_id,assignment_id));
        CREATE TABLE IF NOT EXISTS assignment_history(id INTEGER PRIMARY KEY, assignment_id INTEGER REFERENCES assignments(id), actor_id INTEGER REFERENCES users(id), event TEXT NOT NULL, details TEXT DEFAULT '', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS announcements(id INTEGER PRIMARY KEY, course_id INTEGER REFERENCES courses(id), author_id INTEGER REFERENCES users(id), title TEXT NOT NULL, body TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS semesters(id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, starts_on TEXT NOT NULL, ends_on TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS recovery_tokens(digest TEXT PRIMARY KEY, user_id INTEGER REFERENCES users(id), expires_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS import_previews(token TEXT PRIMARY KEY, admin_id INTEGER REFERENCES users(id), payload TEXT NOT NULL, expires_at TEXT NOT NULL);
        ''')
        cols={r[1] for r in con.execute('PRAGMA table_info(courses)')}
        if 'archived' not in cols:con.execute('ALTER TABLE courses ADD COLUMN archived INTEGER NOT NULL DEFAULT 0')
        if 'semester_id' not in cols:con.execute('ALTER TABLE courses ADD COLUMN semester_id INTEGER REFERENCES semesters(id)')
        con.commit()

    @app.context_processor
    def feature_context():
        return {'semesters':db().execute('SELECT * FROM semesters ORDER BY starts_on DESC').fetchall() if g.user else []}

    @app.get('/sw.js')
    def service_worker():
        response=app.send_static_file('sw.js');response.headers['Cache-Control']='no-cache';return response

    @app.route('/admin/import',methods=['GET','POST'])
    @require('admin')
    def import_users():
        import json
        rows=[];errors=[];preview_token=None
        if request.method=='POST' and request.form.get('preview_token'):
            db().execute('BEGIN IMMEDIATE')
            token=request.form['preview_token'];preview=db().execute('SELECT * FROM import_previews WHERE token=? AND admin_id=? AND expires_at>?',(token,g.user['id'],datetime.now().isoformat())).fetchone()
            if not preview:abort(400)
            rows=json.loads(preview['payload'])
            try:
                for r in rows:db().execute('INSERT INTO users(student_id,email,password_hash,full_name,role) VALUES(?,?,?,?,?)',(r['student_id'],r['email'],r['password_hash'],r['full_name'],r['role']))
                db().execute('DELETE FROM import_previews WHERE token=?',(token,));audit('CSV_USERS_IMPORTED',str(len(rows)));db().commit()
            except sqlite3.IntegrityError:db().rollback();flash(tr('invalid_data'),'error');return redirect(url_for('import_users'))
            flash(tr('saved'),'success');return redirect(url_for('admin'))
        if request.method=='POST':
            upload=request.files.get('file')
            if not upload:abort(400)
            try:
                content=upload.read(1024*1024+1)
                if len(content)>1024*1024:raise ValueError()
                reader=csv.DictReader(io.StringIO(content.decode('utf-8-sig')))
                required={'student_id','email','full_name','role','password'}
                if not required.issubset(reader.fieldnames or []):raise ValueError()
                seen_email=set();seen_id=set()
                for index,r in enumerate(reader,2):
                    if index>501:raise ValueError()
                    if not all(r.get(k) for k in required) or r['role'] not in ('student','teacher') or not 10<=len(r['password'])<=200 or not r['email'].endswith('@astanait.edu.kz') or r['email'] in seen_email or r['student_id'] in seen_id or db().execute('SELECT 1 FROM users WHERE email=? OR student_id=?',(r['email'],r['student_id'])).fetchone():errors.append(index);continue
                    seen_email.add(r['email']);seen_id.add(r['student_id']);r['password_hash']=password_hash(r.pop('password'));rows.append(r)
            except (ValueError,UnicodeError,csv.Error):errors.append(0)
            if rows and not errors:
                preview_token=secrets.token_urlsafe(24);db().execute('DELETE FROM import_previews WHERE expires_at<?',(datetime.now().isoformat(),));db().execute('INSERT INTO import_previews VALUES(?,?,?,?)',(preview_token,g.user['id'],json.dumps(rows),(datetime.now()+timedelta(minutes=15)).isoformat()));db().commit()
        return render_template('import_users.html',rows=rows,errors=errors,preview_token=preview_token)

    @app.route('/profile',methods=['GET','POST'])
    @require()
    def profile():
        if request.method=='POST':
            f=request.form
            try:
                year=int(f.get('study_year','1'));assert 1<=year<=8
                assert all(len(f.get(k,''))<=limit for k,limit in [('specialty',120),('group_name',40),('phone',40),('bio',1000)])
                avatar=f.get('avatar','');assert avatar in ('','initials','blue','gold')
            except (ValueError,AssertionError):abort(400)
            db().execute('INSERT INTO profiles(user_id,specialty,group_name,study_year,phone,bio,avatar) VALUES(?,?,?,?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET specialty=excluded.specialty,group_name=excluded.group_name,study_year=excluded.study_year,phone=excluded.phone,bio=excluded.bio,avatar=excluded.avatar',(g.user['id'],f.get('specialty','').strip(),f.get('group_name','').strip(),year,f.get('phone','').strip(),f.get('bio','').strip(),avatar))
            audit('PROFILE_UPDATED');db().commit();flash(tr('saved'),'success');return redirect(url_for('profile'))
        return render_template('profile.html',profile=db().execute('SELECT * FROM profiles WHERE user_id=?',(g.user['id'],)).fetchone())

    @app.get('/calendar')
    @require()
    def calendar():
        try:
            selected=datetime.strptime(request.args.get('month',datetime.now().strftime('%Y-%m')),'%Y-%m')
            if not 1900<=selected.year<=2100:raise ValueError()
        except ValueError:abort(400)
        events=[a for a in assignments_for_user() if a['due_date'].startswith(selected.strftime('%Y-%m'))]
        return render_template('calendar.html',events=events,month=selected.strftime('%Y-%m'),weeks=cal.Calendar(firstweekday=0).monthdatescalendar(selected.year,selected.month),previous_month=(selected-timedelta(days=1)).strftime('%Y-%m'),next_month=(selected.replace(day=28)+timedelta(days=4)).strftime('%Y-%m'))

    @app.post('/assignments/<int:assignment_id>/draft')
    @require('student')
    def save_draft(assignment_id):
        assignment_access(assignment_id)
        body=request.form.get('body','')
        if len(body)>100000:abort(400)
        if db().execute("SELECT 1 FROM submissions WHERE assignment_id=? AND student_id=? AND status='graded'",(assignment_id,g.user['id'])).fetchone():abort(403)
        db().execute('BEGIN IMMEDIATE')
        old=db().execute('SELECT revision FROM assignment_drafts WHERE user_id=? AND assignment_id=?',(g.user['id'],assignment_id)).fetchone()
        try:revision=int(request.form.get('revision','0'))
        except ValueError:abort(400)
        if revision!=(old['revision'] if old else 0):
            db().rollback();return jsonify(error='draft_conflict'),409
        db().execute('INSERT INTO assignment_drafts(user_id,assignment_id,body) VALUES(?,?,?) ON CONFLICT(user_id,assignment_id) DO UPDATE SET body=excluded.body,revision=assignment_drafts.revision+1,updated_at=CURRENT_TIMESTAMP',(g.user['id'],assignment_id,body));db().commit()
        return jsonify(saved=True,revision=revision+1)

    @app.post('/courses/<int:course_id>/announcements')
    @require('teacher','admin')
    def create_announcement(course_id):
        course_access(course_id,True);title=request.form.get('title','').strip();body=request.form.get('body','').strip()
        if not title or len(title)>150 or not body or len(body)>10000:abort(400)
        db().execute('INSERT INTO announcements(course_id,author_id,title,body) VALUES(?,?,?,?)',(course_id,g.user['id'],title,body))
        for row in db().execute('SELECT student_id FROM enrollments WHERE course_id=?',(course_id,)):notify(row[0],'new_announcement',title)
        audit('ANNOUNCEMENT_CREATED',str(course_id));db().commit();return redirect(url_for('course',course_id=course_id,tab='announcements'))

    @app.get('/analytics')
    @require('teacher','admin')
    def analytics():
        rows=[]
        for c in course_rows():
            r=dict(c);r.update(dict(db().execute("SELECT count(s.id) submitted, sum(CASE WHEN s.status='submitted' THEN 1 ELSE 0 END) awaiting_review, avg(CASE WHEN s.status='graded' THEN 100.0*s.grade/a.max_points END) average_grade FROM assignments a LEFT JOIN submissions s ON s.assignment_id=a.id AND s.status!='draft' WHERE a.course_id=?",(c['id'],)).fetchone()))
            r['expected']=db().execute('SELECT (SELECT count(*) FROM assignments WHERE course_id=?)*(SELECT count(*) FROM enrollments WHERE course_id=?)',(c['id'],c['id'])).fetchone()[0]
            r['completion']=round(100*r['submitted']/r['expected']) if r['expected'] else 0;rows.append(r)
        return render_template('analytics.html',analytics=rows)

    @app.route('/security',methods=['GET','POST'])
    @require()
    def security():
        if request.method=='POST':
            action=request.form.get('action')
            if action=='password':
                new=request.form.get('new_password','')
                if not password_matches(request.form.get('current_password',''),g.user['password_hash']) or not 10<=len(new)<=200:abort(400)
                db().execute('UPDATE users SET password_hash=? WHERE id=?',(password_hash(new),g.user['id']))
                db().execute('DELETE FROM recovery_tokens WHERE user_id=?',(g.user['id'],))
                db().execute('DELETE FROM portal_sessions WHERE user_id=? AND token!=?',(g.user['id'],session['auth']))
            elif action=='revoke_others':db().execute('DELETE FROM portal_sessions WHERE user_id=? AND token!=?',(g.user['id'],session['auth']))
            else:abort(400)
            audit('SECURITY_'+action.upper());db().commit();flash(tr('saved'),'success');return redirect(url_for('security'))
        sessions=db().execute('SELECT expires_at,token=? AS current FROM portal_sessions WHERE user_id=? AND expires_at>? ORDER BY expires_at DESC',(session['auth'],g.user['id'],datetime.now().isoformat())).fetchall()
        return render_template('security.html',sessions=sessions)

    @app.route('/recover',methods=['GET','POST'])
    def recover():
        if request.method=='POST':
            db().execute('BEGIN IMMEDIATE')
            digest=hashlib.sha256(request.form.get('token','').encode()).hexdigest();new=request.form.get('new_password','')
            row=db().execute('SELECT * FROM recovery_tokens WHERE digest=? AND expires_at>?',(digest,datetime.now().isoformat())).fetchone()
            if not row or not 10<=len(new)<=200:abort(400)
            db().execute('UPDATE users SET password_hash=? WHERE id=?',(password_hash(new),row['user_id']));db().execute('DELETE FROM recovery_tokens WHERE user_id=?',(row['user_id'],));db().execute('DELETE FROM portal_sessions WHERE user_id=?',(row['user_id'],));audit('PASSWORD_RECOVERED',user_id=row['user_id']);db().commit();return redirect(url_for('login'))
        return render_template('recover.html')

    @app.post('/admin/recovery')
    @require('admin')
    def issue_recovery():
        uid=request.form.get('user_id')
        if not db().execute('SELECT 1 FROM users WHERE id=? AND active=1',(uid,)).fetchone():abort(404)
        token=secrets.token_urlsafe(32);db().execute('DELETE FROM recovery_tokens WHERE user_id=?',(uid,));db().execute('INSERT INTO recovery_tokens VALUES(?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),uid,(datetime.now()+timedelta(minutes=15)).isoformat()));audit('RECOVERY_ISSUED',str(uid));db().commit()
        return render_template('recovery_token.html',recovery_token=token)

    @app.post('/admin/semesters')
    @require('admin')
    def create_semester():
        f=request.form
        try:
            start=datetime.strptime(f.get('starts_on',''),'%Y-%m-%d');end=datetime.strptime(f.get('ends_on',''),'%Y-%m-%d');assert end>start and 0<len(f.get('name','').strip())<=100
        except (ValueError,AssertionError):abort(400)
        db().execute('INSERT INTO semesters(name,starts_on,ends_on) VALUES(?,?,?)',(f['name'].strip(),f['starts_on'],f['ends_on']));audit('SEMESTER_CREATED');db().commit();return redirect(url_for('admin'))

    @app.post('/courses/<int:course_id>/archive')
    @require('admin')
    def archive_course(course_id):
        course_access(course_id)
        if request.form.get('archived') not in ('0','1'):abort(400)
        db().execute('UPDATE courses SET archived=?,semester_id=? WHERE id=?',(int(request.form['archived']),request.form.get('semester_id') or None,course_id));audit('COURSE_ARCHIVE_CHANGED',str(course_id));db().commit();return redirect(url_for('admin'))
