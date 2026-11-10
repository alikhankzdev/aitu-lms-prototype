"""Build a portable demo archive; exclude secrets, backups and personal uploads."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import sqlite3
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT.parent / 'ICT_LMS_WEBSITE_SANZHAR_UPDATED.zip'
with tempfile.TemporaryDirectory() as temporary:
    snapshot = Path(temporary) / 'aitu_lms.sqlite'
    with sqlite3.connect(ROOT / 'aitu_lms.sqlite') as source, sqlite3.connect(snapshot) as dest:
        source.backup(dest)
        dest.execute('DELETE FROM portal_sessions')
        dest.execute('DELETE FROM login_attempts')
        dest.commit()
    with ZipFile(TARGET, 'w', ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob('*')):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            if rel.parts[0] == 'static' and path.match('course-*.png'):
                continue
            if any(p.startswith('.') or p in ('__pycache__', 'backups') for p in rel.parts):
                continue
            if path.suffix in ('.pyc', '.so', '.dylib') or path.name.endswith(('-wal', '-shm')):
                continue
            if rel.parts[0] == 'private_uploads' and not path.name.startswith('demo_material_'):
                continue
            if path.name in ('legacy_web_prototype.py', 'dash.html', 'sub.html'):
                continue
            archive.write(snapshot if rel.as_posix() == 'aitu_lms.sqlite' else path, ROOT.name + '/' + rel.as_posix())
        assert archive.testzip() is None
print(TARGET)
