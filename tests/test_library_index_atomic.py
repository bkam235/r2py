"""The pattern index is saved atomically (2026-10-25): parallel readers never see a half-written index.json.

Parallel workers that share a library (the offline verification helpers) read index.json while another process
rewrites it; a plain write_text let them read an empty file (JSONDecodeError).
"""
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITER = """
import sys
sys.path.insert(0, {root!r})
from pathlib import Path
from r2py.library.index import PatternIndex
idx = PatternIndex(Path({d!r}))
idx._data = {{"k": ["x" * 2000] * 400}}
for _ in range(60):
    idx._save()
"""


class TestAtomicSave(unittest.TestCase):
    def test_a_reader_in_another_process_never_sees_a_partial_index(self):
        d = tempfile.mkdtemp()
        from r2py.library.index import PatternIndex
        path = PatternIndex(Path(d))._path
        writer = subprocess.Popen([sys.executable, "-c", WRITER.format(root=str(ROOT), d=d)])
        bad = 0
        try:
            while writer.poll() is None:
                try:
                    json.loads(path.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    bad += 1
                except (PermissionError, FileNotFoundError):
                    pass
                time.sleep(0.002)
        finally:
            writer.wait(timeout=120)
        self.assertEqual(writer.returncode, 0)
        self.assertEqual(bad, 0)


if __name__ == "__main__":
    unittest.main()
