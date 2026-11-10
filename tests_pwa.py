"""Check the public install resources without touching the working database."""
import json
import shutil
import struct
import tempfile
import unittest
from pathlib import Path
from app import BASE, create_app


class PwaTests(unittest.TestCase):
    def test_public_install_resources_and_private_navigation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy2(BASE / 'aitu_lms.sqlite', root / 'test.sqlite')
            app = create_app({'TESTING': True, 'DATABASE': str(root / 'test.sqlite'), 'UPLOAD_FOLDER': str(root / 'uploads')})
            client = app.test_client()
            worker = client.get('/sw.js')
            self.assertEqual(worker.status_code, 200)
            self.assertIn('javascript', worker.content_type)
            worker.close()
            response = client.get('/static/manifest.webmanifest')
            manifest = json.loads(response.data)
            response.close()
            self.assertEqual(manifest['scope'], '/')
            self.assertEqual(manifest['display'], 'standalone')
            for size in (192, 512):
                icon = next(icon for icon in manifest['icons'] if icon['sizes'] == f'{size}x{size}')
                response = client.get(icon['src'])
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data[:8], b'\x89PNG\r\n\x1a\n')
                self.assertEqual(struct.unpack('!II', response.data[16:24]), (size, size))
                response.close()
            response = client.get('/static/offline.html')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'data-lang="kk"', response.data)
            response.close()
            self.assertEqual(client.get('/dashboard').status_code, 302)
            self.assertEqual(client.get('/files/1').status_code, 302)


if __name__ == '__main__':
    unittest.main()
