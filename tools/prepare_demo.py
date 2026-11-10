"""Refresh explicitly labelled demo records without changing existing coursework."""
from pathlib import Path
from datetime import datetime, timedelta
import sqlite3

BASE = Path(__file__).resolve().parents[1]

def main():
    con = sqlite3.connect(BASE / 'aitu_lms.sqlite')
    con.execute('PRAGMA foreign_keys=ON')
    backup_dir = BASE / 'backups'
    backup_dir.mkdir(exist_ok=True)
    backup_path = backup_dir / ('before_demo_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.sqlite')
    with sqlite3.connect(backup_path) as backup:
        con.backup(backup)
    now = datetime.now()
    with con:
        con.execute("UPDATE assignments SET title=replace(title,'Assigment','Assignment') WHERE title LIKE '%Assigment%'")
        for cid, code, owner in con.execute('SELECT id,course_code,instructor_id FROM courses WHERE archived=0').fetchall():
            for index, offset in enumerate((0, 1, 7)):
                title = f'[DEMO] {code} practice {index + 1}'
                due = (now + timedelta(days=offset)).replace(hour=23,minute=59,second=0,microsecond=0).isoformat(' ')
                row = con.execute('SELECT id FROM assignments WHERE course_id=? AND title=?',(cid,title)).fetchone()
                if row:
                    con.execute('UPDATE assignments SET due_date=? WHERE id=?',(due,row[0]))
                else:
                    con.execute('INSERT INTO assignments(course_id,title,description,due_date,max_points) VALUES(?,?,?,?,100)',(cid,title,'Demonstration exercise: write a short response and optionally attach a permitted file. Synthetic demo content.',due))
            title = f'[DEMO] Welcome to {code}'
            if not con.execute('SELECT 1 FROM announcements WHERE course_id=? AND title=?',(cid,title)).fetchone():
                con.execute('INSERT INTO announcements(course_id,author_id,title,body) VALUES(?,?,?,?)',(cid,owner,title,'Demo announcement: open the practice task, submit an answer and review feedback.'))
            stored = f'demo_material_{cid}.txt'
            folder = BASE / 'private_uploads'
            folder.mkdir(exist_ok=True)
            (folder / stored).write_text(f'{code} demonstration study guide\nSynthetic material for LMS demonstration.\nOpen a practice task, write an answer, attach a file, then submit.\n',encoding='utf-8')
            if not con.execute('SELECT 1 FROM files WHERE stored_name=?',(stored,)).fetchone():
                con.execute('INSERT INTO files(course_id,owner_id,title,original_name,stored_name) VALUES(?,?,?,?,?)',(cid,owner,'[DEMO] Study guide',f'{code}_demo_guide.txt',stored))
        for uid, in con.execute("SELECT id FROM users WHERE role='student' AND active=1").fetchall():
            title = '[DEMO] Practice tasks available'
            if not con.execute('SELECT 1 FROM notifications WHERE user_id=? AND title=?',(uid,title)).fetchone():
                con.execute('INSERT INTO notifications(user_id,title,body) VALUES(?,?,?)',(uid,title,'Demonstration tasks have deadlines today, tomorrow and next week. Open your courses to practise the submission workflow.'))
    print('Demo refreshed. Backup:',backup_path)
    con.close()

if __name__ == '__main__':
    main()
