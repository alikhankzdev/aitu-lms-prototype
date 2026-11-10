"""Local AITU learning portal. Run python3 app.py; data stays in this project."""
from pathlib import Path
import sys, os, sqlite3, secrets, hashlib, hmac, math, shutil
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import urlsplit
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / 'vendor'))
from flask import Flask, g, session, request, redirect, url_for, render_template, abort, flash, send_file
from werkzeug.utils import secure_filename

def password_hash(password):
    salt = secrets.token_hex(16)
    return 'scrypt$' + salt + '$' + hashlib.scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1).hex()

def password_matches(password, stored):
    if stored.startswith('scrypt$'):
        _, salt, digest = stored.split('$')
        return hmac.compare_digest(hashlib.scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1).hex(), digest)
    return hmac.compare_digest(hashlib.sha256((password + 'aitu_salt_2026').encode()).hexdigest(), stored)

def create_app(config=None):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.update(DATABASE=str(BASE/'aitu_lms.sqlite'), UPLOAD_FOLDER=str(BASE/'private_uploads'), MAX_CONTENT_LENGTH=10*1024*1024,
                      SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', PERMANENT_SESSION_LIFETIME=timedelta(hours=2))
    if config: app.config.update(config)
    if os.environ.get('LMS_HTTPS') == '1': app.config['SESSION_COOKIE_SECURE']=True
    secret = BASE/'.session-secret'
    if app.config.get('TESTING'): app.secret_key='test-only-secret'
    else:
        if not secret.exists(): secret.write_text(secrets.token_hex(32)); secret.chmod(0o600)
        app.secret_key=secret.read_text().strip()

    def db():
        if 'db' not in g:
            g.db=sqlite3.connect(app.config['DATABASE']); g.db.row_factory=sqlite3.Row
            g.db.execute('PRAGMA foreign_keys=ON')
        return g.db
    app.db=db
    @app.teardown_appcontext
    def close_db(error=None):
        con=g.pop('db',None)
        if con: con.close()
    def init_db():
        path=Path(app.config['DATABASE'])
        if not path.exists(): raise RuntimeError('Existing project database is required')
        con=sqlite3.connect(path)
        if not con.execute("SELECT 1 FROM sqlite_master WHERE name='portal_sessions'").fetchone():
            dest=path.parent/'backups'; dest.mkdir(exist_ok=True)
            backup=sqlite3.connect(dest/('before_portal_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.sqlite'))
            con.backup(backup); backup.close()
        con.executescript('''
        CREATE TABLE IF NOT EXISTS portal_sessions (token TEXT PRIMARY KEY, user_id INTEGER REFERENCES users(id), expires_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS notifications (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), title TEXT NOT NULL, body TEXT NOT NULL DEFAULT '', is_read INTEGER NOT NULL DEFAULT 0, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY, course_id INTEGER NOT NULL REFERENCES courses(id), submission_id INTEGER REFERENCES submissions(id), owner_id INTEGER NOT NULL REFERENCES users(id), title TEXT NOT NULL, original_name TEXT NOT NULL, stored_name TEXT NOT NULL UNIQUE, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS login_attempts (address TEXT PRIMARY KEY, attempts INTEGER NOT NULL DEFAULT 0, last_attempt TEXT NOT NULL);
        ''')
        cols={r[1] for r in con.execute('PRAGMA table_info(users)')}
        if 'active' not in cols: con.execute('ALTER TABLE users ADD COLUMN active INTEGER NOT NULL DEFAULT 1')
        if 'graded_at' not in {r[1] for r in con.execute('PRAGMA table_info(submissions)')}: con.execute('ALTER TABLE submissions ADD COLUMN graded_at TEXT')
        con.commit(); con.close()
        Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
    with app.app_context(): init_db()

    def tr(key, **kwargs):
        try:
            from i18n import translate
            return translate(key, g.get('lang','ru'), **kwargs)
        except (ImportError, AttributeError):
            try:
                from i18n import TRANSLATIONS
                return TRANSLATIONS.get(g.get('lang','ru'),{}).get(key,key).format(**kwargs)
            except (ImportError, KeyError, AttributeError): return key.replace('_',' ').format(**kwargs)
    def csrf():
        if 'csrf' not in session: session['csrf']=secrets.token_urlsafe(32)
        return session['csrf']
    def audit(action, details='', user_id=None):
        db().execute('INSERT INTO audit_logs(user_id,action,ip_address,details) VALUES(?,?,?,?)',
                     (user_id if user_id is not None else (g.user['id'] if g.user else None),action,request.remote_addr or 'local',details))
    def notify(user_id,title,body=''):
        db().execute('INSERT INTO notifications(user_id,title,body) VALUES(?,?,?)',(user_id,title,body))
    def require(*roles):
        def deco(fn):
            @wraps(fn)
            def wrapper(*args,**kwargs):
                if not g.user: return redirect(url_for('login'))
                if roles and g.user['role'] not in roles: abort(403)
                return fn(*args,**kwargs)
            return wrapper
        return deco
    @app.before_request
    def load_user():
        g.lang=request.cookies.get('lang','ru')
        if g.lang not in ('ru','kk','en'): g.lang='ru'
        g.user=None
        token=session.get('auth')
        if token:
            g.user=db().execute('SELECT u.* FROM portal_sessions s JOIN users u ON u.id=s.user_id WHERE s.token=? AND s.expires_at>? AND u.active=1',(token,datetime.now().isoformat())).fetchone()
            if not g.user: session.pop('auth',None)
        if request.method=='POST' and (not session.get('csrf') or not hmac.compare_digest(str(session.get('csrf','')),str(request.form.get('csrf',request.form.get('csrf_token',''))))):
            abort(400, description='csrf_error')
    @app.context_processor
    def context():
        unread=db().execute('SELECT count(*) FROM notifications WHERE user_id=? AND is_read=0',(g.user['id'],)).fetchone()[0] if g.user else 0
        return dict(t=tr,lang=g.lang,user=g.user,csrf_token=csrf,unread_count=unread,now=datetime.now())
    @app.template_filter('datetime_ui')
    def datetime_ui(value):
        if not value: return '—'
        try: parsed=datetime.fromisoformat(str(value))
        except (ValueError,TypeError): return str(value)
        return parsed.strftime('%Y-%m-%d %H:%M' if g.get('lang')=='en' else '%d.%m.%Y %H:%M')
    @app.after_request
    def headers(response):
        response.headers.update({'X-Content-Type-Options':'nosniff','X-Frame-Options':'DENY','Referrer-Policy':'same-origin','Cache-Control':'no-store'})
        response.headers['Permissions-Policy']='camera=(), microphone=(), geolocation=()'
        response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'"
        if request.endpoint == 'static' and response.status_code in (200,206,304):
            response.headers['Cache-Control']='public, max-age=86400'
        return response
    @app.url_defaults
    def static_version(endpoint, values):
        if endpoint == 'static' and 'filename' in values:
            path=BASE/'static'/values['filename']
            if path.is_file(): values.setdefault('v',str(path.stat().st_mtime_ns))
    @app.errorhandler(400)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(413)
    def error(e): return render_template('error.html',code=e.code,message=tr('error_'+str(e.code))),e.code
    @app.errorhandler(sqlite3.IntegrityError)
    def integrity(e):
        db().rollback(); flash(tr('invalid_data'),'error'); return redirect(request.referrer if request.referrer and urlsplit(request.referrer).netloc==request.host else url_for('dashboard'))
    def course_access(cid,write=False):
        row=db().execute('SELECT c.*,u.full_name AS teacher_name FROM courses c JOIN users u ON u.id=c.instructor_id WHERE c.id=?',(cid,)).fetchone()
        if not row: abort(404)
        if request.method == 'POST' and row['archived'] and request.endpoint != 'archive_course':
            abort(403)
        if g.user['role']=='admin': return row
        if g.user['role']=='teacher' and row['instructor_id']==g.user['id']: return row
        if not write and g.user['role']=='student' and db().execute('SELECT 1 FROM enrollments WHERE course_id=? AND student_id=?',(cid,g.user['id'])).fetchone(): return row
        abort(403)
    def assignment_access(aid,write=False):
        a=db().execute('SELECT a.*,c.course_code,c.course_name,c.instructor_id FROM assignments a JOIN courses c ON c.id=a.course_id WHERE a.id=?',(aid,)).fetchone()
        if not a: abort(404)
        course_access(a['course_id'],write); return a
    def course_rows():
        sql='SELECT c.*,u.full_name AS teacher_name FROM courses c JOIN users u ON u.id=c.instructor_id'
        args=[]
        if g.user['role']=='student': sql+=' JOIN enrollments e ON e.course_id=c.id WHERE e.student_id=?'; args=[g.user['id']]
        elif g.user['role']=='teacher': sql+=' WHERE c.instructor_id=?'; args=[g.user['id']]
        result=[]
        for row in db().execute(sql+' ORDER BY c.course_code',args).fetchall():
            c=dict(row)
            c['visual_key']=next((key for prefix,key in [('ICT','ict'),('MATH','algebra'),('CS','programming'),('ENG','english'),('CULT','culture'),('CALC','calculus')] if c['course_code'].upper().startswith(prefix)),'general')
            c['assignment_count']=db().execute('SELECT count(*) FROM assignments WHERE course_id=?',(c['id'],)).fetchone()[0]
            c['completed_count']=db().execute("SELECT count(*) FROM submissions s JOIN assignments a ON a.id=s.assignment_id WHERE a.course_id=? AND s.student_id=? AND s.status IN ('submitted','graded')",(c['id'],g.user['id'])).fetchone()[0]
            c['expected_count']=c['assignment_count']
            if g.user['role']!='student':
                c['expected_count']*=db().execute('SELECT count(*) FROM enrollments WHERE course_id=?',(c['id'],)).fetchone()[0]
                c['completed_count']=db().execute("SELECT count(*) FROM submissions s JOIN assignments a ON a.id=s.assignment_id JOIN enrollments e ON e.course_id=a.course_id AND e.student_id=s.student_id WHERE a.course_id=? AND s.status IN ('submitted','graded')",(c['id'],)).fetchone()[0]
            c['progress']=round(100*c['completed_count']/c['expected_count']) if c['expected_count'] else 0
            result.append(c)
        return result
    def assignments_for_user():
        rows=[]
        for c in course_rows():
            for a in db().execute('SELECT a.*,c.course_code,c.course_name,c.instructor_id,s.status,s.grade,s.submitted_at,s.graded_at FROM assignments a JOIN courses c ON c.id=a.course_id LEFT JOIN submissions s ON s.assignment_id=a.id AND s.student_id=? WHERE a.course_id=? ORDER BY a.due_date',(g.user['id'],c['id'])):
                d=dict(a); d['status']=d['status'] or ('overdue' if d['due_date']<datetime.now().strftime('%Y-%m-%d %H:%M:%S') else 'pending')
                if g.user['role']!='student':
                    counts=db().execute("SELECT count(*) total,sum(CASE WHEN status='submitted' THEN 1 ELSE 0 END) waiting,sum(CASE WHEN status='graded' THEN 1 ELSE 0 END) graded FROM submissions WHERE assignment_id=? AND status!='draft'",(d['id'],)).fetchone()
                    d['submission_count']=counts['total'];d['review_count']=counts['waiting'] or 0
                    d['graded_count']=counts['graded'] or 0
                    d['status']='submitted' if d['review_count'] else ('graded' if counts['total'] else ('overdue' if d['due_date']<datetime.now().strftime('%Y-%m-%d %H:%M:%S') else 'pending'))
                rows.append(d)
        return sorted(rows,key=lambda a:(a['status'] in ('graded','submitted'),a['due_date']))
    def paged(rows):
        try: page=max(1,int(request.args.get('page',1)))
        except ValueError: page=1
        pages=max(1,math.ceil(len(rows)/15)); page=min(page,pages)
        return rows[(page-1)*15:page*15],page,pages,len(rows)
    @app.route('/language/<lang>')
    def set_language(lang):
        if lang not in ('ru','kk','en'): abort(404)
        next_url=request.args.get('next','/')
        if not next_url.startswith('/') or next_url.startswith('//') or '\\' in next_url: next_url='/'
        r=redirect(next_url);r.set_cookie('lang',lang,max_age=365*86400,samesite='Lax');return r
    @app.route('/login',methods=['GET','POST'])
    def login():
        if request.method=='POST':
            ip_key='ip:'+ (request.remote_addr or 'local')
            ip_attempt=db().execute('SELECT * FROM login_attempts WHERE address=?',(ip_key,)).fetchone()
            if ip_attempt and ip_attempt['attempts']>=60 and datetime.fromisoformat(ip_attempt['last_attempt'])>datetime.now()-timedelta(minutes=1):
                return render_template('login.html',error=tr('rate_limited'),email=request.form.get('email','')),429,{'Retry-After':'60'}
            address=(request.remote_addr or 'local')+'|'+request.form.get('email','').strip().casefold(); attempt=db().execute('SELECT * FROM login_attempts WHERE address=?',(address,)).fetchone()
            if attempt and attempt['attempts']>=5 and datetime.fromisoformat(attempt['last_attempt'])>datetime.now()-timedelta(minutes=1):
                remaining=max(1,math.ceil(60-(datetime.now()-datetime.fromisoformat(attempt['last_attempt'])).total_seconds()))
                wait={'ru':f'Повторите вход через {remaining} с.','kk':f'{remaining} секундтан кейін қайталаңыз.','en':f'Try again in {remaining} seconds.'}[g.lang]
                return render_template('login.html',error=tr('rate_limited')+' '+wait,email=request.form.get('email','')),429,{'Retry-After':str(remaining)}
            row=db().execute('SELECT * FROM users WHERE email=? AND active=1',(request.form.get('email','').strip(),)).fetchone()
            if row and password_matches(request.form.get('password',''),row['password_hash']):
                token=secrets.token_urlsafe(32); session.clear();session['auth']=token;session.permanent=True
                db().execute('INSERT INTO portal_sessions VALUES(?,?,?)',(token,row['id'],(datetime.now()+timedelta(hours=2)).isoformat()))
                if not row['password_hash'].startswith('scrypt$'): db().execute('UPDATE users SET password_hash=? WHERE id=?',(password_hash(request.form['password']),row['id']))
                db().execute('DELETE FROM login_attempts WHERE address=?',(address,));audit('LOGIN_SUCCESS',user_id=row['id']);db().commit();return redirect(url_for('dashboard'))
            db().execute('INSERT INTO login_attempts VALUES(?,1,?) ON CONFLICT(address) DO UPDATE SET attempts=CASE WHEN last_attempt<? THEN 1 ELSE attempts+1 END,last_attempt=excluded.last_attempt',(address,datetime.now().isoformat(),(datetime.now()-timedelta(minutes=1)).isoformat()))
            db().execute('INSERT INTO login_attempts VALUES(?,1,?) ON CONFLICT(address) DO UPDATE SET attempts=CASE WHEN last_attempt<? THEN 1 ELSE attempts+1 END,last_attempt=excluded.last_attempt',(ip_key,datetime.now().isoformat(),(datetime.now()-timedelta(minutes=1)).isoformat()))
            audit('LOGIN_FAILED');db().commit();return render_template('login.html',error=tr('invalid_credentials'),email=request.form.get('email','')),401
        return render_template('login.html',error=None,email='')
    @app.post('/logout')
    def logout():
        db().execute('DELETE FROM portal_sessions WHERE token=?',(session.get('auth',''),));db().commit();session.clear();return redirect(url_for('login'))
    @app.get('/')
    @app.get('/dashboard')
    @require()
    def dashboard():
        allrows=assignments_for_user();q=request.args.get('q','').strip();status=request.args.get('status','')
        rows=[a for a in allrows if q.casefold() in (a['title']+' '+a['course_code']+' '+(a['description'] or '')).casefold() and (not status or a['status']==status)]
        course_filter=request.args.get('course_id','');sort=request.args.get('sort','due_asc')
        if course_filter:rows=[a for a in rows if str(a['course_id'])==course_filter]
        if request.args.get('instructor_id'):rows=[a for a in rows if str(a['instructor_id'])==request.args['instructor_id']]
        if request.args.get('from'):rows=[a for a in rows if a['due_date'][:10]>=request.args['from']]
        if request.args.get('to'):rows=[a for a in rows if a['due_date'][:10]<=request.args['to']]
        rows.sort(key=lambda a:a['title'].casefold() if sort=='title' else a['due_date'],reverse=sort=='due_desc')
        rows,page,pages,total=paged(rows)
        recent_grades=sorted((a for a in allrows if a['status']=='graded' and a['grade'] is not None),key=lambda a:(a['graded_at'] or a['submitted_at'] or '',a['id']),reverse=True)[:5]
        instructors={c['instructor_id']:c['teacher_name'] for c in course_rows()}
        today=datetime.now().strftime('%Y-%m-%d')
        visible_courses=course_rows();active_ids={c['id'] for c in visible_courses if not c['archived']}
        unfinished=sorted((a for a in allrows if a['course_id'] in active_ids and a['status'] in ('pending','overdue')),key=lambda a:a['due_date'])
        review_queue=[]
        if g.user['role']!='student':
            for c in visible_courses:
                if c['archived']:continue
                review_queue.extend(dict(r) for r in db().execute("SELECT s.id submission_id,s.submitted_at,u.full_name student_name,a.id assignment_id,a.title,c.course_code FROM submissions s JOIN users u ON u.id=s.student_id JOIN assignments a ON a.id=s.assignment_id JOIN courses c ON c.id=a.course_id WHERE a.course_id=? AND s.status='submitted' ORDER BY s.submitted_at",(c['id'],)))
            review_queue.sort(key=lambda r:r['submitted_at'])
        admin_summary={}
        if g.user['role']=='admin':
            admin_summary=dict(db().execute('SELECT (SELECT count(*) FROM users) users,(SELECT count(*) FROM users WHERE active=1) active_users,(SELECT count(*) FROM courses) courses,(SELECT count(*) FROM courses WHERE archived=1) archived_courses,(SELECT count(*) FROM enrollments) enrollments').fetchone())
        hub={'today_tasks':[a for a in unfinished if a['due_date'][:10]==today], 'upcoming_tasks':[a for a in unfinished if a['due_date'][:10]>today][:5], 'overdue_tasks':[a for a in unfinished if a['due_date'][:10]<today], 'review_queue':review_queue[:8], 'review_total':len(review_queue),'admin_summary':admin_summary,'today_date':today}
        return render_template('dashboard.html',hub=hub,recent_grades=recent_grades,instructors=instructors,courses=visible_courses,assignments=rows,stats={'courses':len(visible_courses),'pending':sum(a['status'] in ('pending','overdue') for a in allrows),'submitted':sum(a['status'] in ('submitted','graded') for a in allrows)},q=q,status=status,page=page,pages=pages,total=total)
    @app.get('/courses')
    @require()
    def courses():
        rows=course_rows();q=request.args.get('q','').strip().casefold()
        rows=[c for c in rows if q in (c['course_code']+' '+c['course_name']+' '+c['teacher_name']).casefold() and (not request.args.get('instructor_id') or str(c['instructor_id'])==request.args['instructor_id'])]
        return render_template('courses.html',courses=rows)
    @app.get('/courses/<int:course_id>')
    @require()
    def course(course_id):
        c=course_access(course_id)
        rows=[a for a in assignments_for_user() if a['course_id']==course_id]
        materials=db().execute('SELECT * FROM files WHERE course_id=? AND submission_id IS NULL ORDER BY created_at DESC',(course_id,)).fetchall()
        material_q=request.args.get('q','').strip().casefold()
        material_type=request.args.get('type','').lower().lstrip('.')
        materials=[m for m in materials if material_q in (m['title']+' '+m['original_name']).casefold() and (not material_type or Path(m['original_name']).suffix.lower()=='.'+material_type)]
        if request.args.get('tab')=='grades':rows=[a for a in rows if a['status']=='graded']
        upcoming=sorted((a for a in rows if a['due_date']>=datetime.now().strftime('%Y-%m-%d %H:%M:%S') and a['status'] not in ('submitted','graded')),key=lambda a:a['due_date'])
        progress=next((item['progress'] for item in course_rows() if item['id']==course_id),0)
        return render_template('course.html',course=c,assignments=rows,materials=materials,announcements=db().execute('SELECT a.*,u.full_name FROM announcements a JOIN users u ON u.id=a.author_id WHERE course_id=? ORDER BY a.id DESC',(course_id,)).fetchall(),next_assignment=upcoming[0] if upcoming else None,course_progress=progress,tab=request.args.get('tab','overview'),can_edit=g.user['role']!='student' and not c['archived'])
    @app.get('/assignments/<int:assignment_id>')
    @require()
    def assignment(assignment_id):
        a=assignment_access(assignment_id)
        sub=db().execute('SELECT * FROM submissions WHERE assignment_id=? AND student_id=?',(assignment_id,g.user['id'])).fetchone()
        attachments=db().execute('SELECT * FROM files WHERE submission_id=?',(sub['id'],)).fetchall() if sub else []
        draft=db().execute('SELECT * FROM assignment_drafts WHERE user_id=? AND assignment_id=?',(g.user['id'],assignment_id)).fetchone()
        history=db().execute('SELECT h.*,u.full_name FROM assignment_history h LEFT JOIN users u ON u.id=h.actor_id WHERE assignment_id=? ORDER BY h.id DESC LIMIT 100',(assignment_id,)).fetchall()
        if g.user['role']=='student':history=[h for h in history if h['actor_id']==g.user['id'] or h['event'] in ('assignment_updated','deadline_changed')]
        return render_template('assignment.html',assignment=a,submission=sub,attachments=attachments,draft=draft,history=history,can_submit=g.user['role']=='student' and not course_access(a['course_id'])['archived'] and not (sub and sub['status']=='graded'),can_grade=g.user['role']!='student' and not course_access(a['course_id'])['archived'])
    def save_upload(cid,submission_id=None):
        f=request.files.get('file')
        if not f or not f.filename: return
        filename=secure_filename(f.filename)
        if not filename or Path(filename).suffix.lower() not in ('.pdf','.txt','.png','.jpg','.jpeg','.webp','.zip','.docx','.pptx','.xlsx','.csv','.py','.cpp'):
            abort(400,description='invalid_file')
        stored=secrets.token_hex(24)+Path(filename).suffix.lower()
        f.save(Path(app.config['UPLOAD_FOLDER'])/stored)
        try: db().execute('INSERT INTO files(course_id,submission_id,owner_id,title,original_name,stored_name) VALUES(?,?,?,?,?,?)',(cid,submission_id,g.user['id'],request.form.get('title',filename).strip() or filename,filename,stored))
        except Exception:
            (Path(app.config['UPLOAD_FOLDER'])/stored).unlink(missing_ok=True);raise
    @app.post('/assignments/<int:assignment_id>/submit')
    @require('student')
    def submit_assignment(assignment_id):
        a=assignment_access(assignment_id);text=request.form.get('submission_text','').strip()
        upload=request.files.get('file')
        if upload and upload.filename:
            position=upload.stream.tell()
            if not upload.stream.read(1):
                flash({'ru':'Файл пуст. Выберите непустой файл.','kk':'Файл бос. Басқа файлды таңдаңыз.','en':'The file is empty. Choose a non-empty file.'}[g.lang],'error')
                return assignment(assignment_id),400
            upload.stream.seek(position)
            suffix=Path(secure_filename(upload.filename)).suffix.lower()
            if suffix not in ('.pdf','.txt','.png','.jpg','.jpeg','.webp','.zip','.docx','.pptx','.xlsx','.csv','.py','.cpp'):
                message={'ru':'Этот тип файла не поддерживается. Выберите файл из списка под полем загрузки.','kk':'Бұл файл түріне қолдау көрсетілмейді. Жүктеу өрісінің астындағы тізімнен файл таңдаңыз.','en':'This file type is not supported. Choose a file type listed below the upload field.'}[g.lang]
                flash(message,'error')
                return assignment(assignment_id),400
        if not text and not request.files.get('file'): flash(tr('answer_required'),'error');return redirect(url_for('assignment',assignment_id=assignment_id))
        old=db().execute('SELECT * FROM submissions WHERE assignment_id=? AND student_id=?',(assignment_id,g.user['id'])).fetchone()
        if old and old['status']=='graded': abort(403)
        db().execute("INSERT INTO submissions(assignment_id,student_id,submission_text,status,submitted_at) VALUES(?,?,?,'submitted',CURRENT_TIMESTAMP) ON CONFLICT(assignment_id,student_id) DO UPDATE SET submission_text=excluded.submission_text,status='submitted',submitted_at=CURRENT_TIMESTAMP",(assignment_id,g.user['id'],text))
        subid=db().execute('SELECT id FROM submissions WHERE assignment_id=? AND student_id=?',(assignment_id,g.user['id'])).fetchone()[0]
        save_upload(a['course_id'],subid)
        db().execute('DELETE FROM assignment_drafts WHERE user_id=? AND assignment_id=?',(g.user['id'],assignment_id))
        db().execute('INSERT INTO assignment_history(assignment_id,actor_id,event) VALUES(?,?,?)',(assignment_id,g.user['id'],'work_submitted'))
        audit('SUBMIT_ASSIGNMENT',str(assignment_id));notify(a['instructor_id'],'new_submission',a['title']);db().commit();flash(tr('answer_saved'),'success');return redirect(url_for('assignment',assignment_id=assignment_id))
    @app.post('/courses/<int:course_id>/assignments')
    @require('teacher','admin')
    def create_assignment(course_id): return persist_assignment(course_id,None)
    @app.post('/assignments/<int:assignment_id>/edit')
    @require('teacher','admin')
    def update_assignment(assignment_id):
        a=assignment_access(assignment_id,True);return persist_assignment(a['course_id'],assignment_id)
    def persist_assignment(cid,aid):
        course_access(cid,True);title=request.form.get('title','').strip();description=request.form.get('description','').strip()
        previous=db().execute('SELECT due_date FROM assignments WHERE id=?',(aid,)).fetchone() if aid else None
        try: due=datetime.fromisoformat(request.form.get('due_date','')).strftime('%Y-%m-%d %H:%M:%S');points=float(request.form.get('max_points','100'));assert title and len(title)<=150 and math.isfinite(points) and 0<points<=100
        except (ValueError,AssertionError): flash(tr('invalid_data'),'error');return redirect(url_for('course',course_id=cid))
        if aid: db().execute('UPDATE assignments SET title=?,description=?,due_date=?,max_points=? WHERE id=?',(title,description,due,points,aid))
        else:
            cur=db().execute('INSERT INTO assignments(course_id,title,description,due_date,max_points) VALUES(?,?,?,?,?)',(cid,title,description,due,points));aid=cur.lastrowid
        event='deadline_changed' if previous and previous['due_date']!=due else 'assignment_updated'
        db().execute('INSERT INTO assignment_history(assignment_id,actor_id,event,details) VALUES(?,?,?,?)',(aid,g.user['id'],event,due))
        for student in db().execute('SELECT student_id FROM enrollments WHERE course_id=?',(cid,)): notify(student[0],event,title)
        audit('SAVE_ASSIGNMENT',str(aid));db().commit();flash(tr('saved'),'success');return redirect(url_for('course',course_id=cid))
    @app.post('/courses/<int:course_id>/materials')
    @require('teacher','admin')
    def upload_material(course_id):
        course_access(course_id,True);save_upload(course_id);audit('UPLOAD_MATERIAL',str(course_id));db().commit();flash(tr('saved'),'success');return redirect(url_for('course',course_id=course_id))
    @app.get('/files/<int:file_id>')
    @require()
    def download(file_id):
        f=db().execute('SELECT * FROM files WHERE id=?',(file_id,)).fetchone()
        if not f: abort(404)
        course_access(f['course_id'])
        if f['submission_id'] and g.user['role']=='student' and f['owner_id']!=g.user['id']: abort(403)
        path=Path(app.config['UPLOAD_FOLDER'])/f['stored_name']
        if not path.is_file(): abort(404)
        return send_file(path,as_attachment=True,download_name=f['original_name'])
    @app.get('/review')
    @require('teacher','admin')
    def review():
        sql='SELECT s.*,u.full_name AS student_name,u.student_id,a.title,a.max_points,c.course_code FROM submissions s JOIN users u ON u.id=s.student_id JOIN assignments a ON a.id=s.assignment_id JOIN courses c ON c.id=a.course_id WHERE s.status != ?';args=['draft']
        if g.user['role']=='teacher':sql+=' AND c.instructor_id=?';args.append(g.user['id'])
        q=request.args.get('q','').strip()
        if q:sql+=' AND (u.full_name LIKE ? OR a.title LIKE ?)';args.extend(['%'+q+'%']*2)
        status=request.args.get('status','')
        if status in ('submitted','graded'):sql+=' AND s.status=?';args.append(status)
        course_id=request.args.get('course_id','')
        if course_id.isdigit():sql+=' AND c.id=?';args.append(int(course_id))
        rows=db().execute(sql+' ORDER BY s.submitted_at DESC,s.id DESC',args).fetchall()
        focus=request.args.get('focus','')
        if focus.isdigit():
            index=next((i for i,row in enumerate(rows) if row['id']==int(focus)),None)
            if index is not None:
                return redirect(url_for('review',q=q,status=status,course_id=course_id,page=index//15+1,_anchor='submission-'+focus))
        rows,page,pages,total=paged(rows)
        attachments={r['id']:db().execute('SELECT * FROM files WHERE submission_id=?',(r['id'],)).fetchall() for r in rows}
        return render_template('review.html',submissions=rows,attachments=attachments,q=q,status=status,review_courses=course_rows(),page=page,pages=pages,total=total)
    @app.post('/submissions/<int:submission_id>/grade')
    @require('teacher','admin')
    def grade_submission(submission_id):
        sub=db().execute('SELECT s.*,a.max_points FROM submissions s JOIN assignments a ON a.id=s.assignment_id WHERE s.id=?',(submission_id,)).fetchone()
        if not sub:abort(404)
        assignment_access(sub['assignment_id'],True)
        return_args={key:request.form.get(key,'') for key in ('q','status','course_id','page')}
        destination=url_for('review',**return_args,_anchor='submission-'+str(submission_id))
        try: grade=float(request.form.get('grade',''));assert math.isfinite(grade) and 0<=grade<=sub['max_points'] and sub['status']!='draft'
        except (ValueError,AssertionError):flash(tr('invalid_grade'),'error');return redirect(destination)
        db().execute("UPDATE submissions SET grade=?,feedback=?,status='graded',graded_at=CURRENT_TIMESTAMP WHERE id=?",(grade,request.form.get('feedback','').strip(),submission_id));notify(sub['student_id'],'work_graded',str(grade));audit('GRADE_SUBMISSION',str(submission_id));db().commit()
        student=db().execute('SELECT full_name FROM users WHERE id=?',(sub['student_id'],)).fetchone()
        flash(tr('saved')+' '+student['full_name']+' · '+str(grade)+' / '+str(sub['max_points']),'success');return redirect(destination)
    @app.route('/notifications',methods=['GET','POST'])
    @require()
    def notifications():
        if request.method=='POST':
            notification_id=request.form.get('notification_id')
            if notification_id:
                try: notification_id=int(notification_id)
                except ValueError: abort(400)
                db().execute('UPDATE notifications SET is_read=1 WHERE id=? AND user_id=?',(notification_id,g.user['id']))
            else:
                db().execute('UPDATE notifications SET is_read=1 WHERE user_id=?',(g.user['id'],))
            db().commit();return redirect(url_for('notifications'))
        return render_template('notifications.html',notifications=db().execute('SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 100',(g.user['id'],)).fetchall())
    @app.get('/admin')
    @require('admin')
    def admin():
        users=db().execute('SELECT id,student_id,email,full_name,role,active FROM users ORDER BY role,full_name').fetchall()
        q=request.args.get('q','').strip()
        filtered=[u for u in users if q.casefold() in (u['full_name']+' '+u['email']+' '+u['student_id']).casefold()]
        user_rows,page,pages,total=paged(filtered)
        return render_template('admin.html',users=users,user_rows=user_rows,q=q,page=page,pages=pages,total=total,courses=course_rows(),enrollments=db().execute('SELECT e.*,u.full_name,c.course_code FROM enrollments e JOIN users u ON u.id=e.student_id JOIN courses c ON c.id=e.course_id ORDER BY e.id DESC LIMIT 100').fetchall(),audit_logs=db().execute('SELECT a.*,u.full_name FROM audit_logs a LEFT JOIN users u ON u.id=a.user_id ORDER BY a.id DESC LIMIT 100').fetchall(),stats={name:db().execute('SELECT count(*) FROM '+name).fetchone()[0] for name in ('users','courses','enrollments','assignments','submissions')})
    @app.post('/admin/action')
    @require('admin')
    def admin_action():
        f=request.form;action=f.get('action')
        if action=='create_user':
            problem=None
            if not f.get('full_name','').strip(): problem='name'
            elif not f.get('student_id','').strip(): problem='student_id'
            elif not f.get('email','').strip().endswith('@astanait.edu.kz'): problem='email'
            elif len(f.get('password',''))<10: problem='password'
            elif f.get('role') not in ('student','teacher','admin'): problem='role'
            elif db().execute('SELECT 1 FROM users WHERE email=? OR student_id=?',(f.get('email','').strip(),f.get('student_id','').strip())).fetchone(): problem='duplicate'
            if problem:
                messages={
                    'ru':{'name':'Введите имя пользователя.','student_id':'Введите ID пользователя.','email':'Email должен заканчиваться на @astanait.edu.kz.','password':'Пароль должен содержать не менее 10 символов.','role':'Выберите допустимую роль.','duplicate':'Пользователь с таким email или ID уже существует.'},
                    'kk':{'name':'Пайдаланушы атын енгізіңіз.','student_id':'Пайдаланушы ID енгізіңіз.','email':'Email @astanait.edu.kz доменімен аяқталуы керек.','password':'Құпиясөз кемінде 10 таңбадан тұруы керек.','role':'Жарамды рөлді таңдаңыз.','duplicate':'Бұл email немесе ID бар пайдаланушы бұрыннан бар.'},
                    'en':{'name':'Enter the user name.','student_id':'Enter the user ID.','email':'Email must end with @astanait.edu.kz.','password':'The password must contain at least 10 characters.','role':'Choose a valid role.','duplicate':'A user with this email or ID already exists.'}}
                flash(messages[g.lang][problem],'error')
                return admin(),400
        try:
            if action=='create_user':
                assert f['role'] in ('student','teacher','admin') and len(f['password'])>=10 and f['email'].endswith('@astanait.edu.kz') and f['full_name'].strip()
                db().execute('INSERT INTO users(student_id,email,password_hash,full_name,role) VALUES(?,?,?,?,?)',(f['student_id'].strip(),f['email'].strip(),password_hash(f['password']),f['full_name'].strip(),f['role']))
            elif action=='update_user':
                uid=int(f['user_id']);role=f['role'];active=int(f.get('active','1'));assert role in ('student','teacher','admin') and active in (0,1)
                if uid==g.user['id'] and (role!='admin' or not active):raise ValueError()
                db().execute('UPDATE users SET full_name=?,role=?,active=? WHERE id=?',(f['full_name'].strip(),role,active,uid));db().execute('DELETE FROM portal_sessions WHERE user_id=?',(uid,))
            elif action in ('create_course','update_course'):
                teacher=db().execute("SELECT id FROM users WHERE id=? AND role='teacher' AND active=1",(int(f['instructor_id']),)).fetchone();assert teacher and f['course_code'].strip() and f['course_name'].strip()
                args=(f['course_code'].strip(),f['course_name'].strip(),teacher['id'],int(f['credits']))
                if action=='create_course':db().execute('INSERT INTO courses(course_code,course_name,instructor_id,credits) VALUES(?,?,?,?)',args)
                else:
                    course_access(int(f['course_id']),True)
                    db().execute('UPDATE courses SET course_code=?,course_name=?,instructor_id=?,credits=? WHERE id=?',args+(int(f['course_id']),))
            elif action=='enroll':
                course_access(int(f['course_id']),True)
                student=db().execute("SELECT id FROM users WHERE id=? AND role='student' AND active=1",(int(f['student_id']),)).fetchone();assert student
                db().execute('INSERT OR IGNORE INTO enrollments(student_id,course_id) VALUES(?,?)',(student['id'],int(f['course_id'])))
            else:abort(400)
        except (ValueError,KeyError,AssertionError):db().rollback();flash(tr('invalid_data'),'error');return redirect(url_for('admin'))
        audit('ADMIN_'+action.upper());db().commit();flash(tr('saved'),'success');return redirect(url_for('admin'))
    @app.post('/admin/backup')
    @require('admin')
    def backup():
        folder=BASE/'backups';folder.mkdir(exist_ok=True);path=folder/('portal_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.sqlite')
        dest=sqlite3.connect(path);db().backup(dest);dest.close();audit('BACKUP_CREATED',path.name);db().commit()
        return send_file(path,as_attachment=True,download_name=path.name)
    from portal_features import register_features
    register_features(app, db, require, course_access, assignment_access, course_rows, assignments_for_user, audit, notify, tr, password_hash, password_matches)
    return app

def run():
    create_app().run(host=os.environ.get('HOST','127.0.0.1'),port=int(os.environ.get('PORT','8002')),debug=False)
if __name__=='__main__':run()
