"""Meaningful permission and persistence regression checks; working DB is never edited."""
import unittest, tempfile, shutil, sqlite3, io
from pathlib import Path
from app import create_app, BASE

class PortalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        shutil.copy2(BASE/'aitu_lms.sqlite',self.root/'test.sqlite')
        self.app=create_app({'TESTING':True,'DATABASE':str(self.root/'test.sqlite'),'UPLOAD_FOLDER':str(self.root/'uploads')})
        self.client=self.app.test_client()
    def tearDown(self):self.tmp.cleanup()
    def token(self,client=None):
        client=client or self.client
        with client.session_transaction() as s:s['csrf']='test-csrf'
        return 'test-csrf'
    def post(self,path,data=None,client=None):
        c=client or self.client;payload=dict(data or {});payload['csrf']=self.token(c)
        return c.post(path,data=payload)
    def login(self,role='student',client=None):
        creds={'student':('261875@astanait.edu.kz','Alikhan2026!'),'teacher':('diana.kazbekova@astanait.edu.kz','DianaPass2026!'),'admin':('admin.lms@astanait.edu.kz','RootAdminSecure99#')}
        email,password=creds[role];return self.post('/login',{'email':email,'password':password},client)
    def sql(self,query,args=()):
        c=sqlite3.connect(self.root/'test.sqlite')
        try:return c.execute(query,args).fetchall()
        finally:c.close()
    def test_admin_invalid_user_preserves_safe_fields_and_error_headings(self):
        self.login('admin')
        response=self.post('/admin/action',{'action':'create_user','student_id':'299998','full_name':'Preserved Audit User','email':'wrong@example.com','password':'DoNotEchoSecret!','role':'teacher'})
        self.assertEqual(response.status_code,400)
        page=response.get_data(as_text=True)
        self.assertIn('value="Preserved Audit User"',page)
        self.assertIn('value="wrong@example.com"',page)
        self.assertIn('open><summary>',page)
        self.assertIn('@astanait.edu.kz',page)
        self.assertNotIn('DoNotEchoSecret!',page)
        self.assertEqual(self.sql("SELECT count(*) FROM users WHERE student_id='299998'")[0][0],0)
        missing=self.client.get('/missing-audit-page').get_data(as_text=True)
        self.assertIn('Страница не найдена',missing)
    def test_csrf_and_authentication_migration(self):
        self.assertEqual(self.client.post('/login',data={}).status_code,400)
        self.assertEqual(self.post('/login',{'email':"' OR 1=1 --",'password':'x'}).status_code,401)
        self.assertEqual(self.login().status_code,302)
        self.assertTrue(self.sql('SELECT password_hash FROM users WHERE student_id=?',('261875',))[0][0].startswith('scrypt$'))
        self.assertEqual(self.client.get('/admin').status_code,403)
        self.assertEqual(self.client.get('/quick_login?role=admin').status_code,404)
    def test_empty_upload_is_rejected_without_changing_submission(self):
        self.login()
        aid=self.sql("SELECT a.id FROM assignments a JOIN enrollments e ON e.course_id=a.course_id JOIN users u ON u.id=e.student_id LEFT JOIN submissions s ON s.assignment_id=a.id AND s.student_id=u.id WHERE u.student_id='261875' AND (s.status IS NULL OR s.status!='graded') LIMIT 1")[0][0]
        before=self.sql('SELECT * FROM submissions WHERE assignment_id=?',(aid,))
        files_before=self.sql('SELECT count(*) FROM files')[0][0]
        response=self.post(f'/assignments/{aid}/submit',{'submission_text':'','file':(io.BytesIO(b''),'empty.txt')})
        self.assertEqual(response.status_code,400)
        self.assertIn('Файл пуст',response.get_data(as_text=True))
        self.assertEqual(self.sql('SELECT * FROM submissions WHERE assignment_id=?',(aid,)),before)
        self.assertEqual(self.sql('SELECT count(*) FROM files')[0][0],files_before)
    def test_ip_limit_catches_attempts_across_different_emails(self):
        for index in range(60):
            response=self.post('/login',{'email':f'audit-{index}@astanait.edu.kz','password':'wrong'})
            self.assertEqual(response.status_code,401)
        blocked=self.post('/login',{'email':'next@astanait.edu.kz','password':'wrong'})
        self.assertEqual(blocked.status_code,429)
        self.assertGreater(int(blocked.headers['Retry-After']),0)
        other=self.app.test_client()
        response=other.post('/login',data={'email':'next@astanait.edu.kz','password':'wrong','csrf':self.token(other)},environ_overrides={'REMOTE_ADDR':'192.0.2.5'})
        self.assertEqual(response.status_code,401)
    def test_static_cache_and_specific_page_titles(self):
        static=self.client.get('/static/app.css')
        self.assertIn('public',static.headers['Cache-Control'])
        self.assertIn('max-age=',static.headers['Cache-Control'])
        static.close()
        self.assertEqual(self.client.get('/login').headers['Cache-Control'],'no-store')
        self.login('admin')
        self.assertIn('<title>Аналитика · AITU LMS</title>',self.client.get('/analytics').get_data(as_text=True))
        self.assertIn('<title>Импорт пользователей · AITU LMS</title>',self.client.get('/admin/import').get_data(as_text=True))
    def test_submission_persistence_files_and_object_permissions(self):
        self.login()
        aid=self.sql("SELECT a.id FROM assignments a JOIN enrollments e ON e.course_id=a.course_id JOIN users u ON u.id=e.student_id LEFT JOIN submissions s ON s.assignment_id=a.id AND s.student_id=u.id WHERE u.student_id='261875' AND (s.status IS NULL OR s.status!='graded') LIMIT 1")[0][0]
        self.assertEqual(self.post(f'/assignments/{aid}/submit',{'submission_text':'Persistent test answer','file':(io.BytesIO(b'test attachment'),'answer.txt')}).status_code,302)
        self.assertEqual(self.sql("SELECT submission_text FROM submissions WHERE assignment_id=? AND student_id=(SELECT id FROM users WHERE student_id='261875')",(aid,))[0][0],'Persistent test answer')
        fid=self.sql('SELECT max(id) FROM files')[0][0]
        response=self.client.get(f'/files/{fid}')
        self.assertEqual(response.data,b'test attachment');response.close()
        self.assertEqual(self.client.get('/static/../aitu_lms.sqlite').status_code,404)
        alien=self.sql("SELECT a.id FROM assignments a WHERE a.course_id NOT IN (SELECT course_id FROM enrollments WHERE student_id=(SELECT id FROM users WHERE student_id='261875')) LIMIT 1")
        if alien:self.assertEqual(self.post(f'/assignments/{alien[0][0]}/submit',{'submission_text':'forbidden'}).status_code,403)
    def test_teacher_grade_validation_and_isolation(self):
        self.login('teacher')
        own=self.sql("SELECT s.id FROM submissions s JOIN assignments a ON a.id=s.assignment_id JOIN courses c ON c.id=a.course_id JOIN users u ON u.id=c.instructor_id WHERE u.email='diana.kazbekova@astanait.edu.kz' AND s.status!='draft' LIMIT 1")[0][0]
        self.assertEqual(self.post(f'/submissions/{own}/grade',{'grade':'nan'}).status_code,302)
        self.assertEqual(self.post(f'/submissions/{own}/grade',{'grade':'150'}).status_code,302)
        self.assertEqual(self.post(f'/submissions/{own}/grade',{'grade':'0','feedback':'Verified zero'}).status_code,302)
        self.assertEqual(self.sql('SELECT grade,feedback FROM submissions WHERE id=?',(own,))[0],(0,'Verified zero'))
        foreign=self.sql("SELECT s.id FROM submissions s JOIN assignments a ON a.id=s.assignment_id JOIN courses c ON c.id=a.course_id JOIN users u ON u.id=c.instructor_id WHERE u.email!='diana.kazbekova@astanait.edu.kz' LIMIT 1")[0][0]
        self.assertEqual(self.post(f'/submissions/{foreign}/grade',{'grade':'50'}).status_code,403)
        self.assertEqual(self.login('student').status_code,302)
    def test_teacher_create_material_and_notifications(self):
        self.login('teacher');cid=self.sql("SELECT c.id FROM courses c JOIN users u ON u.id=c.instructor_id WHERE u.email='diana.kazbekova@astanait.edu.kz' LIMIT 1")[0][0]
        r=self.post(f'/courses/{cid}/assignments',{'title':'New test task','description':'Run the checks','due_date':'2027-01-01T15:00','max_points':'100'})
        self.assertEqual(r.status_code,302);self.assertEqual(self.sql("SELECT count(*) FROM assignments WHERE title='New test task'")[0][0],1)
        self.assertGreater(self.sql('SELECT count(*) FROM notifications')[0][0],0)
        self.assertEqual(self.post(f'/courses/{cid}/materials',{'title':'Test notes','file':(io.BytesIO(b'notes'),'notes.txt')}).status_code,302)
        self.assertEqual(self.post(f'/courses/{cid}/materials',{'file':(io.BytesIO(b'bad'),'unsafe.html')}).status_code,400)
    def test_admin_create_enroll_and_logout_invalidation(self):
        self.login('admin')
        self.assertEqual(self.post('/admin/action',{'action':'create_user','student_id':'299999','email':'299999@astanait.edu.kz','password':'Temporary2027!','full_name':'Audit Student','role':'student'}).status_code,302)
        uid=self.sql("SELECT id FROM users WHERE student_id='299999'")[0][0];cid=self.sql('SELECT id FROM courses LIMIT 1')[0][0]
        self.post('/admin/action',{'action':'enroll','student_id':uid,'course_id':cid})
        self.assertEqual(self.sql('SELECT count(*) FROM enrollments WHERE student_id=?',(uid,))[0][0],1)
        with self.client.session_transaction() as s:old=s['auth']
        self.post('/logout');self.assertEqual(self.sql('SELECT count(*) FROM portal_sessions WHERE token=?',(old,))[0][0],0)
    def test_locales_and_open_redirect(self):
        self.assertEqual(self.client.get('/language/kk?next=//evil.example').location,'/')
        self.assertEqual(self.client.get('/language/de').status_code,404)
        for lang in ('ru','kk','en'):
            self.client.get('/language/'+lang)
            self.assertEqual(self.client.get('/login').status_code,200)

    def test_notification_read_isolation(self):
        self.login()
        uid=self.sql("SELECT id FROM users WHERE student_id='261875'")[0][0]
        con=sqlite3.connect(self.root/'test.sqlite')
        try:
            con.execute('DELETE FROM notifications')
            con.executemany('INSERT INTO notifications(id,user_id,title) VALUES(?,?,?)',[(1,uid,'first'),(2,uid,'second'),(3,1,'foreign')]);con.commit()
        finally:con.close()
        self.assertEqual(self.post('/notifications',{'notification_id':'1'}).status_code,302)
        self.assertEqual(self.sql('SELECT id,is_read FROM notifications ORDER BY id'),[(1,1),(2,0),(3,0)])
        self.post('/notifications',{'notification_id':'3'})
        self.assertEqual(self.sql('SELECT is_read FROM notifications WHERE id=3')[0][0],0)
        self.assertEqual(self.post('/notifications',{'notification_id':'invalid'}).status_code,400)
        self.post('/notifications',{'action':'mark_all'})
        self.assertEqual(self.sql('SELECT id,is_read FROM notifications ORDER BY id'),[(1,1),(2,1),(3,0)])

    def test_all_role_pages_render(self):
        for role in ('student','teacher','admin'):
            self.login(role)
            for lang in ('ru','kk','en'):
                self.client.get('/language/'+lang)
                for path in ('/dashboard','/courses','/notifications'):
                    with self.subTest(role=role,lang=lang,path=path):self.assertEqual(self.client.get(path).status_code,200)
                if role=='student':
                    cid=self.sql("SELECT e.course_id FROM enrollments e JOIN users u ON u.id=e.student_id WHERE u.student_id='261875' LIMIT 1")[0][0]
                elif role=='teacher':
                    cid=self.sql("SELECT c.id FROM courses c JOIN users u ON u.id=c.instructor_id WHERE u.email='diana.kazbekova@astanait.edu.kz' LIMIT 1")[0][0]
                else:cid=self.sql('SELECT id FROM courses LIMIT 1')[0][0]
                self.assertEqual(self.client.get(f'/courses/{cid}').status_code,200)
                aid=self.sql('SELECT id FROM assignments WHERE course_id=? LIMIT 1',(cid,))[0][0]
                self.assertEqual(self.client.get(f'/assignments/{aid}').status_code,200)
                if role!='student':self.assertEqual(self.client.get('/review').status_code,200)
                if role=='admin':self.assertEqual(self.client.get('/admin').status_code,200)

    def test_draft_conflicts_and_profile_permissions(self):
        self.login()
        aid=self.sql("SELECT a.id FROM assignments a JOIN enrollments e ON e.course_id=a.course_id JOIN users u ON u.id=e.student_id LEFT JOIN submissions s ON s.assignment_id=a.id AND s.student_id=u.id WHERE u.student_id='261875' AND (s.status IS NULL OR s.status!='graded') LIMIT 1")[0][0]
        self.assertEqual(self.post(f'/assignments/{aid}/draft',{'body':'draft','revision':0}).json['revision'],1)
        self.assertEqual(self.post(f'/assignments/{aid}/draft',{'body':'stale','revision':0}).status_code,409)
        self.assertEqual(self.post(f'/assignments/{aid}/draft',{'body':'new','revision':1}).json['revision'],2)
        self.assertEqual(self.post('/profile',{'specialty':'Software','group_name':'SE','study_year':'2','avatar':''}).status_code,302)
        self.assertEqual(self.sql('SELECT specialty FROM profiles')[0][0],'Software')
        self.assertEqual(self.post('/admin/semesters',{'name':'forbidden'}).status_code,403)

    def test_archive_blocks_student_writes_and_restores(self):
        self.login()
        aid,cid=self.sql("SELECT a.id,a.course_id FROM assignments a JOIN enrollments e ON e.course_id=a.course_id JOIN users u ON u.id=e.student_id LEFT JOIN submissions s ON s.assignment_id=a.id AND s.student_id=u.id WHERE u.student_id='261875' AND (s.status IS NULL OR s.status!='graded') LIMIT 1")[0]
        self.login('admin');self.assertEqual(self.post(f'/courses/{cid}/archive',{'archived':'1'}).status_code,302)
        self.login()
        self.assertEqual(self.client.get(f'/courses/{cid}').status_code,200)
        self.assertEqual(self.post(f'/assignments/{aid}/draft',{'body':'blocked','revision':0}).status_code,403)
        self.assertEqual(self.post(f'/assignments/{aid}/submit',{'submission_text':'blocked'}).status_code,403)
        self.login('admin');self.assertEqual(self.post(f'/courses/{cid}/archive',{'archived':'0'}).status_code,302)
        self.login();self.assertEqual(self.post(f'/assignments/{aid}/draft',{'body':'allowed','revision':0}).status_code,200)
        self.assertEqual(self.client.get('/calendar?month=9999-12').status_code,400)

    def test_dashboard_grade_data_and_filters(self):
        from flask import template_rendered
        captured=[]
        def capture(sender, template, context, **extra):captured.append(context)
        template_rendered.connect(capture,self.app)
        try:
            self.login()
            self.client.get('/dashboard')
            context=captured[-1]
            self.assertIn('recent_grades',context)
            self.assertTrue(all(a['status']=='graded' and a['grade'] is not None for a in context['recent_grades']))
            self.client.get('/dashboard?instructor_id=999999')
            self.assertEqual(captured[-1]['total'],0)
            cid=self.sql("SELECT e.course_id FROM enrollments e JOIN users u ON u.id=e.student_id WHERE u.student_id='261875' LIMIT 1")[0][0]
            self.client.get(f'/courses/{cid}?tab=materials&q=nonexistent-material')
            self.assertEqual(captured[-1]['materials'],[])
            self.client.get(f'/courses/{cid}?tab=materials&type=pdf')
            self.assertTrue(all(m['original_name'].lower().endswith('.pdf') for m in captured[-1]['materials']))
            self.login('teacher');self.client.get('/dashboard')
            for a in captured[-1]['assignments']:
                from datetime import datetime
                expected='submitted' if a['review_count'] else ('graded' if a['submission_count'] else ('overdue' if a['due_date']<datetime.now().strftime('%Y-%m-%d %H:%M:%S') else 'pending'))
                self.assertEqual(a['status'],expected)
                self.assertGreaterEqual(a['graded_count'],0)
            for c in captured[-1]['courses']:self.assertTrue(0<=c['progress']<=100)
        finally:template_rendered.disconnect(capture,self.app)

    def test_dashboard_action_hub_is_role_scoped(self):
        from flask import template_rendered
        captured=[]
        def capture(sender,template,context,**extra):captured.append(context)
        template_rendered.connect(capture,self.app)
        try:
            self.login('student');self.client.get('/dashboard');context=captured[-1];hub=context['hub']
            allowed={c['id'] for c in context['courses'] if not c['archived']}
            for bucket in ('today_tasks','upcoming_tasks','overdue_tasks'):
                for task in hub[bucket]:
                    self.assertIn(task['course_id'],allowed);self.assertIn(task['status'],('pending','overdue'))
            self.assertEqual(hub['review_queue'],[]);self.assertEqual(hub['admin_summary'],{})
            self.assertTrue(all(c['visual_key'] for c in context['courses']))
            self.login('teacher');self.client.get('/dashboard');hub=captured[-1]['hub']
            self.assertEqual(hub['admin_summary'],{})
            self.assertGreaterEqual(hub['review_total'],len(hub['review_queue']))
            self.login('admin');self.client.get('/dashboard')
            self.assertEqual(captured[-1]['hub']['admin_summary']['users'],self.sql('SELECT count(*) FROM users')[0][0])
        finally:template_rendered.disconnect(capture,self.app)

    def test_archived_teacher_admin_writes_blocked(self):
        self.login('teacher')
        cid=self.sql("SELECT c.id FROM courses c JOIN users u ON u.id=c.instructor_id WHERE u.email='diana.kazbekova@astanait.edu.kz' LIMIT 1")[0][0]
        self.login('admin');self.post(f'/courses/{cid}/archive',{'archived':'1'})
        for role in ('teacher','admin'):
            self.login(role)
            self.assertEqual(self.post(f'/courses/{cid}/assignments',{'title':'blocked'}).status_code,403)
            self.assertEqual(self.post(f'/courses/{cid}/announcements',{'title':'blocked','body':'blocked'}).status_code,403)
            self.assertEqual(self.post(f'/courses/{cid}/materials',{'file':(io.BytesIO(b'blocked'),'blocked.txt')}).status_code,403)
        uid=self.sql("SELECT id FROM users WHERE role='student' LIMIT 1")[0][0]
        self.assertEqual(self.post('/admin/action',{'action':'enroll','student_id':uid,'course_id':cid}).status_code,403)

    def test_feature_pages_locales(self):
        for role in ('student','teacher','admin'):
            self.login(role)
            for lang in ('ru','kk','en'):
                self.client.get('/language/'+lang)
                for path in ('/profile','/security','/calendar'):
                    with self.subTest(role=role,lang=lang,path=path):self.assertEqual(self.client.get(path).status_code,200)
                self.assertEqual(self.client.get('/analytics').status_code,403 if role=='student' else 200)
                self.assertEqual(self.client.get('/admin/import').status_code,200 if role=='admin' else 403)

    def test_csv_preview_commit_and_recovery_single_use(self):
        self.login('admin')
        payload=b'student_id,email,full_name,role,password\n299998,299998@astanait.edu.kz,Imported User,student,TemporaryPass2027!\n'
        self.assertEqual(self.post('/admin/import',{'file':(io.BytesIO(payload),'users.csv')}).status_code,200)
        token=self.sql('SELECT token FROM import_previews')[0][0]
        self.assertEqual(self.sql("SELECT count(*) FROM users WHERE student_id='299998'")[0][0],0)
        self.assertEqual(self.post('/admin/import',{'preview_token':token}).status_code,302)
        self.assertEqual(self.post('/admin/import',{'preview_token':token}).status_code,400)
        uid=self.sql("SELECT id FROM users WHERE student_id='299998'")[0][0]
        import hashlib
        con=sqlite3.connect(self.root/'test.sqlite');con.execute('INSERT INTO recovery_tokens VALUES(?,?,?)',(hashlib.sha256(b'test-recovery').hexdigest(),uid,'2099-01-01'));con.commit();con.close()
        self.assertEqual(self.post('/recover',{'token':'test-recovery','new_password':'ChangedSecure2027!'}).status_code,302)
        self.assertEqual(self.post('/recover',{'token':'test-recovery','new_password':'ChangedSecure2027!'}).status_code,400)

if __name__=='__main__':unittest.main(verbosity=2)
